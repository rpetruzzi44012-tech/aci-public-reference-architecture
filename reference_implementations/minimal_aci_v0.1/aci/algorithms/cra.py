"""Simplified Coherence Repair Algorithm for ACI v0.1.

This module compares explicit normalized proposition fields. It does not
perform general semantic contradiction detection or infer logical negation
from keywords in free text.
"""

from __future__ import annotations

from collections.abc import Callable, Iterable
from dataclasses import dataclass
from enum import StrEnum, unique
from uuid import uuid4

from ..core import (
    DiagnosticMixin,
    ReviewDecision,
    ScoreBundle,
    SymbolicStructure,
)
from ..enums import (
    AlgorithmName,
    DecisionStatus,
    DecisionType,
)
from ..metadata import ThresholdCheck, create_threshold_check
from ..review_context import (
    ReviewContext,
    UnresolvedReviewItem,
    run_algorithm_where_required,
)
from ..state import ArchitectureState

IDProvider = Callable[[], str]


class CoherenceEvaluationError(RuntimeError):
    """Raised when CRA cannot produce a valid bounded judgment."""


@unique
class PropositionPolarity(StrEnum):
    AFFIRMED = "proposition_polarity.affirmed"
    DENIED = "proposition_polarity.denied"


@unique
class CoherenceRelation(StrEnum):
    COMPATIBLE = "coherence_relation.compatible"
    DIRECT_CONTRADICTION = "coherence_relation.direct_contradiction"
    UNRESOLVED = "coherence_relation.unresolved"


@dataclass(frozen=True, slots=True)
class NormalizedProposition(DiagnosticMixin):
    """A lexical comparison form; it carries no grounding authority."""

    structure_id: str
    subject: str
    relation: str
    object_value: str
    polarity: PropositionPolarity

    def __post_init__(self) -> None:
        _require_nonempty_text(self.structure_id, "structure_id")
        for field_name in ("subject", "relation", "object_value"):
            value = getattr(self, field_name)
            normalized = normalize_proposition_field(value)
            object.__setattr__(self, field_name, normalized)
        if not isinstance(self.polarity, PropositionPolarity):
            raise TypeError("polarity must be PropositionPolarity")


@dataclass(frozen=True, slots=True)
class PropositionComparisonFixture(DiagnosticMixin):
    """One explicit comparison used instead of inferred text semantics."""

    comparison_id: str
    target: NormalizedProposition
    counterpart: NormalizedProposition

    def __post_init__(self) -> None:
        _require_nonempty_text(self.comparison_id, "comparison_id")
        if not isinstance(self.target, NormalizedProposition):
            raise TypeError("target must be NormalizedProposition")
        if not isinstance(self.counterpart, NormalizedProposition):
            raise TypeError("counterpart must be NormalizedProposition")
        if self.target.structure_id == self.counterpart.structure_id:
            raise ValueError(
                "comparison requires two distinct structure identifiers"
            )


@dataclass(frozen=True, slots=True)
class CoherenceAssessment(DiagnosticMixin):
    """Typed comparison result that recommends no direct graph mutation."""

    comparison_id: str
    target_id: str
    counterpart_id: str
    relation: CoherenceRelation
    coherence_score: float
    coherence_pressure: float
    threshold_check: ThresholdCheck

    def __post_init__(self) -> None:
        _require_nonempty_text(self.comparison_id, "comparison_id")
        _require_nonempty_text(self.target_id, "target_id")
        _require_nonempty_text(self.counterpart_id, "counterpart_id")
        if self.target_id == self.counterpart_id:
            raise ValueError("assessment requires distinct structure IDs")
        if not isinstance(self.relation, CoherenceRelation):
            raise TypeError("relation must be CoherenceRelation")
        _require_normalized(self.coherence_score, "coherence_score")
        _require_normalized(
            self.coherence_pressure,
            "coherence_pressure",
        )
        if self.coherence_score + self.coherence_pressure != 1.0:
            raise ValueError(
                "coherence_score and coherence_pressure must sum to 1.0"
            )
        if not isinstance(self.threshold_check, ThresholdCheck):
            raise TypeError("threshold_check must be ThresholdCheck")
        if self.threshold_check.structure_id != self.target_id:
            raise ValueError("threshold_check must reference target_id")
        if self.threshold_check.threshold_name != "coherence_threshold":
            raise ValueError(
                "threshold_check must use coherence_threshold"
            )
        if (
            self.threshold_check.observed_value
            != self.coherence_pressure
        ):
            raise ValueError(
                "threshold observation must equal coherence_pressure"
            )

    @property
    def requires_tension_preservation(self) -> bool:
        return self.relation is not CoherenceRelation.COMPATIBLE


def normalize_proposition_field(value: str) -> str:
    """Apply only visible lexical normalization: trim, casefold, collapse."""

    _require_nonempty_text(value, "proposition field")
    return " ".join(value.casefold().split())


def compare_propositions(
    fixture: PropositionComparisonFixture,
    architecture_state: ArchitectureState,
) -> CoherenceAssessment:
    """Compare explicit fields without attempting general semantic inference."""

    if not isinstance(fixture, PropositionComparisonFixture):
        raise TypeError("fixture must be PropositionComparisonFixture")
    if not isinstance(architecture_state, ArchitectureState):
        raise TypeError("architecture_state must be ArchitectureState")

    target = fixture.target
    counterpart = fixture.counterpart
    same_proposition = (
        target.subject == counterpart.subject
        and target.relation == counterpart.relation
        and target.object_value == counterpart.object_value
    )
    if same_proposition and target.polarity is not counterpart.polarity:
        relation = CoherenceRelation.DIRECT_CONTRADICTION
        coherence_pressure = 1.0
    elif same_proposition:
        relation = CoherenceRelation.COMPATIBLE
        coherence_pressure = 0.0
    else:
        relation = CoherenceRelation.UNRESOLVED
        coherence_pressure = 0.5

    coherence_score = 1.0 - coherence_pressure
    threshold_check = create_threshold_check(
        architecture_state,
        structure_id=target.structure_id,
        threshold_name="coherence_threshold",
        observed_value=coherence_pressure,
    )
    return CoherenceAssessment(
        comparison_id=fixture.comparison_id,
        target_id=target.structure_id,
        counterpart_id=counterpart.structure_id,
        relation=relation,
        coherence_score=coherence_score,
        coherence_pressure=coherence_pressure,
        threshold_check=threshold_check,
    )


def _default_decision_id_provider() -> str:
    return f"decision-{uuid4()}"


def _default_unresolved_id_provider() -> str:
    return f"unresolved-{uuid4()}"


def run_cra_where_required(
    context: ReviewContext,
    comparisons: Iterable[PropositionComparisonFixture] = (),
    *,
    decision_id_provider: IDProvider = _default_decision_id_provider,
    unresolved_id_provider: IDProvider = _default_unresolved_id_provider,
) -> None:
    """Append CRA decisions and preserve tensions in ReviewContext only."""

    if not isinstance(context, ReviewContext):
        raise TypeError("context must be ReviewContext")
    if not callable(decision_id_provider):
        raise TypeError("decision_id_provider must be callable")
    if not callable(unresolved_id_provider):
        raise TypeError("unresolved_id_provider must be callable")
    fixtures = tuple(comparisons)
    for position, fixture in enumerate(fixtures):
        if not isinstance(fixture, PropositionComparisonFixture):
            raise TypeError(
                f"comparisons[{position}] must be "
                "PropositionComparisonFixture"
            )
    target_ids = [fixture.target.structure_id for fixture in fixtures]
    if len(target_ids) != len(set(target_ids)):
        raise CoherenceEvaluationError(
            "v0.1 permits one CRA comparison per target per review call"
        )

    def reviewer(review_context: ReviewContext) -> None:
        state_view = review_context.architecture_state
        for fixture in fixtures:
            target = review_context.get_target(
                fixture.target.structure_id
            )
            review_context.get_target(
                fixture.counterpart.structure_id
            )
            if review_context.latest_by_algorithm(
                target.structure_id,
                AlgorithmName.CRA,
            ) is not None:
                continue

            assessment = compare_propositions(fixture, state_view)
            grounding_score, grounding_source = (
                _preserved_grounding(review_context, target)
            )
            decision = _decision_from_assessment(
                target,
                assessment,
                grounding_score=grounding_score,
                grounding_source=grounding_source,
                audit_id=review_context.audit_id,
                decision_id=decision_id_provider(),
            )
            validation = state_view.algorithm_registry.validate_decision(
                decision,
                target,
            )
            if not validation.accepted:
                codes = ", ".join(validation.reason_codes)
                raise CoherenceEvaluationError(
                    "CRA produced a registry-invalid decision: "
                    f"{codes}"
                )
            review_context.append_decision(decision)
            if assessment.requires_tension_preservation:
                review_context.record_unresolved(
                    UnresolvedReviewItem(
                        item_id=unresolved_id_provider(),
                        target_id=target.structure_id,
                        reason=_build_unresolved_reason(assessment),
                        decision_ref=decision.decision_id,
                    )
                )

    run_algorithm_where_required(context, reviewer)


def _preserved_grounding(
    context: ReviewContext,
    target: SymbolicStructure,
) -> tuple[float, str]:
    grounding_decision = context.latest_grounding(target.structure_id)
    if grounding_decision is not None:
        return (
            grounding_decision.scores.grounding_score,
            f"GEA decision {grounding_decision.decision_id}",
        )
    return (
        target.metadata.grounding_score,
        "authoritative target metadata snapshot",
    )


def _decision_from_assessment(
    target: SymbolicStructure,
    assessment: CoherenceAssessment,
    *,
    grounding_score: float,
    grounding_source: str,
    audit_id: str,
    decision_id: str,
) -> ReviewDecision:
    decision_type, status = _route_assessment(assessment)
    return ReviewDecision(
        decision_id=decision_id,
        algorithm_name=AlgorithmName.CRA,
        target_id=target.structure_id,
        decision_type=decision_type,
        status=status,
        scores=ScoreBundle(
            grounding_score=grounding_score,
            coherence_score=assessment.coherence_score,
        ),
        rationale=_build_rationale(
            assessment,
            grounding_score,
            grounding_source,
        ),
        authorized=False,
        audit_id=audit_id,
    )


def _route_assessment(
    assessment: CoherenceAssessment,
) -> tuple[DecisionType, DecisionStatus]:
    if assessment.relation is CoherenceRelation.DIRECT_CONTRADICTION:
        return DecisionType.REPAIR, DecisionStatus.PROVISIONAL
    if assessment.relation is CoherenceRelation.UNRESOLVED:
        return DecisionType.DELAY, DecisionStatus.PENDING_REVIEW
    return (
        DecisionType.APPROVE_WITH_MONITORING,
        DecisionStatus.MONITORING,
    )


def _build_rationale(
    assessment: CoherenceAssessment,
    grounding_score: float,
    grounding_source: str,
) -> str:
    check = assessment.threshold_check
    threshold_result = "passed" if check.result else "failed"
    return (
        f"CRA classified comparison {assessment.comparison_id} between "
        f"{assessment.target_id} and {assessment.counterpart_id} as "
        f"{assessment.relation.value}. Coherence pressure "
        f"{assessment.coherence_pressure:.3f} {threshold_result} "
        f"{check.threshold_name}={check.threshold_value:.3f} "
        f"({check.direction}); compatibility score="
        f"{assessment.coherence_score:.3f}. Grounding score "
        f"{grounding_score:.3f} was preserved from {grounding_source}; "
        "CRA created no evidence and granted no grounding."
    )


def _build_unresolved_reason(
    assessment: CoherenceAssessment,
) -> str:
    return (
        f"{assessment.relation.value} remains unresolved for comparison "
        f"{assessment.comparison_id} between {assessment.target_id} and "
        f"{assessment.counterpart_id}; state recording requires a later "
        "authorized plan."
    )


def _require_nonempty_text(value: str, field_name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a nonempty string")


def _require_normalized(value: float, field_name: str) -> None:
    if not isinstance(value, int | float) or isinstance(value, bool):
        raise TypeError(f"{field_name} must be numeric")
    if not 0.0 <= float(value) <= 1.0:
        raise ValueError(f"{field_name} must be in [0.0, 1.0]")


__all__ = [
    "CoherenceAssessment",
    "CoherenceEvaluationError",
    "CoherenceRelation",
    "NormalizedProposition",
    "PropositionComparisonFixture",
    "PropositionPolarity",
    "compare_propositions",
    "normalize_proposition_field",
    "run_cra_where_required",
]
