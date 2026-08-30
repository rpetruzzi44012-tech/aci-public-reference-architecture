"""Run four representative Minimal ACI Prototype v0.1 cycles.

Run from the ``aci_prototype`` directory:

    .venv/bin/python -m examples.run_minimal_cycle
"""

from __future__ import annotations

import json
from collections import defaultdict

from aci import (
    AlgorithmName,
    ArchitectureState,
    CycleResult,
    EscalationEvent,
    EscalationUrgency,
    GovernanceState,
    run_integrated_cognitive_cycle,
)


class DeterministicExampleIDs:
    """Readable identifiers make the example output reproducible."""

    def __init__(self, prefix: str) -> None:
        self.prefix = prefix
        self.counts: defaultdict[str, int] = defaultdict(int)

    def __call__(self, kind: str) -> str:
        self.counts[kind] += 1
        return f"{self.prefix}-{kind}-{self.counts[kind]:03d}"


class ExampleFault(RuntimeError):
    """Explicit fault used only by the aborted-cycle example."""


def _fixed_time() -> str:
    return "2026-07-01T12:00:00+00:00"


def _run(
    label: str,
    state: ArchitectureState,
    content: str,
    *,
    fault_injector=None,
) -> CycleResult:
    return run_integrated_cognitive_cycle(
        state,
        content,
        id_provider=DeterministicExampleIDs(label),
        time_provider=_fixed_time,
        fault_injector=fault_injector,
    )


def build_example_results() -> dict[str, CycleResult]:
    """Return committed, escalated, governance-blocked, and aborted cycles."""

    committed = _run(
        "committed",
        ArchitectureState(state_id="state-committed"),
        "A provisional claim requiring grounding review.",
    )

    escalation = EscalationEvent(
        escalation_id="escalation-prior-001",
        target_id="escalated-structure-001",
        reason="Independent review remains pending.",
        urgency=EscalationUrgency.NORMAL,
        decision_ref="decision-prior-001",
        from_algorithm=AlgorithmName.GEA,
        to_algorithm=AlgorithmName.CRA,
        resolved=False,
        audit_ref="audit-prior-001",
    )
    escalated = _run(
        "escalated",
        ArchitectureState(
            state_id="state-escalated",
            governance_state=GovernanceState(
                pending_escalations=[escalation],
            ),
        ),
        "A qualified claim awaiting independent review.",
    )

    governance_blocked = _run(
        "blocked",
        ArchitectureState(state_id="state-governance-blocked"),
        "Propose an architectural redesign for the system.",
    )

    def fail_after_application(point: str) -> None:
        if point == "plan_applied":
            raise ExampleFault("demonstrated failure after isolated application")

    aborted = _run(
        "aborted",
        ArchitectureState(state_id="state-aborted"),
        "A claim used to demonstrate transaction abort.",
        fault_injector=fail_after_application,
    )

    return {
        "committed": committed,
        "escalated_qualified": escalated,
        "governance_blocked": governance_blocked,
        "aborted": aborted,
    }


def state_summary(result: CycleResult) -> dict:
    """Compress the returned architecture state without hiding its domains."""

    state = result.updated_state
    governance = state.governance_state
    return {
        "state_id": state.state_id,
        "active_structure_ids": sorted(state.active_structures),
        "graph_counts": {
            "memory": {
                "nodes": len(state.memory_graph.nodes),
                "relations": len(
                    state.memory_graph.persistence_relations
                ),
            },
            "evidence": {
                "objects": len(state.evidence_graph.evidence_objects),
                "links": len(state.evidence_graph.links),
                "source_relations": len(
                    state.evidence_graph.source_relations
                ),
            },
            "coherence": {
                "relations": len(state.coherence_graph.relations),
                "unresolved_tensions": len(
                    state.coherence_graph.unresolved_tensions
                ),
            },
            "scale": {
                "labels": len(state.scale_graph.scale_labels),
                "mismatches": len(state.scale_graph.mismatch_records),
            },
            "authority": {
                "edges": len(governance.authority_graph.authority_edges),
                "veto_rules": len(governance.authority_graph.veto_rules),
                "escalation_rules": len(
                    governance.authority_graph.escalation_rules
                ),
            },
        },
        "governance": {
            "mode": governance.governance_mode.value,
            "active_veto_count": len(governance.active_vetoes),
            "pending_escalation_ids": [
                event.escalation_id
                for event in governance.pending_escalations
                if not event.resolved
            ],
        },
        "audit_statuses": [
            audit.status.value for audit in state.audit_log
        ],
        "state_change_count": len(state.state_changes),
        "graph_update_count": len(state.applied_graph_updates),
        "rollback_count": len(state.rollback_points),
        "monitoring_trigger_count": len(state.monitoring_triggers),
    }


def structured_result(result: CycleResult) -> dict:
    """Expose the required cycle artifacts as JSON-serializable data."""

    state = result.updated_state
    return {
        "cycle_status": result.status.value,
        "output_object": (
            result.output.to_dict() if result.output is not None else None
        ),
        "audit_record": result.audit_record.to_dict(),
        "state_delta": (
            result.audit_record.state_delta.to_dict()
            if result.audit_record.state_delta is not None
            else None
        ),
        "unresolved_items": list(result.unresolved_items),
        "pending_escalations": [
            event.to_dict()
            for event in state.governance_state.pending_escalations
            if not event.resolved
        ],
        "state_summary": state_summary(result),
    }


def main() -> None:
    for label, result in build_example_results().items():
        print(f"=== {label} ===")
        print(
            json.dumps(
                structured_result(result),
                indent=2,
                sort_keys=True,
            )
        )


if __name__ == "__main__":
    main()
