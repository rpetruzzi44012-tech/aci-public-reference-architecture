import json
from collections import defaultdict
from copy import deepcopy

import pytest

from aci.audit import (
    AbortedAuditData,
    AuditLifecycleError,
    CommittedAuditData,
    bind_audit_reference_to_output,
    bind_audit_reference_to_state_change,
    capture_baseline_fingerprint,
    capture_baseline_reference,
    create_pending_audit,
    finalize_aborted_audit,
    finalize_committed_audit,
)
from aci.core import (
    EscalationEvent,
    GraphUpdate,
    OutputObject,
    ReviewDecision,
    RollbackPoint,
    ScoreBundle,
    StateChange,
    StateDelta,
    SymbolicMetadata,
    SymbolicStructure,
)
from aci.enums import (
    AlgorithmName,
    AuditStatus,
    AuthorityLevel,
    CandidateStatus,
    DecisionStatus,
    DecisionType,
    EpistemicStatus,
    EscalationUrgency,
    GraphName,
    GraphUpdateType,
    GovernanceMode,
    OutputType,
    ScaleLabel,
    StructureType,
    SymbolicState,
)
from aci.cycle import run_integrated_cognitive_cycle
from aci.graphs import (
    AuthorityGraph,
    CoherenceGraph,
    EvidenceGraph,
    MemoryGraph,
    ScaleGraph,
)
from aci.state import (
    ArchitectureState,
    BudgetState,
    GovernanceState,
    ThresholdState,
    capture_baseline,
)


def fixed_time(value: str):
    return lambda: value


def make_pending():
    return create_pending_audit(
        cycle_id="cycle-001",
        input_ref="input-001",
        baseline_state_ref="state-001",
        baseline_fingerprint="sha256:baseline",
        id_provider=lambda: "audit-001",
        time_provider=fixed_time("2026-06-28T08:00:00+00:00"),
    )


def make_structure():
    return SymbolicStructure(
        structure_id="structure-001",
        content="A provisional claim.",
        structure_type=StructureType.CLAIM,
        current_state=SymbolicState.CANDIDATE,
        metadata=SymbolicMetadata(
            origin="input-001",
            epistemic_status=EpistemicStatus.UNGROUNDED,
            scale_label=ScaleLabel.CLAIM,
            candidate_status=CandidateStatus.NONE,
            authority_level=AuthorityLevel.NONE,
            audit_refs=["audit-001"],
        ),
    )


def make_decision():
    return ReviewDecision(
        decision_id="decision-001",
        algorithm_name=AlgorithmName.GEA,
        target_id="structure-001",
        decision_type=DecisionType.APPROVE_WITH_MONITORING,
        status=DecisionStatus.PROVISIONAL,
        scores=ScoreBundle(
            grounding_score=0.75,
            coherence_score=0.60,
            confidence_score=0.70,
        ),
        rationale="Typed evidence supports provisional approval.",
        authorized=True,
        audit_id="audit-001",
    )


def make_state_change(change_id="change-001"):
    return StateChange(
        change_id=change_id,
        target_id="structure-001",
        change_type="metadata_update",
        decision_ref="decision-001",
        audit_ref="audit-001",
        payload={"field": "grounding_score"},
    )


def make_graph_update():
    return GraphUpdate(
        update_id="graph-update-001",
        graph_name=GraphName.EVIDENCE_GRAPH,
        update_type=GraphUpdateType.EDGE_ADDED,
        affected_nodes=["structure-001"],
        affected_edges=["evidence-edge-001"],
        decision_ref="decision-001",
        audit_ref="audit-001",
    )


def make_escalation():
    return EscalationEvent(
        escalation_id="escalation-001",
        target_id="structure-001",
        reason="Monitor unresolved source independence.",
        urgency=EscalationUrgency.NORMAL,
        decision_ref="decision-001",
        from_algorithm=AlgorithmName.GEA,
        to_algorithm=AlgorithmName.CRA,
        audit_ref="audit-001",
    )


def make_rollback():
    return RollbackPoint(
        rollback_id="rollback-001",
        state_ref="state-001",
        affected_structures=["structure-001"],
        affected_graphs=[GraphName.EVIDENCE_GRAPH],
        reason_created="Protect baseline before graph application.",
        audit_ref="audit-001",
    )


def make_delta():
    return StateDelta(
        delta_id="delta-001",
        before_state_ref="state-001",
        after_state_ref="state-002",
        audit_ref="audit-001",
        applied_change_ids=["change-001"],
        graph_update_ids=["graph-update-001"],
        escalation_ids=["escalation-001"],
        rollback_ids=["rollback-001"],
    )


def make_commit_data():
    return CommittedAuditData(
        target_structure_ids=["structure-001"],
        created_structures=[make_structure()],
        algorithms_invoked=[AlgorithmName.CRA],
        decisions=[make_decision()],
        accepted_plan_items=[make_state_change()],
        rejected_plan_items=[make_state_change("change-rejected-001")],
        graph_updates=[make_graph_update()],
        budget_effects=[
            {
                "budget": "verification",
                "before": 1.0,
                "after": 0.9,
            }
        ],
        threshold_effects=[
            {
                "threshold": "grounding_threshold",
                "observed": 0.75,
                "passed": True,
            }
        ],
        rollback_points_created=[make_rollback()],
        state_delta=make_delta(),
        provisional_output_ref="output-001",
        unresolved_tensions=["source-independence"],
        escalation_events=[make_escalation()],
    )


def test_pending_reservation_is_a_real_audit_record_with_injected_values():
    audit = make_pending()

    assert audit.audit_id == "audit-001"
    assert audit.status is AuditStatus.PENDING
    assert audit.input_ref == "input-001"
    assert audit.baseline_state_ref == "state-001"
    assert audit.baseline_fingerprint == "sha256:baseline"
    assert audit.started_at == "2026-06-28T08:00:00+00:00"
    assert audit.finalized_at is None


def test_committed_finalization_records_complete_witness_data_once():
    audit = make_pending()
    data = make_commit_data()

    result = finalize_committed_audit(
        audit,
        data,
        time_provider=fixed_time("2026-06-28T08:01:00+00:00"),
    )

    assert result is audit
    assert audit.status is AuditStatus.COMMITTED
    assert audit.finalized_at == "2026-06-28T08:01:00+00:00"
    assert audit.target_structure_ids == ["structure-001"]
    assert audit.algorithms_invoked == [AlgorithmName.CRA, AlgorithmName.GEA]
    assert audit.decision_refs == ["decision-001"]
    assert audit.decisions[0].status is DecisionStatus.PROVISIONAL
    assert audit.decisions[0].scores.grounding_score == 0.75
    assert audit.state_change_refs == ["change-001"]
    assert audit.rejected_plan_items[0].change_id == "change-rejected-001"
    assert audit.graph_update_refs == ["graph-update-001"]
    assert audit.rollback_refs == ["rollback-001"]
    assert audit.escalation_refs == ["escalation-001"]
    assert audit.output_refs == ["output-001"]
    assert audit.state_delta == make_delta()
    assert audit.budget_effects[0]["after"] == 0.9
    assert audit.threshold_effects[0]["passed"] is True
    assert audit.unresolved_tensions == ["source-independence"]
    assert audit.error is None
    diagnostics = json.loads(json.dumps(audit.to_dict(), sort_keys=True))
    assert diagnostics["decisions"][0]["scores"]["grounding_score"] == 0.75


def test_finalized_audit_is_isolated_from_caller_owned_commit_data():
    audit = make_pending()
    data = make_commit_data()

    finalize_committed_audit(audit, data)
    data.decisions[0].rationale = "Caller mutation."
    data.budget_effects[0]["after"] = 0.0
    data.created_structures.clear()

    assert audit.decisions[0].rationale != "Caller mutation."
    assert audit.budget_effects[0]["after"] == 0.9
    assert len(audit.created_structures) == 1


@pytest.mark.parametrize("terminal_action", ["commit", "abort"])
def test_committed_audit_rejects_every_second_terminal_transition(terminal_action):
    audit = make_pending()
    finalize_committed_audit(audit, make_commit_data())

    with pytest.raises(AuditLifecycleError):
        if terminal_action == "commit":
            finalize_committed_audit(audit, CommittedAuditData())
        else:
            finalize_aborted_audit(
                audit,
                AbortedAuditData(
                    failure_stage="application",
                    error="late failure",
                ),
            )


def test_aborted_finalization_witnesses_failure_without_domain_delta():
    audit = make_pending()
    data = AbortedAuditData(
        failure_stage="state_application",
        error="Injected application failure.",
        target_structure_ids=["structure-001"],
        algorithms_invoked=[AlgorithmName.CRA],
        decisions=[make_decision()],
        rejected_plan_items=[make_state_change("change-rejected-001")],
        unresolved_tensions=["application-failure"],
        escalation_events=[make_escalation()],
    )

    finalize_aborted_audit(
        audit,
        data,
        time_provider=fixed_time("2026-06-28T08:02:00+00:00"),
    )

    assert audit.status is AuditStatus.ABORTED
    assert audit.failure_stage == "state_application"
    assert audit.error == "Injected application failure."
    assert audit.decisions == [make_decision()]
    assert audit.rejected_plan_items[0].change_id == "change-rejected-001"
    assert audit.escalation_refs == ["escalation-001"]
    assert audit.created_structures == []
    assert audit.accepted_plan_items == []
    assert audit.graph_updates == []
    assert audit.budget_effects == []
    assert audit.threshold_effects == []
    assert audit.rollback_points_created == []
    assert audit.state_delta is None
    assert audit.state_change_refs == []
    assert audit.graph_update_refs == []
    assert audit.output_refs == []


@pytest.mark.parametrize("terminal_action", ["commit", "abort"])
def test_aborted_audit_rejects_every_second_terminal_transition(terminal_action):
    audit = make_pending()
    finalize_aborted_audit(
        audit,
        AbortedAuditData(failure_stage="review", error="review failed"),
    )

    with pytest.raises(AuditLifecycleError):
        if terminal_action == "commit":
            finalize_committed_audit(audit, CommittedAuditData())
        else:
            finalize_aborted_audit(
                audit,
                AbortedAuditData(
                    failure_stage="review",
                    error="repeat abort",
                ),
            )


def test_invalid_commit_is_atomic_and_leaves_reservation_pending():
    audit = make_pending()
    data = make_commit_data()
    data.graph_updates[0].audit_ref = "audit-forged"

    with pytest.raises(ValueError, match="must reference audit audit-001"):
        finalize_committed_audit(audit, data)

    assert audit.status is AuditStatus.PENDING
    assert audit.finalized_at is None
    assert audit.decisions == []
    assert audit.graph_updates == []
    assert audit.state_delta is None


def test_invalid_terminal_timestamp_leaves_reservation_pending():
    audit = make_pending()

    with pytest.raises(ValueError, match="finalized_at"):
        finalize_committed_audit(
            audit,
            CommittedAuditData(),
            time_provider=lambda: "",
        )

    assert audit.status is AuditStatus.PENDING
    assert audit.finalized_at is None


def test_baseline_reference_and_fingerprint_are_stable_and_state_sensitive():
    state = ArchitectureState(state_id="state-001")
    baseline = capture_baseline(state)
    live_fingerprint = capture_baseline_fingerprint(state)

    state.monitoring_triggers.append("later-change")

    assert capture_baseline_reference(state) == "state-001"
    assert capture_baseline_reference(baseline) == "state-001"
    assert live_fingerprint == capture_baseline_fingerprint(baseline)
    assert live_fingerprint != capture_baseline_fingerprint(state)
    assert live_fingerprint.startswith("sha256:")


def test_reference_binding_returns_copies_and_rejects_aborted_audits():
    pending = make_pending()
    output = OutputObject(
        output_id="output-001",
        output_type=OutputType.QUALIFIED_RESPONSE,
        content="Provisional.",
    )
    change = StateChange(
        change_id="change-001",
        target_id="structure-001",
        change_type="metadata_update",
        decision_ref="decision-001",
        audit_ref="audit-unbound",
    )

    bound_output = bind_audit_reference_to_output(output, pending)
    bound_change = bind_audit_reference_to_state_change(change, pending)

    assert bound_output.audit_ref == "audit-001"
    assert bound_change.audit_ref == "audit-001"
    assert output.audit_ref is None
    assert change.audit_ref == "audit-unbound"

    finalize_aborted_audit(
        pending,
        AbortedAuditData(failure_stage="review", error="review failed"),
    )
    with pytest.raises(AuditLifecycleError):
        bind_audit_reference_to_output(output, pending)
    with pytest.raises(AuditLifecycleError):
        bind_audit_reference_to_state_change(change, pending)


def test_empty_injected_identifier_is_rejected():
    with pytest.raises(ValueError, match="audit_id"):
        create_pending_audit(
            cycle_id="cycle-001",
            input_ref="input-001",
            baseline_state_ref="state-001",
            id_provider=lambda: "",
        )


class Stage21IDs:
    def __init__(self):
        self.counts = defaultdict(int)

    def __call__(self, kind):
        self.counts[kind] += 1
        return f"{kind}-stage21-{self.counts[kind]:03d}"


class Stage21Fault(RuntimeError):
    pass


def make_nested_hardening_state():
    memory = SymbolicStructure(
        structure_id="baseline-memory",
        content="A prior governed memory.",
        structure_type=StructureType.PERSISTENT_KNOWLEDGE,
        current_state=SymbolicState.PERSISTENT,
        metadata=SymbolicMetadata(
            origin="prior-input",
            epistemic_status=EpistemicStatus.STRONGLY_GROUNDED,
            scale_label=ScaleLabel.MEMORY,
            candidate_status=CandidateStatus.NONE,
            authority_level=AuthorityLevel.MEMORY_INFLUENCE,
            grounding_score=1.0,
            coherence_score=1.0,
            persistence_score=1.0,
            uncertainty=0.0,
            audit_refs=["audit-prior"],
        ),
    )
    pending = EscalationEvent(
        escalation_id="escalation-prior",
        target_id=memory.structure_id,
        reason="Prior unresolved review remains pending.",
        urgency=EscalationUrgency.NORMAL,
        decision_ref="decision-prior",
        from_algorithm=AlgorithmName.GEA,
        to_algorithm=AlgorithmName.CRA,
        resolved=False,
        audit_ref="audit-prior",
    )
    return ArchitectureState(
        state_id="state-hardening",
        active_structures={memory.structure_id: memory},
        memory_graph=MemoryGraph(
            nodes={memory.structure_id: memory},
            persistence_relations=[
                {
                    "relation_id": "memory-relation-prior",
                    "target_id": memory.structure_id,
                    "audit_ref": "audit-prior",
                }
            ],
        ),
        evidence_graph=EvidenceGraph(
            source_relations=[
                {
                    "relation_id": "source-relation-prior",
                    "source_ref": "source://prior",
                }
            ]
        ),
        coherence_graph=CoherenceGraph(
            relations=[
                {
                    "relation_id": "coherence-prior",
                    "target_id": memory.structure_id,
                }
            ],
            unresolved_tensions=["tension-prior"],
            coherence_pressure=0.2,
        ),
        scale_graph=ScaleGraph(
            scale_labels={memory.structure_id: ScaleLabel.MEMORY},
            mismatch_records=[
                {
                    "record_id": "scale-record-prior",
                    "target_id": memory.structure_id,
                }
            ],
        ),
        governance_state=GovernanceState(
            governance_mode=GovernanceMode.CAUTION,
            authority_graph=AuthorityGraph(
                domains=["memory", "governance"],
                authority_edges=[
                    {
                        "edge_id": "authority-prior",
                        "source": "governance",
                        "target": "memory",
                    }
                ],
                veto_rules=[
                    {
                        "rule_id": "veto-rule-prior",
                        "scope": memory.structure_id,
                    }
                ],
                escalation_rules=[
                    {
                        "rule_id": "escalation-rule-prior",
                        "target": "review",
                    }
                ],
            ),
            active_vetoes=[
                {
                    "veto_id": "veto-prior",
                    "target_id": memory.structure_id,
                    "reason": "Prior veto remains active.",
                    "audit_ref": "audit-prior",
                }
            ],
            pending_escalations=[pending],
            governance_memory=[
                {
                    "precedent_id": "precedent-prior",
                    "result": "defer",
                }
            ],
        ),
        budgets=BudgetState(
            stability_budget=0.8,
            novelty_budget=0.7,
            verification_budget=0.6,
            attention_budget=0.5,
            recovery_capacity=0.9,
        ),
        thresholds=ThresholdState(
            grounding_threshold=0.65,
            persistence_threshold=0.8,
            legitimacy_threshold=0.9,
        ),
        monitoring_triggers=["monitor-prior"],
    )


def domain_snapshot(state):
    snapshot = state.to_dict()
    snapshot.pop("audit_log")
    return snapshot


def run_stage21_cycle(state, input_value, **kwargs):
    return run_integrated_cognitive_cycle(
        state,
        input_value,
        id_provider=Stage21IDs(),
        time_provider=kwargs.pop(
            "time_provider",
            fixed_time("2026-07-01T12:00:00+00:00"),
        ),
        **kwargs,
    )


def test_cycle_reserves_pending_audit_before_first_faultable_work():
    state = make_nested_hardening_state()

    def fail_at_reservation(point):
        if point == "audit_reserved":
            raise Stage21Fault("reservation observed")

    result = run_stage21_cycle(
        state,
        "A claim that must not reach parsing.",
        fault_injector=fail_at_reservation,
    )

    assert result.audit_record.status is AuditStatus.ABORTED
    assert result.audit_record.started_at is not None
    assert result.audit_record.finalized_at is not None
    assert result.audit_record.failure_stage == "audit_reserved"
    assert result.audit_record.algorithms_invoked == [AlgorithmName.ICC]
    assert result.audit_record.target_structure_ids == []
    assert domain_snapshot(result.updated_state) == domain_snapshot(state)
    assert len(result.updated_state.audit_log) == 1


@pytest.mark.parametrize(
    ("failure_family", "fault_point"),
    [
        ("parsing", "input_parsed"),
        ("metadata", "metadata_initialized"),
        ("review", "review_cga"),
        ("planning", "plan_created"),
        ("application", "plan_applied"),
        ("output", "provisional_output_generated"),
        ("audit_finalization", "commit_candidate_finalized"),
    ],
)
def test_named_cycle_failures_preserve_nested_domain_state(
    failure_family,
    fault_point,
):
    state = make_nested_hardening_state()
    original = deepcopy(state)

    def inject(point):
        if point == fault_point:
            raise Stage21Fault(failure_family)

    result = run_stage21_cycle(
        state,
        "A provisional claim for transaction hardening.",
        fault_injector=inject,
    )

    assert result.audit_record.status is AuditStatus.ABORTED
    assert result.audit_record.failure_stage == fault_point
    assert result.audit_record.state_delta is None
    assert result.audit_record.accepted_plan_items == []
    assert result.audit_record.graph_updates == []
    assert result.output is None
    assert domain_snapshot(result.updated_state) == domain_snapshot(original)
    assert domain_snapshot(state) == domain_snapshot(original)
    assert result.updated_state.audit_log == [result.audit_record]

    recovered = result.updated_state
    assert recovered.memory_graph is not recovered.evidence_graph
    assert recovered.evidence_graph is not recovered.coherence_graph
    assert recovered.coherence_graph is not recovered.scale_graph
    assert (
        recovered.scale_graph
        is not recovered.governance_state.authority_graph
    )
    assert recovered.governance_state.governance_mode is GovernanceMode.CAUTION
    assert recovered.governance_state.active_vetoes == (
        original.governance_state.active_vetoes
    )
    assert recovered.governance_state.pending_escalations == (
        original.governance_state.pending_escalations
    )
    assert not recovered.governance_state.pending_escalations[0].resolved
    assert recovered.budgets == original.budgets
    assert recovered.thresholds == original.thresholds


def test_failure_inside_committed_audit_finalization_aborts_cleanly():
    state = make_nested_hardening_state()

    class FailCommitFinalizationTime:
        def __init__(self):
            self.calls = 0

        def __call__(self):
            self.calls += 1
            if self.calls == 2:
                raise Stage21Fault("commit finalization clock failed")
            return f"2026-07-01T12:00:0{self.calls}+00:00"

    time_provider = FailCommitFinalizationTime()
    result = run_stage21_cycle(
        state,
        "A claim reaching committed-audit finalization.",
        time_provider=time_provider,
    )

    assert time_provider.calls == 3
    assert result.audit_record.status is AuditStatus.ABORTED
    assert result.audit_record.failure_stage == "commit_candidate_finalized"
    assert "commit finalization clock failed" in result.audit_record.error
    assert result.audit_record.state_delta is None
    assert domain_snapshot(result.updated_state) == domain_snapshot(state)


def test_committed_cycle_links_output_changes_decisions_and_audit():
    state = ArchitectureState(state_id="state-commit-hardening")
    result = run_stage21_cycle(
        state,
        "An unsupported claim requiring revision.",
    )

    assert result.audit_record.status is AuditStatus.COMMITTED
    assert result.output is not None
    assert result.output.audit_finalized
    assert result.output.audit_ref == result.audit_record.audit_id
    assert result.output.output_id in result.audit_record.output_refs
    assert result.audit_record.state_delta is not None
    assert result.audit_record.state_delta.audit_ref == (
        result.audit_record.audit_id
    )
    assert result.audit_record.decisions
    for decision in result.audit_record.decisions:
        assert isinstance(decision.status, DecisionStatus)
        assert isinstance(decision.scores, ScoreBundle)
        assert set(decision.scores.to_dict()) >= {
            "grounding_score",
            "coherence_score",
            "persistence_score",
            "legitimacy_score",
            "constitutional_risk_score",
        }
    assert result.updated_state.state_changes
    for change in result.updated_state.state_changes:
        assert change.audit_ref == result.audit_record.audit_id
        assert change.decision_ref in result.audit_record.decision_refs
    for update in result.updated_state.applied_graph_updates:
        assert update.audit_ref == result.audit_record.audit_id
        assert update.decision_ref in result.audit_record.decision_refs


def test_high_risk_full_cycle_creates_scoped_rollback_and_no_output():
    result = run_stage21_cycle(
        ArchitectureState(state_id="state-high-risk"),
        "Propose an architectural redesign.",
    )

    assert result.audit_record.status is AuditStatus.COMMITTED
    assert result.output is not None
    assert result.output.output_type is OutputType.NO_OUTPUT
    assert result.output.content is None
    assert result.audit_record.rollback_points_created
    for rollback in result.audit_record.rollback_points_created:
        assert rollback.audit_ref == result.audit_record.audit_id
        assert rollback.state_ref == "state-high-risk"
        assert rollback.affected_structures == ["structure-stage21-001"]
        assert rollback.valid_until == "cycle-end"
    assert result.updated_state.rollback_points == (
        result.audit_record.rollback_points_created
    )
