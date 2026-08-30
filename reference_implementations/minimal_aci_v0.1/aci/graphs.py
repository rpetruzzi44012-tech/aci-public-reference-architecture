"""Separated minimal graph containers for ACI prototype state."""

from __future__ import annotations

from dataclasses import dataclass, field

from .core import DiagnosticMixin, JSONValue, SymbolicStructure
from .enums import ScaleLabel
from .evidence import EvidenceLink, EvidenceObject


def _require_nonempty_text(value: str, field_name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a nonempty string")


def _require_record_list(
    values: list[dict[str, JSONValue]],
    field_name: str,
) -> None:
    if not isinstance(values, list):
        raise TypeError(f"{field_name} must be a list")
    for position, record in enumerate(values):
        if not isinstance(record, dict):
            raise TypeError(f"{field_name}[{position}] must be a dictionary")
        for key in record:
            _require_nonempty_text(key, f"{field_name}[{position}] key")


@dataclass(slots=True)
class MemoryGraph(DiagnosticMixin):
    """Persistent structures and relations earned through persistence review."""

    nodes: dict[str, SymbolicStructure] = field(default_factory=dict)
    persistence_relations: list[dict[str, JSONValue]] = field(
        default_factory=list
    )

    def __post_init__(self) -> None:
        if not isinstance(self.nodes, dict):
            raise TypeError("nodes must be a dictionary")
        for structure_id, structure in self.nodes.items():
            _require_nonempty_text(structure_id, "nodes key")
            if not isinstance(structure, SymbolicStructure):
                raise TypeError("nodes values must be SymbolicStructure")
            if structure.structure_id != structure_id:
                raise ValueError(
                    "memory node key must match SymbolicStructure.structure_id"
                )
        _require_record_list(
            self.persistence_relations,
            "persistence_relations",
        )


@dataclass(slots=True)
class EvidenceGraph(DiagnosticMixin):
    """Evidence-domain objects, typed links, and source relations."""

    evidence_objects: dict[str, EvidenceObject] = field(default_factory=dict)
    links: list[EvidenceLink] = field(default_factory=list)
    source_relations: list[dict[str, JSONValue]] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not isinstance(self.evidence_objects, dict):
            raise TypeError("evidence_objects must be a dictionary")
        for evidence_id, evidence in self.evidence_objects.items():
            _require_nonempty_text(evidence_id, "evidence_objects key")
            if not isinstance(evidence, EvidenceObject):
                raise TypeError(
                    "evidence_objects values must be EvidenceObject"
                )
            if evidence.evidence_id != evidence_id:
                raise ValueError(
                    "evidence object key must match EvidenceObject.evidence_id"
                )
        if not isinstance(self.links, list):
            raise TypeError("links must be a list")
        for position, link in enumerate(self.links):
            if not isinstance(link, EvidenceLink):
                raise TypeError(f"links[{position}] must be EvidenceLink")
        _require_record_list(self.source_relations, "source_relations")


@dataclass(slots=True)
class CoherenceGraph(DiagnosticMixin):
    """Compatibility relations and unresolved tension pressure."""

    relations: list[dict[str, JSONValue]] = field(default_factory=list)
    unresolved_tensions: list[str] = field(default_factory=list)
    coherence_pressure: float | None = None

    def __post_init__(self) -> None:
        _require_record_list(self.relations, "relations")
        if not isinstance(self.unresolved_tensions, list):
            raise TypeError("unresolved_tensions must be a list")
        for position, tension_id in enumerate(self.unresolved_tensions):
            _require_nonempty_text(
                tension_id,
                f"unresolved_tensions[{position}]",
            )
        if self.coherence_pressure is not None:
            if (
                not isinstance(self.coherence_pressure, int | float)
                or isinstance(self.coherence_pressure, bool)
            ):
                raise TypeError("coherence_pressure must be numeric or None")
            if self.coherence_pressure < 0.0:
                raise ValueError("coherence_pressure cannot be negative")


@dataclass(slots=True)
class ScaleGraph(DiagnosticMixin):
    """Structure scale labels and explicit mismatch records."""

    scale_labels: dict[str, ScaleLabel] = field(default_factory=dict)
    mismatch_records: list[dict[str, JSONValue]] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not isinstance(self.scale_labels, dict):
            raise TypeError("scale_labels must be a dictionary")
        for structure_id, scale_label in self.scale_labels.items():
            _require_nonempty_text(structure_id, "scale_labels key")
            if not isinstance(scale_label, ScaleLabel):
                raise TypeError("scale_labels values must be ScaleLabel")
        _require_record_list(self.mismatch_records, "mismatch_records")


@dataclass(slots=True)
class AuthorityGraph(DiagnosticMixin):
    """Possible authority, veto, and escalation relations among domains."""

    domains: list[str] = field(default_factory=list)
    authority_edges: list[dict[str, JSONValue]] = field(default_factory=list)
    veto_rules: list[dict[str, JSONValue]] = field(default_factory=list)
    escalation_rules: list[dict[str, JSONValue]] = field(
        default_factory=list
    )

    def __post_init__(self) -> None:
        if not isinstance(self.domains, list):
            raise TypeError("domains must be a list")
        for position, domain in enumerate(self.domains):
            _require_nonempty_text(domain, f"domains[{position}]")
        if len(self.domains) != len(set(self.domains)):
            raise ValueError("domains must be unique")
        _require_record_list(self.authority_edges, "authority_edges")
        _require_record_list(self.veto_rules, "veto_rules")
        _require_record_list(self.escalation_rules, "escalation_rules")


__all__ = [
    "AuthorityGraph",
    "CoherenceGraph",
    "EvidenceGraph",
    "MemoryGraph",
    "ScaleGraph",
]
