import pytest

from aci.algorithms.gea import (
    GroundingEvaluationError,
    evaluate_grounding,
    run_gea_where_required,
)
from aci.core import SymbolicMetadata, SymbolicStructure
from aci.enums import (
    AlgorithmName,
    AuthorityLevel,
    CandidateStatus,
    DecisionStatus,
    DecisionType,
    EpistemicStatus,
    EvidenceRelationType,
    ScaleLabel,
    StructureType,
    SymbolicState,
    VerificationStatus,
)
from aci.evidence import EvidenceLink, EvidenceObject
from aci.graphs import EvidenceGraph
from aci.review_context import ReviewContext, ReviewContextError
from aci.state import ArchitectureState, ThresholdState


def make_target(
    *,
    structure_id="structure-001",
    structure_type=StructureType.CLAIM,
    content="A claim requiring grounding review.",
    epistemic_status=EpistemicStatus.UNKNOWN,
    coherence_score=0.0,
):
    scale_label = (
        ScaleLabel.HYPOTHESIS
        if structure_type is StructureType.HYPOTHESIS
        else ScaleLabel.CLAIM
    )
    return SymbolicStructure(
        structure_id=structure_id,
        content=content,
        structure_type=structure_type,
        current_state=SymbolicState.CANDIDATE,
        metadata=SymbolicMetadata(
            origin="input-001",
            epistemic_status=epistemic_status,
            scale_label=scale_label,
            candidate_status=CandidateStatus.NONE,
            authority_level=AuthorityLevel.NONE,
            coherence_score=coherence_score,
        ),
    )


def make_evidence(
    *,
    evidence_id="evidence-001",
    source_ref="source://study-001",
):
    return EvidenceObject(
        evidence_id=evidence_id,
        content="A measured result.",
        source_ref=source_ref,
    )


def make_link(
    *,
    evidence_id="evidence-001",
    target_id="structure-001",
    source_ref="source://study-001",
    relation_type=EvidenceRelationType.SUPPORTS,
    verification_status=VerificationStatus.VERIFIED,
):
    return EvidenceLink(
        evidence_id=evidence_id,
        target_structure_id=target_id,
        source_ref=source_ref,
        relation_type=relation_type,
        verification_status=verification_status,
    )


def make_state(
    *targets,
    evidence_objects=(),
    links=(),
    grounding_threshold=0.70,
):
    target_values = list(targets) or [make_target()]
    return ArchitectureState(
        state_id="state-001",
        active_structures={
            target.structure_id: target
            for target in target_values
        },
        evidence_graph=EvidenceGraph(
            evidence_objects={
                evidence.evidence_id: evidence
                for evidence in evidence_objects
            },
            links=list(links),
        ),
        thresholds=ThresholdState(
            grounding_threshold=grounding_threshold,
        ),
    )


def make_context(*targets, state=None):
    target_values = list(targets) or [make_target()]
    architecture_state = state or make_state(*target_values)
    return ReviewContext(
        audit_id="audit-001",
        architecture_state=architecture_state,
        targets=target_values,
    )


def sequential_ids(*values):
    iterator = iter(values)
    return lambda: next(iterator)


def test_verified_support_creates_partial_grounding_assessment():
    target = make_target()
    evidence = make_evidence()
    state = make_state(
        target,
        evidence_objects=[evidence],
        links=[make_link()],
    )

    assessment = evaluate_grounding(target, state)

    assert assessment.grounding_score == 1.0
    assert assessment.epistemic_status is EpistemicStatus.PARTIALLY_GROUNDED
    assert assessment.supporting_evidence_ids == ("evidence-001",)
    assert assessment.threshold_check.threshold_name == "grounding_threshold"
    assert assessment.threshold_check.threshold_value == 0.70
    assert assessment.threshold_check.direction == "minimum_required"
    assert assessment.threshold_check.result


def test_unsupported_hypothesis_remains_speculative_and_is_delayed():
    target = make_target(structure_type=StructureType.HYPOTHESIS)
    context = make_context(target)

    run_gea_where_required(
        context,
        id_provider=lambda: "decision-gea-001",
    )

    decision = context.latest_grounding(target.structure_id)
    assert decision.decision_type is DecisionType.DELAY
    assert decision.status is DecisionStatus.PENDING_REVIEW
    assert decision.scores.grounding_score == 0.0
    assert EpistemicStatus.SPECULATIVE.value in decision.rationale
    assert "Verified supports=0" in decision.rationale


@pytest.mark.parametrize(
    "verification_status",
    [
        VerificationStatus.UNVERIFIED,
        VerificationStatus.FAILED,
    ],
)
def test_nonverified_support_does_not_increase_grounding(
    verification_status,
):
    target = make_target()
    evidence = make_evidence()
    state = make_state(
        target,
        evidence_objects=[evidence],
        links=[make_link(verification_status=verification_status)],
    )

    assessment = evaluate_grounding(target, state)

    assert assessment.grounding_score == 0.0
    assert assessment.epistemic_status is EpistemicStatus.UNGROUNDED
    assert assessment.supporting_evidence_ids == ()
    if verification_status is VerificationStatus.FAILED:
        assert assessment.failed_verification_ids == ("evidence-001",)
    else:
        assert assessment.unverified_evidence_ids == ("evidence-001",)


def test_evidential_rhetoric_without_links_has_no_grounding_authority():
    target = make_target(
        content="There is evidence because a study proves this claim."
    )
    context = make_context(target)

    run_gea_where_required(
        context,
        id_provider=lambda: "decision-gea-001",
    )

    decision = context.latest_grounding(target.structure_id)
    assert decision.scores.grounding_score == 0.0
    assert decision.decision_type is DecisionType.REVISE
    assert "evidential wording were not counted" in decision.rationale


def test_internal_coherence_does_not_count_as_external_evidence():
    target = make_target(
        content="This claim is internally coherent.",
        epistemic_status=EpistemicStatus.INTERNALLY_COHERENT,
        coherence_score=1.0,
    )
    context = make_context(target)

    run_gea_where_required(
        context,
        id_provider=lambda: "decision-gea-001",
    )

    decision = context.latest_grounding(target.structure_id)
    assert target.metadata.coherence_score == 1.0
    assert decision.scores.grounding_score == 0.0
    assert decision.decision_type is DecisionType.REVISE
    assert "Internal coherence" in decision.rationale


def test_verified_contradiction_remains_visible_and_rejects_unsupported_claim():
    target = make_target()
    evidence = make_evidence()
    state = make_state(
        target,
        evidence_objects=[evidence],
        links=[
            make_link(
                relation_type=EvidenceRelationType.CONTRADICTS,
            )
        ],
    )
    context = make_context(target, state=state)

    run_gea_where_required(
        context,
        id_provider=lambda: "decision-gea-001",
    )

    decision = context.latest_grounding(target.structure_id)
    assert decision.decision_type is DecisionType.REJECT
    assert decision.status is DecisionStatus.FINAL
    assert decision.scores.grounding_score == 0.0
    assert EpistemicStatus.CONTRADICTED.value in decision.rationale
    assert "verified contradictions=1" in decision.rationale


def test_mixed_verified_support_and_contradiction_is_contested_not_approved():
    target = make_target()
    supporting = make_evidence(
        evidence_id="evidence-support",
        source_ref="source://support",
    )
    contradicting = make_evidence(
        evidence_id="evidence-contradiction",
        source_ref="source://contradiction",
    )
    state = make_state(
        target,
        evidence_objects=[supporting, contradicting],
        links=[
            make_link(
                evidence_id="evidence-support",
                source_ref="source://support",
            ),
            make_link(
                evidence_id="evidence-contradiction",
                source_ref="source://contradiction",
                relation_type=EvidenceRelationType.CONTRADICTS,
            ),
        ],
        grounding_threshold=0.40,
    )
    context = make_context(target, state=state)

    assessment = evaluate_grounding(target, state)
    run_gea_where_required(
        context,
        id_provider=lambda: "decision-gea-001",
    )

    assert assessment.grounding_score == 0.5
    assert assessment.threshold_check.result
    assert assessment.epistemic_status is EpistemicStatus.CONTRADICTED
    decision = context.latest_grounding(target.structure_id)
    assert decision.decision_type is DecisionType.REVISE
    assert decision.status is DecisionStatus.PROVISIONAL


def test_verified_non_supporting_relation_does_not_increase_grounding():
    target = make_target()
    evidence = make_evidence()
    state = make_state(
        target,
        evidence_objects=[evidence],
        links=[
            make_link(
                relation_type=EvidenceRelationType.QUALIFIES,
            )
        ],
    )

    assessment = evaluate_grounding(target, state)

    assert assessment.grounding_score == 0.0
    assert assessment.supporting_evidence_ids == ()
    assert assessment.non_supporting_verified_ids == ("evidence-001",)


def test_invalid_typed_link_is_visible_but_cannot_establish_grounding():
    target = make_target()
    state = make_state(
        target,
        links=[make_link(evidence_id="evidence-missing")],
    )

    assessment = evaluate_grounding(target, state)

    assert assessment.grounding_score == 0.0
    assert assessment.invalid_evidence_ids == ("evidence-missing",)
    assert assessment.epistemic_status is EpistemicStatus.UNGROUNDED


def test_run_gea_appends_registered_decision_with_cycle_audit_id():
    target = make_target()
    evidence = make_evidence()
    state = make_state(
        target,
        evidence_objects=[evidence],
        links=[make_link()],
    )
    context = make_context(target, state=state)

    assert run_gea_where_required(
        context,
        id_provider=lambda: "decision-gea-001",
    ) is None

    decision = context.latest_grounding(target.structure_id)
    validation = state.algorithm_registry.validate_decision(decision, target)
    assert validation.accepted
    assert decision.decision_id == "decision-gea-001"
    assert decision.algorithm_name is AlgorithmName.GEA
    assert decision.decision_type is DecisionType.APPROVE_WITH_MONITORING
    assert decision.status is DecisionStatus.MONITORING
    assert decision.audit_id == "audit-001"
    assert not decision.authorized


def test_gea_does_not_mutate_state_evidence_or_authoritative_metadata():
    target = make_target()
    evidence = make_evidence()
    state = make_state(
        target,
        evidence_objects=[evidence],
        links=[make_link()],
    )
    context = make_context(target, state=state)
    state_before = state.to_dict()
    target_before = target.to_dict()

    run_gea_where_required(
        context,
        id_provider=lambda: "decision-gea-001",
    )

    assert state.to_dict() == state_before
    assert target.to_dict() == target_before
    assert target.metadata.epistemic_status is EpistemicStatus.UNKNOWN
    assert target.metadata.grounding_score == 0.0


def test_gea_skips_non_claim_targets_and_targets_already_reviewed():
    claim = make_target()
    observation = make_target(
        structure_id="structure-observation",
        structure_type=StructureType.OBSERVATION,
    )
    state = make_state(claim, observation)
    context = make_context(claim, observation, state=state)
    ids = sequential_ids("decision-gea-001")

    run_gea_where_required(context, id_provider=ids)
    run_gea_where_required(
        context,
        id_provider=lambda: pytest.fail("GEA reran completed review"),
    )

    assert len(context.decisions) == 1
    assert context.decisions[0].target_id == claim.structure_id
    assert (
        context.latest_grounding(observation.structure_id)
        is None
    )


def test_multi_target_review_preserves_target_order_and_deterministic_ids():
    first = make_target(structure_id="structure-001")
    second = make_target(
        structure_id="structure-002",
        structure_type=StructureType.HYPOTHESIS,
    )
    state = make_state(first, second)
    context = make_context(first, second, state=state)

    run_gea_where_required(
        context,
        id_provider=sequential_ids(
            "decision-gea-001",
            "decision-gea-002",
        ),
    )

    assert [
        (decision.decision_id, decision.target_id)
        for decision in context.decisions
    ] == [
        ("decision-gea-001", "structure-001"),
        ("decision-gea-002", "structure-002"),
    ]


def test_duplicate_decision_id_aborts_entire_gea_review_append():
    first = make_target(structure_id="structure-001")
    second = make_target(structure_id="structure-002")
    state = make_state(first, second)
    context = make_context(first, second, state=state)

    with pytest.raises(ReviewContextError, match="duplicate decision_id"):
        run_gea_where_required(
            context,
            id_provider=lambda: "decision-duplicate",
        )

    assert context.decisions == ()
    assert context.review_trace == ()


def test_evaluate_grounding_rejects_out_of_scope_structure_type():
    observation = make_target(
        structure_type=StructureType.OBSERVATION,
    )
    state = make_state(observation)

    with pytest.raises(
        GroundingEvaluationError,
        match="only claim and hypothesis",
    ):
        evaluate_grounding(observation, state)


def test_all_emitted_decision_types_are_within_registered_gea_authority():
    registry_types = set(
        ArchitectureState(
            state_id="state-registry",
        ).algorithm_registry.get_spec(
            AlgorithmName.GEA
        ).permitted_decision_types
    )

    assert {
        DecisionType.APPROVE_WITH_MONITORING,
        DecisionType.REVISE,
        DecisionType.DELAY,
        DecisionType.REJECT,
    }.issubset(registry_types)
