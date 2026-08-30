import json

import pytest

from aci.algorithms.cga import (
    evaluate_governance,
    run_cga_where_required,
)
from aci.algorithms.cra import (
    NormalizedProposition,
    PropositionComparisonFixture,
    PropositionPolarity,
    run_cra_where_required,
)
from aci.algorithms.gea import run_gea_where_required
from aci.algorithms.mssa import run_mssa_where_required
from aci.algorithms.pca import run_pca_where_required
from aci.algorithms.stubs import run_aea_stub_where_required
from aci.core import ReviewDecision, ScoreBundle, SymbolicStructure
from aci.enums import (
    AlgorithmName,
    CandidateStatus,
    DecisionStatus,
    DecisionType,
    EvidenceRelationType,
    GovernanceMode,
    StructureType,
    SymbolicState,
    VerificationStatus,
)
from aci.evidence import EvidenceLink, EvidenceObject
from aci.graphs import EvidenceGraph
from aci.metadata import initialize_metadata
from aci.review_context import (
    AlgorithmContractError,
    ReviewContext,
    ReviewContextError,
    UnresolvedReviewItem,
    run_algorithm_where_required,
)
from aci.state import ArchitectureState


def make_target(
    structure_id="structure-001",
    structure_type=StructureType.CLAIM,
):
    return SymbolicStructure(
        structure_id=structure_id,
        content="A candidate under dependent review.",
        structure_type=structure_type,
        current_state=SymbolicState.CANDIDATE,
        metadata=initialize_metadata(origin="input-001"),
    )


def make_context(*targets):
    target_values = list(targets) or [make_target()]
    state = ArchitectureState(
        state_id="state-001",
        active_structures={
            target.structure_id: target
            for target in target_values
        },
        monitoring_triggers=["baseline-monitor"],
    )
    return ReviewContext(
        audit_id="audit-001",
        architecture_state=state,
        targets=target_values,
    ), state


def make_decision(
    *,
    decision_id="decision-001",
    algorithm_name=AlgorithmName.GEA,
    target_id="structure-001",
    decision_type=DecisionType.APPROVE_WITH_MONITORING,
    status=DecisionStatus.PROVISIONAL,
    grounding_score=0.0,
    persistence_score=0.0,
    audit_id="audit-001",
):
    return ReviewDecision(
        decision_id=decision_id,
        algorithm_name=algorithm_name,
        target_id=target_id,
        decision_type=decision_type,
        status=status,
        scores=ScoreBundle(
            grounding_score=grounding_score,
            persistence_score=persistence_score,
        ),
        rationale="A typed test judgment.",
        authorized=False,
        audit_id=audit_id,
    )


def test_context_captures_read_isolated_state_and_targets():
    target = make_target()
    context, state = make_context(target)
    state_before = state.to_dict()
    target_before = target.to_dict()

    state_view = context.architecture_state
    target_view = context.get_target(target.structure_id)
    state_view.monitoring_triggers.append("reviewer-local")
    state_view.active_structures[target.structure_id].content = "mutated view"
    target_view.metadata.grounding_score = 1.0

    assert state.to_dict() == state_before
    assert target.to_dict() == target_before
    assert context.architecture_state.to_dict() == state_before
    assert context.get_target(target.structure_id).to_dict() == target_before


def test_decision_queries_preserve_append_order_and_latest_algorithm_result():
    context, _ = make_context()
    decisions = [
        make_decision(
            decision_id="decision-gea-001",
            grounding_score=0.40,
        ),
        make_decision(
            decision_id="decision-cra-001",
            algorithm_name=AlgorithmName.CRA,
            decision_type=DecisionType.REPAIR,
        ),
        make_decision(
            decision_id="decision-gea-002",
            grounding_score=0.80,
        ),
    ]

    context.append_decisions(decisions)

    assert [
        decision.decision_id
        for decision in context.decisions_for("structure-001")
    ] == [
        "decision-gea-001",
        "decision-cra-001",
        "decision-gea-002",
    ]
    assert (
        context.latest_by_algorithm(
            "structure-001",
            AlgorithmName.GEA,
        ).decision_id
        == "decision-gea-002"
    )
    assert context.latest_grounding("structure-001").decision_id == (
        "decision-gea-002"
    )
    assert context.latest_coherence("structure-001").decision_id == (
        "decision-cra-001"
    )
    assert (
        context.latest_score(
            "structure-001",
            AlgorithmName.GEA,
            "grounding_score",
        )
        == 0.80
    )


def test_append_rejects_wrong_audit_and_unknown_target():
    context, _ = make_context()

    with pytest.raises(ReviewContextError, match="audit_id"):
        context.append_decision(
            make_decision(audit_id="audit-forged")
        )
    with pytest.raises(ReviewContextError, match="unknown target_id"):
        context.append_decision(
            make_decision(target_id="structure-missing")
        )

    assert context.decisions == ()
    assert context.review_trace == ()


def test_batch_append_is_atomic_when_any_decision_is_invalid():
    context, _ = make_context()
    valid = make_decision(decision_id="decision-valid")
    invalid = make_decision(
        decision_id="decision-invalid",
        audit_id="audit-forged",
    )

    with pytest.raises(ReviewContextError, match="audit_id"):
        context.append_decisions([valid, invalid])

    assert context.decisions == ()
    assert context.review_trace == ()


def test_duplicate_decision_identifiers_are_rejected():
    context, _ = make_context()
    context.append_decision(make_decision())

    with pytest.raises(ReviewContextError, match="duplicate decision_id"):
        context.append_decision(make_decision())

    assert len(context.decisions) == 1


def test_stored_decisions_are_isolated_from_caller_mutation():
    context, _ = make_context()
    decision = make_decision(grounding_score=0.70)
    context.append_decision(decision)

    decision.rationale = "caller mutation"
    returned = context.latest_grounding("structure-001")
    returned.scores.grounding_score = 0.0

    stored = context.latest_grounding("structure-001")
    assert stored.rationale == "A typed test judgment."
    assert stored.scores.grounding_score == 0.70


def test_review_trace_is_typed_and_strictly_ordered():
    context, _ = make_context()
    context.append_decisions(
        [
            make_decision(decision_id="decision-001"),
            make_decision(
                decision_id="decision-002",
                algorithm_name=AlgorithmName.CRA,
                decision_type=DecisionType.REPAIR,
            ),
        ]
    )

    assert [entry.sequence for entry in context.review_trace] == [1, 2]
    assert [entry.algorithm_name for entry in context.review_trace] == [
        AlgorithmName.GEA,
        AlgorithmName.CRA,
    ]
    assert [entry.decision_id for entry in context.review_trace] == [
        "decision-001",
        "decision-002",
    ]


def test_unresolved_items_are_append_only_and_decision_linked():
    context, _ = make_context()
    context.append_decision(make_decision())
    item = UnresolvedReviewItem(
        item_id="unresolved-001",
        target_id="structure-001",
        reason="Independent evidence remains unavailable.",
        decision_ref="decision-001",
    )

    context.record_unresolved(item)

    assert context.unresolved_items == (item,)
    assert context.unresolved_for("structure-001") == (item,)
    with pytest.raises(ReviewContextError, match="duplicate unresolved"):
        context.record_unresolved(item)
    with pytest.raises(ReviewContextError, match="unknown decision_ref"):
        context.record_unresolved(
            UnresolvedReviewItem(
                item_id="unresolved-002",
                target_id="structure-001",
                reason="Missing review.",
                decision_ref="decision-missing",
            )
        )


def test_later_reviewer_consumes_earlier_typed_judgment_without_mutation():
    target = make_target()
    context, state = make_context(target)
    state_before = state.to_dict()
    target_before = target.to_dict()

    def grounding_review(review_context):
        reviewed_target = review_context.get_target("structure-001")
        assert reviewed_target.metadata.grounding_score == 0.0
        review_context.append_decision(
            make_decision(
                decision_id="decision-gea",
                grounding_score=0.82,
            )
        )

    def persistence_review(review_context):
        grounding = review_context.latest_grounding("structure-001")
        assert grounding is not None
        assert grounding.scores.grounding_score == 0.82
        review_context.append_decision(
            make_decision(
                decision_id="decision-pca",
                algorithm_name=AlgorithmName.PCA,
                decision_type=DecisionType.DELAY,
                status=DecisionStatus.PENDING_REVIEW,
                grounding_score=grounding.scores.grounding_score,
                persistence_score=0.25,
            )
        )

    assert run_algorithm_where_required(context, grounding_review) is None
    assert run_algorithm_where_required(context, persistence_review) is None

    assert [decision.algorithm_name for decision in context.decisions] == [
        AlgorithmName.GEA,
        AlgorithmName.PCA,
    ]
    assert context.latest_persistence("structure-001").scores == ScoreBundle(
        grounding_score=0.82,
        persistence_score=0.25,
    )
    assert context.has_blocking_decision("structure-001")
    assert state.to_dict() == state_before
    assert target.to_dict() == target_before


def test_algorithm_return_value_violates_contract_and_rolls_back_history():
    context, _ = make_context()

    def invalid_reviewer(review_context):
        decision = make_decision()
        review_context.append_decision(decision)
        return decision

    with pytest.raises(AlgorithmContractError, match="return None"):
        run_algorithm_where_required(context, invalid_reviewer)

    assert context.decisions == ()
    assert context.review_trace == ()


def test_algorithm_exception_rolls_back_partial_review_history():
    context, _ = make_context()

    def failing_reviewer(review_context):
        review_context.append_decision(make_decision())
        review_context.record_unresolved(
            UnresolvedReviewItem(
                item_id="unresolved-001",
                target_id="structure-001",
                reason="Failure after append.",
                decision_ref="decision-001",
            )
        )
        raise RuntimeError("injected reviewer failure")

    with pytest.raises(RuntimeError, match="injected reviewer failure"):
        run_algorithm_where_required(context, failing_reviewer)

    assert context.decisions == ()
    assert context.unresolved_items == ()
    assert context.review_trace == ()


def test_private_state_or_target_mutation_is_detected_and_restored():
    context, _ = make_context()
    before = context.architecture_state.to_dict()
    target_before = context.get_target("structure-001").to_dict()

    def violating_reviewer(review_context):
        review_context._state_snapshot.monitoring_triggers.append("hidden")
        review_context._targets["structure-001"].metadata.grounding_score = 1.0

    with pytest.raises(AlgorithmContractError, match="mutated audit, state"):
        run_algorithm_where_required(context, violating_reviewer)

    assert context.architecture_state.to_dict() == before
    assert context.get_target("structure-001").to_dict() == target_before


def test_private_audit_mutation_is_detected_and_restored():
    context, _ = make_context()

    def violating_reviewer(review_context):
        review_context._audit_id = "audit-forged"

    with pytest.raises(AlgorithmContractError, match="mutated audit"):
        run_algorithm_where_required(context, violating_reviewer)

    assert context.audit_id == "audit-001"


def test_existing_review_history_cannot_be_removed_or_rewritten():
    context, _ = make_context()
    context.append_decision(make_decision())
    decisions_before = context.decisions
    trace_before = context.review_trace

    def violating_reviewer(review_context):
        review_context._decisions.clear()
        review_context._review_trace.clear()

    with pytest.raises(AlgorithmContractError, match="existing review history"):
        run_algorithm_where_required(context, violating_reviewer)

    assert context.decisions == decisions_before
    assert context.review_trace == trace_before


def test_decision_append_cannot_bypass_ordered_trace():
    context, _ = make_context()

    def violating_reviewer(review_context):
        review_context._decisions.append(make_decision())

    with pytest.raises(AlgorithmContractError, match="ordered decision tracing"):
        run_algorithm_where_required(context, violating_reviewer)

    assert context.decisions == ()
    assert context.review_trace == ()


def test_queries_are_target_scoped_across_multiple_targets():
    first = make_target("structure-001")
    second = make_target("structure-002")
    context, _ = make_context(first, second)
    context.append_decisions(
        [
            make_decision(
                decision_id="decision-001",
                target_id="structure-001",
            ),
            make_decision(
                decision_id="decision-002",
                target_id="structure-002",
            ),
        ]
    )

    assert [
        decision.decision_id
        for decision in context.decisions_for("structure-001")
    ] == ["decision-001"]
    assert [
        decision.decision_id
        for decision in context.decisions_for("structure-002")
    ] == ["decision-002"]


def test_unknown_query_target_and_score_field_fail_visibly():
    context, _ = make_context()

    with pytest.raises(ReviewContextError, match="unknown target_id"):
        context.decisions_for("structure-missing")
    with pytest.raises(ValueError, match="unknown score_field"):
        context.latest_score(
            "structure-001",
            AlgorithmName.GEA,
            "not_a_score",
        )


def test_duplicate_target_identifiers_are_rejected():
    target = make_target()
    state = ArchitectureState(state_id="state-001")

    with pytest.raises(ReviewContextError, match="duplicate target_id"):
        ReviewContext(
            audit_id="audit-001",
            architecture_state=state,
            targets=[target, target],
        )


def test_audit_identity_is_read_only():
    context, _ = make_context()

    with pytest.raises(AttributeError):
        context.audit_id = "audit-forged"

    assert context.audit_id == "audit-001"


def test_context_serializes_review_lineage_without_embedding_live_state():
    context, _ = make_context()
    context.append_decision(make_decision())
    context.record_unresolved(
        UnresolvedReviewItem(
            item_id="unresolved-001",
            target_id="structure-001",
            reason="Awaiting independent evidence.",
            decision_ref="decision-001",
        )
    )

    diagnostics = json.loads(json.dumps(context.to_dict(), sort_keys=True))

    assert diagnostics["audit_id"] == "audit-001"
    assert diagnostics["architecture_state_ref"] == "state-001"
    assert diagnostics["target_ids"] == ["structure-001"]
    assert diagnostics["decisions"][0]["algorithm_name"] == "algorithm.gea"
    assert diagnostics["review_trace"][0]["sequence"] == 1
    assert diagnostics["unresolved_items"][0]["item_id"] == "unresolved-001"
    assert "memory_graph" not in diagnostics


def test_real_pca_consumes_gea_and_cra_decisions_without_mutation():
    target = SymbolicStructure(
        structure_id="structure-001",
        content="A persistence candidate with typed support.",
        structure_type=StructureType.CLAIM,
        current_state=SymbolicState.CANDIDATE,
        metadata=initialize_metadata(
            origin="input-001",
            candidate_status=CandidateStatus.PERSISTENCE_CANDIDATE,
            audit_refs=["audit-001"],
        ),
    )
    counterpart = make_target("structure-002")
    evidence = EvidenceObject(
        evidence_id="evidence-001",
        content="A verified measurement.",
        source_ref="source://measurement-001",
    )
    link = EvidenceLink(
        evidence_id=evidence.evidence_id,
        target_structure_id=target.structure_id,
        source_ref=evidence.source_ref,
        relation_type=EvidenceRelationType.SUPPORTS,
        verification_status=VerificationStatus.VERIFIED,
    )
    state = ArchitectureState(
        state_id="state-pca-dependency",
        active_structures={
            target.structure_id: target,
            counterpart.structure_id: counterpart,
        },
        evidence_graph=EvidenceGraph(
            evidence_objects={evidence.evidence_id: evidence},
            links=[link],
        ),
    )
    context = ReviewContext(
        audit_id="audit-001",
        architecture_state=state,
        targets=[target, counterpart],
    )
    comparison = PropositionComparisonFixture(
        comparison_id="comparison-001",
        target=NormalizedProposition(
            structure_id=target.structure_id,
            subject="system",
            relation="has",
            object_value="property",
            polarity=PropositionPolarity.AFFIRMED,
        ),
        counterpart=NormalizedProposition(
            structure_id=counterpart.structure_id,
            subject="system",
            relation="has",
            object_value="property",
            polarity=PropositionPolarity.AFFIRMED,
        ),
    )
    state_before = state.to_dict()
    target_before = target.to_dict()
    gea_ids = iter(("decision-gea-target", "decision-gea-counterpart"))

    run_gea_where_required(context, id_provider=lambda: next(gea_ids))
    run_cra_where_required(
        context,
        (comparison,),
        decision_id_provider=lambda: "decision-cra-target",
        unresolved_id_provider=lambda: "unresolved-unused",
    )
    run_pca_where_required(
        context,
        id_provider=lambda: "decision-pca-target",
    )

    target_decisions = context.decisions_for(target.structure_id)
    assert [decision.algorithm_name for decision in target_decisions] == [
        AlgorithmName.GEA,
        AlgorithmName.CRA,
        AlgorithmName.PCA,
    ]
    pca = context.latest_persistence(target.structure_id)
    assert pca.decision_type is DecisionType.PERSIST
    assert pca.status is DecisionStatus.PROVISIONAL
    assert pca.scores.grounding_score == 1.0
    assert pca.scores.coherence_score == 1.0
    assert pca.scores.persistence_score == 1.0
    assert state.to_dict() == state_before
    assert target.to_dict() == target_before


def test_real_cga_consumes_scale_and_escalation_decisions_without_mutation():
    target = SymbolicStructure(
        structure_id="structure-001",
        content="A neutral architectural candidate.",
        structure_type=StructureType.ARCHITECTURAL_CANDIDATE,
        current_state=SymbolicState.CANDIDATE,
        metadata=initialize_metadata(
            origin="input-001",
            candidate_status=CandidateStatus.ARCHITECTURE_CANDIDATE,
            audit_refs=["audit-001"],
        ),
    )
    state = ArchitectureState(
        state_id="state-cga-dependency",
        active_structures={target.structure_id: target},
    )
    context = ReviewContext(
        audit_id="audit-001",
        architecture_state=state,
        targets=[target],
    )
    state_before = state.to_dict()
    target_before = target.to_dict()

    run_mssa_where_required(
        context,
        id_provider=lambda: "decision-mssa",
    )
    run_aea_stub_where_required(
        context,
        id_provider=lambda: "decision-aea",
    )
    assessment = evaluate_governance(context, target.structure_id)

    assert assessment.dependency_decision_refs == (
        "decision-mssa",
        "decision-aea",
    )
    assert assessment.pending_escalation_refs == (
        "decision-mssa",
        "decision-aea",
    )
    assert assessment.recommended_mode is GovernanceMode.CONSTITUTIONAL_RISK
    assert assessment.output_block_recommended

    run_cga_where_required(
        context,
        id_provider=lambda: "decision-cga",
    )

    assert [
        decision.algorithm_name
        for decision in context.decisions_for(target.structure_id)
    ] == [
        AlgorithmName.MSSA,
        AlgorithmName.AEA,
        AlgorithmName.CGA,
    ]
    cga = context.latest_by_algorithm(target.structure_id, AlgorithmName.CGA)
    assert cga.status is DecisionStatus.BLOCKED
    assert cga.scores.constitutional_risk_score > 0.0
    assert cga.output_block_recommended
    assert state.to_dict() == state_before
    assert target.to_dict() == target_before
