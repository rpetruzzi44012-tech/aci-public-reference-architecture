import json
from dataclasses import FrozenInstanceError

import pytest

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
from aci.registry import (
    AlgorithmRegistry,
    AlgorithmSpec,
    RegistryChangeRequest,
    create_default_registry,
)
from aci.state import ArchitectureState, clone_state


def make_target(
    *,
    structure_type: StructureType = StructureType.CLAIM,
    scale_label: ScaleLabel = ScaleLabel.CLAIM,
) -> SymbolicStructure:
    return SymbolicStructure(
        structure_id="structure-001",
        content="A target requiring governed review.",
        structure_type=structure_type,
        current_state=SymbolicState.CANDIDATE,
        metadata=SymbolicMetadata(
            origin="input-001",
            epistemic_status=EpistemicStatus.UNGROUNDED,
            scale_label=scale_label,
            candidate_status=CandidateStatus.NONE,
            authority_level=AuthorityLevel.NONE,
        ),
    )


def make_decision(
    *,
    algorithm_name: AlgorithmName = AlgorithmName.GEA,
    decision_type: DecisionType = DecisionType.APPROVE,
    status: DecisionStatus = DecisionStatus.PROVISIONAL,
    escalation_target: str | None = None,
    authorized: bool = False,
) -> ReviewDecision:
    return ReviewDecision(
        decision_id="decision-001",
        algorithm_name=algorithm_name,
        target_id="structure-001",
        decision_type=decision_type,
        status=status,
        scores=ScoreBundle(),
        rationale="A structured test decision.",
        authorized=authorized,
        escalation_target=escalation_target,
        audit_id="audit-001",
    )


def test_default_registry_is_complete_and_explicit():
    registry = create_default_registry()

    assert isinstance(registry, AlgorithmRegistry)
    assert set(registry.algorithms) == set(AlgorithmName)
    assert len(registry.algorithms) == 10
    for algorithm_name, spec in registry.algorithms.items():
        assert spec.algorithm_name is algorithm_name
        assert spec.permitted_structure_types
        assert isinstance(spec.maximum_target_scale, ScaleLabel)
        assert isinstance(spec.authority_level, AuthorityLevel)
        assert spec.state_mutation_prohibited
    serialized = json.loads(json.dumps(registry.to_dict()))
    assert serialized["algorithms"]["algorithm.icc"]["coordinator"] is True


def test_protected_stubs_and_icc_coordinator_are_explicit():
    registry = create_default_registry()

    for algorithm_name in (
        AlgorithmName.IPA,
        AlgorithmName.SRA,
        AlgorithmName.NGSA,
        AlgorithmName.AEA,
    ):
        spec = registry.get_spec(algorithm_name)
        assert spec.protected
        assert spec.stub
        assert set(spec.permitted_decision_types).issubset(
            {
                DecisionType.SANDBOX,
                DecisionType.DELAY,
                DecisionType.ESCALATE,
            }
        )

    icc = registry.get_spec(AlgorithmName.ICC)
    assert icc.protected
    assert icc.coordinator
    assert not icc.stub
    assert icc.permitted_decision_types == ()


def test_registry_specs_and_mapping_are_immutable():
    registry = create_default_registry()
    spec = registry.get_spec(AlgorithmName.GEA)

    with pytest.raises(TypeError):
        registry.algorithms[AlgorithmName.GEA] = spec

    with pytest.raises(FrozenInstanceError):
        spec.protected = False


def test_architecture_state_receives_independent_default_registry():
    first = ArchitectureState(state_id="state-001")
    second = ArchitectureState(state_id="state-002")
    working = clone_state(first)

    assert isinstance(first.algorithm_registry, AlgorithmRegistry)
    assert isinstance(second.algorithm_registry, AlgorithmRegistry)
    assert first.algorithm_registry is not second.algorithm_registry
    assert working.algorithm_registry is first.algorithm_registry


def test_permitted_decision_is_accepted_and_serializable():
    registry = create_default_registry()
    result = registry.validate_decision(
        make_decision(),
        make_target(),
    )

    assert result.accepted
    assert result.issues == ()
    assert result.reason_codes == ()
    assert json.loads(json.dumps(result.to_dict())) == {
        "decision_id": "decision-001",
        "target_id": "structure-001",
        "algorithm_identity": "algorithm.gea",
        "accepted": True,
        "issues": [],
    }


def test_forged_algorithm_name_is_rejected_visibly():
    registry = create_default_registry()
    decision = make_decision()
    decision.algorithm_name = "FORGED"

    result = registry.validate_decision(decision, make_target())

    assert not result.accepted
    assert "unregistered_algorithm" in result.reason_codes
    assert result.algorithm_identity == "FORGED"


def test_excessive_decision_type_is_rejected():
    result = create_default_registry().validate_decision(
        make_decision(decision_type=DecisionType.PERSIST),
        make_target(),
    )

    assert not result.accepted
    assert result.reason_codes == ("decision_type_not_permitted",)


def test_illegal_escalation_target_is_rejected():
    result = create_default_registry().validate_decision(
        make_decision(
            decision_type=DecisionType.ESCALATE,
            status=DecisionStatus.ESCALATED,
            escalation_target="AEA",
        ),
        make_target(),
    )

    assert not result.accepted
    assert "escalation_target_not_permitted" in result.reason_codes


def test_registered_permitted_escalation_is_accepted():
    result = create_default_registry().validate_decision(
        make_decision(
            decision_type=DecisionType.ESCALATE,
            status=DecisionStatus.ESCALATED,
            escalation_target="CRA",
        ),
        make_target(),
    )

    assert result.accepted


def test_excessive_target_scale_is_rejected():
    result = create_default_registry().validate_decision(
        make_decision(),
        make_target(scale_label=ScaleLabel.ARCHITECTURE),
    )

    assert not result.accepted
    assert result.reason_codes == ("target_scale_exceeds_authority",)


def test_ineligible_target_type_is_rejected():
    result = create_default_registry().validate_decision(
        make_decision(),
        make_target(structure_type=StructureType.GOVERNANCE_OBJECT),
    )

    assert not result.accepted
    assert result.reason_codes == ("target_type_not_permitted",)


def test_stub_cannot_finalize_or_claim_authorization():
    target = make_target(
        structure_type=StructureType.ARCHITECTURAL_CANDIDATE,
        scale_label=ScaleLabel.ARCHITECTURE,
    )
    decision = make_decision(
        algorithm_name=AlgorithmName.IPA,
        decision_type=DecisionType.SANDBOX,
        status=DecisionStatus.FINAL,
        authorized=True,
    )

    result = create_default_registry().validate_decision(decision, target)

    assert not result.accepted
    assert "stub_cannot_finalize" in result.reason_codes
    assert "stub_cannot_authorize" in result.reason_codes


def test_self_authorizing_registry_change_is_rejected():
    change = RegistryChangeRequest(
        request_id="registry-change-001",
        proposer_algorithm=AlgorithmName.GEA,
        target_algorithm=AlgorithmName.GEA,
        change_kind="authority",
        reason="Expand grounding authority.",
        audit_ref="audit-001",
    )

    result = create_default_registry().validate_decision(
        make_decision(authorized=True),
        make_target(),
        change_request=change,
    )

    assert not result.accepted
    assert "self_modification_prohibited" in result.reason_codes
    assert "protected_algorithm_change_prohibited" in result.reason_codes
    assert "direct_registry_change_prohibited" in result.reason_codes


def test_ordinary_algorithm_cannot_change_icc_call_order():
    change = RegistryChangeRequest(
        request_id="registry-change-001",
        proposer_algorithm=AlgorithmName.CGA,
        target_algorithm=AlgorithmName.ICC,
        change_kind="call_order",
        reason="Reorder the integrated cycle.",
        audit_ref="audit-001",
    )
    decision = make_decision(
        algorithm_name=AlgorithmName.CGA,
        decision_type=DecisionType.APPROVE,
    )
    target = make_target(
        structure_type=StructureType.GOVERNANCE_OBJECT,
        scale_label=ScaleLabel.ARCHITECTURE,
    )

    result = create_default_registry().validate_decision(
        decision,
        target,
        change_request=change,
    )

    assert not result.accepted
    assert "protected_algorithm_change_prohibited" in result.reason_codes
    assert "icc_change_prohibited" in result.reason_codes
    assert "direct_registry_change_prohibited" in result.reason_codes


def test_icc_is_registered_but_cannot_issue_review_decisions():
    result = create_default_registry().validate_decision(
        make_decision(algorithm_name=AlgorithmName.ICC),
        make_target(),
    )

    assert not result.accepted
    assert "coordinator_not_reviewer" in result.reason_codes
    assert "decision_type_not_permitted" in result.reason_codes


def test_reviewer_spec_cannot_enable_direct_state_mutation():
    with pytest.raises(ValueError, match="prohibit direct state mutation"):
        AlgorithmSpec(
            algorithm_name=AlgorithmName.GEA,
            purpose="Invalid mutable reviewer.",
            permitted_structure_types=(StructureType.CLAIM,),
            permitted_decision_types=(DecisionType.APPROVE,),
            authority_level=AuthorityLevel.ACTIVE_REASONING,
            maximum_target_scale=ScaleLabel.CLAIM,
            permitted_escalation_targets=(AlgorithmName.CRA,),
            protected=True,
            stub=False,
            state_mutation_prohibited=False,
        )


def test_rejected_authority_attacks_cannot_mutate_registry():
    registry = create_default_registry()
    baseline = registry.to_dict()

    forged = make_decision()
    forged.algorithm_name = "FORGED"
    excessive = make_decision(decision_type=DecisionType.PERSIST)
    self_authorizing = make_decision(authorized=True)
    self_change = RegistryChangeRequest(
        request_id="registry-change-self",
        proposer_algorithm=AlgorithmName.GEA,
        target_algorithm=AlgorithmName.GEA,
        change_kind="authority",
        reason="Grant the reviewer more authority.",
        audit_ref="audit-001",
    )

    results = [
        registry.validate_decision(forged, make_target()),
        registry.validate_decision(excessive, make_target()),
        registry.validate_decision(
            self_authorizing,
            make_target(),
            change_request=self_change,
        ),
    ]

    assert all(not result.accepted for result in results)
    assert "unregistered_algorithm" in results[0].reason_codes
    assert "decision_type_not_permitted" in results[1].reason_codes
    assert "self_modification_prohibited" in results[2].reason_codes
    assert "protected_algorithm_change_prohibited" in results[2].reason_codes
    assert registry.to_dict() == baseline
