import json
from enum import StrEnum

import pytest

from aci.core import (
    AuditRecord,
    CycleResult,
    EscalationEvent,
    GraphUpdate,
    InputObject,
    OutputObject,
    ReviewDecision,
    RollbackPoint,
    ScoreBundle,
    StateChange,
    StateChangePlan,
    StateDelta,
    SymbolicMetadata,
    SymbolicStructure,
)
from aci.enums import (
    ENUM_FAMILIES,
    AlgorithmName,
    AuditStatus,
    AuthorityLevel,
    BudgetType,
    CandidateStatus,
    CycleStatus,
    DecisionStatus,
    DecisionType,
    EpistemicStatus,
    EscalationUrgency,
    EvidenceRelationType,
    GovernanceMode,
    GraphName,
    GraphUpdateType,
    OutputType,
    ScaleLabel,
    StructureType,
    SymbolicState,
    VerificationStatus,
)


EXPECTED_MEMBERS = {
    StructureType: [
        "OBSERVATION",
        "CLAIM",
        "QUESTION",
        "HYPOTHESIS",
        "NOVELTY_CANDIDATE",
        "EVIDENCE_ITEM",
        "MEMORY_CANDIDATE",
        "PERSISTENT_KNOWLEDGE",
        "COHERENCE_TENSION",
        "SCALE_CONFLICT",
        "ARCHITECTURAL_CANDIDATE",
        "GOVERNANCE_OBJECT",
        "CONSTITUTIONAL_OBJECT",
    ],
    SymbolicState: [
        "RECEIVED",
        "PARSED",
        "CANDIDATE",
        "SANDBOXED",
        "HYPOTHESIS",
        "GROUNDED_PARTIAL",
        "GROUNDED_STRONG",
        "COHERENCE_REVIEW",
        "PERSISTENCE_REVIEW",
        "TEMPORARY",
        "ARCHIVED",
        "PERSISTENT",
        "QUALIFIED_PERSISTENT",
        "DEPRECATED",
        "RETRACTED",
        "REJECTED",
        "ARCHITECTURAL_REVIEW",
        "GOVERNANCE_REVIEW",
        "CONSTITUTIONAL_REVIEW",
    ],
    EpistemicStatus: [
        "UNKNOWN",
        "UNGROUNDED",
        "SPECULATIVE",
        "INTERNALLY_COHERENT",
        "PARTIALLY_GROUNDED",
        "STRONGLY_GROUNDED",
        "CONTRADICTED",
        "REJECTED",
    ],
    ScaleLabel: [
        "OBSERVATION",
        "CLAIM",
        "HYPOTHESIS",
        "MEMORY",
        "PRINCIPLE",
        "ARCHITECTURE",
        "CONSTITUTIONAL",
    ],
    CandidateStatus: [
        "NONE",
        "PERSISTENCE_CANDIDATE",
        "PRINCIPLE_CANDIDATE",
        "ARCHITECTURE_CANDIDATE",
        "CONSTITUTIONAL_CANDIDATE",
    ],
    AuthorityLevel: [
        "NONE",
        "TEMPORARY_USE",
        "ACTIVE_REASONING",
        "MEMORY_INFLUENCE",
        "ARCHITECTURAL_INFLUENCE",
        "INVARIANT_CONSTRAINT",
        "CONSTITUTIONAL_AUTHORITY",
    ],
    DecisionType: [
        "APPROVE",
        "APPROVE_WITH_MONITORING",
        "SANDBOX",
        "REVISE",
        "REPAIR",
        "DELAY",
        "DEMOTE",
        "PROMOTE_CANDIDATE",
        "PERSIST",
        "ARCHIVE",
        "RETRACT",
        "REJECT",
        "ROLLBACK",
        "ESCALATE",
        "AMENDMENT_REVIEW",
    ],
    GovernanceMode: [
        "NORMAL",
        "CAUTION",
        "CONSTITUTIONAL_RISK",
        "EMERGENCY",
        "AMENDMENT_REVIEW",
        "LOCKDOWN",
    ],
    OutputType: [
        "DIRECT_RESPONSE",
        "QUALIFIED_RESPONSE",
        "SPECULATIVE_RESPONSE",
        "GROUNDED_RESPONSE",
        "SUMMARY",
        "CLASSIFICATION",
        "ACTION_RECOMMENDATION",
        "GOVERNANCE_NOTICE",
        "ESCALATION_NOTICE",
        "REFUSAL",
        "INTERNAL_REVIEW_RESULT",
        "NO_OUTPUT",
    ],
    AlgorithmName: [
        "IPA",
        "SRA",
        "NGSA",
        "GEA",
        "PCA",
        "CRA",
        "MSSA",
        "AEA",
        "CGA",
        "ICC",
    ],
    AuditStatus: ["PENDING", "COMMITTED", "ABORTED"],
    CycleStatus: ["COMMITTED", "ABORTED"],
    EvidenceRelationType: [
        "SUPPORTS",
        "WEAKENS",
        "CONTRADICTS",
        "QUALIFIES",
        "DEPENDS_ON",
        "REQUIRES_MORE_EVIDENCE",
    ],
    VerificationStatus: ["UNVERIFIED", "VERIFIED", "FAILED"],
    DecisionStatus: [
        "FINAL",
        "PROVISIONAL",
        "BLOCKED",
        "ESCALATED",
        "PENDING_REVIEW",
        "MONITORING",
    ],
    EscalationUrgency: ["LOW", "NORMAL", "HIGH", "CRITICAL"],
    GraphName: [
        "MEMORY_GRAPH",
        "EVIDENCE_GRAPH",
        "COHERENCE_GRAPH",
        "SCALE_GRAPH",
        "AUTHORITY_GRAPH",
    ],
    GraphUpdateType: [
        "NODE_ADDED",
        "NODE_REMOVED",
        "EDGE_ADDED",
        "EDGE_REMOVED",
        "RELATION_UPDATED",
        "GRAPH_REPAIRED",
        "GRAPH_ROLLBACK",
        "GRAPH_REBUILT",
    ],
    BudgetType: ["STABILITY", "NOVELTY", "VERIFICATION", "ATTENTION", "RECOVERY"],
}

EXPECTED_PREFIXES = {
    StructureType: "structure",
    SymbolicState: "symbolic_state",
    EpistemicStatus: "epistemic",
    ScaleLabel: "scale",
    CandidateStatus: "candidate",
    AuthorityLevel: "authority",
    DecisionType: "decision",
    GovernanceMode: "governance",
    OutputType: "output",
    AlgorithmName: "algorithm",
    AuditStatus: "audit",
    CycleStatus: "cycle",
    EvidenceRelationType: "evidence_relation",
    VerificationStatus: "verification",
    DecisionStatus: "decision_status",
    EscalationUrgency: "escalation_urgency",
    GraphName: "graph",
    GraphUpdateType: "graph_update",
    BudgetType: "budget",
}


@pytest.mark.parametrize("enum_type", ENUM_FAMILIES)
def test_enum_members_are_explicit_and_stable(enum_type):
    assert [member.name for member in enum_type] == EXPECTED_MEMBERS[enum_type]


@pytest.mark.parametrize("enum_type", ENUM_FAMILIES)
def test_enum_values_are_expected_unique_strings(enum_type):
    values = [member.value for member in enum_type]
    expected_values = [
        f"{EXPECTED_PREFIXES[enum_type]}.{name.lower()}"
        for name in EXPECTED_MEMBERS[enum_type]
    ]

    assert issubclass(enum_type, StrEnum)
    assert all(isinstance(value, str) for value in values)
    assert values == expected_values
    assert len(values) == len(set(values))


@pytest.mark.parametrize("enum_type", ENUM_FAMILIES)
def test_enum_values_round_trip_and_serialize_readably(enum_type):
    for member in enum_type:
        assert enum_type(member.value) is member
        assert str(member) == member.value
        assert json.loads(json.dumps(member)) == member.value


def test_serialized_values_are_disjoint_across_enum_families():
    all_values = [member.value for enum_type in ENUM_FAMILIES for member in enum_type]

    assert len(all_values) == len(set(all_values))


def test_cross_category_members_cannot_be_silently_substituted():
    assert StructureType.CLAIM != ScaleLabel.CLAIM
    assert StructureType.HYPOTHESIS != EpistemicStatus.SPECULATIVE
    assert CandidateStatus.ARCHITECTURE_CANDIDATE != ScaleLabel.ARCHITECTURE
    assert AuthorityLevel.CONSTITUTIONAL_AUTHORITY != ScaleLabel.CONSTITUTIONAL
    assert DecisionType.ESCALATE != DecisionStatus.ESCALATED
    assert AuditStatus.COMMITTED != CycleStatus.COMMITTED

    with pytest.raises(ValueError):
        ScaleLabel(StructureType.CLAIM)
    with pytest.raises(ValueError):
        AuthorityLevel(CandidateStatus.CONSTITUTIONAL_CANDIDATE)
    with pytest.raises(ValueError):
        CycleStatus(AuditStatus.COMMITTED)


def test_authority_does_not_encode_review_requirement():
    assert "REVIEW_REQUIRED" not in AuthorityLevel.__members__


def test_transaction_lifecycle_statuses_are_exact():
    assert set(AuditStatus) == {
        AuditStatus.PENDING,
        AuditStatus.COMMITTED,
        AuditStatus.ABORTED,
    }
    assert set(CycleStatus) == {CycleStatus.COMMITTED, CycleStatus.ABORTED}


def make_metadata(**overrides):
    values = {
        "origin": "unit-test",
        "epistemic_status": EpistemicStatus.SPECULATIVE,
        "scale_label": ScaleLabel.CLAIM,
        "candidate_status": CandidateStatus.NONE,
        "authority_level": AuthorityLevel.TEMPORARY_USE,
        "grounding_score": 0.1,
        "coherence_score": 0.2,
        "persistence_score": 0.0,
        "uncertainty": 0.8,
    }
    values.update(overrides)
    return SymbolicMetadata(**values)


def make_structure(**overrides):
    values = {
        "structure_id": "S-001",
        "content": "A bounded claim.",
        "structure_type": StructureType.CLAIM,
        "current_state": SymbolicState.CANDIDATE,
        "metadata": make_metadata(),
    }
    values.update(overrides)
    return SymbolicStructure(**values)


def make_scores(**overrides):
    values = {
        "grounding_score": 0.25,
        "coherence_score": 0.5,
        "persistence_score": 0.1,
        "confidence_score": 0.6,
        "risk_score": 0.2,
    }
    values.update(overrides)
    return ScoreBundle(**values)


def make_decision(**overrides):
    values = {
        "decision_id": "D-001",
        "algorithm_name": AlgorithmName.GEA,
        "target_id": "S-001",
        "decision_type": DecisionType.APPROVE_WITH_MONITORING,
        "status": DecisionStatus.PROVISIONAL,
        "scores": make_scores(),
        "rationale": "Enough structure for provisional review.",
        "authorized": True,
        "audit_id": "A-001",
    }
    values.update(overrides)
    return ReviewDecision(**values)


def make_committed_audit(**overrides):
    values = {
        "audit_id": "A-001",
        "status": AuditStatus.COMMITTED,
        "cycle_id": "C-001",
        "baseline_state_ref": "state-before",
        "started_at": "2026-06-26T08:00:00",
        "finalized_at": "2026-06-26T08:01:00",
        "decision_refs": ["D-001"],
    }
    values.update(overrides)
    return AuditRecord(**values)


def make_aborted_audit(**overrides):
    values = {
        "audit_id": "A-002",
        "status": AuditStatus.ABORTED,
        "cycle_id": "C-002",
        "baseline_state_ref": "state-before",
        "started_at": "2026-06-26T08:00:00",
        "finalized_at": "2026-06-26T08:01:00",
        "failure_stage": "planned_application",
        "error": "planned failure",
    }
    values.update(overrides)
    return AuditRecord(**values)


def test_core_objects_instantiate_compare_and_serialize_for_diagnostics():
    structure = make_structure()
    decision = make_decision()
    graph_update = GraphUpdate(
        update_id="GU-001",
        graph_name=GraphName.MEMORY_GRAPH,
        update_type=GraphUpdateType.NODE_ADDED,
        affected_nodes=["S-001"],
        affected_edges=[],
        decision_ref=decision.decision_id,
        audit_ref="A-001",
    )
    state_change = StateChange(
        change_id="SC-001",
        target_id=structure.structure_id,
        change_type="metadata.update",
        decision_ref=decision.decision_id,
        audit_ref="A-001",
        payload={"field": "current_state"},
    )
    escalation = EscalationEvent(
        escalation_id="E-001",
        target_id=structure.structure_id,
        reason="Needs constitutional review if promoted.",
        urgency=EscalationUrgency.NORMAL,
        decision_ref=decision.decision_id,
        from_algorithm=AlgorithmName.GEA,
        to_domain="governance",
        audit_ref="A-001",
    )
    rollback = RollbackPoint(
        rollback_id="RB-001",
        state_ref="state-before",
        affected_structures=[structure.structure_id],
        affected_graphs=[GraphName.MEMORY_GRAPH],
        reason_created="High-risk graph update.",
        audit_ref="A-001",
    )
    plan = StateChangePlan(
        plan_id="P-001",
        decision_refs=[decision.decision_id],
        changes=[state_change],
        graph_updates=[graph_update],
        rollback_points=[rollback],
        escalation_events=[escalation],
        audit_ref="A-001",
    )
    delta = StateDelta(
        delta_id="SD-001",
        before_state_ref="state-before",
        after_state_ref="state-after",
        audit_ref="A-001",
        applied_change_ids=[state_change.change_id],
        graph_update_ids=[graph_update.update_id],
        escalation_ids=[escalation.escalation_id],
        rollback_ids=[rollback.rollback_id],
    )
    output = OutputObject(
        output_id="O-001",
        output_type=OutputType.QUALIFIED_RESPONSE,
        content="Provisional output.",
        supporting_structure_ids=[structure.structure_id],
        epistemic_status=EpistemicStatus.SPECULATIVE,
        decision_status=DecisionStatus.PROVISIONAL,
        unresolved_tensions=["Needs external evidence."],
        audit_ref="A-001",
        audit_finalized=True,
    )
    result = CycleResult.committed(
        cycle_id="C-001",
        updated_state={"state_ref": "state-after", "delta_id": delta.delta_id},
        audit_record=make_committed_audit(
            state_change_refs=[state_change.change_id],
            graph_update_refs=[graph_update.update_id],
            escalation_refs=[escalation.escalation_id],
            rollback_refs=[rollback.rollback_id],
            output_refs=[output.output_id],
        ),
        output=output,
        unresolved_items=["external-evidence"],
        escalation_events=[escalation],
        monitoring_triggers=["monitor-persistence"],
    )

    assert make_structure() == structure
    diagnostics = result.to_dict()
    assert diagnostics["status"] == "cycle.committed"
    assert diagnostics["audit_record"]["status"] == "audit.committed"
    assert diagnostics["output"]["output_type"] == "output.qualified_response"
    assert diagnostics["escalation_events"][0]["from_algorithm"] == "algorithm.gea"
    assert json.loads(json.dumps(diagnostics, sort_keys=True)) == diagnostics
    assert plan.to_dict()["graph_updates"][0]["decision_ref"] == decision.decision_id


def test_input_object_serializes_and_keeps_context_refs_separate():
    first = InputObject(input_id="I-001", content="hello")
    second = InputObject(input_id="I-002", content="world")

    first.context_refs.append("CTX-001")

    assert first.to_dict() == {
        "input_id": "I-001",
        "content": "hello",
        "source": "user",
        "context_refs": ["CTX-001"],
        "audit_ref": None,
    }
    assert second.context_refs == []


def test_mutable_defaults_are_not_shared_between_core_objects():
    first_metadata = make_metadata()
    second_metadata = make_metadata()
    first_metadata.audit_refs.append("A-001")

    first_audit = AuditRecord(audit_id="A-010", status=AuditStatus.PENDING)
    second_audit = AuditRecord(audit_id="A-011", status=AuditStatus.PENDING)
    first_audit.decision_refs.append("D-010")

    first_plan = StateChangePlan(plan_id="P-010", decision_refs=["D-010"])
    second_plan = StateChangePlan(plan_id="P-011", decision_refs=["D-011"])
    first_plan.changes.append(
        StateChange(
            change_id="SC-010",
            target_id="S-010",
            change_type="state.noop",
            decision_ref="D-010",
            audit_ref="A-010",
        )
    )

    first_output = OutputObject(output_id="O-010", output_type=OutputType.NO_OUTPUT)
    second_output = OutputObject(output_id="O-011", output_type=OutputType.NO_OUTPUT)
    first_output.unresolved_tensions.append("not-shared")

    assert second_metadata.audit_refs == []
    assert second_audit.decision_refs == []
    assert second_plan.changes == []
    assert second_output.unresolved_tensions == []


@pytest.mark.parametrize(
    "factory,kwargs",
    [
        (lambda **kw: make_metadata(**kw), {"scale_label": CandidateStatus.NONE}),
        (lambda **kw: make_metadata(**kw), {"candidate_status": ScaleLabel.CLAIM}),
        (lambda **kw: make_metadata(**kw), {"authority_level": ScaleLabel.CONSTITUTIONAL}),
        (lambda **kw: make_structure(**kw), {"structure_type": ScaleLabel.CLAIM}),
        (lambda **kw: make_structure(**kw), {"current_state": DecisionStatus.FINAL}),
        (lambda **kw: make_decision(**kw), {"algorithm_name": DecisionType.APPROVE}),
        (lambda **kw: make_decision(**kw), {"status": AuditStatus.COMMITTED}),
    ],
)
def test_core_model_construction_rejects_wrong_enum_families(factory, kwargs):
    with pytest.raises(TypeError):
        factory(**kwargs)


@pytest.mark.parametrize(
    "factory",
    [
        lambda: InputObject(input_id="", content="x"),
        lambda: make_structure(structure_id=" "),
        lambda: make_decision(decision_id=""),
        lambda: StateChange(
            change_id="SC-001",
            target_id="S-001",
            change_type="state.update",
            decision_ref="D-001",
            audit_ref="",
        ),
        lambda: GraphUpdate(
            update_id="GU-001",
            graph_name=GraphName.MEMORY_GRAPH,
            update_type=GraphUpdateType.NODE_ADDED,
            affected_nodes=[],
            affected_edges=[],
            decision_ref="D-001",
            audit_ref="A-001",
        ),
    ],
)
def test_core_models_reject_empty_identifiers_and_unscoped_updates(factory):
    with pytest.raises(ValueError):
        factory()


@pytest.mark.parametrize(
    "factory",
    [
        lambda: ScoreBundle(grounding_score=-0.01),
        lambda: ScoreBundle(confidence_score=1.01),
        lambda: make_metadata(uncertainty=2.0),
        lambda: OutputObject(
            output_id="O-001",
            output_type=OutputType.SUMMARY,
            grounding_score=1.5,
        ),
    ],
)
def test_score_fields_must_remain_bounded(factory):
    with pytest.raises(ValueError):
        factory()


def test_review_decision_preserves_judgment_without_mutation():
    decision = make_decision(authorized=False, status=DecisionStatus.BLOCKED)

    assert decision.authorized is False
    assert decision.to_dict()["scores"]["coherence_score"] == 0.5
    assert "changes" not in decision.to_dict()

    with pytest.raises(ValueError):
        make_decision(decision_type=DecisionType.ESCALATE, status=DecisionStatus.ESCALATED)


def test_audit_record_enforces_pending_committed_and_aborted_lifecycle():
    pending = AuditRecord(audit_id="A-PENDING", status=AuditStatus.PENDING)
    committed = make_committed_audit()
    aborted = make_aborted_audit()

    assert pending.finalized_at is None
    assert committed.status is AuditStatus.COMMITTED
    assert aborted.error == "planned failure"

    with pytest.raises(ValueError):
        AuditRecord(
            audit_id="A-BAD-PENDING",
            status=AuditStatus.PENDING,
            finalized_at="2026-06-26T08:01:00",
        )
    with pytest.raises(ValueError):
        AuditRecord(audit_id="A-BAD-COMMIT", status=AuditStatus.COMMITTED)
    with pytest.raises(ValueError):
        AuditRecord(
            audit_id="A-BAD-ABORT",
            status=AuditStatus.ABORTED,
            finalized_at="2026-06-26T08:01:00",
        )


def test_escalation_event_requires_one_source_and_one_target():
    event = EscalationEvent(
        escalation_id="E-010",
        target_id="S-010",
        reason="Route to governance.",
        urgency=EscalationUrgency.HIGH,
        decision_ref="D-010",
        from_domain="review",
        to_algorithm=AlgorithmName.CGA,
    )

    assert event.to_dict()["to_algorithm"] == "algorithm.cga"

    with pytest.raises(ValueError):
        EscalationEvent(
            escalation_id="E-011",
            target_id="S-011",
            reason="ambiguous source",
            urgency=EscalationUrgency.HIGH,
            decision_ref="D-011",
            from_algorithm=AlgorithmName.GEA,
            from_domain="review",
            to_algorithm=AlgorithmName.CGA,
        )


def test_rollback_point_and_graph_update_preserve_authorizing_refs():
    rollback = RollbackPoint(
        rollback_id="RB-010",
        state_ref="state-before",
        affected_structures=[],
        affected_graphs=[GraphName.AUTHORITY_GRAPH],
        reason_created="Protected authority change.",
        audit_ref="A-010",
        valid_until="cycle-end",
    )
    graph_update = GraphUpdate(
        update_id="GU-010",
        graph_name=GraphName.AUTHORITY_GRAPH,
        update_type=GraphUpdateType.EDGE_ADDED,
        affected_nodes=[],
        affected_edges=["edge.authority.S-010"],
        decision_ref="D-010",
        audit_ref="A-010",
    )

    assert rollback.to_dict()["affected_graphs"] == ["graph.authority_graph"]
    assert graph_update.decision_ref == "D-010"

    with pytest.raises(ValueError):
        RollbackPoint(
            rollback_id="RB-011",
            state_ref="state-before",
            affected_structures=[],
            affected_graphs=[],
            reason_created="unscoped",
            audit_ref="A-011",
        )


def test_cycle_result_committed_and_aborted_constructors_enforce_lifecycle():
    output = OutputObject(
        output_id="O-020",
        output_type=OutputType.NO_OUTPUT,
        audit_ref="A-020",
        audit_finalized=True,
    )
    committed = CycleResult.committed(
        cycle_id="C-020",
        updated_state={"state_ref": "state-after"},
        audit_record=make_committed_audit(
            audit_id="A-020",
            output_refs=[output.output_id],
        ),
        output=output,
    )
    aborted = CycleResult.aborted(
        cycle_id="C-021",
        audit_record=make_aborted_audit(audit_id="A-021"),
        error="failed before commit",
    )

    assert committed.status is CycleStatus.COMMITTED
    assert aborted.status is CycleStatus.ABORTED
    assert aborted.to_dict()["error"] == "failed before commit"

    with pytest.raises(ValueError):
        CycleResult.committed(
            cycle_id="C-BAD",
            updated_state=None,
            audit_record=make_committed_audit(audit_id="A-BAD"),
        )
    with pytest.raises(ValueError):
        CycleResult.aborted(
            cycle_id="C-BAD-2",
            audit_record=make_committed_audit(audit_id="A-BAD-2"),
            error="wrong audit status",
        )
    with pytest.raises(ValueError, match="cannot contain output"):
        CycleResult.aborted(
            cycle_id="C-BAD-3",
            audit_record=make_aborted_audit(audit_id="A-BAD-3"),
            error="failed before commit",
            output=OutputObject(
                output_id="O-BAD-3",
                output_type=OutputType.NO_OUTPUT,
            ),
        )
