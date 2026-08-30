"""Simplified Grounding Evaluation Algorithm for ACI v0.1."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
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
    EpistemicStatus,
    EvidenceRelationType,
    StructureType,
    VerificationStatus,
)
from ..evidence import (
    EvidenceValidationError,
    is_grounding_eligible,
    links_for_target,
)
from ..metadata import ThresholdCheck, create_threshold_check
from ..review_context import ReviewContext, run_algorithm_where_required
from ..state import ArchitectureState

IDProvider = Callable[[], str]

_GEA_TARGET_TYPES = frozenset(
    {
        StructureType.CLAIM,
        StructureType.HYPOTHESIS,
    }
)


class GroundingEvaluationError(RuntimeError):
    """Raised when GEA cannot produce a valid registered judgment."""


@dataclass(frozen=True, slots=True)
class GroundingAssessment(DiagnosticMixin):
    """Typed grounding result that recommends no direct state mutation."""

    target_id: str
    epistemic_status: EpistemicStatus
    grounding_score: float
    threshold_check: ThresholdCheck
    supporting_evidence_ids: tuple[str, ...] = ()
    contradicting_evidence_ids: tuple[str, ...] = ()
    weakening_evidence_ids: tuple[str, ...] = ()
    non_supporting_verified_ids: tuple[str, ...] = ()
    unverified_evidence_ids: tuple[str, ...] = ()
    failed_verification_ids: tuple[str, ...] = ()
    invalid_evidence_ids: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        _require_nonempty_text(self.target_id, "target_id")
        if not isinstance(self.epistemic_status, EpistemicStatus):
            raise TypeError("epistemic_status must be EpistemicStatus")
        _require_normalized(self.grounding_score, "grounding_score")
        if not isinstance(self.threshold_check, ThresholdCheck):
            raise TypeError("threshold_check must be ThresholdCheck")
        if self.threshold_check.structure_id != self.target_id:
            raise ValueError("threshold_check must reference target_id")
        if self.threshold_check.threshold_name != "grounding_threshold":
            raise ValueError(
                "threshold_check must use grounding_threshold"
            )
        if self.threshold_check.observed_value != self.grounding_score:
            raise ValueError(
                "threshold_check observed value must equal grounding_score"
            )
        for field_name in (
            "supporting_evidence_ids",
            "contradicting_evidence_ids",
            "weakening_evidence_ids",
            "non_supporting_verified_ids",
            "unverified_evidence_ids",
            "failed_verification_ids",
            "invalid_evidence_ids",
        ):
            _require_reference_tuple(getattr(self, field_name), field_name)

    @property
    def unsupported(self) -> bool:
        return not self.supporting_evidence_ids

    @property
    def contradicted(self) -> bool:
        return bool(self.contradicting_evidence_ids)


def _default_id_provider() -> str:
    return f"decision-{uuid4()}"


def evaluate_grounding(
    target: SymbolicStructure,
    architecture_state: ArchitectureState,
) -> GroundingAssessment:
    """Classify typed evidence without changing state or target metadata."""

    if not isinstance(target, SymbolicStructure):
        raise TypeError("target must be SymbolicStructure")
    if target.structure_type not in _GEA_TARGET_TYPES:
        raise GroundingEvaluationError(
            "GEA evaluates only claim and hypothesis structures in v0.1"
        )
    if not isinstance(architecture_state, ArchitectureState):
        raise TypeError("architecture_state must be ArchitectureState")

    graph = architecture_state.evidence_graph
    target_ids = {target.structure_id}
    supporting: list[str] = []
    contradicting: list[str] = []
    weakening: list[str] = []
    non_supporting_verified: list[str] = []
    unverified: list[str] = []
    failed: list[str] = []
    invalid: list[str] = []

    for link in links_for_target(graph.links, target.structure_id):
        try:
            eligible = is_grounding_eligible(
                link,
                evidence_by_id=graph.evidence_objects,
                target_structure_ids=target_ids,
            )
        except EvidenceValidationError:
            invalid.append(link.evidence_id)
            continue

        if not eligible:
            if link.verification_status is VerificationStatus.FAILED:
                failed.append(link.evidence_id)
            else:
                unverified.append(link.evidence_id)
            continue

        if link.relation_type is EvidenceRelationType.SUPPORTS:
            supporting.append(link.evidence_id)
        elif link.relation_type is EvidenceRelationType.CONTRADICTS:
            contradicting.append(link.evidence_id)
        elif link.relation_type is EvidenceRelationType.WEAKENS:
            weakening.append(link.evidence_id)
        else:
            non_supporting_verified.append(link.evidence_id)

    evaluative_count = (
        len(supporting)
        + len(contradicting)
        + len(weakening)
    )
    grounding_score = (
        len(supporting) / evaluative_count
        if evaluative_count
        else 0.0
    )
    threshold_check = create_threshold_check(
        architecture_state,
        structure_id=target.structure_id,
        threshold_name="grounding_threshold",
        observed_value=grounding_score,
    )

    if contradicting:
        epistemic_status = EpistemicStatus.CONTRADICTED
    elif (
        supporting
        and not weakening
        and threshold_check.result
    ):
        epistemic_status = EpistemicStatus.PARTIALLY_GROUNDED
    elif target.structure_type is StructureType.HYPOTHESIS:
        epistemic_status = EpistemicStatus.SPECULATIVE
    else:
        epistemic_status = EpistemicStatus.UNGROUNDED

    return GroundingAssessment(
        target_id=target.structure_id,
        epistemic_status=epistemic_status,
        grounding_score=grounding_score,
        threshold_check=threshold_check,
        supporting_evidence_ids=tuple(supporting),
        contradicting_evidence_ids=tuple(contradicting),
        weakening_evidence_ids=tuple(weakening),
        non_supporting_verified_ids=tuple(non_supporting_verified),
        unverified_evidence_ids=tuple(unverified),
        failed_verification_ids=tuple(failed),
        invalid_evidence_ids=tuple(invalid),
    )


def run_gea_where_required(
    context: ReviewContext,
    *,
    id_provider: IDProvider = _default_id_provider,
) -> None:
    """Append one registered GEA decision for each unreviewed claim/hypothesis."""

    if not isinstance(context, ReviewContext):
        raise TypeError("context must be ReviewContext")
    if not callable(id_provider):
        raise TypeError("id_provider must be callable")

    def reviewer(review_context: ReviewContext) -> None:
        state_view = review_context.architecture_state
        for target in review_context.targets:
            if target.structure_type not in _GEA_TARGET_TYPES:
                continue
            if review_context.latest_by_algorithm(
                target.structure_id,
                AlgorithmName.GEA,
            ) is not None:
                continue

            assessment = evaluate_grounding(target, state_view)
            decision = _decision_from_assessment(
                target,
                assessment,
                audit_id=review_context.audit_id,
                decision_id=id_provider(),
            )
            validation = state_view.algorithm_registry.validate_decision(
                decision,
                target,
            )
            if not validation.accepted:
                codes = ", ".join(validation.reason_codes)
                raise GroundingEvaluationError(
                    "GEA produced a registry-invalid decision: "
                    f"{codes}"
                )
            review_context.append_decision(decision)

    run_algorithm_where_required(context, reviewer)


def _decision_from_assessment(
    target: SymbolicStructure,
    assessment: GroundingAssessment,
    *,
    audit_id: str,
    decision_id: str,
) -> ReviewDecision:
    decision_type, status = _route_assessment(target, assessment)
    return ReviewDecision(
        decision_id=decision_id,
        algorithm_name=AlgorithmName.GEA,
        target_id=target.structure_id,
        decision_type=decision_type,
        status=status,
        scores=ScoreBundle(
            grounding_score=assessment.grounding_score,
        ),
        rationale=_build_rationale(target, assessment),
        authorized=False,
        audit_id=audit_id,
    )


def _route_assessment(
    target: SymbolicStructure,
    assessment: GroundingAssessment,
) -> tuple[DecisionType, DecisionStatus]:
    if assessment.contradicted:
        if assessment.supporting_evidence_ids:
            return DecisionType.REVISE, DecisionStatus.PROVISIONAL
        return DecisionType.REJECT, DecisionStatus.FINAL
    if assessment.weakening_evidence_ids:
        return DecisionType.REVISE, DecisionStatus.PROVISIONAL
    if (
        assessment.supporting_evidence_ids
        and assessment.threshold_check.result
    ):
        return (
            DecisionType.APPROVE_WITH_MONITORING,
            DecisionStatus.MONITORING,
        )
    if target.structure_type is StructureType.HYPOTHESIS:
        return DecisionType.DELAY, DecisionStatus.PENDING_REVIEW
    return DecisionType.REVISE, DecisionStatus.PROVISIONAL


def _build_rationale(
    target: SymbolicStructure,
    assessment: GroundingAssessment,
) -> str:
    check = assessment.threshold_check
    result = "passed" if check.result else "failed"
    return (
        f"GEA recommends {assessment.epistemic_status.value} for "
        f"{target.structure_id}. Grounding score "
        f"{assessment.grounding_score:.3f} {result} "
        f"{check.threshold_name}={check.threshold_value:.3f} "
        f"({check.direction}). Verified supports="
        f"{len(assessment.supporting_evidence_ids)} "
        f"{assessment.supporting_evidence_ids}; verified contradictions="
        f"{len(assessment.contradicting_evidence_ids)} "
        f"{assessment.contradicting_evidence_ids}; verified weakening="
        f"{len(assessment.weakening_evidence_ids)} "
        f"{assessment.weakening_evidence_ids}; other verified relations="
        f"{len(assessment.non_supporting_verified_ids)}; unverified="
        f"{len(assessment.unverified_evidence_ids)}; failed verification="
        f"{len(assessment.failed_verification_ids)}; invalid references="
        f"{len(assessment.invalid_evidence_ids)}. Internal coherence and "
        "evidential wording were not counted as external evidence."
    )


def _require_nonempty_text(value: str, field_name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a nonempty string")


def _require_normalized(value: float, field_name: str) -> None:
    if not isinstance(value, int | float) or isinstance(value, bool):
        raise TypeError(f"{field_name} must be numeric")
    if not 0.0 <= float(value) <= 1.0:
        raise ValueError(f"{field_name} must be in [0.0, 1.0]")


def _require_reference_tuple(
    values: tuple[str, ...],
    field_name: str,
) -> None:
    if not isinstance(values, tuple):
        raise TypeError(f"{field_name} must be a tuple")
    for position, value in enumerate(values):
        _require_nonempty_text(value, f"{field_name}[{position}]")


__all__ = [
    "GroundingAssessment",
    "GroundingEvaluationError",
    "IDProvider",
    "evaluate_grounding",
    "run_gea_where_required",
]
