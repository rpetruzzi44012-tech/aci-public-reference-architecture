from copy import deepcopy

import pytest

from aci.core import (
    AuditRecord,
    EscalationEvent,
    GraphUpdate,
    ReviewDecision,
    RollbackPoint,
    ScoreBundle,
    StateChange,
    StateChangePlan,
    SymbolicMetadata,
    SymbolicStructure,
)
from aci.enums import (
    AlgorithmName,
    AuditStatus,
    AuthorityLevel,
    BudgetType,
    CandidateStatus,
    DecisionStatus,
    DecisionType,
    EpistemicStatus,
    EscalationUrgency,
    EvidenceRelationType,
    GraphName,
    GraphUpdateType,
    ScaleLabel,
    StructureType,
    SymbolicState,
    VerificationStatus,
)
from aci.registry import DecisionValidationResult
from aci.state import ArchitectureState, clone_state
from aci.state_update import (
    StateChangeApplicationError,
    apply_state_change_plan,
    calculate_state_delta,
)


AUDIT_ID = "audit-017"


def make_structure(
    structure_id: str = "structure-001",
    *,
    scale_label: ScaleLabel = ScaleLabel.CLAIM,
    authority_level: AuthorityLevel = AuthorityLevel.NONE,
    current_state: SymbolicState = SymbolicState.CANDIDATE,
) -> SymbolicStructure:
    return SymbolicStructure(
        structure_id=structure_id,
        content=f"Provisional content for {structure_id}.",
        structure_type=StructureType.CLAIM,
        current_state=current_state,
        metadata=SymbolicMetadata(
            origin="input-017",
            epistemic_status=EpistemicStatus.UNGROUNDED,
            scale_label=scale_label,
            candidate_status=CandidateStatus.NONE,
            authority_level=authority_level,
            grounding_score=0.2,
            coherence_score=0.4,
            persistence_score=0.1,
            uncertainty=0.8,
            audit_refs=[],
        ),
    )


def make_pending_audit(audit_id: str = AUDIT_ID) -> AuditRecord:
    return AuditRecord(
        audit_id=audit_id,
        status=AuditStatus.PENDING,
        cycle_id="cycle-017",
        baseline_state_ref="state-017",
    )


def make_state(
    *structures: SymbolicStructure,
    audit_id: str = AUDIT_ID,
) -> ArchitectureState:
    values = list(structures) or [make_structure()]
    return ArchitectureState(
        state_id="state-017",
        active_structures={
            structure.structure_id: structure
            for structure in values
        },
        audit_log=[make_pending_audit(audit_id)],
    )


def validation(
    decision_id: str,
    algorithm: AlgorithmName,
    target_id: str = "structure-001",
) -> DecisionValidationResult:
    return DecisionValidationResult(
        decision_id=decision_id,
        target_id=target_id,
        algorithm_identity=algorithm.value,
        accepted=True,
        issues=(),
    )


def make_plan(
    algorithms: dict[str, AlgorithmName],
    *,
    changes: list[StateChange] | None = None,
    updates: list[GraphUpdate] | None = None,
    rollbacks: list[RollbackPoint] | None = None,
    escalations: list[EscalationEvent] | None = None,
    plan_id: str = "plan-017",
) -> StateChangePlan:
    changes = changes or []
    updates = updates or []
    rollbacks = rollbacks or []
    escalations = escalations or []
    target_by_decision = {
        effect.decision_ref: effect.target_id
        for effect in (*changes, *escalations)
    }
    for update in updates:
        target_by_decision.setdefault(
            update.decision_ref,
            update.affected_nodes[0] if update.affected_nodes else "structure-001",
        )
    return StateChangePlan(
        plan_id=plan_id,
        decision_refs=list(algorithms),
        changes=changes,
        graph_updates=updates,
        rollback_points=rollbacks,
        escalation_events=escalations,
        validation_results=[
            validation(
                decision_id,
                algorithm,
                target_by_decision.get(decision_id, "structure-001"),
            )
            for decision_id, algorithm in algorithms.items()
        ],
        rationale=["Application fixture with preserved validation."],
        authorized=bool(algorithms),
        audit_ref=AUDIT_ID,
    )


def structure_change(
    decision_ref: str,
    new_state: SymbolicState,
    authority_level: AuthorityLevel,
    *,
    target_id: str = "structure-001",
) -> StateChange:
    return StateChange(
        change_id=f"change-{decision_ref}",
        target_id=target_id,
        change_type="structure_state_change",
        decision_ref=decision_ref,
        audit_ref=AUDIT_ID,
        payload={
            "new_state": new_state.value,
            "authority_level": authority_level.value,
        },
    )


def memory_update(
    decision_ref: str,
    update_type: GraphUpdateType,
    *,
    target_id: str = "structure-001",
    payload: dict | None = None,
) -> GraphUpdate:
    return GraphUpdate(
        update_id=f"update-{decision_ref}",
        graph_name=GraphName.MEMORY_GRAPH,
        update_type=update_type,
        affected_nodes=[target_id],
        affected_edges=[],
        decision_ref=decision_ref,
        audit_ref=AUDIT_ID,
        payload=payload or {},
    )


def rollback(
    *,
    structures: list[str] | None = None,
    graphs: list[GraphName] | None = None,
) -> RollbackPoint:
    return RollbackPoint(
        rollback_id="rollback-017",
        state_ref="state-017",
        affected_structures=structures or [],
        affected_graphs=graphs or [],
        reason_created="Preserve exact pre-application scope.",
        audit_ref=AUDIT_ID,
        valid_until="cycle-end",
    )


@pytest.mark.parametrize(
    ("algorithm", "new_state", "authority_level"),
    [
        (
            AlgorithmName.GEA,
            SymbolicState.SANDBOXED,
            AuthorityLevel.TEMPORARY_USE,
        ),
        (
            AlgorithmName.GEA,
            SymbolicState.REJECTED,
            AuthorityLevel.NONE,
        ),
    ],
)
def test_basic_structure_operations_apply_to_returned_copy_only(
    algorithm,
    new_state,
    authority_level,
):
    source = make_state()
    before = clone_state(source)
    decision_ref = f"decision-{new_state.name.lower()}"
    plan = make_plan(
        {decision_ref: algorithm},
        changes=[
            structure_change(decision_ref, new_state, authority_level),
        ],
    )

    applied = apply_state_change_plan(source, plan, AUDIT_ID)

    assert applied.active_structures["structure-001"].current_state is new_state
    assert (
        applied.active_structures["structure-001"].metadata.authority_level
        is authority_level
    )
    assert applied.state_changes[0].decision_ref == decision_ref
    assert applied.state_changes[0].audit_ref == AUDIT_ID
    assert source == before


@pytest.mark.parametrize(
    ("new_state", "update_type", "needs_rollback"),
    [
        (SymbolicState.ARCHIVED, GraphUpdateType.NODE_ADDED, False),
        (SymbolicState.PERSISTENT, GraphUpdateType.NODE_ADDED, True),
        (SymbolicState.RETRACTED, GraphUpdateType.RELATION_UPDATED, True),
    ],
)
def test_memory_operations_apply_only_as_paired_pca_artifacts(
    new_state,
    update_type,
    needs_rollback,
):
    source = make_state(
        make_structure(
            current_state=(
                SymbolicState.PERSISTENT
                if new_state is SymbolicState.RETRACTED
                else SymbolicState.CANDIDATE
            ),
            authority_level=(
                AuthorityLevel.MEMORY_INFLUENCE
                if new_state is SymbolicState.RETRACTED
                else AuthorityLevel.NONE
            ),
        )
    )
    if new_state is SymbolicState.RETRACTED:
        source.memory_graph.nodes["structure-001"] = deepcopy(
            source.active_structures["structure-001"]
        )
    before = clone_state(source)
    decision_ref = f"decision-{new_state.name.lower()}"
    authority = (
        AuthorityLevel.MEMORY_INFLUENCE
        if new_state is SymbolicState.PERSISTENT
        else AuthorityLevel.NONE
    )
    update = memory_update(
        decision_ref,
        update_type,
        payload=(
            {"operation": "sync_structure"}
            if update_type is GraphUpdateType.RELATION_UPDATED
            else None
        ),
    )
    plan = make_plan(
        {decision_ref: AlgorithmName.PCA},
        changes=[structure_change(decision_ref, new_state, authority)],
        updates=[update],
        rollbacks=(
            [rollback(structures=["structure-001"])]
            if needs_rollback
            else []
        ),
    )

    applied = apply_state_change_plan(source, plan, AUDIT_ID)

    assert applied.active_structures["structure-001"].current_state is new_state
    assert applied.memory_graph.nodes["structure-001"].current_state is new_state
    assert applied.applied_graph_updates[0].decision_ref == decision_ref
    assert applied.applied_graph_updates[0].audit_ref == AUDIT_ID
    assert bool(applied.rollback_points) is needs_rollback
    assert source == before


@pytest.mark.parametrize(
    ("change_type", "payload", "algorithm", "expected_state", "marker"),
    [
        (
            "mark_for_revision",
            {"review_state": SymbolicState.COHERENCE_REVIEW.value},
            AlgorithmName.GEA,
            SymbolicState.COHERENCE_REVIEW,
            "revision_required",
        ),
        (
            "delay",
            {"reason": "Wait for a missing dependency."},
            AlgorithmName.GEA,
            SymbolicState.CANDIDATE,
            "delayed",
        ),
        (
            "monitoring_trigger_add",
            {"condition": "watch-grounding"},
            AlgorithmName.GEA,
            SymbolicState.CANDIDATE,
            "watch-grounding",
        ),
    ],
)
def test_revision_delay_and_monitoring_match_the_plan(
    change_type,
    payload,
    algorithm,
    expected_state,
    marker,
):
    source = make_state()
    decision_ref = f"decision-{change_type}"
    change = StateChange(
        change_id=f"change-{change_type}",
        target_id="structure-001",
        change_type=change_type,
        decision_ref=decision_ref,
        audit_ref=AUDIT_ID,
        payload=payload,
    )

    applied = apply_state_change_plan(
        source,
        make_plan({decision_ref: algorithm}, changes=[change]),
        AUDIT_ID,
    )

    assert applied.active_structures["structure-001"].current_state is expected_state
    assert any(marker in trigger for trigger in applied.monitoring_triggers)


def test_coherence_tension_is_recorded_without_grounding_promotion():
    source = make_state()
    before_grounding = source.active_structures[
        "structure-001"
    ].metadata.grounding_score
    change = StateChange(
        change_id="change-tension",
        target_id="structure-001",
        change_type="coherence_tension_add",
        decision_ref="decision-cra",
        audit_ref=AUDIT_ID,
        payload={
            "tension_id": "tension-017",
            "reason": "Two structured propositions remain incompatible.",
        },
    )

    applied = apply_state_change_plan(
        source,
        make_plan(
            {"decision-cra": AlgorithmName.CRA},
            changes=[change],
        ),
        AUDIT_ID,
    )

    assert applied.coherence_graph.unresolved_tensions == ["tension-017"]
    assert applied.coherence_graph.relations[0]["decision_ref"] == "decision-cra"
    assert applied.coherence_graph.relations[0]["audit_ref"] == AUDIT_ID
    assert (
        applied.active_structures["structure-001"].metadata.grounding_score
        == before_grounding
    )
    assert applied.evidence_graph == source.evidence_graph


def test_demotion_updates_scale_without_changing_authority():
    source = make_state(
        make_structure(
            scale_label=ScaleLabel.MEMORY,
            authority_level=AuthorityLevel.MEMORY_INFLUENCE,
        )
    )
    change = StateChange(
        change_id="change-demote",
        target_id="structure-001",
        change_type="scale_demotion_request",
        decision_ref="decision-mssa",
        audit_ref=AUDIT_ID,
        payload={"operation": "demote_one_level"},
    )
    update = GraphUpdate(
        update_id="update-demote",
        graph_name=GraphName.SCALE_GRAPH,
        update_type=GraphUpdateType.RELATION_UPDATED,
        affected_nodes=["structure-001"],
        affected_edges=[],
        decision_ref="decision-mssa",
        audit_ref=AUDIT_ID,
        payload={"operation": "sync_demoted_scale"},
    )

    applied = apply_state_change_plan(
        source,
        make_plan(
            {"decision-mssa": AlgorithmName.MSSA},
            changes=[change],
            updates=[update],
        ),
        AUDIT_ID,
    )

    target = applied.active_structures["structure-001"]
    assert target.metadata.scale_label is ScaleLabel.HYPOTHESIS
    assert target.metadata.authority_level is AuthorityLevel.MEMORY_INFLUENCE
    assert (
        applied.scale_graph.scale_labels["structure-001"]
        is ScaleLabel.HYPOTHESIS
    )
    assert applied.governance_state.authority_graph == (
        source.governance_state.authority_graph
    )


def test_escalation_enters_governance_pending_and_remains_unresolved():
    source = make_state()
    event = EscalationEvent(
        escalation_id="escalation-017",
        target_id="structure-001",
        reason="Grounding review cannot resolve the coherence dependency.",
        urgency=EscalationUrgency.NORMAL,
        decision_ref="decision-escalate",
        from_algorithm=AlgorithmName.GEA,
        to_algorithm=AlgorithmName.CRA,
        resolved=False,
        audit_ref=AUDIT_ID,
    )

    applied = apply_state_change_plan(
        source,
        make_plan(
            {"decision-escalate": AlgorithmName.GEA},
            escalations=[event],
        ),
        AUDIT_ID,
    )

    assert applied.governance_state.pending_escalations == [event]
    assert applied.governance_state.pending_escalations[0].resolved is False
    assert applied.active_structures == source.active_structures


def test_all_five_graph_domains_apply_separately_with_provenance():
    targets = [
        make_structure("structure-memory"),
        make_structure("structure-evidence"),
        make_structure("structure-coherence"),
        make_structure("structure-scale"),
        make_structure("structure-authority"),
    ]
    source = make_state(*targets)
    persist_change = structure_change(
        "decision-pca",
        SymbolicState.PERSISTENT,
        AuthorityLevel.MEMORY_INFLUENCE,
        target_id="structure-memory",
    )
    updates = [
        memory_update(
            "decision-pca",
            GraphUpdateType.NODE_ADDED,
            target_id="structure-memory",
        ),
        GraphUpdate(
            update_id="update-evidence-object",
            graph_name=GraphName.EVIDENCE_GRAPH,
            update_type=GraphUpdateType.NODE_ADDED,
            affected_nodes=["evidence-017"],
            affected_edges=[],
            decision_ref="decision-gea",
            audit_ref=AUDIT_ID,
            payload={
                "evidence_object": {
                    "evidence_id": "evidence-017",
                    "content": "A typed test observation.",
                    "source_ref": "source-017",
                }
            },
        ),
        GraphUpdate(
            update_id="update-evidence-link",
            graph_name=GraphName.EVIDENCE_GRAPH,
            update_type=GraphUpdateType.EDGE_ADDED,
            affected_nodes=["structure-evidence"],
            affected_edges=["evidence-017->structure-evidence"],
            decision_ref="decision-gea",
            audit_ref=AUDIT_ID,
            payload={
                "evidence_link": {
                    "evidence_id": "evidence-017",
                    "target_structure_id": "structure-evidence",
                    "source_ref": "source-017",
                    "relation_type": EvidenceRelationType.SUPPORTS.value,
                    "verification_status": VerificationStatus.VERIFIED.value,
                }
            },
        ),
        GraphUpdate(
            update_id="update-coherence",
            graph_name=GraphName.COHERENCE_GRAPH,
            update_type=GraphUpdateType.EDGE_ADDED,
            affected_nodes=["structure-coherence"],
            affected_edges=["coherence-017"],
            decision_ref="decision-cra",
            audit_ref=AUDIT_ID,
            payload={
                "relation": {
                    "relation_id": "coherence-017",
                    "relation_type": "compatible",
                }
            },
        ),
        GraphUpdate(
            update_id="update-scale",
            graph_name=GraphName.SCALE_GRAPH,
            update_type=GraphUpdateType.NODE_ADDED,
            affected_nodes=["structure-scale"],
            affected_edges=[],
            decision_ref="decision-mssa",
            audit_ref=AUDIT_ID,
            payload={"scale_label": ScaleLabel.HYPOTHESIS.value},
        ),
        GraphUpdate(
            update_id="update-authority",
            graph_name=GraphName.AUTHORITY_GRAPH,
            update_type=GraphUpdateType.EDGE_ADDED,
            affected_nodes=["structure-authority"],
            affected_edges=["authority-017"],
            decision_ref="decision-cga",
            audit_ref=AUDIT_ID,
            payload={
                "collection": "authority_edges",
                "relation": {
                    "edge_id": "authority-017",
                    "from_domain": "governance",
                    "to_domain": "output",
                },
            },
        ),
    ]
    plan = make_plan(
        {
            "decision-pca": AlgorithmName.PCA,
            "decision-gea": AlgorithmName.GEA,
            "decision-cra": AlgorithmName.CRA,
            "decision-mssa": AlgorithmName.MSSA,
            "decision-cga": AlgorithmName.CGA,
        },
        changes=[persist_change],
        updates=updates,
        rollbacks=[
            rollback(
                structures=["structure-memory"],
                graphs=[
                    GraphName.MEMORY_GRAPH,
                    GraphName.AUTHORITY_GRAPH,
                ],
            )
        ],
    )

    applied = apply_state_change_plan(source, plan, AUDIT_ID)

    assert set(applied.memory_graph.nodes) == {"structure-memory"}
    assert set(applied.evidence_graph.evidence_objects) == {"evidence-017"}
    assert len(applied.evidence_graph.links) == 1
    assert applied.coherence_graph.relations[0]["decision_ref"] == "decision-cra"
    assert applied.scale_graph.scale_labels == {
        "structure-scale": ScaleLabel.HYPOTHESIS
    }
    assert applied.governance_state.authority_graph.authority_edges[0][
        "decision_ref"
    ] == "decision-cga"
    assert {
        update.graph_name
        for update in applied.applied_graph_updates
    } == set(GraphName)
    assert all(
        update.audit_ref == AUDIT_ID
        for update in applied.applied_graph_updates
    )


def test_evidence_algorithm_cannot_write_memory_and_failure_is_atomic():
    source = make_state()
    before = clone_state(source)
    change = structure_change(
        "decision-gea",
        SymbolicState.PERSISTENT,
        AuthorityLevel.MEMORY_INFLUENCE,
    )
    plan = make_plan(
        {"decision-gea": AlgorithmName.GEA},
        changes=[change],
        updates=[
            memory_update(
                "decision-gea",
                GraphUpdateType.NODE_ADDED,
            )
        ],
        rollbacks=[rollback(structures=["structure-001"])],
    )

    with pytest.raises(
        StateChangeApplicationError,
        match="require PCA authorization",
    ):
        apply_state_change_plan(source, plan, AUDIT_ID)

    assert source == before


def test_authority_graph_rejects_non_governance_authorization_atomically():
    source = make_state()
    before = clone_state(source)
    update = GraphUpdate(
        update_id="update-forged-authority",
        graph_name=GraphName.AUTHORITY_GRAPH,
        update_type=GraphUpdateType.NODE_ADDED,
        affected_nodes=["output"],
        affected_edges=[],
        decision_ref="decision-gea",
        audit_ref=AUDIT_ID,
    )
    plan = make_plan(
        {"decision-gea": AlgorithmName.GEA},
        updates=[update],
        rollbacks=[rollback(graphs=[GraphName.AUTHORITY_GRAPH])],
    )

    with pytest.raises(
        StateChangeApplicationError,
        match="require CGA authorization",
    ):
        apply_state_change_plan(source, plan, AUDIT_ID)

    assert source == before


def test_budget_effect_exposes_domain_cost_and_verification_cost():
    source = make_state()
    change = StateChange(
        change_id="change-budget",
        target_id="structure-001",
        change_type="budget_effect",
        decision_ref="decision-budget",
        audit_ref=AUDIT_ID,
        payload={
            "budget_type": BudgetType.ATTENTION.value,
            "delta": -0.1,
            "verification_cost": 0.2,
            "reason": "Apply and verify the authorized state plan.",
        },
    )

    applied = apply_state_change_plan(
        source,
        make_plan(
            {"decision-budget": AlgorithmName.GEA},
            changes=[change],
        ),
        AUDIT_ID,
    )

    assert applied.budgets.attention_budget == pytest.approx(0.9)
    assert applied.budgets.verification_budget == pytest.approx(0.8)
    assert applied.state_changes[0].payload["verification_cost"] == 0.2
    assert source.budgets.attention_budget == 1.0
    assert source.budgets.verification_budget == 1.0


def test_rejected_and_no_op_items_never_become_application_effects():
    source = make_state()
    rejected = make_review_decision("decision-rejected")
    no_op = make_review_decision("decision-no-op")
    plan = StateChangePlan(
        plan_id="plan-no-effects",
        decision_refs=[],
        validation_results=[],
        rejected_decisions=[rejected],
        no_op_items=[no_op],
        rationale=["No decision was authorized for application."],
        authorized=False,
        audit_ref=AUDIT_ID,
    )

    applied = apply_state_change_plan(source, plan, AUDIT_ID)

    assert applied == source
    assert applied is not source
    assert applied.state_changes == []
    assert applied.applied_graph_updates == []


def test_high_risk_change_requires_scoped_valid_rollback():
    source = make_state()
    plan = make_plan(
        {"decision-pca": AlgorithmName.PCA},
        changes=[
            structure_change(
                "decision-pca",
                SymbolicState.PERSISTENT,
                AuthorityLevel.MEMORY_INFLUENCE,
            )
        ],
        updates=[
            memory_update(
                "decision-pca",
                GraphUpdateType.NODE_ADDED,
            )
        ],
    )

    with pytest.raises(
        StateChangeApplicationError,
        match="requires scoped rollback",
    ):
        apply_state_change_plan(source, plan, AUDIT_ID)


def test_same_plan_cannot_be_applied_twice_to_one_state_lineage():
    source = make_state()
    change = StateChange(
        change_id="change-once",
        target_id="structure-001",
        change_type="monitoring_trigger_add",
        decision_ref="decision-once",
        audit_ref=AUDIT_ID,
        payload={"condition": "apply-once"},
    )
    plan = make_plan(
        {"decision-once": AlgorithmName.GEA},
        changes=[change],
        plan_id="plan-once",
    )
    applied_once = apply_state_change_plan(source, plan, AUDIT_ID)
    before_second_attempt = clone_state(applied_once)

    with pytest.raises(
        StateChangeApplicationError,
        match="identifiers already exist",
    ):
        apply_state_change_plan(applied_once, plan, AUDIT_ID)

    assert applied_once == before_second_attempt


def test_partial_persistence_plan_is_rejected_before_application():
    source = make_state()
    plan = make_plan(
        {"decision-pca": AlgorithmName.PCA},
        changes=[
            structure_change(
                "decision-pca",
                SymbolicState.PERSISTENT,
                AuthorityLevel.MEMORY_INFLUENCE,
            )
        ],
        rollbacks=[rollback(structures=["structure-001"])],
    )

    with pytest.raises(
        StateChangeApplicationError,
        match="paired graph.memory_graph update",
    ):
        apply_state_change_plan(source, plan, AUDIT_ID)


def test_state_delta_reports_exact_domains_and_audit_history_separately():
    baseline = make_state()
    change = StateChange(
        change_id="change-budget",
        target_id="structure-001",
        change_type="budget_effect",
        decision_ref="decision-budget",
        audit_ref=AUDIT_ID,
        payload={
            "budget_type": BudgetType.ATTENTION.value,
            "delta": -0.1,
            "verification_cost": 0.2,
            "reason": "Visible Stage 17 accounting.",
        },
    )
    applied = apply_state_change_plan(
        baseline,
        make_plan(
            {"decision-budget": AlgorithmName.GEA},
            changes=[change],
        ),
        AUDIT_ID,
    )

    delta = calculate_state_delta(baseline, applied)

    assert set(delta.domain_changes) == {"budgets"}
    assert delta.applied_change_ids == ["change-budget"]
    assert delta.graph_update_ids == []
    assert delta.escalation_ids == []
    assert delta.rollback_ids == []
    assert delta.audit_ref == AUDIT_ID
    assert delta.audit_log_changed is False
    assert delta.audit_log_before_refs == [AUDIT_ID]
    assert delta.audit_log_after_refs == [AUDIT_ID]

    audit_only = clone_state(baseline)
    audit_only.audit_log.append(make_pending_audit("audit-018"))
    audit_delta = calculate_state_delta(baseline, audit_only)

    assert audit_delta.domain_changes == {}
    assert audit_delta.audit_log_changed is True
    assert audit_delta.audit_ref == "audit-018"
    assert audit_delta.audit_log_before_refs == [AUDIT_ID]
    assert audit_delta.audit_log_after_refs == [AUDIT_ID, "audit-018"]

    terminal_audit = clone_state(baseline)
    terminal_audit.audit_log[0] = AuditRecord(
        audit_id=AUDIT_ID,
        status=AuditStatus.COMMITTED,
        cycle_id="cycle-017",
        baseline_state_ref="state-017",
        finalized_at="2026-06-30T12:00:00+00:00",
    )
    terminal_delta = calculate_state_delta(baseline, terminal_audit)

    assert terminal_delta.domain_changes == {}
    assert terminal_delta.audit_log_changed is True
    assert terminal_delta.audit_ref == AUDIT_ID
    assert terminal_delta.audit_log_before_refs == [AUDIT_ID]
    assert terminal_delta.audit_log_after_refs == [AUDIT_ID]


def test_application_requires_matching_pending_audit():
    source = make_state()
    change = StateChange(
        change_id="change-monitor",
        target_id="structure-001",
        change_type="monitoring_trigger_add",
        decision_ref="decision-monitor",
        audit_ref=AUDIT_ID,
        payload={"condition": "watch"},
    )
    plan = make_plan(
        {"decision-monitor": AlgorithmName.GEA},
        changes=[change],
    )
    source.audit_log[0].status = AuditStatus.COMMITTED
    source.audit_log[0].finalized_at = "2026-06-30T12:00:00+00:00"

    with pytest.raises(
        StateChangeApplicationError,
        match="matching PENDING audit",
    ):
        apply_state_change_plan(source, plan, AUDIT_ID)


def make_review_decision(decision_id: str) -> ReviewDecision:
    return ReviewDecision(
        decision_id=decision_id,
        algorithm_name=AlgorithmName.GEA,
        target_id="structure-001",
        decision_type=DecisionType.APPROVE,
        status=DecisionStatus.PROVISIONAL,
        scores=ScoreBundle(),
        rationale="Preserved non-applicable review decision.",
        authorized=False,
        audit_id=AUDIT_ID,
    )
