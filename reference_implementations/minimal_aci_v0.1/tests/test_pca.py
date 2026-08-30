import pytest

from aci.algorithms.pca import (
    PersistenceEvaluationError,
    PersistenceOutcome,
    evaluate_persistence_candidate,
    run_pca_where_required,
)
from aci.core import (
    ReviewDecision,
    ScoreBundle,
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
    ScaleLabel,
    StructureType,
    SymbolicState,
)
from aci.review_context import ReviewContext, UnresolvedReviewItem
from aci.state import ArchitectureState, ThresholdState, clone_state


def make_target(
    *,
    structure_id="structure-001",
    structure_type=StructureType.CLAIM,
    candidate_status=CandidateStatus.PERSISTENCE_CANDIDATE,
    scale_label=ScaleLabel.CLAIM,
    audit_refs=("audit-001",),
    content="A reviewed persistence candidate.",
):
    return SymbolicStructure(
        structure_id=structure_id,
        content=content,
        structure_type=structure_type,
        current_state=SymbolicState.CANDIDATE,
        metadata=SymbolicMetadata(
            origin="input-001",
            epistemic_status=EpistemicStatus.UNKNOWN,
            scale_label=scale_label,
            candidate_status=candidate_status,
            authority_level=AuthorityLevel.NONE,
            audit_refs=list(audit_refs),
        ),
    )


def make_state(
    *targets,
    grounding_threshold=0.70,
    persistence_threshold=0.75,
):
    target_values = list(targets) or [make_target()]
    return ArchitectureState(
        state_id="state-001",
        active_structures={
            target.structure_id: target
            for target in target_values
        },
        thresholds=ThresholdState(
            grounding_threshold=grounding_threshold,
            persistence_threshold=persistence_threshold,
        ),
    )


def make_context(*targets, state=None):
    target_values = list(targets) or [make_target()]
    return ReviewContext(
        audit_id="audit-001",
        architecture_state=state or make_state(*target_values),
        targets=target_values,
    )


def make_prior_decision(
    algorithm_name,
    *,
    target_id="structure-001",
    decision_type=DecisionType.APPROVE_WITH_MONITORING,
    status=DecisionStatus.MONITORING,
    grounding_score=0.0,
    coherence_score=0.0,
    suffix="001",
):
    return ReviewDecision(
        decision_id=f"decision-{algorithm_name.name.lower()}-{suffix}",
        algorithm_name=algorithm_name,
        target_id=target_id,
        decision_type=decision_type,
        status=status,
        scores=ScoreBundle(
            grounding_score=grounding_score,
            coherence_score=coherence_score,
        ),
        rationale="Prior typed review judgment.",
        authorized=False,
        audit_id="audit-001",
    )


def append_grounding(
    context,
    *,
    target_id="structure-001",
    decision_type=DecisionType.APPROVE_WITH_MONITORING,
    status=DecisionStatus.MONITORING,
    score=1.0,
    suffix="001",
):
    context.append_decision(
        make_prior_decision(
            AlgorithmName.GEA,
            target_id=target_id,
            decision_type=decision_type,
            status=status,
            grounding_score=score,
            suffix=suffix,
        )
    )


def append_coherence(
    context,
    *,
    target_id="structure-001",
    decision_type=DecisionType.APPROVE_WITH_MONITORING,
    status=DecisionStatus.MONITORING,
    score=1.0,
    suffix="001",
    unresolved=False,
):
    decision = make_prior_decision(
        AlgorithmName.CRA,
        target_id=target_id,
        decision_type=decision_type,
        status=status,
        coherence_score=score,
        suffix=suffix,
    )
    context.append_decision(decision)
    if unresolved:
        context.record_unresolved(
            UnresolvedReviewItem(
                item_id=f"unresolved-{suffix}",
                target_id=target_id,
                reason="CRA requires preserved unresolved review.",
                decision_ref=decision.decision_id,
            )
        )


def append_eligible_dependencies(
    context,
    *,
    target_id="structure-001",
    suffix="001",
):
    append_grounding(
        context,
        target_id=target_id,
        suffix=suffix,
    )
    append_coherence(
        context,
        target_id=target_id,
        suffix=suffix,
    )


def test_missing_gea_decision_remains_unresolved_despite_gate_score():
    context = make_context()
    append_coherence(context)

    assessment = evaluate_persistence_candidate(
        context,
        "structure-001",
    )
    run_pca_where_required(
        context,
        id_provider=lambda: "decision-pca-001",
    )

    assert assessment.outcome is PersistenceOutcome.UNRESOLVED
    assert assessment.persistence_score == 0.8
    assert assessment.persistence_check.result
    assert "missing GEA decision" in assessment.reasons
    decision = context.latest_persistence("structure-001")
    assert decision.decision_type is DecisionType.DELAY
    assert decision.status is DecisionStatus.PENDING_REVIEW


def test_missing_cra_decision_cannot_be_replaced_by_grounding():
    context = make_context()
    append_grounding(context)

    assessment = evaluate_persistence_candidate(
        context,
        "structure-001",
    )

    assert assessment.outcome is PersistenceOutcome.UNRESOLVED
    assert assessment.grounding_eligible
    assert not assessment.coherence_eligible
    assert "missing CRA decision" in assessment.reasons


def test_insufficient_grounding_routes_to_non_authoritative_archive():
    context = make_context()
    append_grounding(
        context,
        decision_type=DecisionType.REVISE,
        status=DecisionStatus.PROVISIONAL,
        score=0.0,
    )
    append_coherence(context)

    run_pca_where_required(
        context,
        id_provider=lambda: "decision-pca-001",
    )

    decision = context.latest_persistence("structure-001")
    assert decision.decision_type is DecisionType.ARCHIVE
    assert decision.status is DecisionStatus.FINAL
    assert not decision.authorized
    assert "archive is non-authoritative" in decision.rationale
    assert context.architecture_state.memory_graph.nodes == {}


def test_unresolved_cra_tension_delays_persistence():
    context = make_context()
    append_grounding(context)
    append_coherence(
        context,
        decision_type=DecisionType.DELAY,
        status=DecisionStatus.PENDING_REVIEW,
        score=0.5,
        unresolved=True,
    )

    assessment = evaluate_persistence_candidate(
        context,
        "structure-001",
    )

    assert assessment.outcome is PersistenceOutcome.UNRESOLVED
    assert assessment.unresolved_dependency
    assert not assessment.coherence_eligible
    assert assessment.cra_decision_ref == "decision-cra-001"


def test_direct_contradiction_rejects_candidate():
    context = make_context()
    append_grounding(context)
    append_coherence(
        context,
        decision_type=DecisionType.REPAIR,
        status=DecisionStatus.PROVISIONAL,
        score=0.0,
        unresolved=True,
    )

    run_pca_where_required(
        context,
        id_provider=lambda: "decision-pca-001",
    )

    decision = context.latest_persistence("structure-001")
    assert decision.decision_type is DecisionType.REJECT
    assert decision.status is DecisionStatus.FINAL
    assert "disqualifying contradiction" in decision.rationale


def test_eligible_candidate_receives_provisional_persist_recommendation():
    context = make_context()
    append_eligible_dependencies(context)

    assessment = evaluate_persistence_candidate(
        context,
        "structure-001",
    )
    run_pca_where_required(
        context,
        id_provider=lambda: "decision-pca-001",
    )

    assert assessment.outcome is PersistenceOutcome.PERSIST_RECOMMENDED
    assert assessment.persistence_score == 1.0
    assert assessment.persistence_check.result
    decision = context.latest_persistence("structure-001")
    assert decision.decision_type is DecisionType.PERSIST
    assert decision.status is DecisionStatus.PROVISIONAL
    assert not decision.authorized
    validation = context.architecture_state.algorithm_registry.validate_decision(
        decision,
        context.get_target("structure-001"),
    )
    assert validation.accepted


def test_missing_current_audit_reference_blocks_recommendation():
    target = make_target(audit_refs=("audit-prior",))
    context = make_context(target)
    append_eligible_dependencies(context)

    assessment = evaluate_persistence_candidate(
        context,
        target.structure_id,
    )
    run_pca_where_required(
        context,
        id_provider=lambda: "decision-pca-001",
    )

    assert assessment.outcome is PersistenceOutcome.DELAYED
    assert not assessment.audit_eligible
    decision = context.latest_persistence(target.structure_id)
    assert decision.decision_type is DecisionType.DELAY
    assert decision.status is DecisionStatus.BLOCKED


def test_grounding_and_coherence_without_candidacy_do_not_create_memory():
    target = make_target(candidate_status=CandidateStatus.NONE)
    context = make_context(target)
    append_eligible_dependencies(context)

    assessment = evaluate_persistence_candidate(
        context,
        target.structure_id,
    )
    run_pca_where_required(
        context,
        id_provider=lambda: pytest.fail(
            "noncandidate should not invoke PCA"
        ),
    )

    assert assessment.outcome is PersistenceOutcome.DELAYED
    assert not assessment.candidate_eligible
    assert context.latest_persistence(target.structure_id) is None
    assert context.architecture_state.memory_graph.nodes == {}


def test_unsupported_but_coherent_claim_is_archived_not_persisted():
    context = make_context()
    append_grounding(
        context,
        decision_type=DecisionType.REVISE,
        status=DecisionStatus.PROVISIONAL,
        score=0.0,
    )
    append_coherence(context, score=1.0)

    assessment = evaluate_persistence_candidate(
        context,
        "structure-001",
    )

    assert assessment.coherence_eligible
    assert not assessment.grounding_eligible
    assert assessment.outcome is PersistenceOutcome.ARCHIVE_RECOMMENDED


def test_speculative_hypothesis_is_not_recommended_for_memory():
    target = make_target(
        structure_type=StructureType.HYPOTHESIS,
        scale_label=ScaleLabel.HYPOTHESIS,
    )
    context = make_context(target)
    append_grounding(
        context,
        decision_type=DecisionType.DELAY,
        status=DecisionStatus.PENDING_REVIEW,
        score=0.0,
    )
    append_coherence(context)

    assessment = evaluate_persistence_candidate(
        context,
        target.structure_id,
    )

    assert assessment.outcome is PersistenceOutcome.UNRESOLVED
    assert not assessment.grounding_eligible
    assert assessment.unresolved_dependency


def test_threshold_checks_name_direction_value_and_result():
    context = make_context(
        state=make_state(
            grounding_threshold=0.90,
            persistence_threshold=0.95,
        )
    )
    append_eligible_dependencies(context)

    assessment = evaluate_persistence_candidate(
        context,
        "structure-001",
    )

    assert assessment.grounding_check.threshold_name == "grounding_threshold"
    assert assessment.grounding_check.direction == "minimum_required"
    assert assessment.grounding_check.observed_value == 1.0
    assert assessment.grounding_check.threshold_value == 0.90
    assert assessment.grounding_check.result
    assert assessment.persistence_check.threshold_name == (
        "persistence_threshold"
    )
    assert assessment.persistence_check.direction == "minimum_required"
    assert assessment.persistence_check.observed_value == 1.0
    assert assessment.persistence_check.threshold_value == 0.95
    assert assessment.persistence_check.result


def test_pca_appends_decision_without_mutating_state_target_or_memory():
    target = make_target()
    state = make_state(target)
    baseline = clone_state(state)
    target_before = target.to_dict()
    context = make_context(target, state=state)
    append_eligible_dependencies(context)
    review_state_before = context.architecture_state

    run_pca_where_required(
        context,
        id_provider=lambda: "decision-pca-001",
    )

    assert state == baseline
    assert target.to_dict() == target_before
    assert context.architecture_state == review_state_before
    assert state.memory_graph.nodes == {}
    assert state.memory_graph.persistence_relations == []


def test_registry_authority_failure_is_visible_and_atomic():
    target = make_target(scale_label=ScaleLabel.PRINCIPLE)
    context = make_context(target)
    append_eligible_dependencies(context)
    decisions_before = context.decisions

    assessment = evaluate_persistence_candidate(
        context,
        target.structure_id,
    )

    assert not assessment.authority_eligible
    with pytest.raises(
        PersistenceEvaluationError,
        match="target_scale_exceeds_authority",
    ):
        run_pca_where_required(
            context,
            id_provider=lambda: "decision-pca-001",
        )
    assert context.decisions == decisions_before
    assert context.latest_persistence(target.structure_id) is None


def test_deterministic_id_is_bound_to_cycle_audit():
    context = make_context()
    append_eligible_dependencies(context)

    run_pca_where_required(
        context,
        id_provider=lambda: "decision-pca-deterministic",
    )

    decision = context.latest_persistence("structure-001")
    assert decision.decision_id == "decision-pca-deterministic"
    assert decision.audit_id == "audit-001"


def test_duplicate_pca_id_rolls_back_all_decisions_from_the_call():
    first = make_target()
    second = make_target(structure_id="structure-002")
    context = make_context(first, second)
    append_eligible_dependencies(
        context,
        target_id=first.structure_id,
        suffix="first",
    )
    append_eligible_dependencies(
        context,
        target_id=second.structure_id,
        suffix="second",
    )
    decisions_before = context.decisions

    with pytest.raises(ValueError, match="duplicate decision_id"):
        run_pca_where_required(
            context,
            id_provider=lambda: "decision-pca-duplicate",
        )

    assert context.decisions == decisions_before
    assert context.latest_persistence(first.structure_id) is None
    assert context.latest_persistence(second.structure_id) is None
