import json

import pytest

from aci.core import InputObject, ReviewDecision, SymbolicStructure
from aci.enums import (
    AuthorityLevel,
    CandidateStatus,
    EpistemicStatus,
    ScaleLabel,
    StructureType,
    SymbolicState,
)
from aci.evidence import EvidenceLink, EvidenceObject
from aci.parser import (
    LEXICAL_INTENT_PATTERNS,
    ParserInputError,
    ParserIntent,
    StructuredParseFixture,
    detect_lexical_intents,
    parse_input_into_symbolic_structures,
    parse_structured_fixtures,
)
from aci.state import ArchitectureState


def sequential_ids(*values):
    return iter(values).__next__


def assert_conservative_candidate(structure):
    assert isinstance(structure, SymbolicStructure)
    assert structure.current_state is SymbolicState.CANDIDATE
    assert structure.metadata.epistemic_status is EpistemicStatus.UNKNOWN
    assert structure.metadata.scale_label is ScaleLabel.CLAIM
    assert structure.metadata.authority_level is AuthorityLevel.NONE
    assert structure.metadata.grounding_score == 0.0
    assert structure.metadata.coherence_score == 0.0
    assert structure.metadata.persistence_score == 0.0
    assert structure.metadata.uncertainty == 1.0
    assert structure.current_state not in {
        SymbolicState.PERSISTENT,
        SymbolicState.QUALIFIED_PERSISTENT,
        SymbolicState.ARCHITECTURAL_REVIEW,
        SymbolicState.GOVERNANCE_REVIEW,
        SymbolicState.CONSTITUTIONAL_REVIEW,
    }


def test_input_object_becomes_traceable_candidate_before_review():
    input_object = InputObject(
        input_id="input-001",
        content="A plain claim.",
        audit_ref="audit-001",
    )

    structures = parse_input_into_symbolic_structures(
        input_object,
        id_provider=lambda: "structure-001",
    )

    assert len(structures) == 1
    structure = structures[0]
    assert structure.structure_id == "structure-001"
    assert structure.content == input_object.content
    assert structure.structure_type is StructureType.CLAIM
    assert structure.metadata.origin == "input-001"
    assert structure.metadata.audit_refs == ["audit-001"]
    assert_conservative_candidate(structure)
    assert not isinstance(structure, ReviewDecision)


def test_string_convenience_input_has_documented_origin_and_deterministic_id():
    structure = parse_input_into_symbolic_structures(
        "A convenience claim.",
        id_provider=lambda: "structure-fixed",
    )[0]

    assert structure.structure_id == "structure-fixed"
    assert structure.metadata.origin == "input.raw"
    assert structure.content == "A convenience claim."
    assert_conservative_candidate(structure)


@pytest.mark.parametrize(
    ("content", "intent", "structure_type", "candidate_status"),
    [
        (
            "Maybe this is a useful hypothesis.",
            ParserIntent.SPECULATION,
            StructureType.HYPOTHESIS,
            CandidateStatus.NONE,
        ),
        (
            "Remember this permanently.",
            ParserIntent.PERSISTENCE_REQUEST,
            StructureType.MEMORY_CANDIDATE,
            CandidateStatus.PERSISTENCE_CANDIDATE,
        ),
        (
            "Escalate this through governance.",
            ParserIntent.GOVERNANCE_REQUEST,
            StructureType.GOVERNANCE_OBJECT,
            CandidateStatus.NONE,
        ),
        (
            "Redesign the architecture.",
            ParserIntent.ARCHITECTURE_REQUEST,
            StructureType.ARCHITECTURAL_CANDIDATE,
            CandidateStatus.ARCHITECTURE_CANDIDATE,
        ),
        (
            "Make this a constitutional invariant.",
            ParserIntent.CONSTITUTIONAL_REQUEST,
            StructureType.CONSTITUTIONAL_OBJECT,
            CandidateStatus.CONSTITUTIONAL_CANDIDATE,
        ),
        (
            "A study proves there is evidence.",
            ParserIntent.EVIDENCE_CLAIM,
            StructureType.CLAIM,
            CandidateStatus.NONE,
        ),
    ],
)
def test_lexical_intent_changes_only_provisional_classification(
    content,
    intent,
    structure_type,
    candidate_status,
):
    assert intent in detect_lexical_intents(content)

    structure = parse_input_into_symbolic_structures(
        content,
        id_provider=lambda: "structure-001",
    )[0]

    assert structure.structure_type is structure_type
    assert structure.metadata.candidate_status is candidate_status
    assert_conservative_candidate(structure)


def test_multi_intent_input_exposes_all_matches_but_uses_fixed_priority():
    content = (
        "Permanent evidence should redesign the architecture as a "
        "constitutional invariant."
    )

    intents = detect_lexical_intents(content)
    structure = parse_input_into_symbolic_structures(
        content,
        id_provider=lambda: "structure-001",
    )[0]

    assert intents == (
        ParserIntent.CONSTITUTIONAL_REQUEST,
        ParserIntent.ARCHITECTURE_REQUEST,
        ParserIntent.PERSISTENCE_REQUEST,
        ParserIntent.EVIDENCE_CLAIM,
    )
    assert structure.structure_type is StructureType.CONSTITUTIONAL_OBJECT
    assert (
        structure.metadata.candidate_status
        is CandidateStatus.CONSTITUTIONAL_CANDIDATE
    )
    assert_conservative_candidate(structure)


def test_structured_fixtures_bypass_keywords_without_bypassing_boundaries():
    fixtures = [
        StructuredParseFixture(
            input_id="fixture-001",
            content="opaque alpha",
            intents=(ParserIntent.PERSISTENCE_REQUEST,),
        ),
        StructuredParseFixture(
            input_id="fixture-002",
            content="opaque beta",
            intents=(ParserIntent.ARCHITECTURE_REQUEST,),
        ),
        StructuredParseFixture(
            input_id="fixture-003",
            content="opaque gamma",
            intents=(ParserIntent.CONSTITUTIONAL_REQUEST,),
        ),
    ]

    structures = parse_structured_fixtures(
        fixtures,
        id_provider=sequential_ids(
            "structure-001",
            "structure-002",
            "structure-003",
        ),
    )

    assert [item.structure_id for item in structures] == [
        "structure-001",
        "structure-002",
        "structure-003",
    ]
    assert [item.metadata.candidate_status for item in structures] == [
        CandidateStatus.PERSISTENCE_CANDIDATE,
        CandidateStatus.ARCHITECTURE_CANDIDATE,
        CandidateStatus.CONSTITUTIONAL_CANDIDATE,
    ]
    for structure in structures:
        assert_conservative_candidate(structure)


def test_evidence_language_never_creates_typed_evidence_or_grounding():
    structure = parse_input_into_symbolic_structures(
        "There is evidence because a study proves it.",
        id_provider=lambda: "structure-001",
    )[0]

    assert structure.structure_type is StructureType.CLAIM
    assert not isinstance(structure, EvidenceObject)
    assert not isinstance(structure, EvidenceLink)
    assert structure.metadata.grounding_score == 0.0
    assert structure.metadata.epistemic_status is EpistemicStatus.UNKNOWN


def test_parser_has_no_path_to_graph_or_architecture_state_mutation():
    state = ArchitectureState(state_id="state-001")
    before = state.to_dict()

    structure = parse_input_into_symbolic_structures(
        "Remember this constitutional architecture permanently.",
        id_provider=lambda: "structure-001",
    )[0]

    assert state.to_dict() == before
    assert state.active_structures == {}
    assert state.memory_graph.nodes == {}
    assert state.evidence_graph.evidence_objects == {}
    assert state.evidence_graph.links == []
    assert state.governance_state.authority_graph.domains == []
    assert structure.structure_id not in state.active_structures
    assert_conservative_candidate(structure)


def test_permanent_and_constitutional_words_do_not_grant_achieved_status():
    persistence = parse_input_into_symbolic_structures(
        "Keep this permanent.",
        id_provider=lambda: "structure-persistence",
    )[0]
    constitutional = parse_input_into_symbolic_structures(
        "This should be constitutional.",
        id_provider=lambda: "structure-constitutional",
    )[0]

    assert (
        persistence.metadata.candidate_status
        is CandidateStatus.PERSISTENCE_CANDIDATE
    )
    assert persistence.metadata.scale_label is not ScaleLabel.MEMORY
    assert persistence.current_state is not SymbolicState.PERSISTENT
    assert (
        constitutional.metadata.candidate_status
        is CandidateStatus.CONSTITUTIONAL_CANDIDATE
    )
    assert constitutional.metadata.scale_label is not ScaleLabel.CONSTITUTIONAL
    assert (
        constitutional.metadata.authority_level
        is not AuthorityLevel.CONSTITUTIONAL_AUTHORITY
    )


def test_multi_sentence_semantic_extraction_remains_deferred():
    content = "First claim. Second claim. Is this a question?"

    structures = parse_input_into_symbolic_structures(
        content,
        id_provider=lambda: "structure-001",
    )

    assert len(structures) == 1
    assert structures[0].content == content


def test_parser_output_serializes_readably():
    structure = parse_input_into_symbolic_structures(
        "Maybe preserve this.",
        id_provider=lambda: "structure-001",
    )[0]

    serialized = json.loads(json.dumps(structure.to_dict(), sort_keys=True))

    assert serialized["structure_id"] == "structure-001"
    assert serialized["current_state"] == "symbolic_state.candidate"
    assert serialized["metadata"]["authority_level"] == "authority.none"
    assert serialized["metadata"]["scale_label"] == "scale.claim"


def test_lexical_rule_table_is_read_only():
    with pytest.raises(TypeError):
        LEXICAL_INTENT_PATTERNS[ParserIntent.SPECULATION] = (r".*",)


@pytest.mark.parametrize(
    "input_value",
    ["", "   ", None, 42],
)
def test_invalid_raw_input_is_rejected(input_value):
    expected_error = ParserInputError if isinstance(input_value, str) else TypeError
    with pytest.raises(expected_error):
        parse_input_into_symbolic_structures(input_value)


def test_invalid_fixture_and_identifier_are_rejected():
    with pytest.raises(TypeError, match=r"fixtures\[0\]"):
        parse_structured_fixtures(["not-a-fixture"])

    with pytest.raises(TypeError, match="intents must be a tuple"):
        StructuredParseFixture(
            input_id="fixture-001",
            content="opaque",
            intents=[ParserIntent.SPECULATION],
        )

    with pytest.raises(ValueError, match="structure_id"):
        parse_input_into_symbolic_structures(
            "A valid claim.",
            id_provider=lambda: "",
        )
