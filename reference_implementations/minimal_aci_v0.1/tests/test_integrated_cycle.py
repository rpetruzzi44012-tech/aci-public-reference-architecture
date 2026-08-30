from __future__ import annotations

from collections import defaultdict
from copy import deepcopy

import pytest

from aci import (
    CYCLE_FAULT_POINTS,
    AlgorithmName,
    ArchitectureState,
    AuditStatus,
    BudgetState,
    CycleStatus,
    DecisionType,
    GovernanceMode,
    InputObject,
    OutputType,
    run_integrated_cognitive_cycle,
)


class DeterministicIDs:
    def __init__(self) -> None:
        self._counts: defaultdict[str, int] = defaultdict(int)

    def __call__(self, kind: str) -> str:
        self._counts[kind] += 1
        return f"{kind}-{self._counts[kind]:03d}"


class InjectedFault(RuntimeError):
    pass


def _fixed_time() -> str:
    return "2026-06-30T12:00:00+00:00"


def _domain_snapshot(state: ArchitectureState) -> dict:
    snapshot = state.to_dict()
    snapshot.pop("audit_log")
    return snapshot


def _state_with_nested_baseline_data() -> ArchitectureState:
    state = ArchitectureState(
        state_id="state-baseline",
        budgets=BudgetState(
            stability_budget=0.9,
            novelty_budget=0.8,
            verification_budget=0.7,
            attention_budget=0.6,
            recovery_capacity=0.5,
        ),
    )
    state.memory_graph.nodes["memory-existing"] = {
        "label": "existing",
        "provenance": {"source": "baseline"},
    }
    state.governance_state.active_vetoes.append(
        {
            "veto_id": "veto-existing",
            "scope": {"target_id": "other-structure"},
        }
    )
    state.monitoring_triggers.append("monitor-existing")
    return state


def test_committed_cycle_runs_governed_order_and_binds_all_effects() -> None:
    state = _state_with_nested_baseline_data()
    original = deepcopy(state)
    checkpoints: list[str] = []

    result = run_integrated_cognitive_cycle(
        state,
        "This claim says there is evidence, but supplies no typed link.",
        id_provider=DeterministicIDs(),
        time_provider=_fixed_time,
        fault_injector=checkpoints.append,
    )

    assert result.status is CycleStatus.COMMITTED
    assert result.audit_record.status is AuditStatus.COMMITTED
    assert result.error is None
    assert result.updated_state is not state
    assert state == original
    assert result.output is not None
    assert result.output.audit_finalized is True
    assert result.output.audit_ref == result.audit_record.audit_id
    assert result.output.output_id in result.audit_record.output_refs
    assert result.updated_state.audit_log == [result.audit_record]
    assert result.audit_record.state_delta is not None
    assert result.audit_record.state_delta.audit_ref == result.audit_record.audit_id
    assert result.audit_record.state_change_plan is not None
    assert result.audit_record.created_structures
    assert result.audit_record.decisions
    assert checkpoints == list(CYCLE_FAULT_POINTS)

    assert result.audit_record.algorithms_invoked == [
        AlgorithmName.ICC,
        AlgorithmName.NGSA,
        AlgorithmName.GEA,
        AlgorithmName.CRA,
        AlgorithmName.SRA,
        AlgorithmName.IPA,
        AlgorithmName.PCA,
        AlgorithmName.MSSA,
        AlgorithmName.AEA,
        AlgorithmName.CGA,
    ]
    assert {
        decision.algorithm_name
        for decision in result.audit_record.decisions
    } == {AlgorithmName.GEA}
    witnessed_plan = result.audit_record.state_change_plan
    disposed_decision_ids = {
        *witnessed_plan.decision_refs,
        *(
            decision.decision_id
            for decision in witnessed_plan.rejected_decisions
        ),
        *(
            decision.decision_id
            for decision in witnessed_plan.no_op_items
        ),
    }
    assert disposed_decision_ids == set(result.audit_record.decision_refs)
    for change in result.updated_state.state_changes:
        assert change.audit_ref == result.audit_record.audit_id
        assert change.decision_ref in result.audit_record.decision_refs


@pytest.mark.parametrize("fault_point", CYCLE_FAULT_POINTS)
def test_every_injected_fault_aborts_without_domain_leak(
    fault_point: str,
) -> None:
    state = _state_with_nested_baseline_data()
    baseline_domain = _domain_snapshot(state)
    baseline_audits = deepcopy(state.audit_log)

    def inject(point: str) -> None:
        if point == fault_point:
            raise InjectedFault(point)

    result = run_integrated_cognitive_cycle(
        state,
        "A provisional claim for transactional testing.",
        id_provider=DeterministicIDs(),
        time_provider=_fixed_time,
        fault_injector=inject,
    )

    assert result.status is CycleStatus.ABORTED
    assert result.audit_record.status is AuditStatus.ABORTED
    assert result.audit_record.failure_stage == fault_point
    assert result.output is None
    assert result.error == f"InjectedFault: {fault_point}"
    assert _domain_snapshot(result.updated_state) == baseline_domain
    assert result.updated_state.audit_log[:-1] == baseline_audits
    assert result.updated_state.audit_log[-1] == result.audit_record
    assert result.audit_record.accepted_plan_items == []
    assert result.audit_record.graph_updates == []
    assert result.audit_record.rollback_points_created == []
    assert result.audit_record.state_delta is None
    assert state.audit_log == baseline_audits
    assert _domain_snapshot(state) == baseline_domain


def test_invalid_input_after_reservation_returns_aborted_cycle() -> None:
    state = ArchitectureState(state_id="state-input-failure")

    result = run_integrated_cognitive_cycle(
        state,
        "   ",
        id_provider=DeterministicIDs(),
        time_provider=_fixed_time,
    )

    assert result.status is CycleStatus.ABORTED
    assert result.audit_record.failure_stage == "input_parsed"
    assert result.output is None
    assert result.updated_state.active_structures == {}
    assert len(result.updated_state.audit_log) == 1
    assert result.updated_state.audit_log[0].status is AuditStatus.ABORTED


def test_conflicting_input_audit_reference_aborts_before_parsing() -> None:
    state = ArchitectureState(state_id="state-input-audit-conflict")
    input_object = InputObject(
        input_id="input-existing",
        content="A claim.",
        audit_ref="audit-from-another-cycle",
    )

    result = run_integrated_cognitive_cycle(
        state,
        input_object,
        id_provider=DeterministicIDs(),
        time_provider=_fixed_time,
    )

    assert result.status is CycleStatus.ABORTED
    assert result.audit_record.failure_stage == "input_parsed"
    assert "conflicts with the current PENDING audit" in result.error
    assert result.updated_state.active_structures == {}


def test_state_owned_budget_pressure_is_visible_to_registered_stub() -> None:
    state = ArchitectureState(
        state_id="state-budget-pressure",
        budgets=BudgetState(
            stability_budget=0.1,
            novelty_budget=0.8,
            verification_budget=0.8,
            attention_budget=0.1,
            recovery_capacity=0.8,
        ),
    )

    result = run_integrated_cognitive_cycle(
        state,
        "Propose an architecture for this system.",
        id_provider=DeterministicIDs(),
        time_provider=_fixed_time,
    )

    assert result.status is CycleStatus.COMMITTED
    sra_decisions = [
        decision
        for decision in result.audit_record.decisions
        if decision.algorithm_name is AlgorithmName.SRA
    ]
    assert len(sra_decisions) == 1
    assert "stability_budget_below_threshold" in sra_decisions[0].rationale
    assert "attention_budget_pressure" in sra_decisions[0].rationale
    assert result.updated_state.budgets == state.budgets
    assert result.updated_state.thresholds == state.thresholds


def test_lockdown_can_commit_without_authorized_external_output() -> None:
    state = ArchitectureState(state_id="state-lockdown")
    state.governance_state.governance_mode = GovernanceMode.LOCKDOWN

    result = run_integrated_cognitive_cycle(
        state,
        "A provisional claim.",
        id_provider=DeterministicIDs(),
        time_provider=_fixed_time,
    )

    assert result.status is CycleStatus.COMMITTED
    assert result.output is None
    assert result.audit_record.provisional_output_ref is None
    assert result.audit_record.output_refs == []


def test_protected_output_rule_review_blocks_without_mutating_governance() -> None:
    state = ArchitectureState(state_id="state-amendment-review")

    result = run_integrated_cognitive_cycle(
        state,
        "Govern the protected output rule change.",
        id_provider=DeterministicIDs(),
        time_provider=_fixed_time,
    )

    assert result.status is CycleStatus.COMMITTED
    assert result.output is not None
    assert result.output.output_type is OutputType.NO_OUTPUT
    cga_decisions = [
        decision
        for decision in result.audit_record.decisions
        if decision.algorithm_name is AlgorithmName.CGA
    ]
    assert len(cga_decisions) == 1
    assert cga_decisions[0].decision_type is DecisionType.AMENDMENT_REVIEW
    assert cga_decisions[0].output_block_recommended is True
    assert (
        result.updated_state.governance_state.governance_mode
        is GovernanceMode.NORMAL
    )
    assert result.audit_record.state_change_plan is not None
    assert [
        change.change_type
        for change in result.audit_record.state_change_plan.changes
    ] == ["delay"]
    assert result.audit_record.rollback_points_created
