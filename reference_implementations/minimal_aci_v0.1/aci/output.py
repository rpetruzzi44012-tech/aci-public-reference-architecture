"""Provisional, review-proportional output for Minimal ACI v0.1."""

from __future__ import annotations

from collections.abc import Callable, Iterable
from dataclasses import replace
from uuid import uuid4

from .core import (
    AuditRecord,
    EpistemicMarker,
    OutputObject,
    ReviewDecision,
    StateChangePlan,
    SymbolicStructure,
)
from .enums import (
    AlgorithmName,
    AuditStatus,
    AuthorityLevel,
    CandidateStatus,
    DecisionStatus,
    DecisionType,
    EpistemicStatus,
    GovernanceMode,
    OutputType,
    ScaleLabel,
    SymbolicState,
)
from .review_context import ReviewContext

IDProvider = Callable[[], str]

_EPISTEMIC_PRECEDENCE = (
    EpistemicStatus.REJECTED,
    EpistemicStatus.CONTRADICTED,
    EpistemicStatus.SPECULATIVE,
    EpistemicStatus.UNGROUNDED,
    EpistemicStatus.UNKNOWN,
    EpistemicStatus.INTERNALLY_COHERENT,
    EpistemicStatus.PARTIALLY_GROUNDED,
    EpistemicStatus.STRONGLY_GROUNDED,
)
_DECISION_PRECEDENCE = (
    DecisionStatus.BLOCKED,
    DecisionStatus.ESCALATED,
    DecisionStatus.PENDING_REVIEW,
    DecisionStatus.PROVISIONAL,
    DecisionStatus.MONITORING,
    DecisionStatus.FINAL,
)
_SCALE_RANK = {value: position for position, value in enumerate(ScaleLabel)}
_AUTHORITY_RANK = {
    value: position
    for position, value in enumerate(AuthorityLevel)
}
_BLOCKING_DECISIONS = frozenset(
    {
        DecisionType.REJECT,
        DecisionType.RETRACT,
        DecisionType.ROLLBACK,
    }
)
_GOVERNANCE_NOTICE_MODES = frozenset(
    {
        GovernanceMode.CONSTITUTIONAL_RISK,
        GovernanceMode.EMERGENCY,
        GovernanceMode.AMENDMENT_REVIEW,
        GovernanceMode.LOCKDOWN,
    }
)


class OutputAuthorizationError(RuntimeError):
    """Raised when output would outrun review, governance, or audit."""


def _default_id_provider() -> str:
    return f"output-{uuid4()}"


def generate_provisional_authorized_output(
    context: ReviewContext,
    plan: StateChangePlan,
    *,
    id_provider: IDProvider = _default_id_provider,
) -> OutputObject | None:
    """Create an unbound output from accepted review and plan artifacts."""

    if not isinstance(context, ReviewContext):
        raise TypeError("context must be ReviewContext")
    if not isinstance(plan, StateChangePlan):
        raise TypeError("plan must be StateChangePlan")
    if not callable(id_provider):
        raise TypeError("id_provider must be callable")

    decisions = _accepted_context_decisions(context, plan)
    if not decisions:
        return None

    structure_ids = _unique(
        decision.target_id
        for decision in decisions
    )
    structures = [
        context.get_target(structure_id)
        for structure_id in structure_ids
    ]
    decisions_by_target = {
        structure_id: [
            decision
            for decision in decisions
            if decision.target_id == structure_id
        ]
        for structure_id in structure_ids
    }
    expressive_structures = [
        structure
        for structure in structures
        if _structure_may_be_expressed(
            structure,
            decisions_by_target[structure.structure_id],
        )
    ]

    markers = collect_epistemic_markers(structures, decisions)
    unresolved_tensions = collect_unresolved_tensions(
        context,
        structure_ids,
    )
    unresolved_tensions = _unique(
        (
            *unresolved_tensions,
            *(
                f"plan-no-op:{decision.decision_id}"
                for decision in plan.no_op_items
            ),
        )
    )
    pending_escalation_ids = _collect_pending_escalation_ids(
        context,
        plan,
        structure_ids,
    )
    state = context.architecture_state
    governance_block_reasons = _governance_block_reasons(
        state=state,
        decisions=decisions,
        structure_ids=structure_ids,
    )
    if not expressive_structures and not pending_escalation_ids:
        governance_block_reasons.append(
            "accepted review permits no external structure expression"
        )

    output_type = determine_output_type(
        markers,
        decisions,
        unresolved_tensions=unresolved_tensions,
        governance_mode=state.governance_state.governance_mode,
        governance_blocked=bool(governance_block_reasons),
        pending_escalation_ids=pending_escalation_ids,
    )
    content = _compose_content(
        output_type=output_type,
        structures=expressive_structures,
        markers=markers,
        decisions=decisions,
        unresolved_tensions=unresolved_tensions,
        governance_block_reasons=governance_block_reasons,
    )

    return OutputObject(
        output_id=id_provider(),
        output_type=output_type,
        content=content,
        supporting_structure_ids=structure_ids,
        supporting_decision_ids=[
            decision.decision_id
            for decision in decisions
        ],
        epistemic_markers=markers,
        epistemic_status=_aggregate_epistemic_status(markers),
        decision_status=_aggregate_decision_status(decisions),
        scale_label=_minimum_scale(markers),
        authority_level=_minimum_authority(markers),
        grounding_score=_minimum_marker_score(
            markers,
            "grounding_score",
        ),
        coherence_score=_minimum_marker_score(
            markers,
            "coherence_score",
        ),
        uncertainty=max(
            (marker.uncertainty for marker in markers),
            default=1.0,
        ),
        unresolved_tensions=unresolved_tensions,
        pending_escalation_ids=pending_escalation_ids,
        audit_ref=None,
        audit_finalized=False,
    )


def collect_epistemic_markers(
    structures: Iterable[SymbolicStructure],
    decisions: Iterable[ReviewDecision],
) -> list[EpistemicMarker]:
    """Preserve per-structure metadata and review provenance."""

    structure_values = list(structures)
    decision_values = list(decisions)
    for position, structure in enumerate(structure_values):
        if not isinstance(structure, SymbolicStructure):
            raise TypeError(
                f"structures[{position}] must be SymbolicStructure"
            )
    for position, decision in enumerate(decision_values):
        if not isinstance(decision, ReviewDecision):
            raise TypeError(
                f"decisions[{position}] must be ReviewDecision"
            )

    markers: list[EpistemicMarker] = []
    for structure in structure_values:
        relevant = [
            decision
            for decision in decision_values
            if decision.target_id == structure.structure_id
        ]
        latest_grounding = _latest_by_algorithm(
            relevant,
            AlgorithmName.GEA,
        )
        latest_coherence = _latest_by_algorithm(
            relevant,
            AlgorithmName.CRA,
        )
        markers.append(
            EpistemicMarker(
                structure_id=structure.structure_id,
                epistemic_status=structure.metadata.epistemic_status,
                scale_label=structure.metadata.scale_label,
                candidate_status=structure.metadata.candidate_status,
                authority_level=structure.metadata.authority_level,
                grounding_score=(
                    latest_grounding.scores.grounding_score
                    if latest_grounding is not None
                    else structure.metadata.grounding_score
                ),
                coherence_score=(
                    latest_coherence.scores.coherence_score
                    if latest_coherence is not None
                    else structure.metadata.coherence_score
                ),
                uncertainty=structure.metadata.uncertainty,
                decision_refs=[
                    decision.decision_id
                    for decision in relevant
                ],
                decision_statuses=_unique(
                    decision.status
                    for decision in relevant
                ),
            )
        )
    return markers


def collect_unresolved_tensions(
    context: ReviewContext,
    supporting_structure_ids: Iterable[str],
) -> list[str]:
    """Collect relevant context and coherence-graph tension identifiers."""

    if not isinstance(context, ReviewContext):
        raise TypeError("context must be ReviewContext")
    structure_ids = _validated_refs(
        supporting_structure_ids,
        "supporting_structure_ids",
    )
    structure_id_set = set(structure_ids)
    unresolved = [
        item.item_id
        for item in context.unresolved_items
        if item.target_id in structure_id_set
    ]
    coherence = context.architecture_state.coherence_graph
    for tension_id in coherence.unresolved_tensions:
        matching_relations = [
            relation
            for relation in coherence.relations
            if _relation_identifier(relation) == tension_id
        ]
        if not matching_relations or any(
            _relation_touches_structures(
                relation,
                structure_id_set,
            )
            for relation in matching_relations
        ):
            unresolved.append(tension_id)
    return _unique(unresolved)


def determine_output_type(
    markers: Iterable[EpistemicMarker],
    decisions: Iterable[ReviewDecision],
    *,
    unresolved_tensions: Iterable[str] = (),
    governance_mode: GovernanceMode = GovernanceMode.NORMAL,
    governance_blocked: bool = False,
    pending_escalation_ids: Iterable[str] = (),
) -> OutputType:
    """Select the least authoritative output type consistent with review."""

    marker_values = list(markers)
    decision_values = list(decisions)
    tension_values = _validated_refs(
        unresolved_tensions,
        "unresolved_tensions",
    )
    escalation_values = _validated_refs(
        pending_escalation_ids,
        "pending_escalation_ids",
    )
    if not isinstance(governance_mode, GovernanceMode):
        raise TypeError("governance_mode must be GovernanceMode")
    if not isinstance(governance_blocked, bool):
        raise TypeError("governance_blocked must be bool")
    for position, marker in enumerate(marker_values):
        if not isinstance(marker, EpistemicMarker):
            raise TypeError(
                f"markers[{position}] must be EpistemicMarker"
            )
    for position, decision in enumerate(decision_values):
        if not isinstance(decision, ReviewDecision):
            raise TypeError(
                f"decisions[{position}] must be ReviewDecision"
            )

    if governance_blocked:
        return OutputType.NO_OUTPUT
    if escalation_values or any(
        decision.decision_type is DecisionType.ESCALATE
        or decision.status is DecisionStatus.ESCALATED
        for decision in decision_values
    ):
        return OutputType.ESCALATION_NOTICE
    if governance_mode in _GOVERNANCE_NOTICE_MODES or any(
        decision.recommended_governance_mode
        in _GOVERNANCE_NOTICE_MODES
        for decision in decision_values
    ):
        return OutputType.GOVERNANCE_NOTICE
    if any(
        marker.epistemic_status is EpistemicStatus.SPECULATIVE
        for marker in marker_values
    ):
        return OutputType.SPECULATIVE_RESPONSE
    if (
        governance_mode is GovernanceMode.CAUTION
        or tension_values
        or any(
            decision.status is DecisionStatus.BLOCKED
            or decision.decision_type in _BLOCKING_DECISIONS
            for decision in decision_values
        )
        or any(
            marker.epistemic_status
            in {
                EpistemicStatus.UNKNOWN,
                EpistemicStatus.UNGROUNDED,
                EpistemicStatus.INTERNALLY_COHERENT,
                EpistemicStatus.PARTIALLY_GROUNDED,
                EpistemicStatus.CONTRADICTED,
                EpistemicStatus.REJECTED,
            }
            for marker in marker_values
        )
    ):
        return OutputType.QUALIFIED_RESPONSE
    if marker_values and all(
        marker.epistemic_status
        is EpistemicStatus.STRONGLY_GROUNDED
        for marker in marker_values
    ):
        return OutputType.GROUNDED_RESPONSE
    return OutputType.QUALIFIED_RESPONSE


def bind_audit_ref_to_output(
    output: OutputObject | None,
    audit: AuditRecord,
) -> OutputObject | None:
    """Bind only a finalized audit that explicitly committed this output."""

    if not isinstance(audit, AuditRecord):
        raise TypeError("audit must be AuditRecord")
    if audit.status is not AuditStatus.COMMITTED:
        raise OutputAuthorizationError(
            "output binding requires finalized COMMITTED audit"
        )
    if output is None:
        if audit.provisional_output_ref is not None or audit.output_refs:
            raise OutputAuthorizationError(
                "committed audit names an output but none was supplied"
            )
        return None
    if not isinstance(output, OutputObject):
        raise TypeError("output must be OutputObject or None")
    if output.audit_ref is not None or output.audit_finalized:
        raise OutputAuthorizationError(
            "output is already audit-bound"
        )
    if (
        audit.provisional_output_ref != output.output_id
        or output.output_id not in audit.output_refs
    ):
        raise OutputAuthorizationError(
            "committed audit does not authorize this provisional output"
        )
    return replace(
        output,
        audit_ref=audit.audit_id,
        audit_finalized=True,
    )


def _accepted_context_decisions(
    context: ReviewContext,
    plan: StateChangePlan,
) -> list[ReviewDecision]:
    if plan.audit_ref != context.audit_id:
        raise OutputAuthorizationError(
            "plan and review context must share an audit reference"
        )
    decisions_by_id = {
        decision.decision_id: decision
        for decision in context.decisions
    }
    accepted_validation_refs = {
        result.decision_id
        for result in plan.validation_results
        if result.accepted
    }
    decisions: list[ReviewDecision] = []
    for decision_ref in plan.decision_refs:
        decision = decisions_by_id.get(decision_ref)
        if decision is None:
            raise OutputAuthorizationError(
                "plan references a decision absent from ReviewContext"
            )
        if decision_ref not in accepted_validation_refs:
            raise OutputAuthorizationError(
                "output support requires preserved accepted validation"
            )
        if decision.audit_id != context.audit_id:
            raise OutputAuthorizationError(
                "supporting decision has the wrong audit reference"
            )
        decisions.append(decision)
    return decisions


def _structure_may_be_expressed(
    structure: SymbolicStructure,
    decisions: list[ReviewDecision],
) -> bool:
    if structure.current_state in {
        SymbolicState.REJECTED,
        SymbolicState.RETRACTED,
    }:
        return False
    return not any(
        decision.decision_type in _BLOCKING_DECISIONS
        or decision.status is DecisionStatus.BLOCKED
        for decision in decisions
    )


def _collect_pending_escalation_ids(
    context: ReviewContext,
    plan: StateChangePlan,
    structure_ids: list[str],
) -> list[str]:
    structure_id_set = set(structure_ids)
    state_events = (
        context.architecture_state
        .governance_state
        .pending_escalations
    )
    return _unique(
        (
            *(
                event.escalation_id
                for event in plan.escalation_events
                if not event.resolved
                and event.target_id in structure_id_set
            ),
            *(
                event.escalation_id
                for event in state_events
                if not event.resolved
                and event.target_id in structure_id_set
            ),
        )
    )


def _governance_block_reasons(
    *,
    state,
    decisions: list[ReviewDecision],
    structure_ids: list[str],
) -> list[str]:
    reasons: list[str] = []
    if state.governance_state.governance_mode is GovernanceMode.LOCKDOWN:
        reasons.append("governance mode is LOCKDOWN")
    for decision in decisions:
        if decision.output_block_recommended:
            reasons.append(
                f"{decision.decision_id} recommends output blocking"
            )
    structure_id_set = set(structure_ids)
    for position, veto in enumerate(
        state.governance_state.active_vetoes
    ):
        target_id = veto.get("target_id")
        if (
            not isinstance(target_id, str)
            or not target_id.strip()
            or target_id == "*"
            or target_id in structure_id_set
        ):
            veto_id = veto.get("veto_id")
            reasons.append(
                f"active veto {veto_id or position} constrains output"
            )
    return _unique(reasons)


def _compose_content(
    *,
    output_type: OutputType,
    structures: list[SymbolicStructure],
    markers: list[EpistemicMarker],
    decisions: list[ReviewDecision],
    unresolved_tensions: list[str],
    governance_block_reasons: list[str],
) -> str | None:
    if output_type is OutputType.NO_OUTPUT:
        return None
    if output_type is OutputType.ESCALATION_NOTICE:
        return (
            "Review remains pending through escalation. "
            "Escalation transfers review obligation; it is not approval."
        )
    if output_type is OutputType.GOVERNANCE_NOTICE:
        return (
            "Governance review constrains this result. "
            "Usefulness, coherence, repetition, or architecture do not "
            "establish legitimacy or constitutional approval."
        )

    text = " ".join(
        structure.content.strip()
        for structure in structures
        if structure.content.strip()
    )
    qualifiers: list[str] = []
    statuses = {
        marker.epistemic_status
        for marker in markers
    }
    if EpistemicStatus.SPECULATIVE in statuses:
        qualifiers.append(
            "This is speculative and is not established knowledge."
        )
    if EpistemicStatus.INTERNALLY_COHERENT in statuses:
        qualifiers.append(
            "Internal coherence is not external evidence."
        )
    if EpistemicStatus.PARTIALLY_GROUNDED in statuses:
        qualifiers.append(
            "Grounding is partial and remains qualified."
        )
    if EpistemicStatus.UNGROUNDED in statuses:
        qualifiers.append(
            "External grounding has not been established."
        )
    if any(
        marker.scale_label is ScaleLabel.MEMORY
        or marker.authority_level is AuthorityLevel.MEMORY_INFLUENCE
        for marker in markers
    ):
        qualifiers.append(
            "Persistent memory is not an invariant."
        )
    if any(
        marker.candidate_status is not CandidateStatus.NONE
        for marker in markers
    ):
        qualifiers.append(
            "Candidate status is not achieved scale or authority."
        )
    if any(
        decision.algorithm_name is AlgorithmName.CGA
        for decision in decisions
    ):
        qualifiers.append(
            "Usefulness does not establish governance legitimacy."
        )
    if any(
        decision.status is DecisionStatus.BLOCKED
        or decision.decision_type in _BLOCKING_DECISIONS
        for decision in decisions
    ):
        qualifiers.append(
            "Some reviewed structures were not authorized for expression."
        )
    if unresolved_tensions:
        qualifiers.append("Unresolved tensions remain.")
    if governance_block_reasons:
        qualifiers.append("Governance constraints remain active.")
    if not text:
        text = "Reviewed structures permit only a qualified status notice."
    return " ".join((text, *qualifiers))


def _aggregate_epistemic_status(
    markers: list[EpistemicMarker],
) -> EpistemicStatus:
    statuses = {
        marker.epistemic_status
        for marker in markers
    }
    for status in _EPISTEMIC_PRECEDENCE:
        if status in statuses:
            return status
    return EpistemicStatus.UNKNOWN


def _aggregate_decision_status(
    decisions: list[ReviewDecision],
) -> DecisionStatus:
    statuses = {decision.status for decision in decisions}
    for status in _DECISION_PRECEDENCE:
        if status in statuses:
            return status
    return DecisionStatus.PROVISIONAL


def _minimum_scale(
    markers: list[EpistemicMarker],
) -> ScaleLabel:
    return min(
        (marker.scale_label for marker in markers),
        key=_SCALE_RANK.__getitem__,
        default=ScaleLabel.OBSERVATION,
    )


def _minimum_authority(
    markers: list[EpistemicMarker],
) -> AuthorityLevel:
    return min(
        (marker.authority_level for marker in markers),
        key=_AUTHORITY_RANK.__getitem__,
        default=AuthorityLevel.NONE,
    )


def _minimum_marker_score(
    markers: list[EpistemicMarker],
    field_name: str,
) -> float:
    return min(
        (
            float(getattr(marker, field_name))
            for marker in markers
        ),
        default=0.0,
    )


def _latest_by_algorithm(
    decisions: list[ReviewDecision],
    algorithm: AlgorithmName,
) -> ReviewDecision | None:
    for decision in reversed(decisions):
        if decision.algorithm_name is algorithm:
            return decision
    return None


def _relation_identifier(relation: dict) -> str | None:
    for key in ("tension_id", "relation_id", "id"):
        value = relation.get(key)
        if isinstance(value, str) and value:
            return value
    return None


def _relation_touches_structures(
    relation: dict,
    structure_ids: set[str],
) -> bool:
    for key in (
        "target_id",
        "structure_id",
        "left_structure_id",
        "right_structure_id",
    ):
        value = relation.get(key)
        if isinstance(value, str) and value in structure_ids:
            return True
    values = relation.get("structure_ids")
    return bool(
        isinstance(values, list)
        and structure_ids.intersection(
            value
            for value in values
            if isinstance(value, str)
        )
    )


def _validated_refs(
    values: Iterable[str],
    field_name: str,
) -> list[str]:
    refs = list(values)
    for position, value in enumerate(refs):
        if not isinstance(value, str) or not value.strip():
            raise ValueError(
                f"{field_name}[{position}] must be nonempty text"
            )
    return _unique(refs)


def _unique(values: Iterable) -> list:
    return list(dict.fromkeys(values))


__all__ = [
    "IDProvider",
    "OutputAuthorizationError",
    "bind_audit_ref_to_output",
    "collect_epistemic_markers",
    "collect_unresolved_tensions",
    "determine_output_type",
    "generate_provisional_authorized_output",
]
