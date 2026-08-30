import pytest

from aci.algorithms.cga import (
    GovernanceClaimKind,
    GovernanceReviewFixture,
    detect_governance_claims,
    evaluate_governance,
    run_cga_where_required,
)
from aci.core import (
    EscalationEvent,
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
    EscalationUrgency,
    GovernanceMode,
    ScaleLabel,
    StructureType,
    SymbolicState,
)
from aci.graphs import AuthorityGraph
from aci.registry import RegistryChangeRequest
from aci.review_context import ReviewContext
from aci.state import ArchitectureState, GovernanceState, clone_state


def make_target(
    *,
    structure_id="governance-001",
    content="A governance proposal requiring legitimacy review.",
    structure_type=StructureType.GOVERNANCE_OBJECT,
    scale_label=ScaleLabel.CLAIM,
    candidate_status=CandidateStatus.NONE,
    authority_level=AuthorityLevel.NONE,
    epistemic_status=EpistemicStatus.UNKNOWN,
):
    return SymbolicStructure(
        structure_id=structure_id,
        content=content,
        structure_type=structure_type,
        current_state=SymbolicState.GOVERNANCE_REVIEW,
        metadata=SymbolicMetadata(
            origin="input-001",
            epistemic_status=epistemic_status,
            scale_label=scale_label,
            candidate_status=candidate_status,
            authority_level=authority_level,
            audit_refs=["audit-001"],
        ),
    )


def make_veto(
    *,
    veto_id="veto-001",
    target_id="governance-001",
    issuing_domain="verification",
    reason="Verification independence requires review.",
    protected=True,
    audit_ref="audit-veto-001",
):
    return {
        "veto_id": veto_id,
        "target_id": target_id,
        "issuing_domain": issuing_domain,
        "reason": reason,
        "protected": protected,
        "audit_ref": audit_ref,
    }


def make_escalation(
    *,
    escalation_id="escalation-001",
    target_id="governance-001",
    from_algorithm=AlgorithmName.MSSA,
    reason="Constitutional authority remains unresolved.",
    resolved=False,
):
    return EscalationEvent(
        escalation_id=escalation_id,
        target_id=target_id,
        reason=reason,
        urgency=EscalationUrgency.HIGH,
        decision_ref="decision-source-001",
        from_algorithm=from_algorithm,
        to_algorithm=AlgorithmName.CGA,
        resolved=resolved,
        audit_ref="audit-001",
    )


def make_state(
    *targets,
    governance_mode=GovernanceMode.NORMAL,
    authority_edges=(),
    veto_rules=(),
    escalation_rules=(),
    active_vetoes=(),
    pending_escalations=(),
):
    target_values = list(targets) or [make_target()]
    return ArchitectureState(
        state_id="state-001",
        active_structures={
            target.structure_id: target
            for target in target_values
        },
        governance_state=GovernanceState(
            governance_mode=governance_mode,
            authority_graph=AuthorityGraph(
                domains=["architecture", "constitutional", "verification"],
                authority_edges=list(authority_edges),
                veto_rules=list(veto_rules),
                escalation_rules=list(escalation_rules),
            ),
            active_vetoes=list(active_vetoes),
            pending_escalations=list(pending_escalations),
            governance_memory=[
                {
                    "precedent_id": "precedent-001",
                    "status": "preserved",
                }
            ],
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
    target_id="governance-001",
    decision_type=DecisionType.ESCALATE,
    status=DecisionStatus.ESCALATED,
    escalation_target=AlgorithmName.CGA,
    suffix="001",
):
    return ReviewDecision(
        decision_id=f"decision-{algorithm_name.name.lower()}-{suffix}",
        algorithm_name=algorithm_name,
        target_id=target_id,
        decision_type=decision_type,
        status=status,
        scores=ScoreBundle(),
        rationale="Prior algorithm judgment requiring governance review.",
        authorized=False,
        escalation_target=(
            escalation_target.value
            if escalation_target is not None
            else None
        ),
        audit_id="audit-001",
    )


def test_transparent_governance_claim_detection_preserves_basis_types():
    target = make_target(
        content=(
            "This useful, popular, coherent idea appears repeatedly in the "
            "corpus and should govern the output policy."
        )
    )

    claims = detect_governance_claims(target)

    assert GovernanceClaimKind.GENERAL in claims
    assert GovernanceClaimKind.UTILITY in claims
    assert GovernanceClaimKind.POPULARITY in claims
    assert GovernanceClaimKind.REPETITION in claims
    assert GovernanceClaimKind.COHERENCE in claims
    assert GovernanceClaimKind.OUTPUT_RULE_CHANGE in claims


def test_useful_governance_proposal_gets_caution_not_legitimacy():
    target = make_target(
        content="This useful and efficient proposal should govern the process."
    )
    context = make_context(target)

    assessment = evaluate_governance(context, target.structure_id)
    run_cga_where_required(
        context,
        id_provider=lambda: "decision-cga-001",
    )

    assert assessment.legitimacy_score == 0.0
    assert not assessment.legitimacy_check.result
    assert assessment.recommended_mode is GovernanceMode.CAUTION
    assert not assessment.output_block_recommended
    decision = context.latest_by_algorithm(target.structure_id, AlgorithmName.CGA)
    assert decision.decision_type is DecisionType.DELAY
    assert decision.status is DecisionStatus.PENDING_REVIEW
    assert not decision.authorized
    assert not decision.output_block_recommended


def test_popularity_repetition_and_coherence_add_no_legitimacy():
    target = make_target(
        content=(
            "This popular and coherent corpus idea has been repeated many "
            "times, so it should govern."
        )
    )
    context = make_context(target)

    assessment = evaluate_governance(context, target.structure_id)

    assert {
        GovernanceClaimKind.POPULARITY,
        GovernanceClaimKind.REPETITION,
        GovernanceClaimKind.COHERENCE,
    }.issubset(assessment.claim_kinds)
    assert assessment.legitimacy_score == 0.0
    assert assessment.recommended_mode is GovernanceMode.CAUTION


def test_architecture_to_constitution_request_consumes_mssa_escalation():
    target = make_target(
        structure_type=StructureType.ARCHITECTURAL_CANDIDATE,
        scale_label=ScaleLabel.ARCHITECTURE,
        candidate_status=CandidateStatus.CONSTITUTIONAL_CANDIDATE,
        content="Make this successful architecture constitutional.",
    )
    context = make_context(target)
    mssa = make_prior_decision(AlgorithmName.MSSA)
    context.append_decision(mssa)

    assessment = evaluate_governance(context, target.structure_id)
    run_cga_where_required(
        context,
        id_provider=lambda: "decision-cga-001",
    )

    assert mssa.decision_id in assessment.pending_escalation_refs
    assert assessment.unauthorized_authority_elevation
    assert assessment.legitimacy_score == 0.0
    assert assessment.recommended_mode is GovernanceMode.CONSTITUTIONAL_RISK
    decision = context.latest_by_algorithm(target.structure_id, AlgorithmName.CGA)
    assert decision.status is DecisionStatus.BLOCKED
    assert decision.recommended_governance_mode is (
        GovernanceMode.CONSTITUTIONAL_RISK
    )
    assert decision.escalation_target is None


def test_successful_architecture_and_aea_stub_do_not_create_authority():
    target = make_target(
        structure_type=StructureType.ARCHITECTURAL_CANDIDATE,
        scale_label=ScaleLabel.ARCHITECTURE,
        candidate_status=CandidateStatus.CONSTITUTIONAL_CANDIDATE,
        content=(
            "The architecture succeeded and worked, so grant it "
            "constitutional authority."
        ),
    )
    context = make_context(target)
    context.append_decision(
        make_prior_decision(
            AlgorithmName.AEA,
            decision_type=DecisionType.SANDBOX,
            status=DecisionStatus.PROVISIONAL,
            escalation_target=None,
        )
    )

    assessment = evaluate_governance(context, target.structure_id)

    assert GovernanceClaimKind.ARCHITECTURAL_SUCCESS in assessment.claim_kinds
    assert assessment.legitimacy_score == 0.0
    assert assessment.unauthorized_authority_elevation
    assert assessment.output_block_recommended


def test_unauthorized_algorithm_authority_change_enters_amendment_review():
    target = make_target()
    context = make_context(target)
    request = RegistryChangeRequest(
        request_id="registry-change-001",
        proposer_algorithm=AlgorithmName.GEA,
        target_algorithm=AlgorithmName.GEA,
        change_kind="authority",
        reason="Give GEA constitutional authority.",
        audit_ref="audit-001",
    )
    fixture = GovernanceReviewFixture(
        target_id=target.structure_id,
        claim_kinds=(GovernanceClaimKind.REGISTRY_CHANGE,),
        registry_change_request=request,
    )

    assessment = evaluate_governance(
        context,
        target.structure_id,
        fixture=fixture,
    )
    run_cga_where_required(
        context,
        [fixture],
        id_provider=lambda: "decision-cga-001",
    )

    assert "self_modification_prohibited" in assessment.registry_issue_codes
    assert (
        "protected_algorithm_change_requires_governance"
        in assessment.registry_issue_codes
    )
    assert assessment.protected_change_requested
    assert assessment.recommended_mode is GovernanceMode.AMENDMENT_REVIEW
    decision = context.latest_by_algorithm(target.structure_id, AlgorithmName.CGA)
    assert decision.decision_type is DecisionType.AMENDMENT_REVIEW
    assert decision.status is DecisionStatus.PENDING_REVIEW
    assert decision.output_block_recommended


def test_protected_output_rule_change_enters_amendment_and_blocks_output():
    target = make_target(content="Change the protected output rule.")
    context = make_context(target)

    assessment = evaluate_governance(context, target.structure_id)
    run_cga_where_required(
        context,
        id_provider=lambda: "decision-cga-001",
    )

    assert assessment.protected_change_requested
    assert assessment.recommended_mode is GovernanceMode.AMENDMENT_REVIEW
    assert assessment.output_block_recommended
    decision = context.latest_by_algorithm(target.structure_id, AlgorithmName.CGA)
    assert decision.decision_type is DecisionType.AMENDMENT_REVIEW


def test_scoped_audited_active_veto_is_visible_and_blocks_output():
    target = make_target()
    state = make_state(target, active_vetoes=[make_veto()])
    context = make_context(target, state=state)

    assessment = evaluate_governance(context, target.structure_id)

    assert len(assessment.veto_findings) == 1
    finding = assessment.veto_findings[0]
    assert finding.veto_id == "veto-001"
    assert finding.target_scope == target.structure_id
    assert finding.issuing_domain == "verification"
    assert finding.reviewable
    assert assessment.recommended_mode is GovernanceMode.CONSTITUTIONAL_RISK
    assert assessment.output_block_recommended


def test_unscoped_unaudited_active_veto_is_exposed_as_governance_risk():
    target = make_target()
    malformed_veto = {
        "veto_id": "veto-malformed",
        "issuing_domain": "unknown",
        "reason": "Hidden veto.",
        "protected": True,
    }
    state = make_state(target, active_vetoes=[malformed_veto])
    context = make_context(target, state=state)

    assessment = evaluate_governance(context, target.structure_id)

    finding = assessment.veto_findings[0]
    assert not finding.scoped
    assert not finding.auditable
    assert not finding.reviewable
    assert "an active veto is unscoped or unauditable" in assessment.reasons
    assert assessment.output_block_recommended


def test_veto_scoped_to_another_target_does_not_block_this_proposal():
    target = make_target(content="A useful governance proposal.")
    state = make_state(
        target,
        active_vetoes=[make_veto(target_id="governance-other")],
    )
    context = make_context(target, state=state)

    assessment = evaluate_governance(context, target.structure_id)

    assert assessment.veto_findings == ()
    assert assessment.recommended_mode is GovernanceMode.CAUTION
    assert not assessment.output_block_recommended


def test_pending_state_escalation_is_consumed_but_not_approved():
    target = make_target()
    escalation = make_escalation()
    state = make_state(target, pending_escalations=[escalation])
    context = make_context(target, state=state)

    assessment = evaluate_governance(context, target.structure_id)

    assert assessment.pending_escalation_refs == ("escalation-001",)
    assert assessment.recommended_mode is GovernanceMode.CONSTITUTIONAL_RISK
    assert assessment.output_block_recommended
    assert assessment.legitimacy_score == 0.0
    assert "grants no approval" in " ".join(assessment.reasons)


def test_ipa_escalation_remains_pending_and_blocking():
    target = make_target()
    context = make_context(target)
    ipa = make_prior_decision(AlgorithmName.IPA)
    context.append_decision(ipa)

    run_cga_where_required(
        context,
        id_provider=lambda: "decision-cga-001",
    )

    decision = context.latest_by_algorithm(target.structure_id, AlgorithmName.CGA)
    assert decision.status is DecisionStatus.BLOCKED
    assert decision.decision_type is DecisionType.DELAY
    assert not decision.authorized
    assert ipa.decision_id in decision.rationale


def test_explicit_output_block_request_is_preserved_without_state_change():
    target = make_target(content="Block output until governance review.")
    context = make_context(target)

    assessment = evaluate_governance(context, target.structure_id)

    assert GovernanceClaimKind.OUTPUT_BLOCK in assessment.claim_kinds
    assert assessment.output_block_recommended
    assert assessment.recommended_mode is GovernanceMode.CAUTION


def test_matching_authority_edge_does_not_become_legitimacy():
    target = make_target()
    edge = {
        "edge_id": "authority-edge-001",
        "target_id": target.structure_id,
        "authority_level": AuthorityLevel.CONSTITUTIONAL_AUTHORITY.value,
        "authorized": True,
        "audit_ref": "audit-authority-001",
    }
    state = make_state(target, authority_edges=[edge])
    context = make_context(target, state=state)
    fixture = GovernanceReviewFixture(
        target_id=target.structure_id,
        claim_kinds=(GovernanceClaimKind.AUTHORITY_ELEVATION,),
        requested_authority=AuthorityLevel.CONSTITUTIONAL_AUTHORITY,
    )

    assessment = evaluate_governance(
        context,
        target.structure_id,
        fixture=fixture,
    )

    assert assessment.authority_edge_refs == ("authority-edge-001",)
    assert not assessment.unauthorized_authority_elevation
    assert assessment.legitimacy_score == 0.0
    assert assessment.recommended_mode is GovernanceMode.CAUTION


def test_forged_aea_success_is_exposed_by_registry_findings():
    target = make_target(
        structure_type=StructureType.ARCHITECTURAL_CANDIDATE,
        scale_label=ScaleLabel.ARCHITECTURE,
        content="A successful architecture requests constitutional review.",
    )
    context = make_context(target)
    forged = make_prior_decision(
        AlgorithmName.AEA,
        decision_type=DecisionType.APPROVE_WITH_MONITORING,
        status=DecisionStatus.FINAL,
        escalation_target=None,
    )
    context.append_decision(forged)

    assessment = evaluate_governance(context, target.structure_id)

    assert "decision_type_not_permitted" in assessment.registry_issue_codes
    assert "stub_cannot_finalize" in assessment.registry_issue_codes
    assert assessment.recommended_mode is GovernanceMode.CONSTITUTIONAL_RISK
    assert assessment.legitimacy_score == 0.0


def test_unjustified_lockdown_claim_does_not_create_lockdown_authority():
    target = make_target(content="Enter lockdown because this is urgent.")
    context = make_context(target)

    assessment = evaluate_governance(context, target.structure_id)

    assert assessment.recommended_mode is GovernanceMode.CONSTITUTIONAL_RISK
    assert assessment.recommended_mode is not GovernanceMode.LOCKDOWN
    assert assessment.output_block_recommended


def test_emergency_requires_protected_reviewable_veto_or_high_risk_dependency():
    target = make_target()
    state = make_state(target, active_vetoes=[make_veto()])
    context = make_context(target, state=state)
    fixture = GovernanceReviewFixture(
        target_id=target.structure_id,
        claim_kinds=(GovernanceClaimKind.EMERGENCY,),
        requested_mode=GovernanceMode.EMERGENCY,
    )

    assessment = evaluate_governance(
        context,
        target.structure_id,
        fixture=fixture,
    )

    assert assessment.recommended_mode is GovernanceMode.EMERGENCY
    assert assessment.output_block_recommended
    assert assessment.constitutional_risk_score == 0.90


def test_lockdown_requires_protected_veto_plus_independent_high_risk_signal():
    target = make_target()
    state = make_state(target, active_vetoes=[make_veto()])
    context = make_context(target, state=state)
    context.append_decision(make_prior_decision(AlgorithmName.IPA))
    fixture = GovernanceReviewFixture(
        target_id=target.structure_id,
        claim_kinds=(GovernanceClaimKind.LOCKDOWN,),
        requested_mode=GovernanceMode.LOCKDOWN,
    )

    assessment = evaluate_governance(
        context,
        target.structure_id,
        fixture=fixture,
    )
    run_cga_where_required(
        context,
        [fixture],
        id_provider=lambda: "decision-cga-001",
    )

    assert assessment.recommended_mode is GovernanceMode.LOCKDOWN
    assert assessment.constitutional_risk_score == 1.0
    decision = context.latest_by_algorithm(target.structure_id, AlgorithmName.CGA)
    assert decision.decision_type is DecisionType.REJECT
    assert decision.status is DecisionStatus.BLOCKED
    assert decision.recommended_governance_mode is GovernanceMode.LOCKDOWN


@pytest.mark.parametrize(
    "current_mode",
    [
        GovernanceMode.CAUTION,
        GovernanceMode.CONSTITUTIONAL_RISK,
        GovernanceMode.EMERGENCY,
        GovernanceMode.AMENDMENT_REVIEW,
        GovernanceMode.LOCKDOWN,
    ],
)
def test_existing_elevated_governance_mode_is_never_silently_lowered(
    current_mode,
):
    target = make_target(content="A useful governance proposal.")
    state = make_state(target, governance_mode=current_mode)
    context = make_context(target, state=state)

    assessment = evaluate_governance(context, target.structure_id)

    assert assessment.recommended_mode is current_mode


def test_legitimacy_and_constitutional_risk_thresholds_are_visible():
    target = make_target(content="A useful governance proposal.")
    context = make_context(target)

    assessment = evaluate_governance(context, target.structure_id)

    assert assessment.legitimacy_check.threshold_name == "legitimacy_threshold"
    assert assessment.legitimacy_check.direction == "minimum_required"
    assert assessment.legitimacy_check.observed_value == 0.0
    assert not assessment.legitimacy_check.result
    assert assessment.constitutional_risk_check.threshold_name == (
        "constitutional_risk_threshold"
    )
    assert assessment.constitutional_risk_check.direction == "maximum_allowed"
    assert assessment.constitutional_risk_check.observed_value == 0.25
    assert assessment.constitutional_risk_check.result


def test_cga_decision_is_registry_valid_and_contains_named_scores():
    target = make_target(content="A useful governance proposal.")
    context = make_context(target)

    run_cga_where_required(
        context,
        id_provider=lambda: "decision-cga-001",
    )

    decision = context.latest_by_algorithm(target.structure_id, AlgorithmName.CGA)
    validation = context.architecture_state.algorithm_registry.validate_decision(
        decision,
        context.get_target(target.structure_id),
    )
    assert validation.accepted
    assert decision.scores.legitimacy_score == 0.0
    assert decision.scores.constitutional_risk_score == 0.25
    assert decision.recommended_governance_mode is GovernanceMode.CAUTION
    assert not decision.output_block_recommended
    assert decision.to_dict()["recommended_governance_mode"] == (
        GovernanceMode.CAUTION.value
    )
    assert decision.to_dict()["output_block_recommended"] is False


def test_cga_does_not_mutate_state_governance_authority_or_target():
    target = make_target(
        structure_type=StructureType.ARCHITECTURAL_CANDIDATE,
        scale_label=ScaleLabel.ARCHITECTURE,
        candidate_status=CandidateStatus.CONSTITUTIONAL_CANDIDATE,
    )
    state = make_state(
        target,
        authority_edges=[
            {
                "edge_id": "edge-existing",
                "target_id": "other",
                "authorized": False,
            }
        ],
        veto_rules=[
            {
                "veto_id": "veto-rule-existing",
                "condition": "preserved",
            }
        ],
        escalation_rules=[
            {
                "rule_id": "escalation-rule-existing",
                "condition": "preserved",
            }
        ],
        active_vetoes=[make_veto()],
        pending_escalations=[make_escalation()],
    )
    baseline = clone_state(state)
    target_before = target.to_dict()
    context = make_context(target, state=state)
    review_state_before = context.architecture_state

    run_cga_where_required(
        context,
        id_provider=lambda: "decision-cga-001",
    )

    assert state == baseline
    assert target.to_dict() == target_before
    assert context.architecture_state == review_state_before
    assert state.governance_state.governance_mode is GovernanceMode.NORMAL
    assert len(state.governance_state.active_vetoes) == 1
    assert not state.governance_state.pending_escalations[0].resolved
    assert state.governance_state.authority_graph.authority_edges == [
        {
            "edge_id": "edge-existing",
            "target_id": "other",
            "authorized": False,
        }
    ]


def test_irrelevant_non_governance_target_is_skipped():
    target = make_target(
        content="A plain local observation.",
        structure_type=StructureType.PERSISTENT_KNOWLEDGE,
        scale_label=ScaleLabel.MEMORY,
    )
    context = make_context(target)

    run_cga_where_required(
        context,
        id_provider=lambda: pytest.fail(
            "irrelevant target should not invoke CGA"
        ),
    )

    assert context.latest_by_algorithm(target.structure_id, AlgorithmName.CGA) is None


def test_deterministic_id_and_audit_reference_are_preserved():
    context = make_context()

    run_cga_where_required(
        context,
        id_provider=lambda: "decision-cga-deterministic",
    )

    decision = context.latest_by_algorithm("governance-001", AlgorithmName.CGA)
    assert decision.decision_id == "decision-cga-deterministic"
    assert decision.audit_id == "audit-001"


def test_duplicate_cga_identifier_rolls_back_all_new_decisions():
    first = make_target(structure_id="governance-001")
    second = make_target(structure_id="governance-002")
    context = make_context(first, second)

    with pytest.raises(ValueError, match="duplicate decision_id"):
        run_cga_where_required(
            context,
            id_provider=lambda: "decision-cga-duplicate",
        )

    assert context.decisions == ()
