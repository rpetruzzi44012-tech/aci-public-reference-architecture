import json
from dataclasses import FrozenInstanceError

import pytest

from aci.core import InputObject, SymbolicMetadata, SymbolicStructure
from aci.enums import (
    AuthorityLevel,
    CandidateStatus,
    EpistemicStatus,
    EvidenceRelationType,
    ScaleLabel,
    StructureType,
    SymbolicState,
    VerificationStatus,
)
from aci.evidence import (
    EvidenceLink,
    EvidenceObject,
    EvidenceValidationError,
    build_evidence_index,
    is_grounding_eligible,
    links_for_target,
    lookup_evidence,
    validate_evidence_link,
)


def make_evidence(
    *,
    evidence_id: str = "evidence-001",
    source_ref: str = "source://study-001",
) -> EvidenceObject:
    return EvidenceObject(
        evidence_id=evidence_id,
        content="Measured result from the named source.",
        source_ref=source_ref,
    )


def make_link(
    *,
    evidence_id: str = "evidence-001",
    target_structure_id: str = "structure-001",
    source_ref: str = "source://study-001",
    relation_type: EvidenceRelationType = EvidenceRelationType.SUPPORTS,
    verification_status: VerificationStatus = VerificationStatus.VERIFIED,
) -> EvidenceLink:
    return EvidenceLink(
        evidence_id=evidence_id,
        target_structure_id=target_structure_id,
        source_ref=source_ref,
        relation_type=relation_type,
        verification_status=verification_status,
    )


def make_structure(content: str) -> SymbolicStructure:
    return SymbolicStructure(
        structure_id="structure-001",
        content=content,
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


def test_evidence_objects_and_links_serialize_readably():
    evidence = make_evidence()
    link = make_link()

    assert json.loads(json.dumps(evidence.to_dict())) == {
        "evidence_id": "evidence-001",
        "content": "Measured result from the named source.",
        "source_ref": "source://study-001",
    }
    assert json.loads(json.dumps(link.to_dict())) == {
        "evidence_id": "evidence-001",
        "target_structure_id": "structure-001",
        "source_ref": "source://study-001",
        "relation_type": "evidence_relation.supports",
        "verification_status": "verification.verified",
    }


def test_evidence_link_is_immutable():
    link = make_link()

    with pytest.raises(FrozenInstanceError):
        link.evidence_id = "evidence-002"


def test_verified_link_is_eligible_after_reference_validation():
    evidence = make_evidence()
    index = build_evidence_index([evidence])
    link = make_link()

    assert (
        validate_evidence_link(
            link,
            evidence_by_id=index,
            target_structure_ids={"structure-001"},
        )
        is evidence
    )
    assert is_grounding_eligible(
        link,
        evidence_by_id=index,
        target_structure_ids={"structure-001"},
    )


@pytest.mark.parametrize(
    "verification_status",
    [VerificationStatus.UNVERIFIED, VerificationStatus.FAILED],
)
def test_nonverified_links_are_not_grounding_eligible(verification_status):
    evidence = make_evidence()
    index = build_evidence_index([evidence])
    link = make_link(verification_status=verification_status)

    assert not is_grounding_eligible(
        link,
        evidence_by_id=index,
        target_structure_ids={"structure-001"},
    )


def test_missing_evidence_object_invalidates_link():
    link = make_link(evidence_id="evidence-missing")

    with pytest.raises(
        EvidenceValidationError,
        match="unknown evidence_id: evidence-missing",
    ):
        validate_evidence_link(
            link,
            evidence_by_id={},
            target_structure_ids={"structure-001"},
        )


def test_missing_target_invalidates_link():
    evidence = make_evidence()
    link = make_link(target_structure_id="structure-missing")

    with pytest.raises(
        EvidenceValidationError,
        match="unknown target_structure_id: structure-missing",
    ):
        validate_evidence_link(
            link,
            evidence_by_id=build_evidence_index([evidence]),
            target_structure_ids={"structure-001"},
        )


def test_mismatched_source_reference_invalidates_link():
    evidence = make_evidence(source_ref="source://canonical")
    link = make_link(source_ref="source://different")

    with pytest.raises(EvidenceValidationError, match="source_ref does not match"):
        validate_evidence_link(
            link,
            evidence_by_id=build_evidence_index([evidence]),
            target_structure_ids={"structure-001"},
        )


def test_mismatched_evidence_index_key_is_detected():
    evidence = make_evidence(evidence_id="evidence-canonical")

    with pytest.raises(EvidenceValidationError, match="index key does not match"):
        lookup_evidence("evidence-alias", {"evidence-alias": evidence})


def test_duplicate_evidence_identifiers_are_rejected():
    with pytest.raises(EvidenceValidationError, match="duplicate evidence_id"):
        build_evidence_index([make_evidence(), make_evidence()])


@pytest.mark.parametrize(
    ("field_name", "field_value"),
    [
        ("evidence_id", ""),
        ("target_structure_id", " "),
        ("source_ref", ""),
    ],
)
def test_malformed_link_identifiers_are_rejected(field_name, field_value):
    values = {
        "evidence_id": "evidence-001",
        "target_structure_id": "structure-001",
        "source_ref": "source://study-001",
    }
    values[field_name] = field_value

    with pytest.raises(ValueError, match=field_name):
        make_link(**values)


def test_malformed_link_enum_family_is_rejected():
    with pytest.raises(TypeError, match="relation_type"):
        make_link(relation_type=VerificationStatus.VERIFIED)

    with pytest.raises(TypeError, match="verification_status"):
        make_link(verification_status=EvidenceRelationType.SUPPORTS)


def test_lookup_helpers_are_explicit_about_found_missing_and_target_scope():
    evidence = make_evidence()
    index = build_evidence_index([evidence])
    target_link = make_link()
    other_link = make_link(target_structure_id="structure-002")

    assert lookup_evidence("evidence-001", index) is evidence
    assert lookup_evidence("evidence-missing", index) is None
    assert links_for_target(
        [target_link, other_link],
        "structure-001",
    ) == (target_link,)
    assert links_for_target([], "structure-001") == ()


def test_rhetorical_evidence_language_has_no_evidential_authority():
    content = "There is evidence because a study proves this claim."
    input_object = InputObject(input_id="input-001", content=content)
    structure = make_structure(content)
    evidence_index = build_evidence_index([])
    links = links_for_target([], structure.structure_id)

    assert input_object.content == content
    assert structure.metadata.grounding_score == 0.0
    assert evidence_index == {}
    assert links == ()
    assert not any(
        is_grounding_eligible(
            link,
            evidence_by_id=evidence_index,
            target_structure_ids={structure.structure_id},
        )
        for link in links
    )
