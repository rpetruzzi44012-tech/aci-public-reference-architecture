"""Logical audit reservation, finalization, and reference binding."""

from __future__ import annotations

import hashlib
import json
from collections.abc import Callable, Iterable
from copy import deepcopy
from dataclasses import dataclass, field, fields, replace
from datetime import datetime, timezone
from uuid import uuid4

from .core import (
    AuditRecord,
    EscalationEvent,
    GraphUpdate,
    JSONValue,
    OutputObject,
    ReviewDecision,
    RollbackPoint,
    StateChange,
    StateChangePlan,
    StateDelta,
    SymbolicStructure,
)
from .enums import AlgorithmName, AuditStatus
from .state import ArchitectureState, StateBaseline

IDProvider = Callable[[], str]
TimeProvider = Callable[[], str]


class AuditLifecycleError(RuntimeError):
    """Raised when an audit transition or reference binding is illegal."""


@dataclass(slots=True)
class CommittedAuditData:
    """Evidence retained when a pending audit commits."""

    target_structure_ids: list[str] = field(default_factory=list)
    created_structures: list[SymbolicStructure] = field(default_factory=list)
    algorithms_invoked: list[AlgorithmName] = field(default_factory=list)
    decisions: list[ReviewDecision] = field(default_factory=list)
    accepted_plan_items: list[StateChange] = field(default_factory=list)
    rejected_plan_items: list[StateChange] = field(default_factory=list)
    state_change_plan: StateChangePlan | None = None
    graph_updates: list[GraphUpdate] = field(default_factory=list)
    budget_effects: list[dict[str, JSONValue]] = field(default_factory=list)
    threshold_effects: list[dict[str, JSONValue]] = field(default_factory=list)
    rollback_points_created: list[RollbackPoint] = field(default_factory=list)
    state_delta: StateDelta | None = None
    provisional_output_ref: str | None = None
    unresolved_tensions: list[str] = field(default_factory=list)
    escalation_events: list[EscalationEvent] = field(default_factory=list)


@dataclass(slots=True)
class AbortedAuditData:
    """Non-mutating trace retained when a pending audit aborts."""

    failure_stage: str
    error: str
    target_structure_ids: list[str] = field(default_factory=list)
    algorithms_invoked: list[AlgorithmName] = field(default_factory=list)
    decisions: list[ReviewDecision] = field(default_factory=list)
    rejected_plan_items: list[StateChange] = field(default_factory=list)
    state_change_plan: StateChangePlan | None = None
    unresolved_tensions: list[str] = field(default_factory=list)
    escalation_events: list[EscalationEvent] = field(default_factory=list)


def _default_id_provider() -> str:
    return f"audit-{uuid4()}"


def _default_time_provider() -> str:
    return datetime.now(timezone.utc).isoformat()


def _require_pending(audit: AuditRecord) -> None:
    if not isinstance(audit, AuditRecord):
        raise TypeError("audit must be AuditRecord")
    if audit.status is not AuditStatus.PENDING:
        raise AuditLifecycleError(
            f"audit {audit.audit_id} already finalized as {audit.status.value}"
        )


def _unique(values: Iterable[str]) -> list[str]:
    return list(dict.fromkeys(values))


def _matching_audit_reference(
    value: str | None,
    audit_id: str,
    field_name: str,
) -> None:
    if value != audit_id:
        raise ValueError(f"{field_name} must reference audit {audit_id}")


def _validate_commit_references(
    audit: AuditRecord,
    data: CommittedAuditData,
) -> None:
    for decision in data.decisions:
        _matching_audit_reference(
            decision.audit_id,
            audit.audit_id,
            f"decision {decision.decision_id} audit_id",
        )
    for change in (*data.accepted_plan_items, *data.rejected_plan_items):
        _matching_audit_reference(
            change.audit_ref,
            audit.audit_id,
            f"state change {change.change_id} audit_ref",
        )
    _validate_plan_witness(
        audit,
        data.state_change_plan,
        data.decisions,
    )
    for update in data.graph_updates:
        _matching_audit_reference(
            update.audit_ref,
            audit.audit_id,
            f"graph update {update.update_id} audit_ref",
        )
    for rollback in data.rollback_points_created:
        _matching_audit_reference(
            rollback.audit_ref,
            audit.audit_id,
            f"rollback point {rollback.rollback_id} audit_ref",
        )
    for escalation in data.escalation_events:
        _matching_audit_reference(
            escalation.audit_ref,
            audit.audit_id,
            f"escalation {escalation.escalation_id} audit_ref",
        )
    if data.state_delta is not None:
        _matching_audit_reference(
            data.state_delta.audit_ref,
            audit.audit_id,
            f"state delta {data.state_delta.delta_id} audit_ref",
        )


def _validate_abort_references(
    audit: AuditRecord,
    data: AbortedAuditData,
) -> None:
    for decision in data.decisions:
        _matching_audit_reference(
            decision.audit_id,
            audit.audit_id,
            f"decision {decision.decision_id} audit_id",
        )
    for change in data.rejected_plan_items:
        _matching_audit_reference(
            change.audit_ref,
            audit.audit_id,
            f"state change {change.change_id} audit_ref",
        )
    _validate_plan_witness(
        audit,
        data.state_change_plan,
        data.decisions,
    )
    for escalation in data.escalation_events:
        _matching_audit_reference(
            escalation.audit_ref,
            audit.audit_id,
            f"escalation {escalation.escalation_id} audit_ref",
        )


def _validate_plan_witness(
    audit: AuditRecord,
    plan: StateChangePlan | None,
    decisions: Iterable[ReviewDecision],
) -> None:
    if plan is None:
        return
    _matching_audit_reference(
        plan.audit_ref,
        audit.audit_id,
        f"state change plan {plan.plan_id} audit_ref",
    )
    recorded_decision_ids = {
        decision.decision_id for decision in decisions
    }
    plan_decisions = (
        *plan.rejected_decisions,
        *plan.no_op_items,
    )
    plan_decision_ids = {
        *plan.decision_refs,
        *(decision.decision_id for decision in plan_decisions),
    }
    missing_decision_ids = plan_decision_ids - recorded_decision_ids
    if missing_decision_ids:
        missing = ", ".join(sorted(missing_decision_ids))
        raise ValueError(
            "state change plan references decisions absent from audit: "
            f"{missing}"
        )
    for decision in plan_decisions:
        _matching_audit_reference(
            decision.audit_id,
            audit.audit_id,
            f"plan decision {decision.decision_id} audit_id",
        )


def _apply_validated_transition(
    audit: AuditRecord,
    candidate: AuditRecord,
) -> AuditRecord:
    for audit_field in fields(AuditRecord):
        setattr(
            audit,
            audit_field.name,
            deepcopy(getattr(candidate, audit_field.name)),
        )
    return audit


def capture_baseline_reference(
    baseline: ArchitectureState | StateBaseline,
) -> str:
    """Return the state identity represented by a live state or baseline."""

    if isinstance(baseline, StateBaseline):
        return baseline.source_state_id
    if isinstance(baseline, ArchitectureState):
        return baseline.state_id
    raise TypeError("baseline must be ArchitectureState or StateBaseline")


def capture_baseline_fingerprint(
    baseline: ArchitectureState | StateBaseline,
) -> str:
    """Create a deterministic diagnostic fingerprint of logical state."""

    if isinstance(baseline, StateBaseline):
        state = baseline.clone()
    elif isinstance(baseline, ArchitectureState):
        state = baseline
    else:
        raise TypeError("baseline must be ArchitectureState or StateBaseline")
    encoded = json.dumps(
        state.to_dict(),
        ensure_ascii=True,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    return f"sha256:{hashlib.sha256(encoded).hexdigest()}"


def create_pending_audit(
    *,
    cycle_id: str,
    input_ref: str,
    baseline_state_ref: str,
    baseline_fingerprint: str | None = None,
    id_provider: IDProvider = _default_id_provider,
    time_provider: TimeProvider = _default_time_provider,
) -> AuditRecord:
    """Reserve a real PENDING audit before any domain mutation."""

    return AuditRecord(
        audit_id=id_provider(),
        status=AuditStatus.PENDING,
        cycle_id=cycle_id,
        input_ref=input_ref,
        baseline_state_ref=baseline_state_ref,
        baseline_fingerprint=baseline_fingerprint,
        started_at=time_provider(),
    )


def finalize_committed_audit(
    audit: AuditRecord,
    data: CommittedAuditData,
    *,
    time_provider: TimeProvider = _default_time_provider,
) -> AuditRecord:
    """Atomically perform the only legal successful terminal transition."""

    _require_pending(audit)
    if not isinstance(data, CommittedAuditData):
        raise TypeError("data must be CommittedAuditData")
    _validate_commit_references(audit, data)
    committed = deepcopy(data)
    target_structure_ids = _unique(
        [
            *committed.target_structure_ids,
            *(item.structure_id for item in committed.created_structures),
            *(item.target_id for item in committed.decisions),
        ]
    )
    algorithms_invoked = list(
        dict.fromkeys(
            [
                *committed.algorithms_invoked,
                *(item.algorithm_name for item in committed.decisions),
            ]
        )
    )
    candidate = replace(
        audit,
        status=AuditStatus.COMMITTED,
        finalized_at=time_provider(),
        target_structure_ids=target_structure_ids,
        created_structures=committed.created_structures,
        algorithms_invoked=algorithms_invoked,
        decisions=committed.decisions,
        accepted_plan_items=committed.accepted_plan_items,
        rejected_plan_items=committed.rejected_plan_items,
        state_change_plan=committed.state_change_plan,
        graph_updates=committed.graph_updates,
        budget_effects=committed.budget_effects,
        threshold_effects=committed.threshold_effects,
        rollback_points_created=committed.rollback_points_created,
        state_delta=committed.state_delta,
        provisional_output_ref=committed.provisional_output_ref,
        unresolved_tensions=committed.unresolved_tensions,
        escalation_events=committed.escalation_events,
        decision_refs=[
            decision.decision_id for decision in committed.decisions
        ],
        state_change_refs=[
            change.change_id for change in committed.accepted_plan_items
        ],
        graph_update_refs=[
            update.update_id for update in committed.graph_updates
        ],
        escalation_refs=[
            event.escalation_id for event in committed.escalation_events
        ],
        rollback_refs=[
            point.rollback_id for point in committed.rollback_points_created
        ],
        output_refs=(
            [committed.provisional_output_ref]
            if committed.provisional_output_ref is not None
            else []
        ),
        failure_stage=None,
        error=None,
    )
    return _apply_validated_transition(audit, candidate)


def finalize_aborted_audit(
    audit: AuditRecord,
    data: AbortedAuditData,
    *,
    time_provider: TimeProvider = _default_time_provider,
) -> AuditRecord:
    """Atomically abort while recording no committed domain delta."""

    _require_pending(audit)
    if not isinstance(data, AbortedAuditData):
        raise TypeError("data must be AbortedAuditData")
    _validate_abort_references(audit, data)
    aborted = deepcopy(data)
    target_structure_ids = _unique(
        [
            *aborted.target_structure_ids,
            *(item.target_id for item in aborted.decisions),
        ]
    )
    algorithms_invoked = list(
        dict.fromkeys(
            [
                *aborted.algorithms_invoked,
                *(item.algorithm_name for item in aborted.decisions),
            ]
        )
    )
    candidate = replace(
        audit,
        status=AuditStatus.ABORTED,
        finalized_at=time_provider(),
        target_structure_ids=target_structure_ids,
        created_structures=[],
        algorithms_invoked=algorithms_invoked,
        decisions=aborted.decisions,
        accepted_plan_items=[],
        rejected_plan_items=aborted.rejected_plan_items,
        state_change_plan=aborted.state_change_plan,
        graph_updates=[],
        budget_effects=[],
        threshold_effects=[],
        rollback_points_created=[],
        state_delta=None,
        provisional_output_ref=None,
        unresolved_tensions=aborted.unresolved_tensions,
        escalation_events=aborted.escalation_events,
        decision_refs=[
            decision.decision_id for decision in aborted.decisions
        ],
        state_change_refs=[],
        graph_update_refs=[],
        escalation_refs=[
            event.escalation_id for event in aborted.escalation_events
        ],
        rollback_refs=[],
        output_refs=[],
        failure_stage=aborted.failure_stage,
        error=aborted.error,
    )
    return _apply_validated_transition(audit, candidate)


def bind_audit_reference_to_output(
    output: OutputObject,
    audit: AuditRecord,
) -> OutputObject:
    """Return an output copy bound to a non-aborted audit reservation."""

    if not isinstance(output, OutputObject):
        raise TypeError("output must be OutputObject")
    if not isinstance(audit, AuditRecord):
        raise TypeError("audit must be AuditRecord")
    if audit.status is AuditStatus.ABORTED:
        raise AuditLifecycleError("cannot bind output to an aborted audit")
    return replace(output, audit_ref=audit.audit_id)


def bind_audit_reference_to_state_change(
    change: StateChange,
    audit: AuditRecord,
) -> StateChange:
    """Return a state-change copy bound to a non-aborted audit reservation."""

    if not isinstance(change, StateChange):
        raise TypeError("change must be StateChange")
    if not isinstance(audit, AuditRecord):
        raise TypeError("audit must be AuditRecord")
    if audit.status is AuditStatus.ABORTED:
        raise AuditLifecycleError("cannot bind state change to an aborted audit")
    return replace(change, audit_ref=audit.audit_id)


__all__ = [
    "AbortedAuditData",
    "AuditLifecycleError",
    "CommittedAuditData",
    "IDProvider",
    "TimeProvider",
    "bind_audit_reference_to_output",
    "bind_audit_reference_to_state_change",
    "capture_baseline_fingerprint",
    "capture_baseline_reference",
    "create_pending_audit",
    "finalize_aborted_audit",
    "finalize_committed_audit",
]
