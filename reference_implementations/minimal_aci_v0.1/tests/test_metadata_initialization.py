import json

import pytest

from aci.core import SymbolicStructure
from aci.enums import (
    AuthorityLevel,
    CandidateStatus,
    EpistemicStatus,
    ScaleLabel,
    StructureType,
    SymbolicState,
)
from aci.metadata import (
    MetadataInitializationError,
    assign_initial_scale_labels,
    create_threshold_check,
    initialize_metadata,
)
from aci.parser import parse_input_into_symbolic_structures
from aci.state import ArchitectureState, ThresholdState


def make_structure(
    structure_type=StructureType.CLAIM,
    *,
    structure_id="structure-001",
    current_state=SymbolicState.CANDIDATE,
    candidate_status=CandidateStatus.NONE,
):
    return SymbolicStructure(
        structure_id=structure_id,
        content="Opaque candidate content.",
        structure_type=structure_type,
        current_state=current_state,
        metadata=initialize_metadata(
            origin="input-001",
            candidate_status=candidate_status,
            audit_refs=["audit-001"],
        ),
    )


def assert_unearned(metadata):
    assert metadata.epistemic_status is EpistemicStatus.UNKNOWN
    assert metadata.authority_level is AuthorityLevel.NONE
    assert metadata.grounding_score == 0.0
    assert metadata.coherence_score == 0.0
    assert metadata.persistence_score == 0.0
    assert metadata.uncertainty == 1.0


def test_initialize_metadata_sets_every_required_field_conservatively():
    metadata = initialize_metadata(
        origin="input-001",
        scale_label=ScaleLabel.HYPOTHESIS,
        candidate_status=CandidateStatus.PERSISTENCE_CANDIDATE,
        audit_refs=["audit-001"],
    )

    assert metadata.origin == "input-001"
    assert metadata.scale_label is ScaleLabel.HYPOTHESIS
    assert (
        metadata.candidate_status
        is CandidateStatus.PERSISTENCE_CANDIDATE
    )
    assert metadata.audit_refs == ["audit-001"]
    assert_unearned(metadata)


def test_initialize_metadata_copies_mutable_audit_references():
    audit_refs = ["audit-001"]
    first = initialize_metadata(origin="input-001", audit_refs=audit_refs)
    second = initialize_metadata(origin="input-002")

    audit_refs.append("audit-external")
    first.audit_refs.append("audit-local")

    assert first.audit_refs == ["audit-001", "audit-local"]
    assert second.audit_refs == []


@pytest.mark.parametrize(
    "scale_label",
    [
        ScaleLabel.MEMORY,
        ScaleLabel.PRINCIPLE,
        ScaleLabel.ARCHITECTURE,
        ScaleLabel.CONSTITUTIONAL,
    ],
)
def test_initialize_metadata_rejects_earned_initial_scales(scale_label):
    with pytest.raises(MetadataInitializationError, match="initial scale"):
        initialize_metadata(
            origin="input-001",
            scale_label=scale_label,
        )


def test_initial_scale_assignment_uses_only_unearned_scale_labels():
    structures = [
        make_structure(
            StructureType.OBSERVATION,
            structure_id="observation-001",
        ),
        make_structure(
            StructureType.HYPOTHESIS,
            structure_id="hypothesis-001",
        ),
        make_structure(
            StructureType.MEMORY_CANDIDATE,
            structure_id="memory-001",
        ),
        make_structure(
            StructureType.ARCHITECTURAL_CANDIDATE,
            structure_id="architecture-001",
        ),
        make_structure(
            StructureType.CONSTITUTIONAL_OBJECT,
            structure_id="constitutional-001",
        ),
    ]

    result = assign_initial_scale_labels(
        structures,
        ArchitectureState(state_id="state-001"),
    )

    assert [item.metadata.scale_label for item in result.structures] == [
        ScaleLabel.OBSERVATION,
        ScaleLabel.HYPOTHESIS,
        ScaleLabel.CLAIM,
        ScaleLabel.CLAIM,
        ScaleLabel.CLAIM,
    ]
    assert all(
        item.metadata.scale_label
        not in {
            ScaleLabel.MEMORY,
            ScaleLabel.PRINCIPLE,
            ScaleLabel.ARCHITECTURE,
            ScaleLabel.CONSTITUTIONAL,
        }
        for item in result.structures
    )


def test_candidate_status_remains_separate_from_achieved_scale():
    structures = [
        make_structure(
            StructureType.MEMORY_CANDIDATE,
            structure_id="memory-001",
        ),
        make_structure(
            StructureType.ARCHITECTURAL_CANDIDATE,
            structure_id="architecture-001",
        ),
        make_structure(
            StructureType.CONSTITUTIONAL_OBJECT,
            structure_id="constitutional-001",
        ),
    ]

    result = assign_initial_scale_labels(
        structures,
        ArchitectureState(state_id="state-001"),
    )

    assert [item.metadata.candidate_status for item in result.structures] == [
        CandidateStatus.PERSISTENCE_CANDIDATE,
        CandidateStatus.ARCHITECTURE_CANDIDATE,
        CandidateStatus.CONSTITUTIONAL_CANDIDATE,
    ]
    assert all(
        item.metadata.scale_label is ScaleLabel.CLAIM
        for item in result.structures
    )
    assert all(
        item.metadata.authority_level is AuthorityLevel.NONE
        for item in result.structures
    )


def test_assignment_preserves_explicit_candidate_intent_from_parser():
    parsed = parse_input_into_symbolic_structures(
        "Treat this as constitutional.",
        id_provider=lambda: "structure-001",
    )[0]

    result = assign_initial_scale_labels(
        [parsed],
        ArchitectureState(state_id="state-001"),
    )
    initialized = result.structures[0]

    assert (
        initialized.metadata.candidate_status
        is CandidateStatus.CONSTITUTIONAL_CANDIDATE
    )
    assert initialized.metadata.scale_label is ScaleLabel.CLAIM
    assert initialized.metadata.authority_level is AuthorityLevel.NONE


def test_assignment_returns_copies_without_mutating_parser_output():
    parsed = parse_input_into_symbolic_structures(
        "Maybe this is a hypothesis.",
        id_provider=lambda: "structure-001",
    )[0]

    result = assign_initial_scale_labels(
        [parsed],
        ArchitectureState(state_id="state-001"),
    )

    assert result.structures[0] is not parsed
    assert parsed.metadata.scale_label is ScaleLabel.CLAIM
    assert result.structures[0].metadata.scale_label is ScaleLabel.HYPOTHESIS


def test_evidence_language_does_not_increase_grounding_during_initialization():
    parsed = parse_input_into_symbolic_structures(
        "A study proves there is evidence.",
        id_provider=lambda: "structure-001",
    )[0]

    result = assign_initial_scale_labels(
        [parsed],
        ArchitectureState(state_id="state-001"),
    )
    initialized = result.structures[0]

    assert initialized.structure_type is StructureType.CLAIM
    assert initialized.metadata.grounding_score == 0.0
    assert initialized.metadata.epistemic_status is EpistemicStatus.UNKNOWN
    grounding_check = next(
        check
        for check in result.threshold_checks
        if check.threshold_name == "grounding_threshold"
    )
    assert grounding_check.result is False


def test_threshold_checks_read_values_and_directions_from_architecture_state():
    state = ArchitectureState(
        state_id="state-001",
        thresholds=ThresholdState(
            grounding_threshold=0.42,
            persistence_threshold=0.37,
        ),
    )

    result = assign_initial_scale_labels(
        [make_structure()],
        state,
    )
    checks = {
        check.threshold_name: check
        for check in result.threshold_checks
    }

    assert state.thresholds.grounding_threshold == 0.42
    assert checks["grounding_threshold"].direction == "minimum_required"
    assert checks["grounding_threshold"].observed_value == 0.0
    assert checks["grounding_threshold"].threshold_value == 0.42
    assert checks["grounding_threshold"].result is False
    assert state.thresholds.persistence_threshold == 0.37
    assert checks["persistence_threshold"].direction == "minimum_required"
    assert checks["persistence_threshold"].threshold_value == 0.37
    assert checks["persistence_threshold"].result is False
    assert result.requires_review


def test_different_state_thresholds_change_result_without_hidden_constants():
    permissive = ArchitectureState(
        state_id="state-permissive",
        thresholds=ThresholdState(grounding_threshold=0.40),
    )
    strict = ArchitectureState(
        state_id="state-strict",
        thresholds=ThresholdState(grounding_threshold=0.60),
    )

    permissive_check = create_threshold_check(
        permissive,
        structure_id="structure-001",
        threshold_name="grounding_threshold",
        observed_value=0.50,
    )
    strict_check = create_threshold_check(
        strict,
        structure_id="structure-001",
        threshold_name="grounding_threshold",
        observed_value=0.50,
    )

    assert permissive_check.threshold_value == 0.40
    assert permissive_check.result is True
    assert strict_check.threshold_value == 0.60
    assert strict_check.result is False


def test_maximum_allowed_threshold_check_names_full_comparison():
    state = ArchitectureState(
        state_id="state-001",
        thresholds=ThresholdState(constitutional_risk_threshold=0.30),
    )

    check = create_threshold_check(
        state,
        structure_id="structure-001",
        threshold_name="constitutional_risk_threshold",
        observed_value=0.40,
    )

    assert check.threshold_name == "constitutional_risk_threshold"
    assert check.direction == "maximum_allowed"
    assert check.observed_value == 0.40
    assert check.threshold_value == 0.30
    assert check.result is False


def test_passing_provisional_thresholds_grants_no_status_or_authority():
    state = ArchitectureState(
        state_id="state-001",
        thresholds=ThresholdState(
            grounding_threshold=0.0,
            persistence_threshold=0.0,
        ),
    )

    result = assign_initial_scale_labels(
        [
            make_structure(
                StructureType.CONSTITUTIONAL_OBJECT,
                candidate_status=CandidateStatus.CONSTITUTIONAL_CANDIDATE,
            )
        ],
        state,
    )
    initialized = result.structures[0]

    assert all(check.result for check in result.threshold_checks)
    assert initialized.metadata.epistemic_status is EpistemicStatus.UNKNOWN
    assert initialized.metadata.persistence_score == 0.0
    assert initialized.metadata.scale_label is ScaleLabel.CLAIM
    assert (
        initialized.metadata.candidate_status
        is CandidateStatus.CONSTITUTIONAL_CANDIDATE
    )
    assert initialized.metadata.authority_level is AuthorityLevel.NONE


def test_metadata_initialization_rejects_reviewed_structure_state():
    reviewed = make_structure(
        current_state=SymbolicState.GROUNDED_PARTIAL,
    )

    with pytest.raises(
        MetadataInitializationError,
        match="cannot overwrite reviewed state",
    ):
        assign_initial_scale_labels(
            [reviewed],
            ArchitectureState(state_id="state-001"),
        )


def test_metadata_result_and_threshold_checks_serialize_readably():
    result = assign_initial_scale_labels(
        [make_structure()],
        ArchitectureState(state_id="state-001"),
    )

    diagnostics = json.loads(json.dumps(result.to_dict(), sort_keys=True))

    assert diagnostics["structures"][0]["metadata"]["uncertainty"] == 1.0
    assert diagnostics["threshold_checks"][0] == {
        "structure_id": "structure-001",
        "threshold_name": "grounding_threshold",
        "direction": "minimum_required",
        "observed_value": 0.0,
        "threshold_value": 0.7,
        "result": False,
    }
