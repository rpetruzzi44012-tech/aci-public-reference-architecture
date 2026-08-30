"""Typed evidence boundary for Minimal ACI Prototype v0.1."""

from __future__ import annotations

from collections.abc import Collection, Iterable, Mapping
from dataclasses import dataclass

from .core import DiagnosticMixin
from .enums import EvidenceRelationType, VerificationStatus


class EvidenceValidationError(ValueError):
    """Raised when an evidence reference cannot be resolved consistently."""


def _require_nonempty_text(value: str, field_name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a nonempty string")


def _require_enum(value: object, enum_type: type[object], field_name: str) -> None:
    if not isinstance(value, enum_type):
        raise TypeError(f"{field_name} must be {enum_type.__name__}")


@dataclass(slots=True)
class EvidenceObject(DiagnosticMixin):
    """An identifiable evidence item with explicit source provenance."""

    evidence_id: str
    content: str
    source_ref: str

    def __post_init__(self) -> None:
        _require_nonempty_text(self.evidence_id, "evidence_id")
        if not isinstance(self.content, str):
            raise TypeError("content must be a string")
        _require_nonempty_text(self.source_ref, "source_ref")


@dataclass(frozen=True, slots=True)
class EvidenceLink(DiagnosticMixin):
    """An immutable typed relation between evidence and a symbolic target."""

    evidence_id: str
    target_structure_id: str
    source_ref: str
    relation_type: EvidenceRelationType
    verification_status: VerificationStatus

    def __post_init__(self) -> None:
        _require_nonempty_text(self.evidence_id, "evidence_id")
        _require_nonempty_text(self.target_structure_id, "target_structure_id")
        _require_nonempty_text(self.source_ref, "source_ref")
        _require_enum(
            self.relation_type,
            EvidenceRelationType,
            "relation_type",
        )
        _require_enum(
            self.verification_status,
            VerificationStatus,
            "verification_status",
        )


def build_evidence_index(
    evidence_objects: Iterable[EvidenceObject],
) -> dict[str, EvidenceObject]:
    """Build a transparent ID index and reject duplicate evidence IDs."""

    index: dict[str, EvidenceObject] = {}
    for position, evidence in enumerate(evidence_objects):
        if not isinstance(evidence, EvidenceObject):
            raise TypeError(
                f"evidence_objects[{position}] must be EvidenceObject"
            )
        if evidence.evidence_id in index:
            raise EvidenceValidationError(
                f"duplicate evidence_id: {evidence.evidence_id}"
            )
        index[evidence.evidence_id] = evidence
    return index


def lookup_evidence(
    evidence_id: str,
    evidence_by_id: Mapping[str, EvidenceObject],
) -> EvidenceObject | None:
    """Return evidence by ID while detecting malformed or mismatched indexes."""

    _require_nonempty_text(evidence_id, "evidence_id")
    evidence = evidence_by_id.get(evidence_id)
    if evidence is None:
        return None
    if not isinstance(evidence, EvidenceObject):
        raise TypeError("evidence index values must be EvidenceObject")
    if evidence.evidence_id != evidence_id:
        raise EvidenceValidationError(
            "evidence index key does not match EvidenceObject.evidence_id"
        )
    return evidence


def links_for_target(
    links: Iterable[EvidenceLink],
    target_structure_id: str,
) -> tuple[EvidenceLink, ...]:
    """Return typed links for one target without interpreting their content."""

    _require_nonempty_text(target_structure_id, "target_structure_id")
    matching: list[EvidenceLink] = []
    for position, link in enumerate(links):
        if not isinstance(link, EvidenceLink):
            raise TypeError(f"links[{position}] must be EvidenceLink")
        if link.target_structure_id == target_structure_id:
            matching.append(link)
    return tuple(matching)


def validate_evidence_link(
    link: EvidenceLink,
    *,
    evidence_by_id: Mapping[str, EvidenceObject],
    target_structure_ids: Collection[str],
) -> EvidenceObject:
    """Resolve a link against known evidence and symbolic target identifiers."""

    if not isinstance(link, EvidenceLink):
        raise TypeError("link must be EvidenceLink")

    known_targets: set[str] = set()
    for position, target_id in enumerate(target_structure_ids):
        _require_nonempty_text(target_id, f"target_structure_ids[{position}]")
        known_targets.add(target_id)

    evidence = lookup_evidence(link.evidence_id, evidence_by_id)
    if evidence is None:
        raise EvidenceValidationError(
            f"unknown evidence_id: {link.evidence_id}"
        )
    if link.target_structure_id not in known_targets:
        raise EvidenceValidationError(
            f"unknown target_structure_id: {link.target_structure_id}"
        )
    if link.source_ref != evidence.source_ref:
        raise EvidenceValidationError(
            "EvidenceLink.source_ref does not match EvidenceObject.source_ref"
        )
    return evidence


def is_grounding_eligible(
    link: EvidenceLink,
    *,
    evidence_by_id: Mapping[str, EvidenceObject],
    target_structure_ids: Collection[str],
) -> bool:
    """Report eligibility for later grounding review without changing grounding."""

    validate_evidence_link(
        link,
        evidence_by_id=evidence_by_id,
        target_structure_ids=target_structure_ids,
    )
    return link.verification_status is VerificationStatus.VERIFIED


__all__ = [
    "EvidenceLink",
    "EvidenceObject",
    "EvidenceValidationError",
    "build_evidence_index",
    "is_grounding_eligible",
    "links_for_target",
    "lookup_evidence",
    "validate_evidence_link",
]
