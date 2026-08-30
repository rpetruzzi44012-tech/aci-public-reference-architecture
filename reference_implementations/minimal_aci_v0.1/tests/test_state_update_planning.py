import pytest

from aci.core import (
    GraphUpdate,
    ReviewDecision,
    ScoreBundle,
    StateChangePlan,
    SymbolicMetadata,
    SymbolicStructure,
)
from aci.enums import (
    AlgorithmName,
    AuthorityLevel,
    CandidateStatus,
    DecisionStatus,
    DecisionType,
    EpistemicStatus,
    GovernanceMode,
    GraphName,
    GraphUpdateType,
    ScaleLabel,
    StructureType,
    SymbolicState,
)
from aci.registry import RegistryChangeRequest, create_default_registry
from aci.review_context import ReviewContext
from aci.state import ArchitectureState, GovernanceState, clone_state
from aci.state_update import (
    CONFLICT_RULES,
    plan_authorized_state_changes,
)


class DeterministicIDs:
    def __init__(self):
        self.current = 0

    def __call__(self):
        self.current += 1
        return f"planning-id-{self.current:03d}"


def make_target(
    *,
    structure_id="structure-001",
    structure_type=StructureType.CLAIM,
    scale_label=ScaleLabel.CLAIM,
    authority_level=AuthorityLevel.NONE,
    candidate_status=CandidateStatus.NONE,
):
    return SymbolicStructure(
        structure_id=structure_id,
        content="A structure awaiting conflict-checked planning.",
        structure_type=structure_type,
        current_state=SymbolicState.CANDIDATE,
        metadata=SymbolicMetadata(
            origin="input-001",
            epistemic_status=EpistemicStatus.UNKNOWN,
            scale_label=scale_label,
            candidate_status=candidate_status,
            authority_level=authority_level,
            audit_refs=["audit-001"],
        ),
    )


def make_state(*targets, governance_mode=GovernanceMode.NORMAL):
    values = list(targets) or [make_target()]
    return ArchitectureState(
        state_id="state-001",
        active_structures={
            target.structure_id: target
            for target in values
        },
        governance_state=GovernanceState(
            governance_mode=governance_mode,
        ),
    )


def make_context(*targets, state=None):
    values = list(targets) or [make_target()]
    return ReviewContext(
        audit_id="audit-001",
        architecture_state=state or make_state(*values),
        targets=values,
    )


def make_decision(
    *,
    decision_id="decision-001",
    algorithm_name=AlgorithmName.GEA,
    target_id="structure-001",
    decision_type=DecisionType.APPROVE_WITH_MONITORING,
    status=DecisionStatus.PROVISIONAL,
    escalation_target=None,
    authorized=False,
    recommended_governance_mode=None,
):
    return ReviewDecision(
        decision_id=decision_id,
        algorithm_name=algorithm_name,
        target_id=target_id,
        decision_type=decision_type,
        status=status,
        scores=ScoreBundle(),
        rationale="A typed planning fixture.",
        authorized=authorized,
        escalation_target=escalation_target,
        audit_id="audit-001",
        recommended_governance_mode=recommended_governance_mode,
    )


def append(context, *decisions):
    context.append_decisions(decisions)
    return context


def decision_ids(decisions):
    return [decision.decision_id for decision in decisions]


def test_registered_decision_enters_plan_as_state_change():
    context = append(
        make_context(),
        make_decision(authorized=True),
    )

    plan = plan_authorized_state_changes(
        context,
        create_default_registry(),
        id_provider=DeterministicIDs(),
    )

    assert plan.authorized is True
    assert plan.decision_refs == ["decision-001"]
    assert len(plan.changes) == 1
    assert plan.changes[0].change_type == "monitoring_trigger_add"
    assert plan.changes[0].decision_ref == "decision-001"
    assert plan.changes[0].audit_ref == "audit-001"
    assert plan.rejected_decisions == []
    assert plan.no_op_items == []
    assert plan.validation_results[0].accepted is True


def test_forged_algorithm_is_rejected_and_preserved_for_audit():
    context = append(make_context(), make_decision())
    context._decisions[0].algorithm_name = "FORGED"

    plan = plan_authorized_state_changes(
        context,
        create_default_registry(),
        id_provider=DeterministicIDs(),
    )

    assert plan.authorized is False
    assert plan.decision_refs == []
    assert decision_ids(plan.rejected_decisions) == ["decision-001"]
    assert plan.validation_results[0].accepted is False
    assert "unregistered_algorithm" in (
        plan.validation_results[0].reason_codes
    )


def test_target_authority_above_algorithm_is_rejected():
    target = make_target(
        authority_level=AuthorityLevel.CONSTITUTIONAL_AUTHORITY,
    )
    context = append(
        make_context(target),
        make_decision(authorized=True),
    )

    plan = plan_authorized_state_changes(
        context,
        create_default_registry(),
        id_provider=DeterministicIDs(),
    )

    assert plan.authorized is False
    assert plan.validation_results[0].reason_codes == (
        "target_authority_exceeds_algorithm",
    )
    assert decision_ids(plan.rejected_decisions) == ["decision-001"]


def test_excessive_decision_type_is_rejected_despite_authorized_claim():
    context = append(
        make_context(),
        make_decision(
            decision_type=DecisionType.PERSIST,
            authorized=True,
        ),
    )

    plan = plan_authorized_state_changes(
        context,
        create_default_registry(),
        id_provider=DeterministicIDs(),
    )

    assert plan.authorized is False
    assert "decision_type_not_permitted" in (
        plan.validation_results[0].reason_codes
    )
    assert decision_ids(plan.rejected_decisions) == ["decision-001"]


def test_blocking_decision_cannot_be_overridden_by_approval():
    approval = make_decision(
        decision_id="decision-gea-approve",
        algorithm_name=AlgorithmName.GEA,
        decision_type=DecisionType.APPROVE_WITH_MONITORING,
        status=DecisionStatus.MONITORING,
    )
    rejection = make_decision(
        decision_id="decision-cra-reject",
        algorithm_name=AlgorithmName.CRA,
        decision_type=DecisionType.REJECT,
        status=DecisionStatus.FINAL,
    )
    context = append(make_context(), approval, rejection)

    plan = plan_authorized_state_changes(
        context,
        create_default_registry(),
        id_provider=DeterministicIDs(),
    )

    assert plan.decision_refs == ["decision-cra-reject"]
    assert plan.changes[0].payload["new_state"] == (
        SymbolicState.REJECTED.value
    )
    assert decision_ids(plan.rejected_decisions) == [
        "decision-gea-approve"
    ]
    assert any("blocking constraints" in rule for rule in CONFLICT_RULES)


def test_equal_authority_incompatible_constraints_create_no_mutation():
    reject = make_decision(
        decision_id="decision-gea-reject",
        algorithm_name=AlgorithmName.GEA,
        decision_type=DecisionType.REJECT,
        status=DecisionStatus.FINAL,
    )
    demote = make_decision(
        decision_id="decision-cra-demote",
        algorithm_name=AlgorithmName.CRA,
        decision_type=DecisionType.DEMOTE,
        status=DecisionStatus.PROVISIONAL,
    )
    context = append(make_context(), reject, demote)

    plan = plan_authorized_state_changes(
        context,
        create_default_registry(),
        id_provider=DeterministicIDs(),
    )

    assert plan.authorized is False
    assert plan.changes == []
    assert plan.graph_updates == []
    assert decision_ids(plan.no_op_items) == [
        "decision-gea-reject",
        "decision-cra-demote",
    ]
    assert any("remain ambiguous" in reason for reason in plan.rationale)


def test_typed_escalation_is_pending_auditable_and_not_approval():
    escalation = make_decision(
        algorithm_name=AlgorithmName.GEA,
        decision_type=DecisionType.ESCALATE,
        status=DecisionStatus.ESCALATED,
        escalation_target=AlgorithmName.CRA.value,
    )
    context = append(make_context(), escalation)

    plan = plan_authorized_state_changes(
        context,
        create_default_registry(),
        id_provider=DeterministicIDs(),
    )

    assert plan.decision_refs == ["decision-001"]
    assert plan.changes == []
    assert len(plan.escalation_events) == 1
    event = plan.escalation_events[0]
    assert event.from_algorithm is AlgorithmName.GEA
    assert event.to_algorithm is AlgorithmName.CRA
    assert event.target_id == "structure-001"
    assert event.resolved is False
    assert event.decision_ref == "decision-001"
    assert event.audit_ref == "audit-001"
    assert event.reason == escalation.rationale
    assert any("no approval" in reason for reason in plan.rationale)


def test_escalation_loop_is_rejected_without_erasing_first_route():
    first = make_decision(
        decision_id="decision-gea-cra",
        algorithm_name=AlgorithmName.GEA,
        decision_type=DecisionType.ESCALATE,
        status=DecisionStatus.ESCALATED,
        escalation_target=AlgorithmName.CRA.value,
    )
    loop = make_decision(
        decision_id="decision-cra-gea",
        algorithm_name=AlgorithmName.CRA,
        decision_type=DecisionType.ESCALATE,
        status=DecisionStatus.ESCALATED,
        escalation_target=AlgorithmName.GEA.value,
    )
    context = append(make_context(), first, loop)

    plan = plan_authorized_state_changes(
        context,
        create_default_registry(),
        id_provider=DeterministicIDs(),
    )

    assert plan.decision_refs == ["decision-gea-cra"]
    assert plan.escalation_events[0].to_algorithm is AlgorithmName.CRA
    assert decision_ids(plan.rejected_decisions) == [
        "decision-cra-gea"
    ]
    assert all(result.accepted for result in plan.validation_results)
    assert any("loop detected" in reason for reason in plan.rationale)


def test_registry_inconsistent_escalation_target_is_rejected():
    context = append(
        make_context(),
        make_decision(
            decision_type=DecisionType.ESCALATE,
            status=DecisionStatus.ESCALATED,
            escalation_target=AlgorithmName.AEA.value,
        ),
    )

    plan = plan_authorized_state_changes(
        context,
        create_default_registry(),
        id_provider=DeterministicIDs(),
    )

    assert plan.escalation_events == []
    assert plan.validation_results[0].reason_codes == (
        "escalation_target_not_permitted",
    )
    assert decision_ids(plan.rejected_decisions) == ["decision-001"]


def make_persistence_context():
    target = make_target(
        structure_type=StructureType.MEMORY_CANDIDATE,
        candidate_status=CandidateStatus.PERSISTENCE_CANDIDATE,
    )
    decision = make_decision(
        algorithm_name=AlgorithmName.PCA,
        decision_type=DecisionType.PERSIST,
        status=DecisionStatus.PROVISIONAL,
    )
    return target, append(make_context(target), decision)


def test_planned_graph_update_references_authorizing_decision():
    target, context = make_persistence_context()

    plan = plan_authorized_state_changes(
        context,
        create_default_registry(),
        id_provider=DeterministicIDs(),
    )

    assert plan.decision_refs == ["decision-001"]
    assert len(plan.graph_updates) == 1
    update = plan.graph_updates[0]
    assert update.graph_name is GraphName.MEMORY_GRAPH
    assert update.update_type is GraphUpdateType.NODE_ADDED
    assert update.affected_nodes == [target.structure_id]
    assert update.decision_ref == "decision-001"
    assert update.audit_ref == "audit-001"


def test_high_risk_persistence_plan_requests_scoped_rollback():
    target, context = make_persistence_context()

    plan = plan_authorized_state_changes(
        context,
        create_default_registry(),
        id_provider=DeterministicIDs(),
    )

    assert len(plan.rollback_points) == 1
    rollback = plan.rollback_points[0]
    assert rollback.state_ref == "state-001"
    assert rollback.affected_structures == [target.structure_id]
    assert rollback.affected_graphs == [GraphName.MEMORY_GRAPH]
    assert rollback.audit_ref == "audit-001"
    assert rollback.valid_until == "cycle-end"


def test_state_change_plan_rejects_unlinked_graph_update():
    update = GraphUpdate(
        update_id="graph-update-001",
        graph_name=GraphName.MEMORY_GRAPH,
        update_type=GraphUpdateType.NODE_ADDED,
        affected_nodes=["structure-001"],
        affected_edges=[],
        decision_ref="decision-unlinked",
        audit_ref="audit-001",
    )

    with pytest.raises(
        ValueError,
        match="must reference an accepted decision",
    ):
        StateChangePlan(
            plan_id="plan-001",
            decision_refs=["decision-accepted"],
            graph_updates=[update],
            audit_ref="audit-001",
        )


def test_self_authorizing_registry_change_is_rejected_and_preserved():
    target = make_target(
        structure_type=StructureType.GOVERNANCE_OBJECT,
        scale_label=ScaleLabel.ARCHITECTURE,
    )
    decision = make_decision(
        algorithm_name=AlgorithmName.CGA,
        decision_type=DecisionType.APPROVE,
        status=DecisionStatus.FINAL,
        authorized=True,
    )
    request = RegistryChangeRequest(
        request_id="registry-change-001",
        proposer_algorithm=AlgorithmName.CGA,
        target_algorithm=AlgorithmName.CGA,
        change_kind="authority",
        reason="Let CGA expand its own authority.",
        audit_ref="audit-001",
    )
    context = append(make_context(target), decision)

    plan = plan_authorized_state_changes(
        context,
        create_default_registry(),
        registry_change_requests={"decision-001": request},
        id_provider=DeterministicIDs(),
    )

    codes = plan.validation_results[0].reason_codes
    assert "self_modification_prohibited" in codes
    assert "protected_algorithm_change_prohibited" in codes
    assert "direct_registry_change_prohibited" in codes
    assert decision_ids(plan.rejected_decisions) == ["decision-001"]
    assert plan.authorized is False


def test_protected_stub_recommendation_is_no_op_not_mutation():
    target = make_target(
        structure_type=StructureType.NOVELTY_CANDIDATE,
        scale_label=ScaleLabel.HYPOTHESIS,
    )
    decision = make_decision(
        algorithm_name=AlgorithmName.NGSA,
        decision_type=DecisionType.SANDBOX,
        status=DecisionStatus.PROVISIONAL,
        authorized=False,
    )
    context = append(make_context(target), decision)

    plan = plan_authorized_state_changes(
        context,
        create_default_registry(),
        id_provider=DeterministicIDs(),
    )

    assert plan.authorized is False
    assert plan.changes == []
    assert decision_ids(plan.no_op_items) == ["decision-001"]
    assert any("protected stub" in reason for reason in plan.rationale)


def test_approval_without_explicit_action_is_preserved_as_no_op():
    context = append(
        make_context(),
        make_decision(
            decision_type=DecisionType.APPROVE,
            status=DecisionStatus.FINAL,
        ),
    )

    plan = plan_authorized_state_changes(
        context,
        create_default_registry(),
        id_provider=DeterministicIDs(),
    )

    assert plan.authorized is False
    assert decision_ids(plan.no_op_items) == ["decision-001"]
    assert plan.rejected_decisions == []


def test_active_governance_mode_can_reject_otherwise_valid_change():
    target = make_target()
    state = make_state(
        target,
        governance_mode=GovernanceMode.CONSTITUTIONAL_RISK,
    )
    context = append(make_context(target, state=state), make_decision())

    plan = plan_authorized_state_changes(
        context,
        create_default_registry(),
        id_provider=DeterministicIDs(),
    )

    assert plan.authorized is False
    assert decision_ids(plan.rejected_decisions) == ["decision-001"]
    assert plan.validation_results[0].accepted is True
    assert any(
        GovernanceMode.CONSTITUTIONAL_RISK.value in reason
        for reason in plan.rationale
    )


def test_every_decision_retains_validation_result_and_disposition():
    valid = make_decision(
        decision_id="decision-valid",
        decision_type=DecisionType.APPROVE,
        status=DecisionStatus.FINAL,
    )
    invalid = make_decision(
        decision_id="decision-invalid",
        decision_type=DecisionType.PERSIST,
        status=DecisionStatus.PROVISIONAL,
        authorized=True,
    )
    context = append(make_context(), valid, invalid)

    plan = plan_authorized_state_changes(
        context,
        create_default_registry(),
        id_provider=DeterministicIDs(),
    )

    assert [
        result.decision_id for result in plan.validation_results
    ] == ["decision-valid", "decision-invalid"]
    assert decision_ids(plan.no_op_items) == ["decision-valid"]
    assert decision_ids(plan.rejected_decisions) == ["decision-invalid"]


def test_planning_preserves_authoritative_state_targets_and_graphs():
    target, context = make_persistence_context()
    authoritative = make_state(target)
    context = ReviewContext(
        audit_id="audit-001",
        architecture_state=authoritative,
        targets=[target],
    )
    context.append_decision(
        make_decision(
            algorithm_name=AlgorithmName.PCA,
            decision_type=DecisionType.PERSIST,
            status=DecisionStatus.PROVISIONAL,
        )
    )
    before_state = clone_state(authoritative)
    before_target = context.get_target(target.structure_id)

    plan = plan_authorized_state_changes(
        context,
        create_default_registry(),
        id_provider=DeterministicIDs(),
    )

    assert authoritative == before_state
    assert context.get_target(target.structure_id) == before_target
    assert authoritative.memory_graph.nodes == {}
    assert authoritative.rollback_points == []
    assert authoritative.governance_state.pending_escalations == []
    assert plan.changes
    assert plan.graph_updates
    assert plan.rollback_points
