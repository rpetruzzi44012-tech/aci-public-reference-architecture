import pytest

from aci.algorithms.cra import (
    CoherenceEvaluationError,
    CoherenceRelation,
    NormalizedProposition,
    PropositionComparisonFixture,
    PropositionPolarity,
    compare_propositions,
    normalize_proposition_field,
    run_cra_where_required,
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
from aci.graphs import CoherenceGraph
from aci.review_context import ReviewContext, ReviewContextError
from aci.state import ArchitectureState, ThresholdState


def make_target(
    *,
    structure_id="structure-001",
    structure_type=StructureType.CLAIM,
    grounding_score=0.0,
    epistemic_status=EpistemicStatus.UNKNOWN,
):
    return SymbolicStructure(
        structure_id=structure_id,
        content="A proposition requiring structured comparison.",
        structure_type=structure_type,
        current_state=SymbolicState.CANDIDATE,
        metadata=SymbolicMetadata(
            origin="input-001",
            epistemic_status=epistemic_status,
            scale_label=ScaleLabel.CLAIM,
            candidate_status=CandidateStatus.NONE,
            authority_level=AuthorityLevel.NONE,
            grounding_score=grounding_score,
        ),
    )


def make_proposition(
    structure_id,
    *,
    subject="reactor",
    relation="is",
    object_value="online",
    polarity=PropositionPolarity.AFFIRMED,
):
    return NormalizedProposition(
        structure_id=structure_id,
        subject=subject,
        relation=relation,
        object_value=object_value,
        polarity=polarity,
    )


def make_fixture(
    *,
    comparison_id="comparison-001",
    target_id="structure-001",
    counterpart_id="structure-002",
    target_subject="reactor",
    target_relation="is",
    target_object="online",
    target_polarity=PropositionPolarity.AFFIRMED,
    counterpart_subject="reactor",
    counterpart_relation="is",
    counterpart_object="online",
    counterpart_polarity=PropositionPolarity.DENIED,
):
    return PropositionComparisonFixture(
        comparison_id=comparison_id,
        target=make_proposition(
            target_id,
            subject=target_subject,
            relation=target_relation,
            object_value=target_object,
            polarity=target_polarity,
        ),
        counterpart=make_proposition(
            counterpart_id,
            subject=counterpart_subject,
            relation=counterpart_relation,
            object_value=counterpart_object,
            polarity=counterpart_polarity,
        ),
    )


def make_state(
    *targets,
    coherence_threshold=0.30,
    unresolved_tensions=(),
):
    target_values = list(targets) or [
        make_target(),
        make_target(structure_id="structure-002"),
    ]
    return ArchitectureState(
        state_id="state-001",
        active_structures={
            target.structure_id: target
            for target in target_values
        },
        coherence_graph=CoherenceGraph(
            unresolved_tensions=list(unresolved_tensions),
        ),
        thresholds=ThresholdState(
            coherence_threshold=coherence_threshold,
        ),
    )


def make_context(*targets, state=None):
    target_values = list(targets) or [
        make_target(),
        make_target(structure_id="structure-002"),
    ]
    architecture_state = state or make_state(*target_values)
    return ReviewContext(
        audit_id="audit-001",
        architecture_state=architecture_state,
        targets=target_values,
    )


def sequential_ids(*values):
    iterator = iter(values)
    return lambda: next(iterator)


def make_grounding_decision(
    *,
    target_id="structure-001",
    grounding_score=0.80,
):
    return ReviewDecision(
        decision_id="decision-gea-001",
        algorithm_name=AlgorithmName.GEA,
        target_id=target_id,
        decision_type=DecisionType.APPROVE_WITH_MONITORING,
        status=DecisionStatus.MONITORING,
        scores=ScoreBundle(grounding_score=grounding_score),
        rationale="Prior typed grounding judgment.",
        authorized=False,
        audit_id="audit-001",
    )


def test_normalization_is_lexical_and_explicit():
    proposition = make_proposition(
        "structure-001",
        subject="  Reactor   CORE ",
        relation=" IS ",
        object_value="  OnLine ",
    )

    assert proposition.subject == "reactor core"
    assert proposition.relation == "is"
    assert proposition.object_value == "online"
    assert normalize_proposition_field("  A   B ") == "a b"


def test_direct_structured_polarity_contradiction_is_detected():
    state = make_state()

    assessment = compare_propositions(make_fixture(), state)

    assert assessment.relation is CoherenceRelation.DIRECT_CONTRADICTION
    assert assessment.coherence_score == 0.0
    assert assessment.coherence_pressure == 1.0
    assert assessment.threshold_check.threshold_name == "coherence_threshold"
    assert assessment.threshold_check.direction == "maximum_allowed"
    assert not assessment.threshold_check.result
    assert assessment.requires_tension_preservation


def test_identical_affirmed_propositions_are_compatible():
    state = make_state()
    fixture = make_fixture(
        counterpart_polarity=PropositionPolarity.AFFIRMED,
    )

    assessment = compare_propositions(fixture, state)

    assert assessment.relation is CoherenceRelation.COMPATIBLE
    assert assessment.coherence_score == 1.0
    assert assessment.coherence_pressure == 0.0
    assert assessment.threshold_check.result
    assert not assessment.requires_tension_preservation


def test_field_mismatch_remains_unresolved_instead_of_forcing_agreement():
    state = make_state()
    fixture = make_fixture(counterpart_object="standby")

    assessment = compare_propositions(fixture, state)

    assert assessment.relation is CoherenceRelation.UNRESOLVED
    assert assessment.coherence_score == 0.5
    assert assessment.coherence_pressure == 0.5
    assert assessment.requires_tension_preservation


def test_keyword_negation_is_not_treated_as_general_logical_analysis():
    state = make_state()
    fixture = make_fixture(
        target_object="open",
        counterpart_object="not open",
        counterpart_polarity=PropositionPolarity.AFFIRMED,
    )

    assessment = compare_propositions(fixture, state)

    assert assessment.relation is CoherenceRelation.UNRESOLVED
    assert assessment.relation is not CoherenceRelation.DIRECT_CONTRADICTION


def test_contradiction_appends_repair_decision_and_linked_unresolved_item():
    context = make_context()

    run_cra_where_required(
        context,
        [make_fixture()],
        decision_id_provider=lambda: "decision-cra-001",
        unresolved_id_provider=lambda: "unresolved-001",
    )

    decision = context.latest_coherence("structure-001")
    assert decision.decision_type is DecisionType.REPAIR
    assert decision.status is DecisionStatus.PROVISIONAL
    assert decision.audit_id == "audit-001"
    assert not decision.authorized
    assert CoherenceRelation.DIRECT_CONTRADICTION.value in decision.rationale
    assert context.unresolved_items[0].item_id == "unresolved-001"
    assert context.unresolved_items[0].decision_ref == decision.decision_id
    assert "authorized plan" in context.unresolved_items[0].reason


def test_compatible_comparison_is_monitored_without_inventing_tension():
    context = make_context()
    fixture = make_fixture(
        counterpart_polarity=PropositionPolarity.AFFIRMED,
    )

    run_cra_where_required(
        context,
        [fixture],
        decision_id_provider=lambda: "decision-cra-001",
        unresolved_id_provider=lambda: pytest.fail(
            "compatible comparison created unresolved tension"
        ),
    )

    decision = context.latest_coherence("structure-001")
    assert decision.decision_type is DecisionType.APPROVE_WITH_MONITORING
    assert decision.status is DecisionStatus.MONITORING
    assert decision.scores.coherence_score == 1.0
    assert context.unresolved_items == ()


def test_ambiguous_comparison_is_delayed_and_preserved_as_unresolved():
    context = make_context()
    fixture = make_fixture(counterpart_object="standby")

    run_cra_where_required(
        context,
        [fixture],
        decision_id_provider=lambda: "decision-cra-001",
        unresolved_id_provider=lambda: "unresolved-001",
    )

    decision = context.latest_coherence("structure-001")
    assert decision.decision_type is DecisionType.DELAY
    assert decision.status is DecisionStatus.PENDING_REVIEW
    assert CoherenceRelation.UNRESOLVED.value in decision.rationale
    assert len(context.unresolved_items) == 1


def test_threshold_passage_does_not_resolve_an_ambiguous_comparison():
    first = make_target()
    second = make_target(structure_id="structure-002")
    state = make_state(
        first,
        second,
        coherence_threshold=0.60,
    )
    fixture = make_fixture(counterpart_object="standby")
    assessment = compare_propositions(fixture, state)
    context = make_context(first, second, state=state)

    run_cra_where_required(
        context,
        [fixture],
        decision_id_provider=lambda: "decision-cra-001",
        unresolved_id_provider=lambda: "unresolved-001",
    )

    assert assessment.threshold_check.result
    assert (
        context.latest_coherence("structure-001").decision_type
        is DecisionType.DELAY
    )


def test_prior_grounding_decision_is_preserved_not_recomputed_or_increased():
    first = make_target(grounding_score=0.10)
    second = make_target(structure_id="structure-002")
    context = make_context(first, second)
    grounding = make_grounding_decision(grounding_score=0.80)
    context.append_decision(grounding)

    run_cra_where_required(
        context,
        [make_fixture()],
        decision_id_provider=lambda: "decision-cra-001",
        unresolved_id_provider=lambda: "unresolved-001",
    )

    coherence = context.latest_coherence("structure-001")
    assert coherence.scores.grounding_score == 0.80
    assert context.latest_grounding("structure-001") == grounding
    assert first.metadata.grounding_score == 0.10
    assert "preserved from GEA decision decision-gea-001" in (
        coherence.rationale
    )
    assert "granted no grounding" in coherence.rationale


def test_metadata_grounding_is_preserved_when_no_gea_decision_exists():
    first = make_target(
        grounding_score=0.65,
        epistemic_status=EpistemicStatus.PARTIALLY_GROUNDED,
    )
    second = make_target(structure_id="structure-002")
    context = make_context(first, second)

    run_cra_where_required(
        context,
        [make_fixture()],
        decision_id_provider=lambda: "decision-cra-001",
        unresolved_id_provider=lambda: "unresolved-001",
    )

    decision = context.latest_coherence("structure-001")
    assert decision.scores.grounding_score == 0.65
    assert first.metadata.epistemic_status is EpistemicStatus.PARTIALLY_GROUNDED


def test_cra_does_not_mutate_state_graphs_evidence_or_target_metadata():
    first = make_target()
    second = make_target(structure_id="structure-002")
    state = make_state(
        first,
        second,
        unresolved_tensions=["existing-tension"],
    )
    context = make_context(first, second, state=state)
    state_before = state.to_dict()
    first_before = first.to_dict()

    run_cra_where_required(
        context,
        [make_fixture()],
        decision_id_provider=lambda: "decision-cra-001",
        unresolved_id_provider=lambda: "unresolved-001",
    )

    assert state.to_dict() == state_before
    assert first.to_dict() == first_before
    assert state.coherence_graph.unresolved_tensions == ["existing-tension"]
    assert state.evidence_graph.evidence_objects == {}
    assert state.evidence_graph.links == []


def test_cra_decisions_are_accepted_by_the_active_registry():
    first = make_target()
    second = make_target(structure_id="structure-002")
    state = make_state(first, second)
    context = make_context(first, second, state=state)

    run_cra_where_required(
        context,
        [make_fixture()],
        decision_id_provider=lambda: "decision-cra-001",
        unresolved_id_provider=lambda: "unresolved-001",
    )

    decision = context.latest_coherence("structure-001")
    assert state.algorithm_registry.validate_decision(
        decision,
        first,
    ).accepted


def test_unknown_comparison_structure_aborts_without_partial_history():
    first = make_target()
    context = make_context(first)

    with pytest.raises(ReviewContextError, match="unknown target_id"):
        run_cra_where_required(
            context,
            [make_fixture(counterpart_id="structure-missing")],
            decision_id_provider=lambda: "decision-cra-001",
            unresolved_id_provider=lambda: "unresolved-001",
        )

    assert context.decisions == ()
    assert context.unresolved_items == ()


def test_registry_ineligible_target_type_is_rejected_before_append():
    first = make_target(structure_type=StructureType.GOVERNANCE_OBJECT)
    second = make_target(structure_id="structure-002")
    state = make_state(first, second)
    context = make_context(first, second, state=state)

    with pytest.raises(
        CoherenceEvaluationError,
        match="registry-invalid",
    ):
        run_cra_where_required(
            context,
            [make_fixture()],
            decision_id_provider=lambda: "decision-cra-001",
            unresolved_id_provider=lambda: "unresolved-001",
        )

    assert context.decisions == ()
    assert context.unresolved_items == ()


def test_duplicate_target_comparisons_are_rejected_as_ambiguous_routing():
    context = make_context()
    comparisons = [
        make_fixture(comparison_id="comparison-001"),
        make_fixture(comparison_id="comparison-002"),
    ]

    with pytest.raises(
        CoherenceEvaluationError,
        match="one CRA comparison per target",
    ):
        run_cra_where_required(context, comparisons)

    assert context.decisions == ()


def test_completed_cra_review_is_not_repeated():
    context = make_context()
    fixture = make_fixture()

    run_cra_where_required(
        context,
        [fixture],
        decision_id_provider=lambda: "decision-cra-001",
        unresolved_id_provider=lambda: "unresolved-001",
    )
    run_cra_where_required(
        context,
        [fixture],
        decision_id_provider=lambda: pytest.fail("CRA reran decision"),
        unresolved_id_provider=lambda: pytest.fail("CRA reran tension"),
    )

    assert len(context.decisions) == 1
    assert len(context.unresolved_items) == 1


def test_multiple_comparisons_preserve_order_and_deterministic_ids():
    targets = [
        make_target(structure_id="structure-001"),
        make_target(structure_id="structure-002"),
        make_target(structure_id="structure-003"),
        make_target(structure_id="structure-004"),
    ]
    state = make_state(*targets)
    context = make_context(*targets, state=state)
    comparisons = [
        make_fixture(
            comparison_id="comparison-001",
            target_id="structure-001",
            counterpart_id="structure-002",
        ),
        make_fixture(
            comparison_id="comparison-002",
            target_id="structure-003",
            counterpart_id="structure-004",
            counterpart_object="standby",
        ),
    ]

    run_cra_where_required(
        context,
        comparisons,
        decision_id_provider=sequential_ids(
            "decision-cra-001",
            "decision-cra-002",
        ),
        unresolved_id_provider=sequential_ids(
            "unresolved-001",
            "unresolved-002",
        ),
    )

    assert [
        (decision.decision_id, decision.target_id)
        for decision in context.decisions
    ] == [
        ("decision-cra-001", "structure-001"),
        ("decision-cra-002", "structure-003"),
    ]
    assert [
        item.item_id for item in context.unresolved_items
    ] == ["unresolved-001", "unresolved-002"]


def test_empty_comparison_set_is_a_no_op():
    context = make_context()

    assert run_cra_where_required(context) is None
    assert context.decisions == ()
    assert context.unresolved_items == ()


def test_fixture_requires_distinct_structures_and_typed_polarity():
    with pytest.raises(ValueError, match="distinct structure"):
        make_fixture(counterpart_id="structure-001")
    with pytest.raises(TypeError, match="polarity"):
        make_proposition("structure-001", polarity="denied")
