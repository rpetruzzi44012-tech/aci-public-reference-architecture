import pytest

from aci.algorithms.mssa import (
    CANDIDATE_REQUESTED_SCALES,
    ScaleAlignmentOutcome,
    ScaleEvaluationError,
    ScaleJumpDirection,
    evaluate_scale_alignment,
    requested_scale_for_candidate,
    run_mssa_where_required,
)
from aci.core import ScoreBundle, SymbolicMetadata, SymbolicStructure
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
from aci.graphs import ScaleGraph
from aci.review_context import ReviewContext
from aci.state import ArchitectureState, ThresholdState, clone_state


def structure_type_for_scale(scale_label):
    return {
        ScaleLabel.OBSERVATION: StructureType.OBSERVATION,
        ScaleLabel.CLAIM: StructureType.CLAIM,
        ScaleLabel.HYPOTHESIS: StructureType.HYPOTHESIS,
        ScaleLabel.MEMORY: StructureType.PERSISTENT_KNOWLEDGE,
        ScaleLabel.PRINCIPLE: StructureType.PERSISTENT_KNOWLEDGE,
        ScaleLabel.ARCHITECTURE: StructureType.ARCHITECTURAL_CANDIDATE,
        ScaleLabel.CONSTITUTIONAL: StructureType.CONSTITUTIONAL_OBJECT,
    }[scale_label]


def make_target(
    *,
    structure_id="structure-001",
    scale_label=ScaleLabel.CLAIM,
    candidate_status=CandidateStatus.ARCHITECTURE_CANDIDATE,
    epistemic_status=EpistemicStatus.UNKNOWN,
    structure_type=None,
):
    return SymbolicStructure(
        structure_id=structure_id,
        content="A structure requesting explicit scale review.",
        structure_type=(
            structure_type
            if structure_type is not None
            else structure_type_for_scale(scale_label)
        ),
        current_state=SymbolicState.CANDIDATE,
        metadata=SymbolicMetadata(
            origin="input-001",
            epistemic_status=epistemic_status,
            scale_label=scale_label,
            candidate_status=candidate_status,
            authority_level=AuthorityLevel.NONE,
            audit_refs=["audit-001"],
        ),
    )


def make_state(*targets, multi_scale_threshold=0.75):
    target_values = list(targets) or [make_target()]
    return ArchitectureState(
        state_id="state-001",
        active_structures={
            target.structure_id: target
            for target in target_values
        },
        scale_graph=ScaleGraph(
            scale_labels={
                target.structure_id: target.metadata.scale_label
                for target in target_values
            },
            mismatch_records=[
                {
                    "record_id": "existing-mismatch",
                    "status": "preserved",
                }
            ],
        ),
        thresholds=ThresholdState(
            multi_scale_threshold=multi_scale_threshold,
        ),
    )


def make_context(*targets, state=None):
    target_values = list(targets) or [make_target()]
    return ReviewContext(
        audit_id="audit-001",
        architecture_state=state or make_state(*target_values),
        targets=target_values,
    )


def test_candidate_mapping_is_complete_and_distinct_from_achieved_scale():
    assert dict(CANDIDATE_REQUESTED_SCALES) == {
        CandidateStatus.NONE: None,
        CandidateStatus.PERSISTENCE_CANDIDATE: ScaleLabel.MEMORY,
        CandidateStatus.PRINCIPLE_CANDIDATE: ScaleLabel.PRINCIPLE,
        CandidateStatus.ARCHITECTURE_CANDIDATE: ScaleLabel.ARCHITECTURE,
        CandidateStatus.CONSTITUTIONAL_CANDIDATE:
            ScaleLabel.CONSTITUTIONAL,
    }
    assert requested_scale_for_candidate(
        CandidateStatus.ARCHITECTURE_CANDIDATE
    ) is ScaleLabel.ARCHITECTURE


def test_no_candidate_is_a_legitimate_no_jump_and_is_not_run():
    target = make_target(candidate_status=CandidateStatus.NONE)
    state = make_state(target)
    context = make_context(target, state=state)

    assessment = evaluate_scale_alignment(target, state)
    run_mssa_where_required(
        context,
        id_provider=lambda: pytest.fail(
            "MSSA should skip targets without scale candidacy"
        ),
    )

    assert assessment.outcome is ScaleAlignmentOutcome.ALIGNED
    assert assessment.requested_scale is None
    assert assessment.direction is ScaleJumpDirection.NONE
    assert assessment.multi_scale_coherence_score == 1.0
    assert context.latest_scale(target.structure_id) is None


@pytest.mark.parametrize(
    ("scale_label", "candidate_status"),
    [
        (ScaleLabel.MEMORY, CandidateStatus.PERSISTENCE_CANDIDATE),
        (ScaleLabel.PRINCIPLE, CandidateStatus.PRINCIPLE_CANDIDATE),
        (ScaleLabel.ARCHITECTURE, CandidateStatus.ARCHITECTURE_CANDIDATE),
        (
            ScaleLabel.CONSTITUTIONAL,
            CandidateStatus.CONSTITUTIONAL_CANDIDATE,
        ),
    ],
)
def test_aligned_candidacy_is_monitored_without_promotion(
    scale_label,
    candidate_status,
):
    target = make_target(
        scale_label=scale_label,
        candidate_status=candidate_status,
    )
    context = make_context(target)

    run_mssa_where_required(
        context,
        id_provider=lambda: "decision-mssa-001",
    )

    decision = context.latest_scale(target.structure_id)
    assert decision.decision_type is DecisionType.APPROVE_WITH_MONITORING
    assert decision.status is DecisionStatus.MONITORING
    assert not decision.authorized
    assert target.metadata.scale_label is scale_label
    assert target.metadata.candidate_status is candidate_status


@pytest.mark.parametrize(
    "epistemic_status",
    [
        EpistemicStatus.UNKNOWN,
        EpistemicStatus.PARTIALLY_GROUNDED,
        EpistemicStatus.STRONGLY_GROUNDED,
    ],
)
def test_claim_or_grounded_claim_to_architecture_escalates_not_promotes(
    epistemic_status,
):
    target = make_target(
        scale_label=ScaleLabel.CLAIM,
        candidate_status=CandidateStatus.ARCHITECTURE_CANDIDATE,
        epistemic_status=epistemic_status,
    )
    context = make_context(target)

    run_mssa_where_required(
        context,
        id_provider=lambda: "decision-mssa-001",
    )

    decision = context.latest_scale(target.structure_id)
    assert decision.decision_type is DecisionType.ESCALATE
    assert decision.status is DecisionStatus.ESCALATED
    assert decision.escalation_target == AlgorithmName.AEA.value
    assert not decision.authorized
    assert target.metadata.scale_label is ScaleLabel.CLAIM
    assert "grants no approval" in decision.rationale


def test_memory_to_principle_is_delayed_even_when_threshold_passes():
    target = make_target(
        scale_label=ScaleLabel.MEMORY,
        candidate_status=CandidateStatus.PRINCIPLE_CANDIDATE,
    )
    state = make_state(target)
    context = make_context(target, state=state)

    assessment = evaluate_scale_alignment(target, state)
    run_mssa_where_required(
        context,
        id_provider=lambda: "decision-mssa-001",
    )

    assert assessment.direction is ScaleJumpDirection.UPWARD
    assert assessment.distance == 1
    assert assessment.threshold_check.result
    decision = context.latest_scale(target.structure_id)
    assert decision.decision_type is DecisionType.DELAY
    assert decision.status is DecisionStatus.BLOCKED
    assert decision.decision_type is not DecisionType.PROMOTE_CANDIDATE


def test_memory_to_constitution_is_rejected_as_layer_bypass():
    target = make_target(
        scale_label=ScaleLabel.MEMORY,
        candidate_status=CandidateStatus.CONSTITUTIONAL_CANDIDATE,
    )
    context = make_context(target)

    run_mssa_where_required(
        context,
        id_provider=lambda: "decision-mssa-001",
    )

    decision = context.latest_scale(target.structure_id)
    assert decision.decision_type is DecisionType.REJECT
    assert decision.status is DecisionStatus.FINAL
    assert decision.escalation_target is None
    assert "bypasses required intermediate review" in decision.rationale


def test_principle_to_architecture_escalates_to_aea():
    target = make_target(
        scale_label=ScaleLabel.PRINCIPLE,
        candidate_status=CandidateStatus.ARCHITECTURE_CANDIDATE,
    )
    context = make_context(target)

    run_mssa_where_required(
        context,
        id_provider=lambda: "decision-mssa-001",
    )

    decision = context.latest_scale(target.structure_id)
    assert decision.decision_type is DecisionType.ESCALATE
    assert decision.status is DecisionStatus.ESCALATED
    assert decision.escalation_target == AlgorithmName.AEA.value


def test_architecture_to_constitution_escalates_to_cga():
    target = make_target(
        scale_label=ScaleLabel.ARCHITECTURE,
        candidate_status=CandidateStatus.CONSTITUTIONAL_CANDIDATE,
    )
    context = make_context(target)

    run_mssa_where_required(
        context,
        id_provider=lambda: "decision-mssa-001",
    )

    decision = context.latest_scale(target.structure_id)
    assert decision.decision_type is DecisionType.ESCALATE
    assert decision.status is DecisionStatus.ESCALATED
    assert decision.escalation_target == AlgorithmName.CGA.value
    assert context.has_blocking_decision(target.structure_id)


def test_ordinary_claim_to_memory_request_is_delayed_without_promotion():
    target = make_target(
        scale_label=ScaleLabel.CLAIM,
        candidate_status=CandidateStatus.PERSISTENCE_CANDIDATE,
    )
    context = make_context(target)

    run_mssa_where_required(
        context,
        id_provider=lambda: "decision-mssa-001",
    )

    decision = context.latest_scale(target.structure_id)
    assert decision.decision_type is DecisionType.DELAY
    assert decision.status is DecisionStatus.BLOCKED
    assert target.metadata.scale_label is ScaleLabel.CLAIM


def test_downward_mismatch_recommends_demotion_not_relabeling():
    target = make_target(
        scale_label=ScaleLabel.ARCHITECTURE,
        candidate_status=CandidateStatus.PRINCIPLE_CANDIDATE,
    )
    context = make_context(target)

    assessment = evaluate_scale_alignment(
        target,
        context.architecture_state,
    )
    run_mssa_where_required(
        context,
        id_provider=lambda: "decision-mssa-001",
    )

    assert assessment.direction is ScaleJumpDirection.DOWNWARD
    decision = context.latest_scale(target.structure_id)
    assert decision.decision_type is DecisionType.DEMOTE
    assert decision.status is DecisionStatus.PROVISIONAL
    assert target.metadata.scale_label is ScaleLabel.ARCHITECTURE


def test_escalation_is_pending_authority_transfer_not_approval():
    target = make_target(
        scale_label=ScaleLabel.PRINCIPLE,
        candidate_status=CandidateStatus.ARCHITECTURE_CANDIDATE,
    )
    context = make_context(target)

    run_mssa_where_required(
        context,
        id_provider=lambda: "decision-mssa-001",
    )

    decision = context.latest_scale(target.structure_id)
    assert decision.status is DecisionStatus.ESCALATED
    assert not decision.authorized
    assert context.has_blocking_decision(target.structure_id)
    assert decision.decision_type not in {
        DecisionType.APPROVE,
        DecisionType.APPROVE_WITH_MONITORING,
        DecisionType.PROMOTE_CANDIDATE,
    }


def test_named_multi_scale_score_and_threshold_remain_visible():
    target = make_target(
        scale_label=ScaleLabel.ARCHITECTURE,
        candidate_status=CandidateStatus.CONSTITUTIONAL_CANDIDATE,
    )
    state = make_state(target, multi_scale_threshold=0.90)
    context = make_context(target, state=state)
    assessment = evaluate_scale_alignment(target, state)

    run_mssa_where_required(
        context,
        id_provider=lambda: "decision-mssa-001",
    )

    assert assessment.multi_scale_coherence_score == pytest.approx(5 / 6)
    assert assessment.threshold_check.threshold_name == (
        "multi_scale_threshold"
    )
    assert assessment.threshold_check.direction == "minimum_required"
    assert assessment.threshold_check.threshold_value == 0.90
    assert not assessment.threshold_check.result
    decision = context.latest_scale(target.structure_id)
    assert decision.scores.multi_scale_coherence_score == pytest.approx(5 / 6)
    assert context.latest_score(
        target.structure_id,
        AlgorithmName.MSSA,
        "multi_scale_coherence_score",
    ) == pytest.approx(5 / 6)
    assert decision.decision_type is DecisionType.ESCALATE


def test_mssa_decisions_are_registry_valid():
    targets = [
        make_target(
            structure_id="aligned",
            scale_label=ScaleLabel.MEMORY,
            candidate_status=CandidateStatus.PERSISTENCE_CANDIDATE,
        ),
        make_target(
            structure_id="delayed",
            scale_label=ScaleLabel.MEMORY,
            candidate_status=CandidateStatus.PRINCIPLE_CANDIDATE,
        ),
        make_target(
            structure_id="rejected",
            scale_label=ScaleLabel.MEMORY,
            candidate_status=CandidateStatus.CONSTITUTIONAL_CANDIDATE,
        ),
        make_target(
            structure_id="escalated",
            scale_label=ScaleLabel.PRINCIPLE,
            candidate_status=CandidateStatus.ARCHITECTURE_CANDIDATE,
        ),
    ]
    context = make_context(*targets)
    identifiers = iter(
        [
            "decision-mssa-aligned",
            "decision-mssa-delayed",
            "decision-mssa-rejected",
            "decision-mssa-escalated",
        ]
    )

    run_mssa_where_required(context, id_provider=lambda: next(identifiers))

    state_view = context.architecture_state
    for target in targets:
        decision = context.latest_scale(target.structure_id)
        validation = state_view.algorithm_registry.validate_decision(
            decision,
            context.get_target(target.structure_id),
        )
        assert validation.accepted


def test_mssa_does_not_mutate_state_metadata_or_scale_graph():
    target = make_target(
        scale_label=ScaleLabel.PRINCIPLE,
        candidate_status=CandidateStatus.ARCHITECTURE_CANDIDATE,
    )
    state = make_state(target)
    baseline = clone_state(state)
    target_before = target.to_dict()
    context = make_context(target, state=state)
    review_state_before = context.architecture_state

    run_mssa_where_required(
        context,
        id_provider=lambda: "decision-mssa-001",
    )

    assert state == baseline
    assert target.to_dict() == target_before
    assert context.architecture_state == review_state_before
    assert state.scale_graph.scale_labels[target.structure_id] is (
        ScaleLabel.PRINCIPLE
    )
    assert state.scale_graph.mismatch_records == [
        {
            "record_id": "existing-mismatch",
            "status": "preserved",
        }
    ]


def test_deterministic_id_and_cycle_audit_are_preserved():
    context = make_context()

    run_mssa_where_required(
        context,
        id_provider=lambda: "decision-mssa-deterministic",
    )

    decision = context.latest_scale("structure-001")
    assert decision.decision_id == "decision-mssa-deterministic"
    assert decision.audit_id == "audit-001"


def test_duplicate_mssa_id_rolls_back_all_new_decisions():
    first = make_target(structure_id="structure-001")
    second = make_target(structure_id="structure-002")
    context = make_context(first, second)

    with pytest.raises(ValueError, match="duplicate decision_id"):
        run_mssa_where_required(
            context,
            id_provider=lambda: "decision-mssa-duplicate",
        )

    assert context.decisions == ()
    assert context.latest_scale(first.structure_id) is None
    assert context.latest_scale(second.structure_id) is None


def test_registry_invalid_target_type_fails_visibly_and_atomically():
    target = make_target(
        scale_label=ScaleLabel.OBSERVATION,
        candidate_status=CandidateStatus.ARCHITECTURE_CANDIDATE,
        structure_type=StructureType.OBSERVATION,
    )
    context = make_context(target)

    with pytest.raises(
        ScaleEvaluationError,
        match="target_type_not_permitted",
    ):
        run_mssa_where_required(
            context,
            id_provider=lambda: "decision-mssa-001",
        )

    assert context.decisions == ()


def test_multi_scale_score_validation_is_normalized():
    with pytest.raises(
        ValueError,
        match="multi_scale_coherence_score must be in",
    ):
        ScoreBundle(multi_scale_coherence_score=1.1)
