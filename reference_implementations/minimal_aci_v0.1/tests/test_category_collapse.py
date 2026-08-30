from __future__ import annotations

from collections import defaultdict
from copy import deepcopy

from aci import (
    AlgorithmName,
    ArchitectureState,
    AuditStatus,
    AuthorityLevel,
    CandidateStatus,
    CycleReviewConfiguration,
    CycleStatus,
    DecisionStatus,
    DecisionType,
    EpistemicStatus,
    EvidenceGraph,
    EvidenceLink,
    EvidenceObject,
    EvidenceRelationType,
    GovernanceClaimKind,
    GovernanceReviewFixture,
    MemoryGraph,
    NormalizedProposition,
    OutputType,
    ParserIntent,
    PropositionComparisonFixture,
    PropositionPolarity,
    ScaleLabel,
    StructuredCycleInput,
    StructuredParseFixture,
    StructureType,
    SymbolicMetadata,
    SymbolicState,
    SymbolicStructure,
    VerificationStatus,
    run_integrated_cognitive_cycle,
)


class DeterministicIDs:
    def __init__(self) -> None:
        self._counts: defaultdict[str, int] = defaultdict(int)

    def __call__(self, kind: str) -> str:
        self._counts[kind] += 1
        return f"{kind}-{self._counts[kind]:03d}"


class ReviewBoundaryFault(RuntimeError):
    pass


def _fixed_time() -> str:
    return "2026-07-01T12:00:00+00:00"


def _structured_input(
    *fixtures: tuple[str, tuple[ParserIntent, ...]],
) -> StructuredCycleInput:
    return StructuredCycleInput(
        input_id="cycle-input-001",
        fixtures=tuple(
            StructuredParseFixture(
                input_id=f"input-{position:03d}",
                content=content,
                intents=intents,
            )
            for position, (content, intents) in enumerate(
                fixtures,
                start=1,
            )
        ),
    )


def _run_cycle(
    input_value,
    *,
    state: ArchitectureState | None = None,
    review_configuration: CycleReviewConfiguration | None = None,
    fault_injector=None,
):
    return run_integrated_cognitive_cycle(
        state or ArchitectureState(state_id="state-001"),
        input_value,
        review_configuration=review_configuration,
        id_provider=DeterministicIDs(),
        time_provider=_fixed_time,
        fault_injector=fault_injector,
    )


def _assert_committed(result) -> None:
    assert result.status is CycleStatus.COMMITTED
    assert result.audit_record.status is AuditStatus.COMMITTED
    assert result.audit_record.state_delta is not None
    assert result.audit_record.state_change_plan is not None
    assert result.audit_record.state_delta.audit_ref == result.audit_record.audit_id
    assert result.updated_state.audit_log[-1] == result.audit_record
    plan = result.audit_record.state_change_plan
    disposed_decision_ids = {
        *plan.decision_refs,
        *(decision.decision_id for decision in plan.rejected_decisions),
        *(decision.decision_id for decision in plan.no_op_items),
    }
    assert disposed_decision_ids == set(result.audit_record.decision_refs)
    assert result.audit_record.accepted_plan_items == plan.changes
    if result.output is not None:
        assert result.output.audit_finalized is True
        assert result.output.audit_ref == result.audit_record.audit_id


def _structure(result, structure_id: str = "structure-001"):
    return result.updated_state.active_structures[structure_id]


def _decisions(result, structure_id: str = "structure-001"):
    return [
        decision
        for decision in result.audit_record.decisions
        if decision.target_id == structure_id
    ]


def _decision(result, algorithm: AlgorithmName, structure_id="structure-001"):
    matches = [
        decision
        for decision in _decisions(result, structure_id)
        if decision.algorithm_name is algorithm
    ]
    assert len(matches) == 1
    return matches[0]


def _marker(result, structure_id: str = "structure-001"):
    assert result.output is not None
    matches = [
        marker
        for marker in result.output.epistemic_markers
        if marker.structure_id == structure_id
    ]
    assert len(matches) == 1
    return matches[0]


def _domain_snapshot(state: ArchitectureState) -> dict:
    snapshot = state.to_dict()
    snapshot.pop("audit_log")
    return snapshot


def _verified_evidence_state(
    target_id: str = "structure-001",
) -> ArchitectureState:
    evidence = EvidenceObject(
        evidence_id="evidence-001",
        content="A verified external measurement.",
        source_ref="source://measurement-001",
    )
    link = EvidenceLink(
        evidence_id=evidence.evidence_id,
        target_structure_id=target_id,
        source_ref=evidence.source_ref,
        relation_type=EvidenceRelationType.SUPPORTS,
        verification_status=VerificationStatus.VERIFIED,
    )
    return ArchitectureState(
        state_id="state-evidence",
        evidence_graph=EvidenceGraph(
            evidence_objects={evidence.evidence_id: evidence},
            links=[link],
        ),
    )


def _compatible_comparison() -> PropositionComparisonFixture:
    return PropositionComparisonFixture(
        comparison_id="comparison-001",
        target=NormalizedProposition(
            structure_id="structure-001",
            subject="system",
            relation="has",
            object_value="property",
            polarity=PropositionPolarity.AFFIRMED,
        ),
        counterpart=NormalizedProposition(
            structure_id="structure-002",
            subject="system",
            relation="has",
            object_value="property",
            polarity=PropositionPolarity.AFFIRMED,
        ),
    )


def _existing_structure(
    *,
    structure_id: str,
    structure_type: StructureType,
    current_state: SymbolicState,
    scale_label: ScaleLabel,
    authority_level: AuthorityLevel,
) -> SymbolicStructure:
    return SymbolicStructure(
        structure_id=structure_id,
        content=f"Existing {scale_label.name.lower()} structure.",
        structure_type=structure_type,
        current_state=current_state,
        metadata=SymbolicMetadata(
            origin="prior-cycle",
            epistemic_status=EpistemicStatus.STRONGLY_GROUNDED,
            scale_label=scale_label,
            candidate_status=CandidateStatus.NONE,
            authority_level=authority_level,
            grounding_score=1.0,
            coherence_score=1.0,
            persistence_score=1.0,
            uncertainty=0.0,
            audit_refs=["audit-prior"],
        ),
    )


def test_01_speculation_is_not_grounded_knowledge() -> None:
    result = _run_cycle(
        _structured_input(
            (
                "A possible explanation offered for review.",
                (ParserIntent.SPECULATION,),
            )
        )
    )
    _assert_committed(result)

    structure = _structure(result)
    gea = _decision(result, AlgorithmName.GEA)
    marker = _marker(result)
    assert structure.structure_type is StructureType.HYPOTHESIS
    assert structure.metadata.epistemic_status is EpistemicStatus.UNKNOWN
    assert structure.metadata.scale_label is ScaleLabel.HYPOTHESIS
    assert structure.metadata.candidate_status is CandidateStatus.NONE
    assert structure.metadata.authority_level is AuthorityLevel.NONE
    assert gea.scores.grounding_score == 0.0
    assert gea.decision_type is DecisionType.DELAY
    assert marker.grounding_score == 0.0
    assert marker.epistemic_status is not EpistemicStatus.STRONGLY_GROUNDED
    assert result.output.output_type is not OutputType.GROUNDED_RESPONSE
    assert "evidence_graph" not in result.audit_record.state_delta.domain_changes


def test_02_internal_coherence_is_not_external_evidence() -> None:
    configuration = CycleReviewConfiguration(
        cra_comparisons=(_compatible_comparison(),),
    )
    result = _run_cycle(
        _structured_input(
            ("The system has the property.", ()),
            ("The system also has the property.", ()),
        ),
        review_configuration=configuration,
    )
    _assert_committed(result)

    decisions = _decisions(result)
    gea = _decision(result, AlgorithmName.GEA)
    cra = _decision(result, AlgorithmName.CRA)
    assert [decision.algorithm_name for decision in decisions] == [
        AlgorithmName.GEA,
        AlgorithmName.CRA,
    ]
    assert cra.scores.coherence_score == 1.0
    assert gea.scores.grounding_score == 0.0
    assert _structure(result).metadata.epistemic_status is EpistemicStatus.UNKNOWN
    assert result.updated_state.evidence_graph.links == []
    assert "evidence_graph" not in result.audit_record.state_delta.domain_changes
    assert result.unresolved_items == []


def test_03_memory_is_not_invariant() -> None:
    memory = _existing_structure(
        structure_id="memory-existing",
        structure_type=StructureType.PERSISTENT_KNOWLEDGE,
        current_state=SymbolicState.PERSISTENT,
        scale_label=ScaleLabel.MEMORY,
        authority_level=AuthorityLevel.MEMORY_INFLUENCE,
    )
    state = ArchitectureState(
        state_id="state-memory",
        active_structures={memory.structure_id: memory},
        memory_graph=MemoryGraph(nodes={memory.structure_id: memory}),
    )
    result = _run_cycle(
        _structured_input(
            (
                "Request constitutional treatment for the existing memory.",
                (ParserIntent.CONSTITUTIONAL_REQUEST,),
            )
        ),
        state=state,
    )
    _assert_committed(result)

    preserved = result.updated_state.active_structures[memory.structure_id]
    candidate = _structure(result)
    assert preserved.metadata.scale_label is ScaleLabel.MEMORY
    assert preserved.metadata.authority_level is AuthorityLevel.MEMORY_INFLUENCE
    assert preserved.metadata.authority_level not in {
        AuthorityLevel.INVARIANT_CONSTRAINT,
        AuthorityLevel.CONSTITUTIONAL_AUTHORITY,
    }
    assert candidate.metadata.candidate_status is CandidateStatus.CONSTITUTIONAL_CANDIDATE
    assert candidate.metadata.scale_label is ScaleLabel.CLAIM
    assert candidate.metadata.authority_level is AuthorityLevel.NONE
    assert result.updated_state.memory_graph.nodes[memory.structure_id] == preserved
    assert "memory_graph" not in result.audit_record.state_delta.domain_changes
    assert "governance_state" not in result.audit_record.state_delta.domain_changes


def test_04_usefulness_is_not_legitimacy() -> None:
    configuration = CycleReviewConfiguration(
        cga_fixtures=(
            GovernanceReviewFixture(
                target_id="structure-001",
                claim_kinds=(GovernanceClaimKind.UTILITY,),
            ),
        )
    )
    result = _run_cycle(
        _structured_input(
            (
                "This useful proposal should govern future behavior.",
                (ParserIntent.GOVERNANCE_REQUEST,),
            )
        ),
        review_configuration=configuration,
    )
    _assert_committed(result)

    cga = _decision(result, AlgorithmName.CGA)
    structure = _structure(result)
    assert [decision.algorithm_name for decision in _decisions(result)] == [
        AlgorithmName.CGA
    ]
    assert cga.scores.legitimacy_score == 0.0
    assert cga.decision_type is DecisionType.DELAY
    assert cga.status is DecisionStatus.PENDING_REVIEW
    assert structure.metadata.authority_level is AuthorityLevel.NONE
    assert result.updated_state.governance_state.authority_graph.authority_edges == []
    assert "governance_state" not in result.audit_record.state_delta.domain_changes
    assert _marker(result).authority_level is AuthorityLevel.NONE


def test_05_evidence_is_not_persistence() -> None:
    state = _verified_evidence_state()
    original_evidence = deepcopy(state.evidence_graph)
    result = _run_cycle(
        _structured_input(("A measured external claim.", ())),
        state=state,
    )
    _assert_committed(result)

    gea = _decision(result, AlgorithmName.GEA)
    structure = _structure(result)
    assert gea.scores.grounding_score == 1.0
    assert gea.decision_type is DecisionType.APPROVE_WITH_MONITORING
    assert AlgorithmName.PCA not in {
        decision.algorithm_name for decision in _decisions(result)
    }
    assert structure.current_state is SymbolicState.CANDIDATE
    assert structure.metadata.candidate_status is CandidateStatus.NONE
    assert structure.metadata.authority_level is AuthorityLevel.NONE
    assert result.updated_state.memory_graph.nodes == {}
    assert result.updated_state.evidence_graph == original_evidence
    assert "memory_graph" not in result.audit_record.state_delta.domain_changes


def test_06_grounded_claim_is_not_architecture() -> None:
    result = _run_cycle(
        _structured_input(("A verified but local claim.", ())),
        state=_verified_evidence_state(),
    )
    _assert_committed(result)

    structure = _structure(result)
    gea = _decision(result, AlgorithmName.GEA)
    marker = _marker(result)
    assert gea.scores.grounding_score == 1.0
    assert marker.grounding_score == 1.0
    assert structure.metadata.scale_label is ScaleLabel.CLAIM
    assert structure.metadata.candidate_status is CandidateStatus.NONE
    assert structure.metadata.authority_level is AuthorityLevel.NONE
    assert AlgorithmName.AEA not in {
        decision.algorithm_name for decision in _decisions(result)
    }
    assert "scale_graph" not in result.audit_record.state_delta.domain_changes
    assert result.updated_state.governance_state.authority_graph.authority_edges == []


def test_07_architecture_is_not_constitution() -> None:
    architecture = _existing_structure(
        structure_id="architecture-existing",
        structure_type=StructureType.ARCHITECTURAL_CANDIDATE,
        current_state=SymbolicState.QUALIFIED_PERSISTENT,
        scale_label=ScaleLabel.ARCHITECTURE,
        authority_level=AuthorityLevel.ARCHITECTURAL_INFLUENCE,
    )
    state = ArchitectureState(
        state_id="state-architecture",
        active_structures={architecture.structure_id: architecture},
    )
    configuration = CycleReviewConfiguration(
        cga_fixtures=(
            GovernanceReviewFixture(
                target_id="structure-001",
                claim_kinds=(
                    GovernanceClaimKind.ARCHITECTURAL_SUCCESS,
                    GovernanceClaimKind.AUTHORITY_ELEVATION,
                ),
            ),
        )
    )
    result = _run_cycle(
        _structured_input(
            (
                "The successful architecture should become constitutional.",
                (ParserIntent.CONSTITUTIONAL_REQUEST,),
            )
        ),
        state=state,
        review_configuration=configuration,
    )
    _assert_committed(result)

    preserved = result.updated_state.active_structures[architecture.structure_id]
    candidate = _structure(result)
    cga = _decision(result, AlgorithmName.CGA)
    assert preserved.metadata.scale_label is ScaleLabel.ARCHITECTURE
    assert preserved.metadata.authority_level is AuthorityLevel.ARCHITECTURAL_INFLUENCE
    assert candidate.metadata.scale_label is ScaleLabel.CLAIM
    assert candidate.metadata.candidate_status is CandidateStatus.CONSTITUTIONAL_CANDIDATE
    assert candidate.metadata.authority_level is AuthorityLevel.NONE
    assert cga.scores.legitimacy_score == 0.0
    assert result.updated_state.governance_state.authority_graph.authority_edges == []
    assert "scale_graph" not in result.audit_record.state_delta.domain_changes


def test_08_escalation_is_not_approval() -> None:
    result = _run_cycle(
        _structured_input(
            (
                "Request architectural redesign.",
                (ParserIntent.ARCHITECTURE_REQUEST,),
            )
        )
    )
    _assert_committed(result)

    decisions = _decisions(result)
    mssa = _decision(result, AlgorithmName.MSSA)
    aea = _decision(result, AlgorithmName.AEA)
    cga = _decision(result, AlgorithmName.CGA)
    plan = result.audit_record.state_change_plan
    assert [decision.algorithm_name for decision in decisions] == [
        AlgorithmName.MSSA,
        AlgorithmName.AEA,
        AlgorithmName.CGA,
    ]
    assert mssa.decision_type is DecisionType.ESCALATE
    assert aea.decision_type is DecisionType.ESCALATE
    assert mssa.status is DecisionStatus.ESCALATED
    assert aea.status is DecisionStatus.ESCALATED
    assert cga.status is DecisionStatus.BLOCKED
    assert {decision.decision_id for decision in plan.rejected_decisions} == {
        mssa.decision_id,
        aea.decision_id,
    }
    assert plan.decision_refs == [cga.decision_id]
    assert result.escalation_events == []
    assert result.updated_state.governance_state.pending_escalations == []
    assert _structure(result).metadata.authority_level is AuthorityLevel.NONE
    assert _structure(result).metadata.scale_label is ScaleLabel.CLAIM


def test_09_output_is_not_truth() -> None:
    result = _run_cycle(
        _structured_input(("An unsupported claim can still be expressed.", ()))
    )
    _assert_committed(result)

    marker = _marker(result)
    assert result.output is not None
    assert result.output.audit_finalized is True
    assert result.output.output_type is OutputType.QUALIFIED_RESPONSE
    assert marker.epistemic_status is EpistemicStatus.UNKNOWN
    assert marker.grounding_score == 0.0
    assert marker.authority_level is AuthorityLevel.NONE
    assert result.output.epistemic_status is not EpistemicStatus.STRONGLY_GROUNDED
    assert result.output.output_type is not OutputType.GROUNDED_RESPONSE
    assert result.audit_record.status is AuditStatus.COMMITTED


def test_10_review_is_not_mutation() -> None:
    state = ArchitectureState(state_id="state-review-boundary")
    baseline_domain = _domain_snapshot(state)

    def stop_after_review(point: str) -> None:
        if point == "review_cga":
            raise ReviewBoundaryFault("stop before planning")

    result = _run_cycle(
        _structured_input(
            (
                "Request architectural redesign.",
                (ParserIntent.ARCHITECTURE_REQUEST,),
            )
        ),
        state=state,
        fault_injector=stop_after_review,
    )

    assert result.status is CycleStatus.ABORTED
    assert result.audit_record.status is AuditStatus.ABORTED
    assert result.audit_record.decisions
    assert result.audit_record.failure_stage == "review_cga"
    assert result.audit_record.state_change_plan is None
    assert result.audit_record.accepted_plan_items == []
    assert result.audit_record.state_delta is None
    assert result.output is None
    assert _domain_snapshot(result.updated_state) == baseline_domain
    assert _domain_snapshot(state) == baseline_domain


def test_11_evidential_language_is_not_typed_evidence() -> None:
    result = _run_cycle(
        _structured_input(
            (
                "A study proves this because there is evidence.",
                (ParserIntent.EVIDENCE_CLAIM,),
            )
        )
    )
    _assert_committed(result)

    structure = _structure(result)
    gea = _decision(result, AlgorithmName.GEA)
    marker = _marker(result)
    assert structure.structure_type is StructureType.CLAIM
    assert structure.metadata.epistemic_status is EpistemicStatus.UNKNOWN
    assert gea.scores.grounding_score == 0.0
    assert result.updated_state.evidence_graph.evidence_objects == {}
    assert result.updated_state.evidence_graph.links == []
    assert marker.grounding_score == 0.0
    assert result.output.output_type is not OutputType.GROUNDED_RESPONSE


def test_12_candidacy_is_not_achieved_scale() -> None:
    result = _run_cycle(
        _structured_input(
            (
                "Request an architectural candidate.",
                (ParserIntent.ARCHITECTURE_REQUEST,),
            )
        )
    )
    _assert_committed(result)

    structure = _structure(result)
    marker = _marker(result)
    mssa = _decision(result, AlgorithmName.MSSA)
    assert structure.structure_type is StructureType.ARCHITECTURAL_CANDIDATE
    assert structure.metadata.candidate_status is CandidateStatus.ARCHITECTURE_CANDIDATE
    assert structure.metadata.scale_label is ScaleLabel.CLAIM
    assert structure.metadata.authority_level is AuthorityLevel.NONE
    assert marker.candidate_status is CandidateStatus.ARCHITECTURE_CANDIDATE
    assert marker.scale_label is ScaleLabel.CLAIM
    assert marker.authority_level is AuthorityLevel.NONE
    assert mssa.decision_type is DecisionType.ESCALATE
    assert mssa.status is DecisionStatus.ESCALATED
    assert "scale_graph" not in result.audit_record.state_delta.domain_changes
