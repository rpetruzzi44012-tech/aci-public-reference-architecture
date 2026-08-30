"""Transparent input-to-candidate parsing for Minimal ACI v0.1.

The string convenience form uses ``input.raw`` as its origin ID. Stage 7 does
not split sentences or perform semantic proposition extraction. It creates one
candidate per input, while ``parse_structured_fixtures`` can create several
deterministic candidates for acceptance tests.
"""

from __future__ import annotations

import re
from collections.abc import Callable, Iterable, Mapping
from dataclasses import dataclass
from enum import StrEnum, unique
from types import MappingProxyType
from uuid import uuid4

from .core import InputObject, SymbolicStructure
from .enums import (
    CandidateStatus,
    StructureType,
    SymbolicState,
)
from .metadata import initialize_metadata

IDProvider = Callable[[], str]


class ParserInputError(ValueError):
    """Raised when parser input cannot form a traceable candidate."""


@unique
class ParserIntent(StrEnum):
    SPECULATION = "parser_intent.speculation"
    PERSISTENCE_REQUEST = "parser_intent.persistence_request"
    GOVERNANCE_REQUEST = "parser_intent.governance_request"
    ARCHITECTURE_REQUEST = "parser_intent.architecture_request"
    CONSTITUTIONAL_REQUEST = "parser_intent.constitutional_request"
    EVIDENCE_CLAIM = "parser_intent.evidence_claim"


LEXICAL_INTENT_PATTERNS: Mapping[ParserIntent, tuple[str, ...]] = MappingProxyType(
    {
        ParserIntent.CONSTITUTIONAL_REQUEST: (
            r"\bconstitution(?:al|ally)?\b",
            r"\binvariant(?:s)?\b",
        ),
        ParserIntent.ARCHITECTURE_REQUEST: (
            r"\barchitectur(?:e|al)\b",
            r"\bredesign\b",
            r"\bself[- ]modif(?:y|ication)\b",
        ),
        ParserIntent.GOVERNANCE_REQUEST: (
            r"\bgovern(?:ance|ed|ing)?\b",
            r"\bveto\b",
            r"\bauthori[sz](?:e|ed|ation)\b",
            r"\bescalat(?:e|ed|ion)\b",
        ),
        ParserIntent.PERSISTENCE_REQUEST: (
            r"\bremember\b",
            r"\bmemory\b",
            r"\bpersist(?:ence|ent|ently)?\b",
            r"\bpermanen(?:t|ce|tly)\b",
            r"\bretain(?:ed|ing)?\b",
            r"\barchive\b",
        ),
        ParserIntent.SPECULATION: (
            r"\bmaybe\b",
            r"\bperhaps\b",
            r"\bpossibly\b",
            r"\bi (?:think|suspect|wonder)\b",
            r"\bhypothes(?:is|ize)\b",
            r"\bspeculat(?:e|ion|ive)\b",
        ),
        ParserIntent.EVIDENCE_CLAIM: (
            r"\bevidence\b",
            r"\bstud(?:y|ies)\b",
            r"\bpro(?:of|ve|ves|ved)\b",
            r"\bbecause\b",
            r"\bsource(?:s)?\b",
        ),
    }
)

INTENT_PRIORITY = tuple(LEXICAL_INTENT_PATTERNS)

_STRUCTURE_TYPE_BY_INTENT: Mapping[ParserIntent, StructureType] = MappingProxyType(
    {
        ParserIntent.SPECULATION: StructureType.HYPOTHESIS,
        ParserIntent.PERSISTENCE_REQUEST: StructureType.MEMORY_CANDIDATE,
        ParserIntent.GOVERNANCE_REQUEST: StructureType.GOVERNANCE_OBJECT,
        ParserIntent.ARCHITECTURE_REQUEST: StructureType.ARCHITECTURAL_CANDIDATE,
        ParserIntent.CONSTITUTIONAL_REQUEST: StructureType.CONSTITUTIONAL_OBJECT,
        # Evidence language is still a claim until typed evidence exists.
        ParserIntent.EVIDENCE_CLAIM: StructureType.CLAIM,
    }
)

_CANDIDATE_STATUS_BY_INTENT: Mapping[
    ParserIntent,
    CandidateStatus,
] = MappingProxyType(
    {
        ParserIntent.PERSISTENCE_REQUEST:
            CandidateStatus.PERSISTENCE_CANDIDATE,
        ParserIntent.ARCHITECTURE_REQUEST:
            CandidateStatus.ARCHITECTURE_CANDIDATE,
        ParserIntent.CONSTITUTIONAL_REQUEST:
            CandidateStatus.CONSTITUTIONAL_CANDIDATE,
    }
)


@dataclass(frozen=True, slots=True)
class StructuredParseFixture:
    """Explicit parser intent for stable category-boundary tests."""

    input_id: str
    content: str
    intents: tuple[ParserIntent, ...] = ()
    audit_ref: str | None = None

    def __post_init__(self) -> None:
        _require_nonempty_text(self.input_id, "input_id")
        _require_nonempty_text(self.content, "content")
        if not isinstance(self.intents, tuple):
            raise TypeError("intents must be a tuple")
        for position, intent in enumerate(self.intents):
            if not isinstance(intent, ParserIntent):
                raise TypeError(
                    f"intents[{position}] must be ParserIntent"
                )
        if len(self.intents) != len(set(self.intents)):
            raise ValueError("intents must not contain duplicates")
        if self.audit_ref is not None:
            _require_nonempty_text(self.audit_ref, "audit_ref")


def _require_nonempty_text(value: str, field_name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ParserInputError(f"{field_name} must be a nonempty string")


def _default_id_provider() -> str:
    return f"structure-{uuid4()}"


def detect_lexical_intents(content: str) -> tuple[ParserIntent, ...]:
    """Return every matched intent in published, deterministic priority order."""

    _require_nonempty_text(content, "content")
    return tuple(
        intent
        for intent, patterns in LEXICAL_INTENT_PATTERNS.items()
        if any(re.search(pattern, content, re.IGNORECASE) for pattern in patterns)
    )


def _primary_intent(
    intents: Iterable[ParserIntent],
) -> ParserIntent | None:
    intent_set = set(intents)
    for intent in INTENT_PRIORITY:
        if intent in intent_set:
            return intent
    return None


def _create_candidate(
    input_object: InputObject,
    intents: tuple[ParserIntent, ...],
    id_provider: IDProvider,
) -> SymbolicStructure:
    primary_intent = _primary_intent(intents)
    structure_type = (
        _STRUCTURE_TYPE_BY_INTENT[primary_intent]
        if primary_intent is not None
        else StructureType.CLAIM
    )
    candidate_status = (
        _CANDIDATE_STATUS_BY_INTENT.get(
            primary_intent,
            CandidateStatus.NONE,
        )
        if primary_intent is not None
        else CandidateStatus.NONE
    )
    audit_refs = (
        [input_object.audit_ref]
        if input_object.audit_ref is not None
        else []
    )
    return SymbolicStructure(
        structure_id=id_provider(),
        content=input_object.content,
        structure_type=structure_type,
        current_state=SymbolicState.CANDIDATE,
        metadata=initialize_metadata(
            origin=input_object.input_id,
            candidate_status=candidate_status,
            audit_refs=audit_refs,
        ),
    )


def parse_input_into_symbolic_structures(
    input_value: InputObject | str,
    *,
    id_provider: IDProvider = _default_id_provider,
    string_input_id: str = "input.raw",
) -> list[SymbolicStructure]:
    """Create one provisional candidate without reviewing or storing it.

    A plain string is a convenience input. It receives ``string_input_id`` as
    its origin. Multi-sentence proposition extraction remains deferred.
    """

    if isinstance(input_value, str):
        _require_nonempty_text(string_input_id, "string_input_id")
        _require_nonempty_text(input_value, "content")
        input_object = InputObject(
            input_id=string_input_id,
            content=input_value,
            source="convenience-string",
        )
    elif isinstance(input_value, InputObject):
        _require_nonempty_text(input_value.content, "content")
        input_object = input_value
    else:
        raise TypeError("input_value must be InputObject or str")

    return [
        _create_candidate(
            input_object,
            detect_lexical_intents(input_object.content),
            id_provider,
        )
    ]


def parse_structured_fixtures(
    fixtures: Iterable[StructuredParseFixture],
    *,
    id_provider: IDProvider = _default_id_provider,
) -> list[SymbolicStructure]:
    """Create candidates from explicit intents without lexical recognition."""

    structures: list[SymbolicStructure] = []
    for position, fixture in enumerate(fixtures):
        if not isinstance(fixture, StructuredParseFixture):
            raise TypeError(
                f"fixtures[{position}] must be StructuredParseFixture"
            )
        input_object = InputObject(
            input_id=fixture.input_id,
            content=fixture.content,
            source="structured-fixture",
            audit_ref=fixture.audit_ref,
        )
        structures.append(
            _create_candidate(
                input_object,
                fixture.intents,
                id_provider,
            )
        )
    return structures


__all__ = [
    "IDProvider",
    "INTENT_PRIORITY",
    "LEXICAL_INTENT_PATTERNS",
    "ParserInputError",
    "ParserIntent",
    "StructuredParseFixture",
    "detect_lexical_intents",
    "parse_input_into_symbolic_structures",
    "parse_structured_fixtures",
]
