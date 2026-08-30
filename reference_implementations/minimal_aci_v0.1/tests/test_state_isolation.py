from dataclasses import FrozenInstanceError

import pytest

from aci.core import (
    AuditRecord,
    EscalationEvent,
    RollbackPoint,
    StateChange,
    SymbolicMetadata,
    SymbolicStructure,
)
from aci.enums import (
    AlgorithmName,
    AuditStatus,
    AuthorityLevel,
    BudgetType,
    CandidateStatus,
    EpistemicStatus,
    EscalationUrgency,
    EvidenceRelationType,
    GovernanceMode,
    GraphName,
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
from aci.state import (
    ArchitectureState,
    BudgetState,
    GovernanceState,
    THRESHOLD_DIRECTIONS,
    THRESHOLD_MEANINGS,
    ThresholdState,
    budget_pressure,
    budget_routing_signals,
    capture_baseline,
    clone_state,
    threshold_direction,
    threshold_meaning,
    threshold_passes,
    threshold_requires_review,
)


def make_structure(
    *,
    structure_id: str = "structure-001",
) -> SymbolicStructure:
    return SymbolicStructure(
        structure_id=structure_id,
        content="A claim under review.",
        structure_type=StructureType.CLAIM,
        current_state=SymbolicState.CANDIDATE,
        metadata=SymbolicMetadata(
            origin="input-001",
            epistemic_status=EpistemicStatus.UNGROUNDED,
            scale_label=ScaleLabel.CLAIM,
            candidate_status=CandidateStatus.NONE,
            authority_level=AuthorityLevel.NONE,
            audit_refs=["audit-001"],
        ),
    )


def make_state() -> ArchitectureState:
    structure = make_structure()
    evidence = EvidenceObject(
        evidence_id="evidence-001",
        content="A measured result.",
        source_ref="source://study-001",
    )
    evidence_link = EvidenceLink(
        evidence_id=evidence.evidence_id,
        target_structure_id=structure.structure_id,
        source_ref=evidence.source_ref,
        relation_type=EvidenceRelationType.SUPPORTS,
        verification_status=VerificationStatus.VERIFIED,
    )
    escalation = EscalationEvent(
        escalation_id="escalation-001",
        target_id=structure.structure_id,
        reason="Constitutional review may be required.",
        urgency=EscalationUrgency.HIGH,
        decision_ref="decision-001",
        from_algorithm=AlgorithmName.GEA,
        to_algorithm=AlgorithmName.CGA,
        audit_ref="audit-001",
    )
    audit = AuditRecord(
        audit_id="audit-001",
        status=AuditStatus.PENDING,
        cycle_id="cycle-001",
        decision_refs=["decision-001"],
    )
    rollback = RollbackPoint(
        rollback_id="rollback-001",
        state_ref="state-001",
        affected_structures=[structure.structure_id],
        affected_graphs=[GraphName.EVIDENCE_GRAPH],
        reason_created="Protect the baseline during evidence update.",
        audit_ref="audit-001",
    )
    state_change = StateChange(
        change_id="change-001",
        target_id=structure.structure_id,
        change_type="metadata_update",
        decision_ref="decision-001",
        audit_ref="audit-001",
        payload={"tags": ["baseline"]},
    )
    return ArchitectureState(
        state_id="state-001",
        active_structures={structure.structure_id: structure},
        memory_graph=MemoryGraph(
            nodes={structure.structure_id: structure},
            persistence_relations=[
                {
                    "relation_id": "memory-relation-001",
                    "tags": ["baseline"],
                }
            ],
        ),
        evidence_graph=EvidenceGraph(
            evidence_objects={evidence.evidence_id: evidence},
            links=[evidence_link],
            source_relations=[
                {
                    "source_id": evidence.source_ref,
                    "source_chain": ["primary"],
                }
            ],
        ),
        coherence_graph=CoherenceGraph(
            relations=[
                {
                    "relation_id": "coherence-relation-001",
                    "notes": ["baseline"],
                }
            ],
            unresolved_tensions=["tension-001"],
            coherence_pressure=0.2,
        ),
        scale_graph=ScaleGraph(
            scale_labels={structure.structure_id: ScaleLabel.CLAIM},
            mismatch_records=[
                {
                    "mismatch_id": "mismatch-001",
                    "history": ["baseline"],
                }
            ],
        ),
        governance_state=GovernanceState(
            governance_mode=GovernanceMode.CAUTION,
            authority_graph=AuthorityGraph(
                domains=["grounding", "constitutional"],
                authority_edges=[
                    {
                        "edge_id": "authority-edge-001",
                        "conditions": ["baseline"],
                    }
                ],
                veto_rules=[
                    {
                        "veto_id": "veto-rule-001",
                        "conditions": ["baseline"],
                    }
                ],
                escalation_rules=[
                    {
                        "rule_id": "escalation-rule-001",
                        "conditions": ["baseline"],
                    }
                ],
            ),
            active_vetoes=[
                {
                    "veto_id": "active-veto-001",
                    "reasons": ["baseline"],
                }
            ],
            pending_escalations=[escalation],
            governance_memory=[
                {
                    "precedent_id": "precedent-001",
                    "tags": ["baseline"],
                }
            ],
        ),
        audit_log=[audit],
        rollback_points=[rollback],
        monitoring_triggers=["grounding-review"],
        state_changes=[state_change],
    )


def test_clone_state_isolates_every_nested_mutable_collection():
    baseline = make_state()
    working = clone_state(baseline)

    working.active_structures["structure-001"].content = "Working content."
    working.active_structures["structure-001"].metadata.audit_refs.append(
        "audit-working"
    )
    working.active_structures["structure-002"] = make_structure(
        structure_id="structure-002"
    )
    working.memory_graph.nodes["structure-002"] = make_structure(
        structure_id="structure-002"
    )
    working.memory_graph.persistence_relations[0]["tags"].append("working")
    working.evidence_graph.evidence_objects["evidence-001"].content = (
        "Working evidence."
    )
    working.evidence_graph.links.append(working.evidence_graph.links[0])
    working.evidence_graph.source_relations[0]["source_chain"].append(
        "working"
    )
    working.coherence_graph.relations[0]["notes"].append("working")
    working.coherence_graph.unresolved_tensions.append("tension-working")
    working.scale_graph.scale_labels["structure-002"] = ScaleLabel.HYPOTHESIS
    working.scale_graph.mismatch_records[0]["history"].append("working")
    authority_graph = working.governance_state.authority_graph
    authority_graph.domains.append("verification")
    authority_graph.authority_edges[0]["conditions"].append("working")
    authority_graph.veto_rules[0]["conditions"].append("working")
    authority_graph.escalation_rules[0]["conditions"].append("working")
    working.governance_state.active_vetoes[0]["reasons"].append("working")
    working.governance_state.pending_escalations[0].resolved = True
    working.governance_state.governance_memory[0]["tags"].append("working")
    working.budgets.stability_budget = 0.2
    working.thresholds.grounding_threshold = 0.9
    working.audit_log[0].decision_refs.append("decision-working")
    working.audit_log[0].state_change_refs.append("change-working")
    working.audit_log[0].graph_update_refs.append("update-working")
    working.audit_log[0].escalation_refs.append("escalation-working")
    working.audit_log[0].rollback_refs.append("rollback-working")
    working.audit_log[0].output_refs.append("output-working")
    working.rollback_points[0].affected_structures.append("structure-002")
    working.rollback_points[0].affected_graphs.append(GraphName.MEMORY_GRAPH)
    working.monitoring_triggers.append("working-trigger")
    working.state_changes[0].payload["tags"].append("working")

    assert set(baseline.active_structures) == {"structure-001"}
    assert baseline.active_structures["structure-001"].content == (
        "A claim under review."
    )
    assert baseline.active_structures["structure-001"].metadata.audit_refs == [
        "audit-001"
    ]
    assert set(baseline.memory_graph.nodes) == {"structure-001"}
    assert baseline.memory_graph.persistence_relations[0]["tags"] == [
        "baseline"
    ]
    assert baseline.evidence_graph.evidence_objects["evidence-001"].content == (
        "A measured result."
    )
    assert len(baseline.evidence_graph.links) == 1
    assert baseline.evidence_graph.source_relations[0]["source_chain"] == [
        "primary"
    ]
    assert baseline.coherence_graph.relations[0]["notes"] == ["baseline"]
    assert baseline.coherence_graph.unresolved_tensions == ["tension-001"]
    assert "structure-002" not in baseline.scale_graph.scale_labels
    assert baseline.scale_graph.mismatch_records[0]["history"] == ["baseline"]
    baseline_authority = baseline.governance_state.authority_graph
    assert baseline_authority.domains == ["grounding", "constitutional"]
    assert baseline_authority.authority_edges[0]["conditions"] == ["baseline"]
    assert baseline_authority.veto_rules[0]["conditions"] == ["baseline"]
    assert baseline_authority.escalation_rules[0]["conditions"] == ["baseline"]
    assert baseline.governance_state.active_vetoes[0]["reasons"] == [
        "baseline"
    ]
    assert not baseline.governance_state.pending_escalations[0].resolved
    assert baseline.governance_state.governance_memory[0]["tags"] == [
        "baseline"
    ]
    assert baseline.budgets.stability_budget == 1.0
    assert baseline.thresholds.grounding_threshold == 0.70
    assert AlgorithmName.GEA in baseline.algorithm_registry.algorithms
    assert working.algorithm_registry is baseline.algorithm_registry
    assert baseline.audit_log[0].decision_refs == ["decision-001"]
    assert baseline.audit_log[0].state_change_refs == []
    assert baseline.audit_log[0].graph_update_refs == []
    assert baseline.audit_log[0].escalation_refs == []
    assert baseline.audit_log[0].rollback_refs == []
    assert baseline.audit_log[0].output_refs == []
    assert baseline.rollback_points[0].affected_structures == [
        "structure-001"
    ]
    assert baseline.rollback_points[0].affected_graphs == [
        GraphName.EVIDENCE_GRAPH
    ]
    assert baseline.monitoring_triggers == ["grounding-review"]
    assert baseline.state_changes[0].payload["tags"] == ["baseline"]


def test_captured_baseline_is_isolated_from_source_and_working_copies():
    source = make_state()
    baseline = capture_baseline(source)
    first_working = baseline.clone()

    source.active_structures.clear()
    first_working.memory_graph.persistence_relations.clear()
    first_working.governance_state.authority_graph.domains.append("working")

    second_working = baseline.clone()

    assert baseline.source_state_id == "state-001"
    assert set(second_working.active_structures) == {"structure-001"}
    assert second_working.memory_graph.persistence_relations
    assert second_working.governance_state.authority_graph.domains == [
        "grounding",
        "constitutional",
    ]
    assert second_working is not first_working

    with pytest.raises(FrozenInstanceError):
        baseline.source_state_id = "state-mutated"


@pytest.mark.parametrize(
    ("field_name", "value", "error_type"),
    [
        ("stability_budget", -0.01, ValueError),
        ("novelty_budget", 1.01, ValueError),
        ("verification_budget", True, TypeError),
    ],
)
def test_budget_values_must_be_normalized(field_name, value, error_type):
    values = {
        "stability_budget": 1.0,
        "novelty_budget": 1.0,
        "verification_budget": 1.0,
        "attention_budget": 1.0,
        "recovery_capacity": 1.0,
    }
    values[field_name] = value

    with pytest.raises(error_type, match=field_name):
        BudgetState(**values)


def test_budget_pressure_is_visible_and_produces_non_authorizing_routes():
    budgets = BudgetState(
        stability_budget=0.20,
        novelty_budget=1.0,
        verification_budget=0.10,
        attention_budget=1.0,
        recovery_capacity=0.0,
    )

    assert budget_pressure(budgets) == {
        BudgetType.STABILITY: "low",
        BudgetType.NOVELTY: "available",
        BudgetType.VERIFICATION: "critical",
        BudgetType.ATTENTION: "available",
        BudgetType.RECOVERY: "exhausted",
    }
    assert budget_routing_signals(budgets) == (
        "low:stability_review",
        "critical:verification_delay",
        "exhausted:recovery_review",
    )
    assert budgets.stability_budget == 0.20
    assert budgets.verification_budget == 0.10
    assert budgets.recovery_capacity == 0.0


def test_budget_and_threshold_defaults_are_independent():
    first_state = ArchitectureState(state_id="state-001")
    second_state = ArchitectureState(state_id="state-002")

    first_state.budgets.attention_budget = 0.4
    first_state.thresholds.legitimacy_threshold = 0.9

    assert second_state.budgets.attention_budget == 1.0
    assert second_state.thresholds.legitimacy_threshold == 0.85


def test_threshold_values_directions_and_meanings_are_visible():
    thresholds = ThresholdState()

    assert set(THRESHOLD_DIRECTIONS) == set(THRESHOLD_MEANINGS)
    assert set(THRESHOLD_DIRECTIONS) == {
        field_name
        for field_name in thresholds.to_dict()
    }
    assert threshold_direction("identity_threshold") == "minimum_required"
    assert threshold_direction("stability_threshold") == "minimum_required"
    assert threshold_direction("novelty_threshold") == "maximum_allowed"
    assert threshold_direction("coherence_threshold") == "maximum_allowed"
    assert threshold_meaning("coherence_threshold") == (
        "maximum unresolved coherence pressure"
    )
    assert all(THRESHOLD_MEANINGS.values())


def test_threshold_checks_expose_later_review_without_granting_authority():
    thresholds = ThresholdState()

    assert threshold_passes(thresholds, "identity_threshold", 0.80)
    assert threshold_requires_review(
        thresholds,
        "identity_threshold",
        0.79,
    )
    assert threshold_passes(
        thresholds,
        "constitutional_risk_threshold",
        0.30,
    )
    assert threshold_requires_review(
        thresholds,
        "constitutional_risk_threshold",
        0.31,
    )
    assert threshold_passes(thresholds, "stability_threshold", 0.25)
    assert threshold_requires_review(
        thresholds,
        "novelty_threshold",
        0.51,
    )


@pytest.mark.parametrize(
    ("field_name", "value", "error_type"),
    [
        ("identity_threshold", -0.01, ValueError),
        ("legitimacy_threshold", 1.01, ValueError),
        ("escalation_threshold", False, TypeError),
    ],
)
def test_threshold_values_must_be_normalized(field_name, value, error_type):
    values = ThresholdState().to_dict()
    values[field_name] = value

    with pytest.raises(error_type, match=field_name):
        ThresholdState(**values)
