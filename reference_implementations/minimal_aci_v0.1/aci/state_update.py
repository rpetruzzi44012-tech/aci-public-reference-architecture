"""State-change planning and isolated working-state application for ACI v0.1."""

from __future__ import annotations

from collections import defaultdict
from collections.abc import Callable, Mapping
from copy import deepcopy
from dataclasses import dataclass, fields, is_dataclass
from enum import StrEnum
from uuid import uuid4

from .core import (
    DiagnosticMixin,
    EscalationEvent,
    GraphUpdate,
    JSONValue,
    ReviewDecision,
    RollbackPoint,
    StateChange,
    StateChangePlan,
    StateDelta,
    SymbolicStructure,
)
from .enums import (
    AlgorithmName,
    AuditStatus,
    AuthorityLevel,
    BudgetType,
    DecisionStatus,
    DecisionType,
    EvidenceRelationType,
    EscalationUrgency,
    GovernanceMode,
    GraphName,
    GraphUpdateType,
    ScaleLabel,
    SymbolicState,
    VerificationStatus,
)
from .evidence import EvidenceLink, EvidenceObject, validate_evidence_link
from .registry import (
    AUTHORITY_RANK,
    AlgorithmRegistry,
    AlgorithmSpec,
    DecisionValidationResult,
    RegistryChangeRequest,
)
from .review_context import ReviewContext
from .state import ArchitectureState, clone_state

IDProvider = Callable[[], str]

CONFLICT_RULES = (
    "registry-invalid decisions are rejected before conflict resolution",
    "valid blocking constraints prevent ordinary enabling decisions",
    "the highest registered authority is selected within the active class",
    "equal-authority incompatible effects produce no mutation",
    "equal-effect duplicates preserve the earliest review-trace decision",
    "escalation records pending review and never grants approval",
)

_BLOCKING_STATUSES = frozenset(
    {
        DecisionStatus.BLOCKED,
        DecisionStatus.ESCALATED,
        DecisionStatus.PENDING_REVIEW,
    }
)
_CONSTRAINT_DECISIONS = frozenset(
    {
        DecisionType.SANDBOX,
        DecisionType.REVISE,
        DecisionType.REPAIR,
        DecisionType.DELAY,
        DecisionType.DEMOTE,
        DecisionType.ARCHIVE,
        DecisionType.RETRACT,
        DecisionType.REJECT,
        DecisionType.ROLLBACK,
        DecisionType.ESCALATE,
        DecisionType.AMENDMENT_REVIEW,
    }
)
_HIGH_RISK_DECISIONS = frozenset(
    {
        DecisionType.PERSIST,
        DecisionType.RETRACT,
        DecisionType.ROLLBACK,
        DecisionType.AMENDMENT_REVIEW,
    }
)
_HIGH_RISK_SCALES = frozenset(
    {
        ScaleLabel.ARCHITECTURE,
        ScaleLabel.CONSTITUTIONAL,
    }
)
_HIGH_RISK_AUTHORITIES = frozenset(
    {
        AuthorityLevel.ARCHITECTURAL_INFLUENCE,
        AuthorityLevel.INVARIANT_CONSTRAINT,
        AuthorityLevel.CONSTITUTIONAL_AUTHORITY,
    }
)
_SCALE_ORDER = tuple(ScaleLabel)
_BUDGET_FIELDS = {
    BudgetType.STABILITY: "stability_budget",
    BudgetType.NOVELTY: "novelty_budget",
    BudgetType.VERIFICATION: "verification_budget",
    BudgetType.ATTENTION: "attention_budget",
    BudgetType.RECOVERY: "recovery_capacity",
}
_DOMAIN_FIELDS = (
    "active_structures",
    "memory_graph",
    "evidence_graph",
    "coherence_graph",
    "scale_graph",
    "governance_state",
    "budgets",
    "thresholds",
    "rollback_points",
    "monitoring_triggers",
)
_ALLOWED_STATE_TRANSITIONS = {
    SymbolicState.SANDBOXED: AuthorityLevel.TEMPORARY_USE,
    SymbolicState.ARCHIVED: AuthorityLevel.NONE,
    SymbolicState.PERSISTENT: AuthorityLevel.MEMORY_INFLUENCE,
    SymbolicState.RETRACTED: AuthorityLevel.NONE,
    SymbolicState.REJECTED: AuthorityLevel.NONE,
}


class StateChangePlanningError(RuntimeError):
    """Raised when planning inputs violate the Stage 16 contract."""


class StateChangeApplicationError(RuntimeError):
    """Raised when an authorized plan cannot be applied exactly and safely."""


@dataclass(frozen=True, slots=True)
class _EligibleDecision:
    decision: ReviewDecision
    target: SymbolicStructure
    specification: AlgorithmSpec

    @property
    def authority_rank(self) -> int:
        return AUTHORITY_RANK[self.specification.authority_level]

    @property
    def is_constraint(self) -> bool:
        return (
            self.decision.status in _BLOCKING_STATUSES
            or self.decision.decision_type in _CONSTRAINT_DECISIONS
        )

    @property
    def effect_signature(self) -> tuple[str, str | None, str | None]:
        mode = self.decision.recommended_governance_mode
        return (
            self.decision.decision_type.value,
            self.decision.escalation_target,
            mode.value if mode is not None else None,
        )


def _default_id_provider() -> str:
    return f"planning-{uuid4()}"


def plan_authorized_state_changes(
    context: ReviewContext,
    registry: AlgorithmRegistry,
    *,
    registry_change_requests: Mapping[
        str,
        RegistryChangeRequest,
    ] | None = None,
    id_provider: IDProvider = _default_id_provider,
) -> StateChangePlan:
    """Build a conflict-checked plan without mutating any architecture object."""

    if not isinstance(context, ReviewContext):
        raise TypeError("context must be ReviewContext")
    if not isinstance(registry, AlgorithmRegistry):
        raise TypeError("registry must be AlgorithmRegistry")
    if not callable(id_provider):
        raise TypeError("id_provider must be callable")

    decisions = context.decisions
    request_index = _validate_change_request_index(
        registry_change_requests,
        decisions,
    )
    targets = {
        target.structure_id: target
        for target in context.targets
    }
    state_view = context.architecture_state
    baseline_state = context.architecture_state
    baseline_targets = context.targets

    plan_id = id_provider()
    validation_results: list[DecisionValidationResult] = []
    eligible: list[_EligibleDecision] = []
    rejected: dict[str, ReviewDecision] = {}
    no_ops: dict[str, ReviewDecision] = {}
    rationale: list[str] = [*CONFLICT_RULES]
    seen_algorithms: dict[str, set[AlgorithmName]] = defaultdict(set)

    for decision in decisions:
        target = targets[decision.target_id]
        validation = registry.validate_decision(
            decision,
            target,
            change_request=request_index.get(decision.decision_id),
        )
        validation_results.append(validation)
        if not validation.accepted:
            _remember_decision(rejected, decision)
            rationale.append(
                f"{decision.decision_id} rejected by registry: "
                f"{', '.join(validation.reason_codes)}"
            )
            continue
        if decision.audit_id != context.audit_id:
            _remember_decision(rejected, decision)
            rationale.append(
                f"{decision.decision_id} rejected: audit reference mismatch"
            )
            continue
        if not _governance_allows_planning(state_view, decision):
            _remember_decision(rejected, decision)
            rationale.append(
                f"{decision.decision_id} rejected by active governance mode "
                f"{state_view.governance_state.governance_mode.value}"
            )
            continue
        if (
            decision.decision_type is DecisionType.ESCALATE
            and _escalation_loops_to_prior_reviewer(
                decision,
                seen_algorithms[decision.target_id],
            )
        ):
            _remember_decision(rejected, decision)
            rationale.append(
                f"{decision.decision_id} rejected: escalation loop detected"
            )
            seen_algorithms[decision.target_id].add(
                decision.algorithm_name
            )
            continue

        specification = registry.get_spec(decision.algorithm_name)
        eligible.append(
            _EligibleDecision(
                decision=decision,
                target=target,
                specification=specification,
            )
        )
        seen_algorithms[decision.target_id].add(decision.algorithm_name)

    accepted_refs: list[str] = []
    changes: list[StateChange] = []
    graph_updates: list[GraphUpdate] = []
    rollback_points: list[RollbackPoint] = []
    escalation_events: list[EscalationEvent] = []

    grouped: dict[str, list[_EligibleDecision]] = defaultdict(list)
    for candidate in eligible:
        grouped[candidate.decision.target_id].append(candidate)

    for target_id in context.target_ids:
        candidates = grouped.get(target_id, [])
        if not candidates:
            continue
        selected, excluded, ambiguous = _resolve_target_conflict(candidates)
        for candidate in excluded:
            _remember_decision(rejected, candidate.decision)
            rationale.append(
                f"{candidate.decision.decision_id} excluded by conservative "
                "conflict precedence"
            )
        for candidate in ambiguous:
            _remember_decision(no_ops, candidate.decision)
            rationale.append(
                f"{candidate.decision.decision_id} retained as no-op: "
                "equal-authority effects remain ambiguous"
            )
        if selected is None:
            continue

        decision = selected.decision
        if selected.specification.stub and (
            decision.decision_type is not DecisionType.ESCALATE
        ):
            _remember_decision(no_ops, decision)
            rationale.append(
                f"{decision.decision_id} retained as no-op: protected stub "
                "may recommend but cannot authorize mutation"
            )
            continue

        if decision.decision_type is DecisionType.ESCALATE:
            event = _create_escalation_event(
                decision,
                audit_ref=context.audit_id,
                escalation_id=id_provider(),
            )
            accepted_refs.append(decision.decision_id)
            escalation_events.append(event)
            rationale.append(
                f"{decision.decision_id} authorized only as pending "
                "escalation; no approval was created"
            )
            continue

        decision_changes, decision_updates = _create_plan_artifacts(
            decision,
            audit_ref=context.audit_id,
            id_provider=id_provider,
        )
        if not decision_changes and not decision_updates:
            _remember_decision(no_ops, decision)
            rationale.append(
                f"{decision.decision_id} retained as no-op: the simplified "
                "decision contains no applicable state action"
            )
            continue

        accepted_refs.append(decision.decision_id)
        changes.extend(decision_changes)
        graph_updates.extend(decision_updates)
        if _requires_rollback(
            decision,
            selected.target,
            decision_updates,
        ):
            rollback_points.append(
                _create_rollback_point(
                    decision,
                    selected.target,
                    state_ref=context.architecture_state_ref,
                    audit_ref=context.audit_id,
                    graph_updates=decision_updates,
                    rollback_id=id_provider(),
                )
            )
        rationale.append(
            f"{decision.decision_id} accepted into planning after registry "
            "and conflict checks"
        )

    if not decisions:
        rationale.append("No review decisions were available for planning")

    plan = StateChangePlan(
        plan_id=plan_id,
        decision_refs=accepted_refs,
        changes=changes,
        graph_updates=graph_updates,
        rollback_points=rollback_points,
        escalation_events=escalation_events,
        validation_results=validation_results,
        rejected_decisions=list(rejected.values()),
        no_op_items=list(no_ops.values()),
        rationale=rationale,
        authorized=bool(accepted_refs),
        audit_ref=context.audit_id,
    )
    if (
        context.architecture_state != baseline_state
        or context.targets != baseline_targets
    ):
        raise StateChangePlanningError(
            "planning mutated review state or target structures"
        )
    return plan


def apply_state_change_plan(
    working_state: ArchitectureState,
    plan: StateChangePlan,
    audit_id: str,
) -> ArchitectureState:
    """Apply one authorized plan to a fresh clone of the supplied state."""

    if not isinstance(working_state, ArchitectureState):
        raise TypeError("working_state must be ArchitectureState")
    if not isinstance(plan, StateChangePlan):
        raise TypeError("plan must be StateChangePlan")
    _require_nonempty_text(audit_id, "audit_id")

    source_snapshot = clone_state(working_state)
    candidate = clone_state(working_state)
    _require_pending_audit(candidate, audit_id)
    algorithms = _validate_plan_for_application(
        candidate,
        plan,
        audit_id,
    )

    if not plan.authorized:
        return candidate

    for rollback_point in plan.rollback_points:
        candidate.rollback_points.append(deepcopy(rollback_point))

    for change in plan.changes:
        _apply_state_change(
            candidate,
            change,
            algorithm=algorithms[change.decision_ref],
            audit_id=audit_id,
        )
        candidate.state_changes.append(deepcopy(change))

    for update in plan.graph_updates:
        _apply_graph_update(
            candidate,
            update,
            algorithm=algorithms[update.decision_ref],
            audit_id=audit_id,
        )
        candidate.applied_graph_updates.append(deepcopy(update))

    for event in plan.escalation_events:
        if event.resolved:
            raise StateChangeApplicationError(
                "planned escalation must remain unresolved"
            )
        candidate.governance_state.pending_escalations.append(
            deepcopy(event)
        )

    if (
        plan.changes
        or plan.graph_updates
        or plan.rollback_points
        or plan.escalation_events
    ):
        candidate.state_id = (
            f"{source_snapshot.state_id}@applied:{plan.plan_id}"
        )
    candidate.__post_init__()
    if working_state != source_snapshot:
        raise StateChangeApplicationError(
            "application leaked into the supplied working-state baseline"
        )
    return candidate


def calculate_state_delta(
    baseline: ArchitectureState,
    working_state: ArchitectureState,
) -> StateDelta:
    """Compare exact domain snapshots while reporting audit history separately."""

    if not isinstance(baseline, ArchitectureState):
        raise TypeError("baseline must be ArchitectureState")
    if not isinstance(working_state, ArchitectureState):
        raise TypeError("working_state must be ArchitectureState")

    domain_changes: dict[str, JSONValue] = {}
    for field_name in _DOMAIN_FIELDS:
        before = _snapshot_value(getattr(baseline, field_name))
        after = _snapshot_value(getattr(working_state, field_name))
        if before != after:
            domain_changes[field_name] = {
                "before": before,
                "after": after,
            }

    applied_changes = _new_models_by_id(
        baseline.state_changes,
        working_state.state_changes,
        "change_id",
    )
    graph_updates = _new_models_by_id(
        baseline.applied_graph_updates,
        working_state.applied_graph_updates,
        "update_id",
    )
    escalations = _new_models_by_id(
        baseline.governance_state.pending_escalations,
        working_state.governance_state.pending_escalations,
        "escalation_id",
    )
    rollbacks = _new_models_by_id(
        baseline.rollback_points,
        working_state.rollback_points,
        "rollback_id",
    )
    before_audits = [audit.audit_id for audit in baseline.audit_log]
    after_audits = [audit.audit_id for audit in working_state.audit_log]
    before_audit_records = {
        audit.audit_id: _snapshot_value(audit)
        for audit in baseline.audit_log
    }
    after_audit_records = {
        audit.audit_id: _snapshot_value(audit)
        for audit in working_state.audit_log
    }
    changed_audit_refs = [
        audit_ref
        for audit_ref in dict.fromkeys((*before_audits, *after_audits))
        if before_audit_records.get(audit_ref)
        != after_audit_records.get(audit_ref)
    ]
    audit_refs = {
        item.audit_ref
        for collection in (
            applied_changes,
            graph_updates,
            escalations,
            rollbacks,
        )
        for item in collection
    }
    audit_refs.update(changed_audit_refs)
    audit_refs.discard(None)
    if len(audit_refs) != 1:
        raise StateChangeApplicationError(
            "state delta requires exactly one transition audit reference"
        )
    audit_ref = next(iter(audit_refs))

    return StateDelta(
        delta_id=(
            f"delta:{baseline.state_id}->{working_state.state_id}:"
            f"{audit_ref}"
        ),
        before_state_ref=baseline.state_id,
        after_state_ref=working_state.state_id,
        audit_ref=audit_ref,
        applied_change_ids=[
            change.change_id for change in applied_changes
        ],
        graph_update_ids=[
            update.update_id for update in graph_updates
        ],
        escalation_ids=[
            escalation.escalation_id for escalation in escalations
        ],
        rollback_ids=[
            rollback.rollback_id for rollback in rollbacks
        ],
        domain_changes=domain_changes,
        audit_log_changed=(
            _snapshot_value(baseline.audit_log)
            != _snapshot_value(working_state.audit_log)
        ),
        audit_log_before_refs=before_audits,
        audit_log_after_refs=after_audits,
    )


def _require_pending_audit(
    state: ArchitectureState,
    audit_id: str,
) -> None:
    matches = [
        audit for audit in state.audit_log if audit.audit_id == audit_id
    ]
    if len(matches) != 1 or matches[0].status is not AuditStatus.PENDING:
        raise StateChangeApplicationError(
            "application requires exactly one matching PENDING audit"
        )


def _validate_plan_for_application(
    state: ArchitectureState,
    plan: StateChangePlan,
    audit_id: str,
) -> dict[str, AlgorithmName]:
    if plan.audit_ref != audit_id:
        raise StateChangeApplicationError(
            "plan audit_ref must match pending audit ID"
        )
    effects = (
        *plan.changes,
        *plan.graph_updates,
        *plan.escalation_events,
    )
    if not plan.authorized and (
        effects or plan.rollback_points or plan.decision_refs
    ):
        raise StateChangeApplicationError(
            "unauthorized plan cannot contain applicable effects"
        )

    accepted_results = {
        result.decision_id: result
        for result in plan.validation_results
        if result.accepted
    }
    if set(plan.decision_refs) != set(accepted_results).intersection(
        plan.decision_refs
    ):
        raise StateChangeApplicationError(
            "every accepted decision requires a preserved accepted validation"
        )
    algorithms: dict[str, AlgorithmName] = {}
    for decision_ref in plan.decision_refs:
        result = accepted_results[decision_ref]
        try:
            algorithms[decision_ref] = AlgorithmName(
                result.algorithm_identity
            )
        except ValueError as error:
            raise StateChangeApplicationError(
                "accepted validation has an unregistered algorithm identity"
            ) from error

    _require_unique_ids(plan.changes, "change_id", "StateChange")
    _require_unique_ids(
        plan.graph_updates,
        "update_id",
        "GraphUpdate",
    )
    _require_unique_ids(
        plan.escalation_events,
        "escalation_id",
        "EscalationEvent",
    )
    _require_unique_ids(
        plan.rollback_points,
        "rollback_id",
        "RollbackPoint",
    )
    _reject_existing_effect_ids(state, plan)
    for effect in effects:
        if effect.audit_ref != audit_id:
            raise StateChangeApplicationError(
                "every applicable effect must reference the pending audit"
            )
        if effect.decision_ref not in algorithms:
            raise StateChangeApplicationError(
                "every applicable effect must reference an accepted decision"
            )
    for rollback_point in plan.rollback_points:
        if rollback_point.audit_ref != audit_id:
            raise StateChangeApplicationError(
                "rollback point must reference the pending audit"
            )
        if rollback_point.state_ref != state.state_id:
            raise StateChangeApplicationError(
                "rollback point must reference the pre-application state"
            )

    high_risk_refs = {
        change.decision_ref
        for change in plan.changes
        if _change_requires_rollback(change, state)
    }
    high_risk_refs.update(
        update.decision_ref
        for update in plan.graph_updates
        if update.graph_name is GraphName.AUTHORITY_GRAPH
    )
    for decision_ref in high_risk_refs:
        affected_targets = {
            change.target_id
            for change in plan.changes
            if change.decision_ref == decision_ref
        }
        affected_graphs = {
            update.graph_name
            for update in plan.graph_updates
            if update.decision_ref == decision_ref
        }
        if not any(
            (
                bool(
                    affected_targets.intersection(
                        rollback_point.affected_structures
                    )
                )
                or bool(
                    affected_graphs.intersection(
                        rollback_point.affected_graphs
                    )
                )
            )
            and rollback_point.valid_until is not None
            for rollback_point in plan.rollback_points
        ):
            raise StateChangeApplicationError(
                f"high-risk decision {decision_ref} requires scoped rollback"
            )
    _validate_paired_plan_artifacts(plan)
    return algorithms


def _reject_existing_effect_ids(
    state: ArchitectureState,
    plan: StateChangePlan,
) -> None:
    comparisons = (
        (
            plan.changes,
            state.state_changes,
            "change_id",
            "StateChange",
        ),
        (
            plan.graph_updates,
            state.applied_graph_updates,
            "update_id",
            "GraphUpdate",
        ),
        (
            plan.escalation_events,
            state.governance_state.pending_escalations,
            "escalation_id",
            "EscalationEvent",
        ),
        (
            plan.rollback_points,
            state.rollback_points,
            "rollback_id",
            "RollbackPoint",
        ),
    )
    for proposed, existing, id_field, model_name in comparisons:
        existing_ids = {
            getattr(item, id_field)
            for item in existing
        }
        collisions = [
            getattr(item, id_field)
            for item in proposed
            if getattr(item, id_field) in existing_ids
        ]
        if collisions:
            raise StateChangeApplicationError(
                f"{model_name} identifiers already exist in working state: "
                f"{', '.join(collisions)}"
            )


def _validate_paired_plan_artifacts(plan: StateChangePlan) -> None:
    for change in plan.changes:
        required_graph: GraphName | None = None
        required_type: GraphUpdateType | None = None
        if change.change_type == "structure_state_change":
            new_state = _parse_enum_payload(
                change.payload,
                "new_state",
                SymbolicState,
            )
            if new_state in {
                SymbolicState.PERSISTENT,
                SymbolicState.ARCHIVED,
            }:
                required_graph = GraphName.MEMORY_GRAPH
                required_type = GraphUpdateType.NODE_ADDED
            elif new_state is SymbolicState.RETRACTED:
                required_graph = GraphName.MEMORY_GRAPH
                required_type = GraphUpdateType.RELATION_UPDATED
        elif change.change_type == "scale_demotion_request":
            required_graph = GraphName.SCALE_GRAPH
            required_type = GraphUpdateType.RELATION_UPDATED

        if required_graph is None:
            continue
        if not any(
            update.decision_ref == change.decision_ref
            and update.graph_name is required_graph
            and update.update_type is required_type
            and change.target_id in update.affected_nodes
            for update in plan.graph_updates
        ):
            raise StateChangeApplicationError(
                f"{change.change_type} requires its paired "
                f"{required_graph.value} update"
            )
    for update in plan.graph_updates:
        if (
            update.graph_name is GraphName.MEMORY_GRAPH
            and update.update_type is GraphUpdateType.NODE_ADDED
        ):
            for target_id in update.affected_nodes:
                if not any(
                    change.decision_ref == update.decision_ref
                    and change.target_id == target_id
                    and change.change_type == "structure_state_change"
                    and _parse_enum_payload(
                        change.payload,
                        "new_state",
                        SymbolicState,
                    )
                    in {
                        SymbolicState.PERSISTENT,
                        SymbolicState.ARCHIVED,
                    }
                    for change in plan.changes
                ):
                    raise StateChangeApplicationError(
                        "memory node addition requires a paired persistence "
                        "or archive transition"
                    )


def _change_requires_rollback(
    change: StateChange,
    state: ArchitectureState,
) -> bool:
    if change.change_type in {
        "rollback_restore_request",
        "governance_mode_change",
    }:
        return True
    if change.change_type == "structure_state_change":
        new_state = _parse_enum_payload(
            change.payload,
            "new_state",
            SymbolicState,
        )
        if new_state in {
            SymbolicState.PERSISTENT,
            SymbolicState.RETRACTED,
        }:
            return True
    target = state.active_structures.get(change.target_id)
    return bool(
        target is not None
        and (
            target.metadata.scale_label in _HIGH_RISK_SCALES
            or target.metadata.authority_level in _HIGH_RISK_AUTHORITIES
        )
    )


def _apply_state_change(
    state: ArchitectureState,
    change: StateChange,
    *,
    algorithm: AlgorithmName,
    audit_id: str,
) -> None:
    if change.change_type == "structure_state_change":
        _apply_structure_state_change(
            state,
            change,
            algorithm=algorithm,
            audit_id=audit_id,
        )
        return
    if change.change_type == "mark_for_revision":
        target = _target_structure(state, change.target_id)
        target.current_state = _parse_enum_payload(
            change.payload,
            "review_state",
            SymbolicState,
        )
        _attach_audit_ref(target, audit_id)
        _append_monitoring_trigger(
            state,
            change,
            "revision_required",
        )
        return
    if change.change_type == "delay":
        _target_structure(state, change.target_id)
        _require_payload_text(change.payload, "reason")
        _append_monitoring_trigger(state, change, "delayed")
        return
    if change.change_type == "monitoring_trigger_add":
        _target_structure(state, change.target_id)
        condition = _require_payload_text(
            change.payload,
            "condition",
        )
        _append_monitoring_trigger(state, change, condition)
        return
    if change.change_type == "coherence_tension_add":
        if algorithm not in {AlgorithmName.CRA, AlgorithmName.CGA}:
            raise StateChangeApplicationError(
                "coherence tension requires CRA or CGA authorization"
            )
        _target_structure(state, change.target_id)
        tension_id = _require_payload_text(
            change.payload,
            "tension_id",
        )
        reason = _require_payload_text(change.payload, "reason")
        if tension_id not in state.coherence_graph.unresolved_tensions:
            state.coherence_graph.unresolved_tensions.append(tension_id)
        state.coherence_graph.relations.append(
            {
                "relation_id": tension_id,
                "target_id": change.target_id,
                "relation_type": "unresolved_tension",
                "reason": reason,
                "decision_ref": change.decision_ref,
                "audit_ref": audit_id,
            }
        )
        return
    if change.change_type == "scale_demotion_request":
        target = _target_structure(state, change.target_id)
        if change.payload.get("operation") != "demote_one_level":
            raise StateChangeApplicationError(
                "scale demotion requires demote_one_level operation"
            )
        target.metadata.scale_label = _demote_enum(
            target.metadata.scale_label,
            _SCALE_ORDER,
        )
        _attach_audit_ref(target, audit_id)
        return
    if change.change_type == "budget_effect":
        _apply_budget_effect(
            state,
            change,
            algorithm=algorithm,
        )
        return
    if change.change_type in {
        "rollback_restore_request",
        "governance_mode_change",
    }:
        raise StateChangeApplicationError(
            f"{change.change_type} application is deferred beyond Stage 17"
        )
    raise StateChangeApplicationError(
        f"unsupported state change type: {change.change_type}"
    )


def _apply_structure_state_change(
    state: ArchitectureState,
    change: StateChange,
    *,
    algorithm: AlgorithmName,
    audit_id: str,
) -> None:
    target = _target_structure(state, change.target_id)
    new_state = _parse_enum_payload(
        change.payload,
        "new_state",
        SymbolicState,
    )
    authority_level = _parse_enum_payload(
        change.payload,
        "authority_level",
        AuthorityLevel,
    )
    if _ALLOWED_STATE_TRANSITIONS.get(new_state) is not authority_level:
        raise StateChangeApplicationError(
            "state transition authority does not match the v0.1 mapping"
        )
    if (
        new_state in {SymbolicState.PERSISTENT, SymbolicState.ARCHIVED}
        and algorithm is not AlgorithmName.PCA
    ):
        raise StateChangeApplicationError(
            "persistence and archive transitions require PCA authorization"
        )
    if (
        new_state is SymbolicState.RETRACTED
        and algorithm not in {AlgorithmName.PCA, AlgorithmName.CGA}
    ):
        raise StateChangeApplicationError(
            "retraction requires PCA or CGA authorization"
        )
    if (
        new_state is SymbolicState.SANDBOXED
        and algorithm not in {AlgorithmName.GEA, AlgorithmName.CGA}
    ):
        raise StateChangeApplicationError(
            "sandbox mutation requires a non-stub GEA or CGA decision"
        )
    target.current_state = new_state
    target.metadata.authority_level = authority_level
    _attach_audit_ref(target, audit_id)


def _apply_budget_effect(
    state: ArchitectureState,
    change: StateChange,
    *,
    algorithm: AlgorithmName,
) -> None:
    if algorithm not in {
        AlgorithmName.GEA,
        AlgorithmName.CRA,
        AlgorithmName.PCA,
        AlgorithmName.MSSA,
        AlgorithmName.CGA,
    }:
        raise StateChangeApplicationError(
            "protected stubs cannot authorize budget mutation"
        )
    budget_type = _parse_enum_payload(
        change.payload,
        "budget_type",
        BudgetType,
    )
    delta = _require_payload_number(change.payload, "delta")
    verification_cost = _require_payload_number(
        change.payload,
        "verification_cost",
    )
    _require_payload_text(change.payload, "reason")
    if delta > 0.0:
        raise StateChangeApplicationError(
            "budget restoration is deferred beyond v0.1"
        )
    if verification_cost < 0.0:
        raise StateChangeApplicationError(
            "verification_cost cannot be negative"
        )

    budget_field = _BUDGET_FIELDS[budget_type]
    proposed = getattr(state.budgets, budget_field) + delta
    verification = state.budgets.verification_budget - verification_cost
    if budget_type is BudgetType.VERIFICATION:
        proposed -= verification_cost
        verification = proposed
    _require_normalized(proposed, f"{budget_type.value} result")
    _require_normalized(verification, "verification budget result")
    setattr(state.budgets, budget_field, proposed)
    state.budgets.verification_budget = verification


def _apply_graph_update(
    state: ArchitectureState,
    update: GraphUpdate,
    *,
    algorithm: AlgorithmName,
    audit_id: str,
) -> None:
    before_other_domains = {
        graph_name: _snapshot_value(_graph_for_name(state, graph_name))
        for graph_name in GraphName
        if graph_name is not update.graph_name
    }
    if update.graph_name is GraphName.MEMORY_GRAPH:
        _apply_memory_graph_update(state, update, algorithm, audit_id)
    elif update.graph_name is GraphName.EVIDENCE_GRAPH:
        _apply_evidence_graph_update(state, update, algorithm, audit_id)
    elif update.graph_name is GraphName.COHERENCE_GRAPH:
        _apply_coherence_graph_update(state, update, algorithm, audit_id)
    elif update.graph_name is GraphName.SCALE_GRAPH:
        _apply_scale_graph_update(state, update, algorithm, audit_id)
    elif update.graph_name is GraphName.AUTHORITY_GRAPH:
        _apply_authority_graph_update(state, update, algorithm, audit_id)
    else:
        raise StateChangeApplicationError(
            f"unsupported graph domain: {update.graph_name}"
        )
    for graph_name, before in before_other_domains.items():
        if _snapshot_value(_graph_for_name(state, graph_name)) != before:
            raise StateChangeApplicationError(
                "graph update crossed its declared domain boundary"
            )


def _apply_memory_graph_update(
    state: ArchitectureState,
    update: GraphUpdate,
    algorithm: AlgorithmName,
    audit_id: str,
) -> None:
    if algorithm not in {AlgorithmName.PCA, AlgorithmName.CGA}:
        raise StateChangeApplicationError(
            "memory graph writes require PCA or CGA authorization"
        )
    if update.update_type is GraphUpdateType.NODE_ADDED and algorithm is not AlgorithmName.PCA:
        raise StateChangeApplicationError(
            "only PCA may add persistent memory graph nodes"
        )
    graph = state.memory_graph
    if update.update_type is GraphUpdateType.NODE_ADDED:
        for structure_id in update.affected_nodes:
            graph.nodes[structure_id] = deepcopy(
                _target_structure(state, structure_id)
            )
    elif update.update_type is GraphUpdateType.NODE_REMOVED:
        for structure_id in update.affected_nodes:
            graph.nodes.pop(structure_id, None)
    elif update.update_type is GraphUpdateType.RELATION_UPDATED:
        if update.payload.get("operation") == "sync_structure":
            for structure_id in update.affected_nodes:
                if structure_id not in graph.nodes:
                    raise StateChangeApplicationError(
                        "memory sync requires an existing memory node"
                    )
                graph.nodes[structure_id] = deepcopy(
                    _target_structure(state, structure_id)
                )
        else:
            relation = _payload_record(update.payload, "relation")
            _upsert_record(
                graph.persistence_relations,
                _record_with_provenance(
                    relation,
                    update,
                    audit_id,
                ),
                "relation_id",
            )
    elif update.update_type is GraphUpdateType.EDGE_ADDED:
        relation = _payload_record(update.payload, "relation")
        graph.persistence_relations.append(
            _record_with_provenance(relation, update, audit_id)
        )
    elif update.update_type is GraphUpdateType.EDGE_REMOVED:
        graph.persistence_relations[:] = _remove_records(
            graph.persistence_relations,
            update.affected_edges,
            "relation_id",
        )
    else:
        raise StateChangeApplicationError(
            "unsupported memory graph update type"
        )


def _apply_evidence_graph_update(
    state: ArchitectureState,
    update: GraphUpdate,
    algorithm: AlgorithmName,
    audit_id: str,
) -> None:
    if algorithm not in {AlgorithmName.GEA, AlgorithmName.CGA}:
        raise StateChangeApplicationError(
            "evidence graph writes require GEA or CGA authorization"
        )
    graph = state.evidence_graph
    if update.update_type is GraphUpdateType.NODE_ADDED:
        record = _payload_record(update.payload, "evidence_object")
        evidence = EvidenceObject(
            evidence_id=_record_text(record, "evidence_id"),
            content=_record_string(record, "content"),
            source_ref=_record_text(record, "source_ref"),
        )
        if evidence.evidence_id not in update.affected_nodes:
            raise StateChangeApplicationError(
                "evidence object must match affected_nodes"
            )
        graph.evidence_objects[evidence.evidence_id] = evidence
    elif update.update_type is GraphUpdateType.NODE_REMOVED:
        for evidence_id in update.affected_nodes:
            graph.evidence_objects.pop(evidence_id, None)
            graph.links[:] = [
                link
                for link in graph.links
                if link.evidence_id != evidence_id
            ]
    elif update.update_type is GraphUpdateType.EDGE_ADDED:
        record = _payload_record(update.payload, "evidence_link")
        link = EvidenceLink(
            evidence_id=_record_text(record, "evidence_id"),
            target_structure_id=_record_text(
                record,
                "target_structure_id",
            ),
            source_ref=_record_text(record, "source_ref"),
            relation_type=_parse_enum_value(
                record.get("relation_type"),
                EvidenceRelationType,
                "relation_type",
            ),
            verification_status=_parse_enum_value(
                record.get("verification_status"),
                VerificationStatus,
                "verification_status",
            ),
        )
        validate_evidence_link(
            link,
            evidence_by_id=graph.evidence_objects,
            target_structure_ids=state.active_structures,
        )
        graph.links.append(link)
    elif update.update_type is GraphUpdateType.EDGE_REMOVED:
        edge_ids = set(update.affected_edges)
        graph.links[:] = [
            link
            for link in graph.links
            if _evidence_link_ref(link) not in edge_ids
        ]
    elif update.update_type is GraphUpdateType.RELATION_UPDATED:
        relation = _payload_record(update.payload, "source_relation")
        _upsert_record(
            graph.source_relations,
            _record_with_provenance(relation, update, audit_id),
            "relation_id",
        )
    else:
        raise StateChangeApplicationError(
            "unsupported evidence graph update type"
        )


def _apply_coherence_graph_update(
    state: ArchitectureState,
    update: GraphUpdate,
    algorithm: AlgorithmName,
    audit_id: str,
) -> None:
    if algorithm not in {AlgorithmName.CRA, AlgorithmName.CGA}:
        raise StateChangeApplicationError(
            "coherence graph writes require CRA or CGA authorization"
        )
    graph = state.coherence_graph
    if update.update_type is GraphUpdateType.NODE_ADDED:
        for tension_id in update.affected_nodes:
            if tension_id not in graph.unresolved_tensions:
                graph.unresolved_tensions.append(tension_id)
    elif update.update_type is GraphUpdateType.NODE_REMOVED:
        graph.unresolved_tensions[:] = [
            tension_id
            for tension_id in graph.unresolved_tensions
            if tension_id not in set(update.affected_nodes)
        ]
    elif update.update_type in {
        GraphUpdateType.EDGE_ADDED,
        GraphUpdateType.RELATION_UPDATED,
        GraphUpdateType.GRAPH_REPAIRED,
    }:
        relation = _payload_record(update.payload, "relation")
        record = _record_with_provenance(relation, update, audit_id)
        if update.update_type is GraphUpdateType.EDGE_ADDED:
            graph.relations.append(record)
        else:
            _upsert_record(graph.relations, record, "relation_id")
    elif update.update_type is GraphUpdateType.EDGE_REMOVED:
        graph.relations[:] = _remove_records(
            graph.relations,
            update.affected_edges,
            "relation_id",
        )
    else:
        raise StateChangeApplicationError(
            "unsupported coherence graph update type"
        )


def _apply_scale_graph_update(
    state: ArchitectureState,
    update: GraphUpdate,
    algorithm: AlgorithmName,
    audit_id: str,
) -> None:
    if algorithm not in {
        AlgorithmName.CRA,
        AlgorithmName.PCA,
        AlgorithmName.MSSA,
        AlgorithmName.CGA,
    }:
        raise StateChangeApplicationError(
            "scale graph write exceeds algorithm authority"
        )
    graph = state.scale_graph
    if update.update_type in {
        GraphUpdateType.NODE_ADDED,
        GraphUpdateType.RELATION_UPDATED,
    }:
        for structure_id in update.affected_nodes:
            if "scale_label" in update.payload:
                scale_label = _parse_enum_payload(
                    update.payload,
                    "scale_label",
                    ScaleLabel,
                )
            else:
                scale_label = _target_structure(
                    state,
                    structure_id,
                ).metadata.scale_label
            graph.scale_labels[structure_id] = scale_label
        if "mismatch_record" in update.payload:
            mismatch = _payload_record(
                update.payload,
                "mismatch_record",
            )
            graph.mismatch_records.append(
                _record_with_provenance(mismatch, update, audit_id)
            )
    elif update.update_type is GraphUpdateType.NODE_REMOVED:
        for structure_id in update.affected_nodes:
            graph.scale_labels.pop(structure_id, None)
    elif update.update_type is GraphUpdateType.EDGE_ADDED:
        mismatch = _payload_record(update.payload, "mismatch_record")
        graph.mismatch_records.append(
            _record_with_provenance(mismatch, update, audit_id)
        )
    elif update.update_type is GraphUpdateType.EDGE_REMOVED:
        graph.mismatch_records[:] = _remove_records(
            graph.mismatch_records,
            update.affected_edges,
            "mismatch_id",
        )
    else:
        raise StateChangeApplicationError(
            "unsupported scale graph update type"
        )


def _apply_authority_graph_update(
    state: ArchitectureState,
    update: GraphUpdate,
    algorithm: AlgorithmName,
    audit_id: str,
) -> None:
    if algorithm is not AlgorithmName.CGA:
        raise StateChangeApplicationError(
            "AuthorityGraph changes require CGA authorization"
        )
    graph = state.governance_state.authority_graph
    collection_name = update.payload.get(
        "collection",
        "authority_edges",
    )
    if collection_name not in {
        "authority_edges",
        "veto_rules",
        "escalation_rules",
    }:
        raise StateChangeApplicationError(
            "unknown AuthorityGraph collection"
        )
    collection = getattr(graph, collection_name)
    if update.update_type is GraphUpdateType.NODE_ADDED:
        for domain in update.affected_nodes:
            if domain not in graph.domains:
                graph.domains.append(domain)
    elif update.update_type is GraphUpdateType.NODE_REMOVED:
        graph.domains[:] = [
            domain
            for domain in graph.domains
            if domain not in set(update.affected_nodes)
        ]
    elif update.update_type in {
        GraphUpdateType.EDGE_ADDED,
        GraphUpdateType.RELATION_UPDATED,
    }:
        relation = _payload_record(update.payload, "relation")
        record = _record_with_provenance(relation, update, audit_id)
        id_field = {
            "authority_edges": "edge_id",
            "veto_rules": "veto_id",
            "escalation_rules": "rule_id",
        }[collection_name]
        if update.update_type is GraphUpdateType.EDGE_ADDED:
            collection.append(record)
        else:
            _upsert_record(collection, record, id_field)
    elif update.update_type is GraphUpdateType.EDGE_REMOVED:
        id_field = {
            "authority_edges": "edge_id",
            "veto_rules": "veto_id",
            "escalation_rules": "rule_id",
        }[collection_name]
        collection[:] = _remove_records(
            collection,
            update.affected_edges,
            id_field,
        )
    else:
        raise StateChangeApplicationError(
            "unsupported authority graph update type"
        )


def _graph_for_name(
    state: ArchitectureState,
    graph_name: GraphName,
) -> object:
    if graph_name is GraphName.MEMORY_GRAPH:
        return state.memory_graph
    if graph_name is GraphName.EVIDENCE_GRAPH:
        return state.evidence_graph
    if graph_name is GraphName.COHERENCE_GRAPH:
        return state.coherence_graph
    if graph_name is GraphName.SCALE_GRAPH:
        return state.scale_graph
    return state.governance_state.authority_graph


def _target_structure(
    state: ArchitectureState,
    structure_id: str,
) -> SymbolicStructure:
    target = state.active_structures.get(structure_id)
    if target is None:
        raise StateChangeApplicationError(
            f"unknown active target: {structure_id}"
        )
    return target


def _attach_audit_ref(
    target: SymbolicStructure,
    audit_id: str,
) -> None:
    if audit_id not in target.metadata.audit_refs:
        target.metadata.audit_refs.append(audit_id)


def _append_monitoring_trigger(
    state: ArchitectureState,
    change: StateChange,
    condition: str,
) -> None:
    state.monitoring_triggers.append(
        f"{condition}|{change.target_id}|{change.decision_ref}|"
        f"{change.audit_ref}"
    )


def _demote_enum(value: StrEnum, order: tuple[StrEnum, ...]) -> StrEnum:
    index = order.index(value)
    return order[max(0, index - 1)]


def _parse_enum_payload(
    payload: Mapping[str, JSONValue],
    key: str,
    enum_type: type[StrEnum],
) -> StrEnum:
    return _parse_enum_value(payload.get(key), enum_type, key)


def _parse_enum_value(
    value: object,
    enum_type: type[StrEnum],
    field_name: str,
) -> StrEnum:
    if isinstance(value, enum_type):
        return value
    if not isinstance(value, str):
        raise StateChangeApplicationError(
            f"{field_name} must identify {enum_type.__name__}"
        )
    try:
        return enum_type(value)
    except ValueError:
        try:
            return enum_type[value]
        except KeyError as error:
            raise StateChangeApplicationError(
                f"unknown {field_name}: {value}"
            ) from error


def _require_payload_text(
    payload: Mapping[str, JSONValue],
    key: str,
) -> str:
    value = payload.get(key)
    if not isinstance(value, str) or not value.strip():
        raise StateChangeApplicationError(
            f"payload {key} must be nonempty text"
        )
    return value


def _require_payload_number(
    payload: Mapping[str, JSONValue],
    key: str,
) -> float:
    value = payload.get(key)
    if not isinstance(value, int | float) or isinstance(value, bool):
        raise StateChangeApplicationError(
            f"payload {key} must be numeric"
        )
    return float(value)


def _payload_record(
    payload: Mapping[str, JSONValue],
    key: str,
) -> dict[str, JSONValue]:
    value = payload.get(key)
    if not isinstance(value, dict):
        raise StateChangeApplicationError(
            f"payload {key} must be a dictionary"
        )
    return deepcopy(value)


def _record_text(
    record: Mapping[str, JSONValue],
    key: str,
) -> str:
    value = record.get(key)
    if not isinstance(value, str) or not value.strip():
        raise StateChangeApplicationError(
            f"record {key} must be nonempty text"
        )
    return value


def _record_string(
    record: Mapping[str, JSONValue],
    key: str,
) -> str:
    value = record.get(key)
    if not isinstance(value, str):
        raise StateChangeApplicationError(
            f"record {key} must be text"
        )
    return value


def _record_with_provenance(
    record: dict[str, JSONValue],
    update: GraphUpdate,
    audit_id: str,
) -> dict[str, JSONValue]:
    record["update_id"] = update.update_id
    record["decision_ref"] = update.decision_ref
    record["audit_ref"] = audit_id
    return record


def _upsert_record(
    records: list[dict[str, JSONValue]],
    record: dict[str, JSONValue],
    id_field: str,
) -> None:
    record_id = _record_text(record, id_field)
    for index, existing in enumerate(records):
        if existing.get(id_field) == record_id:
            records[index] = record
            return
    records.append(record)


def _remove_records(
    records: list[dict[str, JSONValue]],
    identifiers: list[str],
    id_field: str,
) -> list[dict[str, JSONValue]]:
    identifier_set = set(identifiers)
    return [
        record
        for record in records
        if record.get(id_field) not in identifier_set
    ]


def _evidence_link_ref(link: EvidenceLink) -> str:
    return f"{link.evidence_id}->{link.target_structure_id}"


def _require_unique_ids(
    values: list[object],
    field_name: str,
    model_name: str,
) -> None:
    identifiers = [getattr(value, field_name) for value in values]
    if len(identifiers) != len(set(identifiers)):
        raise StateChangeApplicationError(
            f"{model_name} identifiers must be unique"
        )


def _require_normalized(value: float, field_name: str) -> None:
    if not 0.0 <= value <= 1.0:
        raise StateChangeApplicationError(
            f"{field_name} must remain in [0.0, 1.0]"
        )


def _new_models_by_id(
    baseline: list[object],
    working: list[object],
    id_field: str,
) -> list[object]:
    baseline_ids = {getattr(value, id_field) for value in baseline}
    return [
        value
        for value in working
        if getattr(value, id_field) not in baseline_ids
    ]


def _snapshot_value(value: object) -> JSONValue:
    if isinstance(value, StrEnum):
        return value.value
    if isinstance(value, DiagnosticMixin):
        return value.to_dict()
    if is_dataclass(value):
        return {
            data_field.name: _snapshot_value(
                getattr(value, data_field.name)
            )
            for data_field in fields(value)
        }
    if isinstance(value, Mapping):
        return {
            str(_snapshot_value(key)): _snapshot_value(item)
            for key, item in value.items()
        }
    if isinstance(value, list | tuple):
        return [_snapshot_value(item) for item in value]
    if isinstance(value, str | int | float | bool) or value is None:
        return value
    raise StateChangeApplicationError(
        f"cannot snapshot domain value of type {type(value).__name__}"
    )


def _validate_change_request_index(
    requests: Mapping[str, RegistryChangeRequest] | None,
    decisions: tuple[ReviewDecision, ...],
) -> dict[str, RegistryChangeRequest]:
    if requests is None:
        return {}
    if not isinstance(requests, Mapping):
        raise TypeError("registry_change_requests must be a mapping or None")
    known_decisions = {decision.decision_id for decision in decisions}
    indexed: dict[str, RegistryChangeRequest] = {}
    for decision_id, request in requests.items():
        _require_nonempty_text(decision_id, "registry change decision ID")
        if decision_id not in known_decisions:
            raise ValueError(
                f"registry change references unknown decision: {decision_id}"
            )
        if not isinstance(request, RegistryChangeRequest):
            raise TypeError(
                "registry_change_requests values must be "
                "RegistryChangeRequest"
            )
        indexed[decision_id] = request
    return indexed


def _governance_allows_planning(
    state: ArchitectureState,
    decision: ReviewDecision,
) -> bool:
    mode = state.governance_state.governance_mode
    if mode is GovernanceMode.LOCKDOWN:
        return decision.decision_type in {
            DecisionType.ROLLBACK,
            DecisionType.REJECT,
            DecisionType.RETRACT,
            DecisionType.ESCALATE,
            DecisionType.AMENDMENT_REVIEW,
        }
    if mode is GovernanceMode.EMERGENCY:
        return decision.decision_type in {
            DecisionType.REPAIR,
            DecisionType.DELAY,
            DecisionType.ROLLBACK,
            DecisionType.ESCALATE,
            DecisionType.REJECT,
            DecisionType.RETRACT,
        }
    if mode is GovernanceMode.CONSTITUTIONAL_RISK:
        return (
            decision.algorithm_name is AlgorithmName.CGA
            or decision.decision_type is DecisionType.ESCALATE
        )
    if mode is GovernanceMode.AMENDMENT_REVIEW:
        return decision.algorithm_name is AlgorithmName.CGA
    return True


def _escalation_loops_to_prior_reviewer(
    decision: ReviewDecision,
    prior_algorithms: set[AlgorithmName],
) -> bool:
    target = _parse_algorithm_reference(decision.escalation_target)
    return target in prior_algorithms


def _resolve_target_conflict(
    candidates: list[_EligibleDecision],
) -> tuple[
    _EligibleDecision | None,
    list[_EligibleDecision],
    list[_EligibleDecision],
]:
    constraints = [
        candidate for candidate in candidates if candidate.is_constraint
    ]
    active_class = constraints or candidates
    highest_authority = max(
        candidate.authority_rank for candidate in active_class
    )
    finalists = [
        candidate
        for candidate in active_class
        if candidate.authority_rank == highest_authority
    ]
    excluded = [
        candidate for candidate in candidates if candidate not in finalists
    ]
    effects = {candidate.effect_signature for candidate in finalists}
    if len(effects) > 1:
        return None, excluded, finalists
    return finalists[0], excluded, finalists[1:]


def _create_plan_artifacts(
    decision: ReviewDecision,
    *,
    audit_ref: str,
    id_provider: IDProvider,
) -> tuple[list[StateChange], list[GraphUpdate]]:
    changes: list[StateChange] = []
    updates: list[GraphUpdate] = []

    if decision.decision_type is DecisionType.APPROVE:
        return changes, updates
    if decision.decision_type is DecisionType.APPROVE_WITH_MONITORING:
        changes.append(
            _monitoring_change(
                decision,
                audit_ref,
                id_provider(),
                "approved_with_monitoring",
            )
        )
    elif decision.decision_type is DecisionType.SANDBOX:
        changes.append(
            _state_transition_change(
                decision,
                audit_ref,
                id_provider(),
                SymbolicState.SANDBOXED,
                AuthorityLevel.TEMPORARY_USE,
            )
        )
    elif decision.decision_type is DecisionType.REVISE:
        changes.append(
            StateChange(
                change_id=id_provider(),
                target_id=decision.target_id,
                change_type="mark_for_revision",
                decision_ref=decision.decision_id,
                audit_ref=audit_ref,
                payload={
                    "review_state": SymbolicState.COHERENCE_REVIEW.value,
                },
            )
        )
    elif decision.decision_type is DecisionType.REPAIR:
        changes.append(
            StateChange(
                change_id=id_provider(),
                target_id=decision.target_id,
                change_type="coherence_tension_add",
                decision_ref=decision.decision_id,
                audit_ref=audit_ref,
                payload={
                    "tension_id": (
                        f"tension:{decision.target_id}:"
                        f"{decision.decision_id}"
                    ),
                    "reason": decision.rationale,
                },
            )
        )
    elif decision.decision_type is DecisionType.DELAY:
        changes.append(
            StateChange(
                change_id=id_provider(),
                target_id=decision.target_id,
                change_type="delay",
                decision_ref=decision.decision_id,
                audit_ref=audit_ref,
                payload={"reason": decision.rationale},
            )
        )
    elif decision.decision_type is DecisionType.PROMOTE_CANDIDATE:
        changes.append(
            _monitoring_change(
                decision,
                audit_ref,
                id_provider(),
                decision.decision_type.value,
            )
        )
    elif decision.decision_type is DecisionType.DEMOTE:
        changes.append(
            StateChange(
                change_id=id_provider(),
                target_id=decision.target_id,
                change_type="scale_demotion_request",
                decision_ref=decision.decision_id,
                audit_ref=audit_ref,
                payload={"operation": "demote_one_level"},
            )
        )
        updates.append(
            GraphUpdate(
                update_id=id_provider(),
                graph_name=GraphName.SCALE_GRAPH,
                update_type=GraphUpdateType.RELATION_UPDATED,
                affected_nodes=[decision.target_id],
                affected_edges=[],
                decision_ref=decision.decision_id,
                audit_ref=audit_ref,
                payload={"operation": "sync_demoted_scale"},
            )
        )
    elif decision.decision_type is DecisionType.PERSIST:
        changes.append(
            _state_transition_change(
                decision,
                audit_ref,
                id_provider(),
                SymbolicState.PERSISTENT,
                AuthorityLevel.MEMORY_INFLUENCE,
            )
        )
        updates.append(
            _memory_node_update(decision, audit_ref, id_provider())
        )
    elif decision.decision_type is DecisionType.ARCHIVE:
        changes.append(
            _state_transition_change(
                decision,
                audit_ref,
                id_provider(),
                SymbolicState.ARCHIVED,
                AuthorityLevel.NONE,
            )
        )
        updates.append(
            _memory_node_update(decision, audit_ref, id_provider())
        )
    elif decision.decision_type is DecisionType.RETRACT:
        changes.append(
            _state_transition_change(
                decision,
                audit_ref,
                id_provider(),
                SymbolicState.RETRACTED,
                AuthorityLevel.NONE,
            )
        )
        updates.append(
            GraphUpdate(
                update_id=id_provider(),
                graph_name=GraphName.MEMORY_GRAPH,
                update_type=GraphUpdateType.RELATION_UPDATED,
                affected_nodes=[decision.target_id],
                affected_edges=[],
                decision_ref=decision.decision_id,
                audit_ref=audit_ref,
                payload={"operation": "sync_structure"},
            )
        )
    elif decision.decision_type is DecisionType.REJECT:
        changes.append(
            _state_transition_change(
                decision,
                audit_ref,
                id_provider(),
                SymbolicState.REJECTED,
                AuthorityLevel.NONE,
            )
        )
    elif decision.decision_type is DecisionType.ROLLBACK:
        changes.append(
            StateChange(
                change_id=id_provider(),
                target_id=decision.target_id,
                change_type="rollback_restore_request",
                decision_ref=decision.decision_id,
                audit_ref=audit_ref,
                payload={"status": "planned"},
            )
        )
    elif decision.decision_type is DecisionType.AMENDMENT_REVIEW:
        changes.append(
            StateChange(
                change_id=id_provider(),
                target_id=decision.target_id,
                change_type="delay",
                decision_ref=decision.decision_id,
                audit_ref=audit_ref,
                payload={"reason": decision.rationale},
            )
        )
    return changes, updates


def _state_transition_change(
    decision: ReviewDecision,
    audit_ref: str,
    change_id: str,
    new_state: SymbolicState,
    authority_level: AuthorityLevel,
) -> StateChange:
    return StateChange(
        change_id=change_id,
        target_id=decision.target_id,
        change_type="structure_state_change",
        decision_ref=decision.decision_id,
        audit_ref=audit_ref,
        payload={
            "new_state": new_state.value,
            "authority_level": authority_level.value,
        },
    )


def _monitoring_change(
    decision: ReviewDecision,
    audit_ref: str,
    change_id: str,
    condition: str,
) -> StateChange:
    return StateChange(
        change_id=change_id,
        target_id=decision.target_id,
        change_type="monitoring_trigger_add",
        decision_ref=decision.decision_id,
        audit_ref=audit_ref,
        payload={"condition": condition},
    )


def _memory_node_update(
    decision: ReviewDecision,
    audit_ref: str,
    update_id: str,
) -> GraphUpdate:
    return GraphUpdate(
        update_id=update_id,
        graph_name=GraphName.MEMORY_GRAPH,
        update_type=GraphUpdateType.NODE_ADDED,
        affected_nodes=[decision.target_id],
        affected_edges=[],
        decision_ref=decision.decision_id,
        audit_ref=audit_ref,
    )


def _create_escalation_event(
    decision: ReviewDecision,
    *,
    audit_ref: str,
    escalation_id: str,
) -> EscalationEvent:
    target_algorithm = _parse_algorithm_reference(
        decision.escalation_target
    )
    if target_algorithm is None:
        raise StateChangePlanningError(
            "validated escalation lost its registered target"
        )
    return EscalationEvent(
        escalation_id=escalation_id,
        target_id=decision.target_id,
        reason=decision.rationale,
        urgency=_escalation_urgency(decision, target_algorithm),
        decision_ref=decision.decision_id,
        from_algorithm=decision.algorithm_name,
        to_algorithm=target_algorithm,
        resolved=False,
        audit_ref=audit_ref,
    )


def _escalation_urgency(
    decision: ReviewDecision,
    target_algorithm: AlgorithmName,
) -> EscalationUrgency:
    if (
        target_algorithm is AlgorithmName.CGA
        or decision.scores.constitutional_risk_score > 0.0
    ):
        return EscalationUrgency.CRITICAL
    if (
        target_algorithm in {AlgorithmName.IPA, AlgorithmName.AEA}
        or decision.scores.identity_risk_score > 0.0
    ):
        return EscalationUrgency.HIGH
    if target_algorithm in {
        AlgorithmName.SRA,
        AlgorithmName.MSSA,
        AlgorithmName.PCA,
    }:
        return EscalationUrgency.NORMAL
    return EscalationUrgency.LOW


def _requires_rollback(
    decision: ReviewDecision,
    target: SymbolicStructure,
    graph_updates: list[GraphUpdate],
) -> bool:
    return bool(
        decision.decision_type in _HIGH_RISK_DECISIONS
        or target.metadata.scale_label in _HIGH_RISK_SCALES
        or target.metadata.authority_level in _HIGH_RISK_AUTHORITIES
        or decision.algorithm_name is AlgorithmName.CGA
        or any(
            update.graph_name is GraphName.AUTHORITY_GRAPH
            for update in graph_updates
        )
    )


def _create_rollback_point(
    decision: ReviewDecision,
    target: SymbolicStructure,
    *,
    state_ref: str,
    audit_ref: str,
    graph_updates: list[GraphUpdate],
    rollback_id: str,
) -> RollbackPoint:
    affected_graphs = list(
        dict.fromkeys(update.graph_name for update in graph_updates)
    )
    if (
        decision.decision_type is DecisionType.AMENDMENT_REVIEW
        and GraphName.AUTHORITY_GRAPH not in affected_graphs
    ):
        affected_graphs.append(GraphName.AUTHORITY_GRAPH)
    return RollbackPoint(
        rollback_id=rollback_id,
        state_ref=state_ref,
        affected_structures=[target.structure_id],
        affected_graphs=affected_graphs,
        reason_created=(
            f"High-risk plan authorized by {decision.decision_id}; "
            "capture baseline scope before application."
        ),
        audit_ref=audit_ref,
        valid_until="cycle-end",
    )


def _parse_algorithm_reference(
    value: str | None,
) -> AlgorithmName | None:
    if value is None:
        return None
    try:
        return AlgorithmName(value)
    except ValueError:
        try:
            return AlgorithmName[value]
        except KeyError:
            return None


def _remember_decision(
    destination: dict[str, ReviewDecision],
    decision: ReviewDecision,
) -> None:
    destination.setdefault(decision.decision_id, deepcopy(decision))


def _require_nonempty_text(value: str, field_name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a nonempty string")


__all__ = [
    "CONFLICT_RULES",
    "IDProvider",
    "StateChangeApplicationError",
    "StateChangePlanningError",
    "apply_state_change_plan",
    "calculate_state_delta",
    "plan_authorized_state_changes",
]
