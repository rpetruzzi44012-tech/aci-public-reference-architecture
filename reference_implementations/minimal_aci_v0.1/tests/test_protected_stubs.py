import pytest

from aci.algorithms.stubs import (
    ProtectedStubError,
    StubReviewFixture,
    detect_architecture_candidate,
    detect_identity_risk_flags,
    detect_novelty_claim,
    evaluate_sra_stub,
    run_aea_stub_where_required,
    run_ipa_stub_where_required,
    run_ngsa_stub_where_required,
    run_sra_stub_where_required,
)
from aci.core import (
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
from aci.review_context import ReviewContext
from aci.state import ArchitectureState, BudgetState, clone_state


def make_target(
    *,
    structure_id="target-001",
    content="A bounded proposal under review.",
    structure_type=StructureType.HYPOTHESIS,
    candidate_status=CandidateStatus.NONE,
    scale_label=ScaleLabel.HYPOTHESIS,
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
            audit_refs=["audit-001"],
        ),
    )


def make_state(
    *targets,
    stability_budget=1.0,
    novelty_budget=1.0,
    attention_budget=1.0,
    unresolved_tensions=(),
    coherence_pressure=None,
):
    target_values = list(targets) or [make_target()]
    return ArchitectureState(
        state_id="state-001",
        active_structures={
            target.structure_id: target
            for target in target_values
        },
        budgets=BudgetState(
            stability_budget=stability_budget,
            novelty_budget=novelty_budget,
            attention_budget=attention_budget,
        ),
        coherence_graph=CoherenceGraph(
            unresolved_tensions=list(unresolved_tensions),
            coherence_pressure=coherence_pressure,
        ),
    )


def make_context(*targets, state=None):
    target_values = list(targets) or [make_target()]
    return ReviewContext(
        audit_id="audit-001",
        architecture_state=state or make_state(*target_values),
        targets=target_values,
    )


def test_transparent_detectors_do_not_grant_status():
    identity = make_target(
        content="This change creates identity continuity risk.",
        structure_type=StructureType.ARCHITECTURAL_CANDIDATE,
        candidate_status=CandidateStatus.ARCHITECTURE_CANDIDATE,
    )
    novelty = make_target(
        content="Explore a counterfactual candidate.",
        structure_type=StructureType.NOVELTY_CANDIDATE,
    )

    assert detect_identity_risk_flags(identity) == ("identity_risk",)
    assert detect_novelty_claim(novelty) is True
    assert detect_architecture_candidate(identity) is True
    assert identity.metadata.scale_label is ScaleLabel.HYPOTHESIS
    assert identity.metadata.authority_level is AuthorityLevel.NONE


def test_ipa_explicit_fixture_escalates_to_cga_as_registered_stub():
    target = make_target(
        structure_type=StructureType.ARCHITECTURAL_CANDIDATE,
        candidate_status=CandidateStatus.ARCHITECTURE_CANDIDATE,
    )
    context = make_context(target)
    run_ipa_stub_where_required(
        context,
        (
            StubReviewFixture(
                target_id=target.structure_id,
                identity_risk_flags=("identity_kernel_boundary",),
            ),
        ),
        id_provider=lambda: "decision-ipa-001",
    )

    decision = context.decisions[0]
    assert decision.algorithm_name is AlgorithmName.IPA
    assert decision.decision_type is DecisionType.ESCALATE
    assert decision.status is DecisionStatus.ESCALATED
    assert decision.escalation_target == AlgorithmName.CGA.value
    assert decision.authorized is False
    assert decision.scores.identity_risk_score == 1.0
    assert context.architecture_state.algorithm_registry.validate_decision(
        decision,
        target,
    ).accepted


def test_ipa_no_explicit_risk_appends_no_decision():
    target = make_target(
        structure_type=StructureType.ARCHITECTURAL_CANDIDATE,
    )
    context = make_context(target)

    run_ipa_stub_where_required(context)

    assert context.decisions == ()


def test_sra_available_capacity_and_no_overload_appends_no_decision():
    target = make_target(structure_type=StructureType.COHERENCE_TENSION)
    context = make_context(target)

    run_sra_stub_where_required(context)

    assert context.decisions == ()


def test_sra_reads_visible_thresholds_and_delays_moderate_tension_overload():
    target = make_target(structure_type=StructureType.COHERENCE_TENSION)
    state = make_state(
        target,
        unresolved_tensions=("tension-001",),
        coherence_pressure=0.4,
    )
    context = make_context(target, state=state)
    assessment = evaluate_sra_stub(context, target.structure_id)

    assert assessment.triggered is True
    assert assessment.signals == ("unresolved_tension_overload",)
    assert assessment.decision_type is DecisionType.DELAY
    checks = {
        check.threshold_name: check
        for check in assessment.threshold_checks
    }
    assert checks["coherence_threshold"].observed_value == 0.4
    assert checks["coherence_threshold"].threshold_value == 0.3
    assert checks["coherence_threshold"].result is False
    assert checks["escalation_threshold"].result is True

    run_sra_stub_where_required(
        context,
        id_provider=lambda: "decision-sra-delay",
    )
    decision = context.decisions[0]
    assert decision.decision_type is DecisionType.DELAY
    assert decision.status is DecisionStatus.PENDING_REVIEW
    assert decision.escalation_target is None


@pytest.mark.parametrize(
    ("budget_name", "budget_value", "expected_signal"),
    (
        ("stability_budget", 0.1, "stability_budget_below_threshold"),
        ("attention_budget", 0.1, "attention_budget_pressure"),
    ),
)
def test_sra_critical_budget_pressure_escalates(
    budget_name,
    budget_value,
    expected_signal,
):
    target = make_target(structure_type=StructureType.COHERENCE_TENSION)
    state_kwargs = {budget_name: budget_value}
    state = make_state(target, **state_kwargs)
    context = make_context(target, state=state)

    run_sra_stub_where_required(
        context,
        id_provider=lambda: f"decision-sra-{budget_name}",
    )

    decision = context.decisions[0]
    assert decision.decision_type is DecisionType.ESCALATE
    assert decision.status is DecisionStatus.ESCALATED
    assert decision.escalation_target == AlgorithmName.CGA.value
    assert expected_signal in decision.rationale
    assert context.architecture_state.algorithm_registry.validate_decision(
        decision,
        target,
    ).accepted


def test_ngsa_claim_recommends_sandbox_without_generating_novelty():
    target = make_target(
        content="Generate a novel hypothesis candidate.",
        structure_type=StructureType.NOVELTY_CANDIDATE,
    )
    state = make_state(
        target,
        stability_budget=0.2,
        novelty_budget=0.1,
    )
    context = make_context(target, state=state)
    before_targets = context.targets

    run_ngsa_stub_where_required(
        context,
        id_provider=lambda: "decision-ngsa-001",
    )

    decision = context.decisions[0]
    assert decision.algorithm_name is AlgorithmName.NGSA
    assert decision.decision_type is DecisionType.SANDBOX
    assert decision.status is DecisionStatus.PROVISIONAL
    assert decision.escalation_target is None
    assert decision.authorized is False
    assert "novelty:critical" in decision.rationale
    assert "stability:low" in decision.rationale
    assert context.targets == before_targets
    assert len(context.targets) == 1
    assert context.architecture_state.algorithm_registry.validate_decision(
        decision,
        target,
    ).accepted


def test_ngsa_no_novelty_claim_appends_no_decision():
    context = make_context()

    run_ngsa_stub_where_required(context)

    assert context.decisions == ()


def test_ngsa_structured_fixture_avoids_keyword_dependency():
    target = make_target(content="Consider this possibility.")
    context = make_context(target)

    run_ngsa_stub_where_required(
        context,
        (
            StubReviewFixture(
                target_id=target.structure_id,
                novelty_claim=True,
            ),
        ),
        id_provider=lambda: "decision-ngsa-fixture",
    )

    assert context.decisions[0].decision_type is DecisionType.SANDBOX


def test_aea_architecture_candidate_escalates_without_promotion():
    target = make_target(
        structure_type=StructureType.ARCHITECTURAL_CANDIDATE,
        candidate_status=CandidateStatus.ARCHITECTURE_CANDIDATE,
        scale_label=ScaleLabel.CLAIM,
    )
    context = make_context(target)

    run_aea_stub_where_required(
        context,
        id_provider=lambda: "decision-aea-001",
    )

    decision = context.decisions[0]
    assert decision.algorithm_name is AlgorithmName.AEA
    assert decision.decision_type is DecisionType.ESCALATE
    assert decision.status is DecisionStatus.ESCALATED
    assert decision.escalation_target == AlgorithmName.CGA.value
    assert decision.authorized is False
    assert context.get_target(
        target.structure_id
    ).metadata.scale_label is ScaleLabel.CLAIM
    assert context.architecture_state.algorithm_registry.validate_decision(
        decision,
        target,
    ).accepted


def test_aea_non_candidate_appends_no_decision():
    target = make_target(structure_type=StructureType.PERSISTENT_KNOWLEDGE)
    context = make_context(target)

    run_aea_stub_where_required(context)

    assert context.decisions == ()


@pytest.mark.parametrize(
    ("runner", "target", "fixture"),
    (
        (
            run_ipa_stub_where_required,
            make_target(
                structure_type=StructureType.ARCHITECTURAL_CANDIDATE,
            ),
            StubReviewFixture(
                target_id="target-001",
                identity_risk_flags=("identity_risk",),
            ),
        ),
        (
            run_ngsa_stub_where_required,
            make_target(structure_type=StructureType.NOVELTY_CANDIDATE),
            None,
        ),
        (
            run_aea_stub_where_required,
            make_target(
                structure_type=StructureType.ARCHITECTURAL_CANDIDATE,
            ),
            None,
        ),
    ),
)
def test_protected_stub_rationale_disclaims_full_review(
    runner,
    target,
    fixture,
):
    context = make_context(target)
    kwargs = {"id_provider": lambda: f"decision-{runner.__name__}"}
    if fixture is None:
        runner(context, **kwargs)
    else:
        runner(context, (fixture,), **kwargs)

    rationale = context.decisions[0].rationale
    assert "v0.1 stub" in rationale
    assert "has not performed full canonical review" in rationale
    assert "grants no mutation" in rationale


def test_sra_stub_rationale_disclaims_full_review():
    target = make_target(structure_type=StructureType.COHERENCE_TENSION)
    state = make_state(target, attention_budget=0.2)
    context = make_context(target, state=state)

    run_sra_stub_where_required(
        context,
        id_provider=lambda: "decision-sra-rationale",
    )

    rationale = context.decisions[0].rationale
    assert "v0.1 stub" in rationale
    assert "has not performed full canonical review" in rationale


@pytest.mark.parametrize(
    ("runner_name", "target", "state", "fixture"),
    (
        (
            "ipa",
            make_target(
                structure_type=StructureType.ARCHITECTURAL_CANDIDATE,
            ),
            None,
            StubReviewFixture(
                target_id="target-001",
                identity_risk_flags=("identity_risk",),
            ),
        ),
        (
            "sra",
            make_target(structure_type=StructureType.COHERENCE_TENSION),
            None,
            None,
        ),
        (
            "ngsa",
            make_target(structure_type=StructureType.NOVELTY_CANDIDATE),
            None,
            None,
        ),
        (
            "aea",
            make_target(
                structure_type=StructureType.ARCHITECTURAL_CANDIDATE,
            ),
            None,
            None,
        ),
    ),
)
def test_every_stub_preserves_authoritative_state(
    runner_name,
    target,
    state,
    fixture,
):
    authoritative = state or (
        make_state(target, stability_budget=0.1)
        if runner_name == "sra"
        else make_state(target)
    )
    before = clone_state(authoritative)
    context = make_context(target, state=authoritative)
    ids = lambda: f"decision-{runner_name}-isolation"

    if runner_name == "ipa":
        run_ipa_stub_where_required(
            context,
            (fixture,),
            id_provider=ids,
        )
    elif runner_name == "sra":
        run_sra_stub_where_required(context, id_provider=ids)
    elif runner_name == "ngsa":
        run_ngsa_stub_where_required(context, id_provider=ids)
    else:
        run_aea_stub_where_required(context, id_provider=ids)

    assert authoritative == before


def test_sra_runner_ignores_targets_outside_registered_jurisdiction():
    target = make_target(
        structure_type=StructureType.CLAIM,
        scale_label=ScaleLabel.CLAIM,
    )
    state = make_state(target, stability_budget=0.1)
    context = make_context(target, state=state)

    run_sra_stub_where_required(context)

    assert context.decisions == ()
    assert context.review_trace == ()


def test_registry_rejection_rolls_back_excessive_scale_decision():
    target = make_target(
        structure_type=StructureType.ARCHITECTURAL_CANDIDATE,
        candidate_status=CandidateStatus.ARCHITECTURE_CANDIDATE,
        scale_label=ScaleLabel.CONSTITUTIONAL,
    )
    context = make_context(target)

    with pytest.raises(
        ProtectedStubError,
        match="target_scale_exceeds_authority",
    ):
        run_aea_stub_where_required(
            context,
            id_provider=lambda: "decision-invalid-aea",
        )

    assert context.decisions == ()
    assert context.review_trace == ()


def test_stub_decisions_are_not_repeated_for_same_target():
    target = make_target(structure_type=StructureType.NOVELTY_CANDIDATE)
    context = make_context(target)
    identifiers = iter(("decision-ngsa-001", "decision-ngsa-002"))

    run_ngsa_stub_where_required(
        context,
        id_provider=lambda: next(identifiers),
    )
    run_ngsa_stub_where_required(
        context,
        id_provider=lambda: next(identifiers),
    )

    assert len(context.decisions) == 1
