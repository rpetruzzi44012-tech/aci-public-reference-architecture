"""Conservative metadata initialization and explicit threshold diagnostics."""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from dataclasses import dataclass, replace
from types import MappingProxyType

from .core import DiagnosticMixin, SymbolicMetadata, SymbolicStructure
from .enums import (
    AuthorityLevel,
    CandidateStatus,
    EpistemicStatus,
    ScaleLabel,
    StructureType,
    SymbolicState,
)
from .state import (
    ArchitectureState,
    ThresholdDirection,
    threshold_direction,
    threshold_passes,
)

INITIAL_SCALE_LABELS = frozenset(
    {
        ScaleLabel.OBSERVATION,
        ScaleLabel.CLAIM,
        ScaleLabel.HYPOTHESIS,
    }
)

_INITIAL_SCALE_BY_TYPE: Mapping[StructureType, ScaleLabel] = MappingProxyType(
    {
        StructureType.OBSERVATION: ScaleLabel.OBSERVATION,
        StructureType.HYPOTHESIS: ScaleLabel.HYPOTHESIS,
        StructureType.NOVELTY_CANDIDATE: ScaleLabel.HYPOTHESIS,
    }
)

_CANDIDATE_STATUS_BY_TYPE: Mapping[
    StructureType,
    CandidateStatus,
] = MappingProxyType(
    {
        StructureType.MEMORY_CANDIDATE:
            CandidateStatus.PERSISTENCE_CANDIDATE,
        StructureType.ARCHITECTURAL_CANDIDATE:
            CandidateStatus.ARCHITECTURE_CANDIDATE,
        StructureType.CONSTITUTIONAL_OBJECT:
            CandidateStatus.CONSTITUTIONAL_CANDIDATE,
    }
)

_INITIALIZABLE_STATES = frozenset(
    {
        SymbolicState.RECEIVED,
        SymbolicState.PARSED,
        SymbolicState.CANDIDATE,
    }
)


class MetadataInitializationError(ValueError):
    """Raised when initialization would overwrite reviewed status."""


@dataclass(frozen=True, slots=True)
class ThresholdCheck(DiagnosticMixin):
    """One visible comparison against architecture-owned threshold state."""

    structure_id: str
    threshold_name: str
    direction: ThresholdDirection
    observed_value: float
    threshold_value: float
    result: bool

    def __post_init__(self) -> None:
        _require_nonempty_text(self.structure_id, "structure_id")
        _require_nonempty_text(self.threshold_name, "threshold_name")
        if self.direction not in {"minimum_required", "maximum_allowed"}:
            raise ValueError("direction must be a known ThresholdDirection")
        _require_normalized(self.observed_value, "observed_value")
        _require_normalized(self.threshold_value, "threshold_value")
        if not isinstance(self.result, bool):
            raise TypeError("result must be bool")


@dataclass(frozen=True, slots=True)
class MetadataInitializationResult(DiagnosticMixin):
    """Initialized copies and the threshold evidence used during routing."""

    structures: tuple[SymbolicStructure, ...]
    threshold_checks: tuple[ThresholdCheck, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.structures, tuple):
            raise TypeError("structures must be a tuple")
        for position, structure in enumerate(self.structures):
            if not isinstance(structure, SymbolicStructure):
                raise TypeError(
                    f"structures[{position}] must be SymbolicStructure"
                )
        if not isinstance(self.threshold_checks, tuple):
            raise TypeError("threshold_checks must be a tuple")
        for position, check in enumerate(self.threshold_checks):
            if not isinstance(check, ThresholdCheck):
                raise TypeError(
                    f"threshold_checks[{position}] must be ThresholdCheck"
                )

    @property
    def requires_review(self) -> bool:
        return any(not check.result for check in self.threshold_checks)


def _require_nonempty_text(value: str, field_name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise MetadataInitializationError(
            f"{field_name} must be a nonempty string"
        )


def _require_normalized(value: float, field_name: str) -> None:
    if not isinstance(value, int | float) or isinstance(value, bool):
        raise TypeError(f"{field_name} must be numeric")
    if not 0.0 <= float(value) <= 1.0:
        raise ValueError(f"{field_name} must be in [0.0, 1.0]")


def initialize_metadata(
    *,
    origin: str,
    scale_label: ScaleLabel = ScaleLabel.CLAIM,
    candidate_status: CandidateStatus = CandidateStatus.NONE,
    audit_refs: Iterable[str] = (),
) -> SymbolicMetadata:
    """Create explicit metadata that contains no earned status."""

    _require_nonempty_text(origin, "origin")
    if not isinstance(scale_label, ScaleLabel):
        raise TypeError("scale_label must be ScaleLabel")
    if scale_label not in INITIAL_SCALE_LABELS:
        raise MetadataInitializationError(
            "initial scale cannot be memory, principle, architecture, "
            "or constitutional"
        )
    if not isinstance(candidate_status, CandidateStatus):
        raise TypeError("candidate_status must be CandidateStatus")
    if isinstance(audit_refs, str):
        raise TypeError("audit_refs must be an iterable of references")
    audit_ref_list = list(audit_refs)
    for position, audit_ref in enumerate(audit_ref_list):
        _require_nonempty_text(audit_ref, f"audit_refs[{position}]")

    return SymbolicMetadata(
        origin=origin,
        epistemic_status=EpistemicStatus.UNKNOWN,
        scale_label=scale_label,
        candidate_status=candidate_status,
        authority_level=AuthorityLevel.NONE,
        grounding_score=0.0,
        coherence_score=0.0,
        persistence_score=0.0,
        uncertainty=1.0,
        audit_refs=audit_ref_list,
    )


def create_threshold_check(
    architecture_state: ArchitectureState,
    *,
    structure_id: str,
    threshold_name: str,
    observed_value: float,
) -> ThresholdCheck:
    """Evaluate one named value against visible provisional state."""

    if not isinstance(architecture_state, ArchitectureState):
        raise TypeError("architecture_state must be ArchitectureState")
    _require_nonempty_text(structure_id, "structure_id")
    _require_nonempty_text(threshold_name, "threshold_name")
    _require_normalized(observed_value, "observed_value")
    direction = threshold_direction(threshold_name)
    threshold_value = getattr(
        architecture_state.thresholds,
        threshold_name,
    )
    return ThresholdCheck(
        structure_id=structure_id,
        threshold_name=threshold_name,
        direction=direction,
        observed_value=float(observed_value),
        threshold_value=float(threshold_value),
        result=threshold_passes(
            architecture_state.thresholds,
            threshold_name,
            observed_value,
        ),
    )


def assign_initial_scale_labels(
    structures: Iterable[SymbolicStructure],
    architecture_state: ArchitectureState,
) -> MetadataInitializationResult:
    """Return initialized copies and explicit non-authorizing threshold checks."""

    if not isinstance(architecture_state, ArchitectureState):
        raise TypeError("architecture_state must be ArchitectureState")

    initialized: list[SymbolicStructure] = []
    checks: list[ThresholdCheck] = []
    for position, structure in enumerate(structures):
        if not isinstance(structure, SymbolicStructure):
            raise TypeError(
                f"structures[{position}] must be SymbolicStructure"
            )
        if structure.current_state not in _INITIALIZABLE_STATES:
            raise MetadataInitializationError(
                "metadata initialization cannot overwrite reviewed state "
                f"{structure.current_state.value}"
            )

        scale_label = _INITIAL_SCALE_BY_TYPE.get(
            structure.structure_type,
            ScaleLabel.CLAIM,
        )
        candidate_status = structure.metadata.candidate_status
        if candidate_status is CandidateStatus.NONE:
            candidate_status = _CANDIDATE_STATUS_BY_TYPE.get(
                structure.structure_type,
                CandidateStatus.NONE,
            )
        metadata = initialize_metadata(
            origin=structure.metadata.origin,
            scale_label=scale_label,
            candidate_status=candidate_status,
            audit_refs=structure.metadata.audit_refs,
        )
        initialized_structure = replace(structure, metadata=metadata)
        initialized.append(initialized_structure)
        checks.extend(
            (
                create_threshold_check(
                    architecture_state,
                    structure_id=structure.structure_id,
                    threshold_name="grounding_threshold",
                    observed_value=metadata.grounding_score,
                ),
                create_threshold_check(
                    architecture_state,
                    structure_id=structure.structure_id,
                    threshold_name="persistence_threshold",
                    observed_value=metadata.persistence_score,
                ),
            )
        )

    return MetadataInitializationResult(
        structures=tuple(initialized),
        threshold_checks=tuple(checks),
    )


__all__ = [
    "INITIAL_SCALE_LABELS",
    "MetadataInitializationError",
    "MetadataInitializationResult",
    "ThresholdCheck",
    "assign_initial_scale_labels",
    "create_threshold_check",
    "initialize_metadata",
]
