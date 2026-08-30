import pytest

from aci.core import (
    EscalationEvent,
    SymbolicMetadata,
    SymbolicStructure,
)
from aci.enums import (
    AlgorithmName,
    AuthorityLevel,
    CandidateStatus,
    EpistemicStatus,
    EscalationUrgency,
    EvidenceRelationType,
    GovernanceMode,
    ScaleLabel,
    StructureType,
    SymbolicState,
    VerificationStatus,
)
from aci.evidence import EvidenceLink, EvidenceObject
from aci.graphs import (
    AuthorityGraph,
    CoherenceGraph,
    EvidenceGraph,
    MemoryGraph,
    ScaleGraph,
)
from aci.state import ArchitectureState, GovernanceState


def make_structure() -> SymbolicStructure:
    return SymbolicStructure(
        structure_id="structure-001",
        content="A typed claim.",
        structure_type=StructureType.CLAIM,
        current_state=SymbolicState.CANDIDATE,
        metadata=SymbolicMetadata(
            origin="input-001",
            epistemic_status=EpistemicStatus.UNGROUNDED,
            scale_label=ScaleLabel.CLAIM,
            candidate_status=CandidateStatus.NONE,
            authority_level=AuthorityLevel.NONE,
        ),
    )


def make_escalation() -> EscalationEvent:
    return EscalationEvent(
        escalation_id="escalation-001",
        target_id="structure-001",
        reason="Local grounding authority is insufficient.",
        urgency=EscalationUrgency.NORMAL,
        decision_ref="decision-001",
        from_algorithm=AlgorithmName.GEA,
        to_algorithm=AlgorithmName.CGA,
        audit_ref="audit-001",
    )


def test_five_graph_domains_are_separate_typed_objects():
    state = ArchitectureState(state_id="state-001")
    graphs = (
        state.memory_graph,
        state.evidence_graph,
        state.coherence_graph,
        state.scale_graph,
        state.governance_state.authority_graph,
    )

    assert tuple(type(graph) for graph in graphs) == (
        MemoryGraph,
        EvidenceGraph,
        CoherenceGraph,
        ScaleGraph,
        AuthorityGraph,
    )
    assert len({id(graph) for graph in graphs}) == 5
    assert not hasattr(state, "authority_graph")
    assert (
        state.governance_state.authority_graph
        is not state.governance_state
    )


def test_graph_content_does_not_cross_domain_boundaries():
    structure = make_structure()
    evidence = EvidenceObject(
        evidence_id="evidence-001",
        content="A measured result.",
        source_ref="source://study-001",
    )
    link = EvidenceLink(
        evidence_id=evidence.evidence_id,
        target_structure_id=structure.structure_id,
        source_ref=evidence.source_ref,
        relation_type=EvidenceRelationType.SUPPORTS,
        verification_status=VerificationStatus.VERIFIED,
    )
    memory_graph = MemoryGraph(nodes={structure.structure_id: structure})
    evidence_graph = EvidenceGraph(
        evidence_objects={evidence.evidence_id: evidence},
        links=[link],
    )
    coherence_graph = CoherenceGraph(
        unresolved_tensions=["tension-001"],
    )
    scale_graph = ScaleGraph(
        scale_labels={structure.structure_id: ScaleLabel.CLAIM},
    )
    authority_graph = AuthorityGraph(domains=["grounding"])

    assert evidence.evidence_id not in memory_graph.nodes
    assert structure.structure_id not in evidence_graph.evidence_objects
    assert coherence_graph.unresolved_tensions == ["tension-001"]
    assert scale_graph.scale_labels == {
        structure.structure_id: ScaleLabel.CLAIM
    }
    assert authority_graph.domains == ["grounding"]


def test_graph_defaults_are_independent():
    first = ArchitectureState(state_id="state-001")
    second = ArchitectureState(state_id="state-002")

    first.memory_graph.persistence_relations.append({"relation_id": "m-001"})
    first.evidence_graph.source_relations.append({"source_id": "source-001"})
    first.coherence_graph.unresolved_tensions.append("tension-001")
    first.scale_graph.mismatch_records.append({"mismatch_id": "scale-001"})
    first.governance_state.authority_graph.domains.append("grounding")

    assert second.memory_graph.persistence_relations == []
    assert second.evidence_graph.source_relations == []
    assert second.coherence_graph.unresolved_tensions == []
    assert second.scale_graph.mismatch_records == []
    assert second.governance_state.authority_graph.domains == []


def test_graphs_reject_objects_from_other_domains():
    structure = make_structure()
    evidence = EvidenceObject(
        evidence_id="evidence-001",
        content="A measured result.",
        source_ref="source://study-001",
    )

    with pytest.raises(TypeError, match="SymbolicStructure"):
        MemoryGraph(nodes={"evidence-001": evidence})

    with pytest.raises(TypeError, match="EvidenceObject"):
        EvidenceGraph(evidence_objects={"structure-001": structure})

    with pytest.raises(TypeError, match="ScaleLabel"):
        ScaleGraph(scale_labels={"structure-001": AuthorityLevel.NONE})

    with pytest.raises(ValueError, match="domains must be unique"):
        AuthorityGraph(domains=["grounding", "grounding"])


def test_governance_state_exposes_active_posture_and_precedent():
    escalation = make_escalation()
    authority_graph = AuthorityGraph(
        domains=["grounding", "constitutional"],
        authority_edges=[
            {
                "source": "grounding",
                "target": "constitutional",
                "relation": "escalates_to",
            }
        ],
    )
    governance = GovernanceState(
        governance_mode=GovernanceMode.CAUTION,
        authority_graph=authority_graph,
        active_vetoes=[
            {
                "veto_id": "veto-001",
                "target_id": "structure-001",
                "reason": "Verification is incomplete.",
            }
        ],
        pending_escalations=[escalation],
        governance_memory=[
            {
                "precedent_id": "precedent-001",
                "audit_ref": "audit-001",
            }
        ],
    )

    assert governance.governance_mode is GovernanceMode.CAUTION
    assert governance.authority_graph is authority_graph
    assert governance.active_vetoes[0]["veto_id"] == "veto-001"
    assert governance.pending_escalations == [escalation]
    assert governance.governance_memory[0]["audit_ref"] == "audit-001"


def test_governance_state_rejects_category_substitution():
    with pytest.raises(TypeError, match="GovernanceMode"):
        GovernanceState(governance_mode=AuthorityLevel.NONE)

    with pytest.raises(TypeError, match="AuthorityGraph"):
        GovernanceState(authority_graph=ScaleGraph())
