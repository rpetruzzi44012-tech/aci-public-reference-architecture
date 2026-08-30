import pytest

from aci.audit import (
    AbortedAuditData,
    CommittedAuditData,
    create_pending_audit,
    finalize_aborted_audit,
    finalize_committed_audit,
)
from aci.core import (
    CycleResult,
    EscalationEvent,
    ReviewDecision,
    ScoreBundle,
    StateChange,
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
    EscalationUrgency,
    GovernanceMode,
    OutputType,
    ScaleLabel,
    StructureType,
    SymbolicState,
)
from aci.output import (
    OutputAuthorizationError,
    bind_audit_ref_to_output,
    collect_epistemic_markers,
    collect_unresolved_tensions,
    determine_output_type,
    generate_provisional_authorized_output,
)
from aci.registry import DecisionValidationResult
from aci.review_context import ReviewContext, UnresolvedReviewItem
from aci.state import ArchitectureState, GovernanceState


AUDIT_ID = "audit-018"


def make_structure(
    *,
    structure_id="structure-001",
    content="A reviewed proposition.",
    structure_type=StructureType.CLAIM,
    epistemic_status=EpistemicStatus.UNGROUNDED,
    scale_label=ScaleLabel.CLAIM,
    candidate_status=CandidateStatus.NONE,
    authority_level=AuthorityLevel.TEMPORARY_USE,
    grounding_score=0.0,
    coherence_score=0.0,
    uncertainty=0.7,
    current_state=SymbolicState.CANDIDATE,
):
    return SymbolicStructure(
        structure_id=structure_id,
        content=content,
        structure_type=structure_type,
        current_state=current_state,
        metadata=SymbolicMetadata(
            origin="input-018",
            epistemic_status=epistemic_status,
            scale_label=scale_label,
            candidate_status=candidate_status,
            authority_level=authority_level,
            grounding_score=grounding_score,
            coherence_score=coherence_score,
            persistence_score=0.0,
            uncertainty=uncertainty,
            audit_refs=[AUDIT_ID],
        ),
    )


def make_state(
    *targets,
    governance_mode=GovernanceMode.NORMAL,
    active_vetoes=(),
    pending_escalations=(),
):
    values = list(targets) or [make_structure()]
    return ArchitectureState(
        state_id="state-018",
        active_structures={
            target.structure_id: target
            for target in values
        },
        governance_state=GovernanceState(
            governance_mode=governance_mode,
            active_vetoes=list(active_vetoes),
            pending_escalations=list(pending_escalations),
        ),
    )


def make_context(*targets, state=None):
    values = list(targets) or [make_structure()]
    return ReviewContext(
        audit_id=AUDIT_ID,
        architecture_state=state or make_state(*values),
        targets=values,
    )


def make_decision(
    *,
    decision_id="decision-001",
    target_id="structure-001",
    algorithm_name=AlgorithmName.GEA,
    decision_type=DecisionType.APPROVE_WITH_MONITORING,
    status=DecisionStatus.MONITORING,
    grounding_score=0.0,
    coherence_score=0.0,
    escalation_target=None,
    recommended_governance_mode=None,
    output_block_recommended=False,
):
    return ReviewDecision(
        decision_id=decision_id,
        algorithm_name=algorithm_name,
        target_id=target_id,
        decision_type=decision_type,
        status=status,
        scores=ScoreBundle(
            grounding_score=grounding_score,
            coherence_score=coherence_score,
        ),
        rationale="Typed review result for output testing.",
        authorized=False,
        escalation_target=escalation_target,
        audit_id=AUDIT_ID,
        recommended_governance_mode=recommended_governance_mode,
        output_block_recommended=output_block_recommended,
    )


def make_plan(*decisions, escalations=()):
    decision_refs = [decision.decision_id for decision in decisions]
    changes = [
        StateChange(
            change_id=f"change-{decision.decision_id}",
            target_id=decision.target_id,
            change_type="monitoring_trigger_add",
            decision_ref=decision.decision_id,
            audit_ref=AUDIT_ID,
            payload={"condition": "output-review"},
        )
        for decision in decisions
        if decision.decision_type is not DecisionType.ESCALATE
    ]
    return StateChangePlan(
        plan_id="plan-018",
        decision_refs=decision_refs,
        changes=changes,
        escalation_events=list(escalations),
        validation_results=[
            DecisionValidationResult(
                decision_id=decision.decision_id,
                target_id=decision.target_id,
                algorithm_identity=decision.algorithm_name.value,
                accepted=True,
                issues=(),
            )
            for decision in decisions
        ],
        rationale=["Resolved output fixture."],
        authorized=bool(decisions),
        audit_ref=AUDIT_ID,
    )


def append(context, *decisions):
    context.append_decisions(decisions)
    return context


def test_qualified_speculation_preserves_candidate_and_review_markers():
    target = make_structure(
        content="A possible transformation rule.",
        epistemic_status=EpistemicStatus.SPECULATIVE,
        scale_label=ScaleLabel.HYPOTHESIS,
        candidate_status=CandidateStatus.ARCHITECTURE_CANDIDATE,
        authority_level=AuthorityLevel.TEMPORARY_USE,
        uncertainty=0.9,
    )
    decision = make_decision(
        decision_type=DecisionType.SANDBOX,
        status=DecisionStatus.PROVISIONAL,
    )
    context = append(make_context(target), decision)

    output = generate_provisional_authorized_output(
        context,
        make_plan(decision),
        id_provider=lambda: "output-speculative",
    )

    assert output is not None
    assert output.output_type is OutputType.SPECULATIVE_RESPONSE
    assert output.audit_ref is None
    assert output.audit_finalized is False
    assert output.supporting_structure_ids == ["structure-001"]
    assert output.supporting_decision_ids == ["decision-001"]
    assert output.epistemic_status is EpistemicStatus.SPECULATIVE
    assert output.scale_label is ScaleLabel.HYPOTHESIS
    assert output.authority_level is AuthorityLevel.TEMPORARY_USE
    marker = output.epistemic_markers[0]
    assert marker.candidate_status is CandidateStatus.ARCHITECTURE_CANDIDATE
    assert marker.scale_label is ScaleLabel.HYPOTHESIS
    assert marker.decision_statuses == [DecisionStatus.PROVISIONAL]
    assert "speculative" in output.content.lower()
    assert "candidate status is not achieved scale" in output.content.lower()


def test_internally_coherent_claim_remains_qualified_and_ungrounded():
    target = make_structure(
        content="The proposal is internally consistent.",
        epistemic_status=EpistemicStatus.INTERNALLY_COHERENT,
        grounding_score=0.0,
        coherence_score=0.8,
    )
    decision = make_decision(
        algorithm_name=AlgorithmName.CRA,
        coherence_score=0.9,
    )
    context = append(make_context(target), decision)

    output = generate_provisional_authorized_output(
        context,
        make_plan(decision),
        id_provider=lambda: "output-coherent",
    )

    assert output is not None
    assert output.output_type is OutputType.QUALIFIED_RESPONSE
    assert output.grounding_score == 0.0
    assert output.coherence_score == 0.9
    assert output.epistemic_markers[0].grounding_score == 0.0
    assert "coherence is not external evidence" in output.content.lower()
    assert output.output_type is not OutputType.GROUNDED_RESPONSE


def test_unresolved_context_and_graph_tensions_remain_visible():
    target = make_structure(
        epistemic_status=EpistemicStatus.PARTIALLY_GROUNDED,
    )
    state = make_state(target)
    state.coherence_graph.unresolved_tensions.append("tension-graph")
    state.coherence_graph.relations.append(
        {
            "relation_id": "tension-graph",
            "target_id": target.structure_id,
            "relation_type": "unresolved",
        }
    )
    context = make_context(target, state=state)
    decision = make_decision(
        algorithm_name=AlgorithmName.CRA,
        decision_type=DecisionType.REPAIR,
        status=DecisionStatus.PROVISIONAL,
    )
    context.append_decision(decision)
    context.record_unresolved(
        UnresolvedReviewItem(
            item_id="tension-context",
            target_id=target.structure_id,
            reason="A structured contradiction remains.",
            decision_ref=decision.decision_id,
        )
    )

    output = generate_provisional_authorized_output(
        context,
        make_plan(decision),
        id_provider=lambda: "output-tension",
    )

    assert output is not None
    assert output.output_type is OutputType.QUALIFIED_RESPONSE
    assert output.unresolved_tensions == [
        "tension-context",
        "tension-graph",
    ]
    assert "unresolved tensions remain" in output.content.lower()
    assert collect_unresolved_tensions(
        context,
        [target.structure_id],
    ) == ["tension-context", "tension-graph"]


def test_pending_governance_escalation_is_notice_not_approval():
    target = make_structure(
        structure_type=StructureType.ARCHITECTURAL_CANDIDATE,
        candidate_status=CandidateStatus.ARCHITECTURE_CANDIDATE,
    )
    decision = make_decision(
        algorithm_name=AlgorithmName.MSSA,
        decision_type=DecisionType.ESCALATE,
        status=DecisionStatus.ESCALATED,
        escalation_target=AlgorithmName.CGA.value,
    )
    event = EscalationEvent(
        escalation_id="escalation-018",
        target_id=target.structure_id,
        reason="Architectural authority remains unresolved.",
        urgency=EscalationUrgency.CRITICAL,
        decision_ref=decision.decision_id,
        from_algorithm=AlgorithmName.MSSA,
        to_algorithm=AlgorithmName.CGA,
        resolved=False,
        audit_ref=AUDIT_ID,
    )
    context = append(make_context(target), decision)

    output = generate_provisional_authorized_output(
        context,
        make_plan(decision, escalations=[event]),
        id_provider=lambda: "output-escalation",
    )

    assert output is not None
    assert output.output_type is OutputType.ESCALATION_NOTICE
    assert output.pending_escalation_ids == ["escalation-018"]
    assert output.decision_status is DecisionStatus.ESCALATED
    assert "not approval" in output.content.lower()


def test_state_pending_escalation_is_preserved_even_when_plan_did_not_create_it():
    target = make_structure()
    decision = make_decision()
    event = EscalationEvent(
        escalation_id="escalation-state-018",
        target_id=target.structure_id,
        reason="Prior governance escalation remains open.",
        urgency=EscalationUrgency.HIGH,
        decision_ref="decision-prior",
        from_algorithm=AlgorithmName.MSSA,
        to_algorithm=AlgorithmName.CGA,
        resolved=False,
        audit_ref="audit-prior",
    )
    state = make_state(target, pending_escalations=[event])
    context = append(make_context(target, state=state), decision)

    output = generate_provisional_authorized_output(
        context,
        make_plan(decision),
        id_provider=lambda: "output-state-escalation",
    )

    assert output is not None
    assert output.output_type is OutputType.ESCALATION_NOTICE
    assert output.pending_escalation_ids == ["escalation-state-018"]


def test_governance_block_returns_structured_no_output():
    target = make_structure(
        structure_type=StructureType.GOVERNANCE_OBJECT,
    )
    decision = make_decision(
        algorithm_name=AlgorithmName.CGA,
        decision_type=DecisionType.DELAY,
        status=DecisionStatus.BLOCKED,
        recommended_governance_mode=GovernanceMode.CONSTITUTIONAL_RISK,
        output_block_recommended=True,
    )
    state = make_state(
        target,
        active_vetoes=[
            {
                "veto_id": "veto-018",
                "target_id": target.structure_id,
                "issuing_domain": "verification",
                "reason": "Independent review is incomplete.",
                "protected": True,
                "audit_ref": "audit-veto-018",
            }
        ],
    )
    context = append(make_context(target, state=state), decision)

    output = generate_provisional_authorized_output(
        context,
        make_plan(decision),
        id_provider=lambda: "output-blocked",
    )

    assert output is not None
    assert output.output_type is OutputType.NO_OUTPUT
    assert output.content is None
    assert output.supporting_decision_ids == [decision.decision_id]
    assert output.epistemic_markers[0].structure_id == target.structure_id
    assert output.audit_ref is None


def test_lockdown_blocks_output_without_inventing_a_refusal_message():
    target = make_structure()
    decision = make_decision()
    state = make_state(target, governance_mode=GovernanceMode.LOCKDOWN)
    context = append(make_context(target, state=state), decision)

    output = generate_provisional_authorized_output(
        context,
        make_plan(decision),
        id_provider=lambda: "output-lockdown",
    )

    assert output is not None
    assert output.output_type is OutputType.NO_OUTPUT
    assert output.content is None


def test_unscoped_active_veto_blocks_instead_of_disappearing():
    target = make_structure()
    decision = make_decision()
    state = make_state(
        target,
        active_vetoes=[
            {
                "veto_id": "veto-unscoped",
                "issuing_domain": "unknown",
                "reason": "Malformed veto still requires review.",
                "protected": True,
            }
        ],
    )
    context = append(make_context(target, state=state), decision)

    output = generate_provisional_authorized_output(
        context,
        make_plan(decision),
        id_provider=lambda: "output-unscoped-veto",
    )

    assert output is not None
    assert output.output_type is OutputType.NO_OUTPUT
    assert output.content is None


def test_memory_and_candidacy_remain_separate_from_invariant_and_scale():
    target = make_structure(
        content="A persistent memory informs this qualified response.",
        epistemic_status=EpistemicStatus.PARTIALLY_GROUNDED,
        scale_label=ScaleLabel.MEMORY,
        candidate_status=CandidateStatus.CONSTITUTIONAL_CANDIDATE,
        authority_level=AuthorityLevel.MEMORY_INFLUENCE,
        current_state=SymbolicState.PERSISTENT,
    )
    decision = make_decision(
        algorithm_name=AlgorithmName.PCA,
        decision_type=DecisionType.APPROVE_WITH_MONITORING,
    )
    context = append(make_context(target), decision)

    output = generate_provisional_authorized_output(
        context,
        make_plan(decision),
        id_provider=lambda: "output-memory",
    )

    assert output is not None
    marker = output.epistemic_markers[0]
    assert marker.scale_label is ScaleLabel.MEMORY
    assert marker.candidate_status is CandidateStatus.CONSTITUTIONAL_CANDIDATE
    assert marker.authority_level is AuthorityLevel.MEMORY_INFLUENCE
    assert output.scale_label is ScaleLabel.MEMORY
    assert output.authority_level is AuthorityLevel.MEMORY_INFLUENCE
    assert output.authority_level is not AuthorityLevel.CONSTITUTIONAL_AUTHORITY
    assert "memory is not an invariant" in output.content.lower()


def test_strong_grounding_can_select_grounded_response_without_scale_elevation():
    target = make_structure(
        epistemic_status=EpistemicStatus.STRONGLY_GROUNDED,
        scale_label=ScaleLabel.CLAIM,
        grounding_score=0.9,
        uncertainty=0.1,
    )
    decision = make_decision(
        grounding_score=0.9,
        status=DecisionStatus.FINAL,
    )
    context = append(make_context(target), decision)
    markers = collect_epistemic_markers([target], [decision])

    assert determine_output_type(
        markers,
        [decision],
    ) is OutputType.GROUNDED_RESPONSE

    output = generate_provisional_authorized_output(
        context,
        make_plan(decision),
        id_provider=lambda: "output-grounded",
    )

    assert output is not None
    assert output.output_type is OutputType.GROUNDED_RESPONSE
    assert output.scale_label is ScaleLabel.CLAIM
    assert output.authority_level is AuthorityLevel.TEMPORARY_USE


def test_final_binding_requires_exact_committed_audit_witness():
    target = make_structure(
        epistemic_status=EpistemicStatus.SPECULATIVE,
    )
    decision = make_decision(decision_type=DecisionType.SANDBOX)
    context = append(make_context(target), decision)
    provisional = generate_provisional_authorized_output(
        context,
        make_plan(decision),
        id_provider=lambda: "output-final-018",
    )
    assert provisional is not None
    pending = create_pending_audit(
        cycle_id="cycle-018",
        input_ref="input-018",
        baseline_state_ref="state-018",
        id_provider=lambda: AUDIT_ID,
        time_provider=lambda: "2026-06-30T18:00:00+00:00",
    )

    with pytest.raises(
        OutputAuthorizationError,
        match="COMMITTED",
    ):
        bind_audit_ref_to_output(provisional, pending)

    finalize_committed_audit(
        pending,
        CommittedAuditData(
            provisional_output_ref=provisional.output_id,
        ),
        time_provider=lambda: "2026-06-30T18:01:00+00:00",
    )
    final = bind_audit_ref_to_output(provisional, pending)

    assert final is not None
    assert final.audit_ref == AUDIT_ID
    assert final.audit_finalized is True
    assert provisional.audit_ref is None
    assert provisional.audit_finalized is False

    with pytest.raises(
        ValueError,
        match="finalized matching audit linkage",
    ):
        CycleResult.committed(
            cycle_id="cycle-unbound",
            updated_state={"state_id": "state-018"},
            audit_record=pending,
            output=provisional,
        )
    committed_cycle = CycleResult.committed(
        cycle_id="cycle-bound",
        updated_state={"state_id": "state-018"},
        audit_record=pending,
        output=final,
    )
    assert committed_cycle.output == final

    with pytest.raises(
        OutputAuthorizationError,
        match="already audit-bound",
    ):
        bind_audit_ref_to_output(final, pending)


def test_binding_rejects_aborted_and_mismatched_audits():
    output_context = make_context()
    decision = make_decision()
    output_context.append_decision(decision)
    provisional = generate_provisional_authorized_output(
        output_context,
        make_plan(decision),
        id_provider=lambda: "output-expected",
    )
    assert provisional is not None

    aborted = create_pending_audit(
        cycle_id="cycle-aborted",
        input_ref="input-018",
        baseline_state_ref="state-018",
        id_provider=lambda: "audit-aborted",
    )
    finalize_aborted_audit(
        aborted,
        AbortedAuditData(
            failure_stage="output",
            error="Output generation failed.",
        ),
    )
    with pytest.raises(OutputAuthorizationError, match="COMMITTED"):
        bind_audit_ref_to_output(provisional, aborted)

    mismatched = create_pending_audit(
        cycle_id="cycle-mismatch",
        input_ref="input-018",
        baseline_state_ref="state-018",
        id_provider=lambda: "audit-mismatch",
    )
    finalize_committed_audit(
        mismatched,
        CommittedAuditData(provisional_output_ref="output-other"),
    )
    with pytest.raises(
        OutputAuthorizationError,
        match="does not authorize",
    ):
        bind_audit_ref_to_output(provisional, mismatched)


def test_output_requires_resolved_plan_decisions_not_raw_target_alone():
    context = make_context()
    empty_plan = StateChangePlan(
        plan_id="plan-empty",
        decision_refs=[],
        rationale=["No accepted review decision."],
        authorized=False,
        audit_ref=AUDIT_ID,
    )

    assert generate_provisional_authorized_output(
        context,
        empty_plan,
        id_provider=lambda: "output-impossible",
    ) is None

    decision = make_decision(decision_id="decision-absent")
    absent_plan = make_plan(decision)
    with pytest.raises(
        OutputAuthorizationError,
        match="absent from ReviewContext",
    ):
        generate_provisional_authorized_output(
            context,
            absent_plan,
        )
