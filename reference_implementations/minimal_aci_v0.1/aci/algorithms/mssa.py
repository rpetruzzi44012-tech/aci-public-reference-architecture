"""Simplified Multi-Scale Synchronization Algorithm for ACI v0.1.

MSSA compares achieved scale with requested candidacy. It may monitor an
aligned request, recommend demotion, block or reject an unearned jump, or
escalate unresolved authority. It never changes scale or metadata.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping
from dataclasses import dataclass
from enum import StrEnum, unique
from types import MappingProxyType
from uuid import uuid4

from ..core import (
    DiagnosticMixin,
    ReviewDecision,
    ScoreBundle,
    SymbolicStructure,
)
from ..enums import (
    AlgorithmName,
    CandidateStatus,
    DecisionStatus,
    DecisionType,
    ScaleLabel,
    StructureType,
)
from ..metadata import ThresholdCheck, create_threshold_check
from ..registry import SCALE_RANK
from ..review_context import ReviewContext, run_algorithm_where_required
from ..state import ArchitectureState

IDProvider = Callable[[], str]

CANDIDATE_REQUESTED_SCALES: Mapping[
    CandidateStatus,
    ScaleLabel | None,
] = MappingProxyType(
    {
        CandidateStatus.NONE: None,
        CandidateStatus.PERSISTENCE_CANDIDATE: ScaleLabel.MEMORY,
        CandidateStatus.PRINCIPLE_CANDIDATE: ScaleLabel.PRINCIPLE,
        CandidateStatus.ARCHITECTURE_CANDIDATE: ScaleLabel.ARCHITECTURE,
        CandidateStatus.CONSTITUTIONAL_CANDIDATE:
            ScaleLabel.CONSTITUTIONAL,
    }
)


class ScaleEvaluationError(RuntimeError):
    """Raised when MSSA cannot produce a valid registered judgment."""


@unique
class ScaleJumpDirection(StrEnum):
    NONE = "scale_jump.none"
    UPWARD = "scale_jump.upward"
    DOWNWARD = "scale_jump.downward"


@unique
class ScaleAlignmentOutcome(StrEnum):
    ALIGNED = "scale_outcome.aligned"
    DEMOTION_RECOMMENDED = "scale_outcome.demotion_recommended"
    DELAYED = "scale_outcome.delayed"
    REJECTED = "scale_outcome.rejected"
    ESCALATED = "scale_outcome.escalated"


@dataclass(frozen=True, slots=True)
class ScaleAssessment(DiagnosticMixin):
    """Typed scale-boundary judgment with no mutation authority."""

    target_id: str
    current_scale: ScaleLabel
    candidate_status: CandidateStatus
    requested_scale: ScaleLabel | None
    direction: ScaleJumpDirection
    distance: int
    multi_scale_coherence_score: float
    threshold_check: ThresholdCheck
    outcome: ScaleAlignmentOutcome
    escalation_target: AlgorithmName | None
    reasons: tuple[str, ...]

    def __post_init__(self) -> None:
        _require_nonempty_text(self.target_id, "target_id")
        if not isinstance(self.current_scale, ScaleLabel):
            raise TypeError("current_scale must be ScaleLabel")
        if not isinstance(self.candidate_status, CandidateStatus):
            raise TypeError("candidate_status must be CandidateStatus")
        expected_scale = CANDIDATE_REQUESTED_SCALES[self.candidate_status]
        if self.requested_scale is not expected_scale:
            raise ValueError(
                "requested_scale must match candidate_status mapping"
            )
        if not isinstance(self.direction, ScaleJumpDirection):
            raise TypeError("direction must be ScaleJumpDirection")
        if not isinstance(self.distance, int) or isinstance(
            self.distance,
            bool,
        ):
            raise TypeError("distance must be int")
        if self.distance < 0:
            raise ValueError("distance cannot be negative")
        _require_normalized(
            self.multi_scale_coherence_score,
            "multi_scale_coherence_score",
        )
        _validate_threshold_check(self)
        if not isinstance(self.outcome, ScaleAlignmentOutcome):
            raise TypeError("outcome must be ScaleAlignmentOutcome")
        if self.escalation_target is not None and not isinstance(
            self.escalation_target,
            AlgorithmName,
        ):
            raise TypeError(
                "escalation_target must be AlgorithmName or None"
            )
        if (
            self.outcome is ScaleAlignmentOutcome.ESCALATED
        ) != (self.escalation_target is not None):
            raise ValueError(
                "only escalated outcomes may name an escalation target"
            )
        if not isinstance(self.reasons, tuple) or not self.reasons:
            raise ValueError("reasons must be a nonempty tuple")
        for position, reason in enumerate(self.reasons):
            _require_nonempty_text(reason, f"reasons[{position}]")

        expected_direction, expected_distance = _classify_jump(
            self.current_scale,
            self.requested_scale,
        )
        if (
            self.direction is not expected_direction
            or self.distance != expected_distance
        ):
            raise ValueError(
                "direction and distance must match achieved/requested scales"
            )
        if (
            self.outcome is ScaleAlignmentOutcome.ALIGNED
            and self.direction is not ScaleJumpDirection.NONE
        ):
            raise ValueError("aligned outcome cannot contain a scale jump")

    @property
    def scale_jump_detected(self) -> bool:
        return self.direction is not ScaleJumpDirection.NONE

    @property
    def promotion_prohibited(self) -> bool:
        return self.direction is ScaleJumpDirection.UPWARD


def _default_id_provider() -> str:
    return f"decision-{uuid4()}"


def requested_scale_for_candidate(
    candidate_status: CandidateStatus,
) -> ScaleLabel | None:
    """Return the requested scale without changing achieved scale."""

    if not isinstance(candidate_status, CandidateStatus):
        raise TypeError("candidate_status must be CandidateStatus")
    return CANDIDATE_REQUESTED_SCALES[candidate_status]


def evaluate_scale_alignment(
    target: SymbolicStructure,
    architecture_state: ArchitectureState,
) -> ScaleAssessment:
    """Compare achieved scale and candidate request without promotion."""

    if not isinstance(target, SymbolicStructure):
        raise TypeError("target must be SymbolicStructure")
    if not isinstance(architecture_state, ArchitectureState):
        raise TypeError("architecture_state must be ArchitectureState")

    current_scale = target.metadata.scale_label
    candidate_status = target.metadata.candidate_status
    requested_scale = requested_scale_for_candidate(candidate_status)
    direction, distance = _classify_jump(
        current_scale,
        requested_scale,
    )
    max_distance = max(SCALE_RANK.values())
    score = 1.0 - (distance / max_distance)
    threshold_check = create_threshold_check(
        architecture_state,
        structure_id=target.structure_id,
        threshold_name="multi_scale_threshold",
        observed_value=score,
    )
    outcome, escalation_target = _route_scale_request(
        current_scale=current_scale,
        requested_scale=requested_scale,
        direction=direction,
    )
    return ScaleAssessment(
        target_id=target.structure_id,
        current_scale=current_scale,
        candidate_status=candidate_status,
        requested_scale=requested_scale,
        direction=direction,
        distance=distance,
        multi_scale_coherence_score=score,
        threshold_check=threshold_check,
        outcome=outcome,
        escalation_target=escalation_target,
        reasons=_build_reasons(
            current_scale=current_scale,
            candidate_status=candidate_status,
            requested_scale=requested_scale,
            direction=direction,
            distance=distance,
            outcome=outcome,
        ),
    )


def run_mssa_where_required(
    context: ReviewContext,
    *,
    id_provider: IDProvider = _default_id_provider,
) -> None:
    """Append MSSA decisions for explicit, unreviewed scale requests."""

    if not isinstance(context, ReviewContext):
        raise TypeError("context must be ReviewContext")
    if not callable(id_provider):
        raise TypeError("id_provider must be callable")

    def reviewer(review_context: ReviewContext) -> None:
        state_view = review_context.architecture_state
        for target in review_context.targets:
            if target.metadata.candidate_status is CandidateStatus.NONE:
                continue
            if review_context.latest_scale(target.structure_id) is not None:
                continue

            assessment = evaluate_scale_alignment(target, state_view)
            decision = _decision_from_assessment(
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
                raise ScaleEvaluationError(
                    "MSSA produced a registry-invalid decision: "
                    f"{codes}"
                )
            review_context.append_decision(decision)

    run_algorithm_where_required(context, reviewer)


def _classify_jump(
    current_scale: ScaleLabel,
    requested_scale: ScaleLabel | None,
) -> tuple[ScaleJumpDirection, int]:
    if requested_scale is None or requested_scale is current_scale:
        return ScaleJumpDirection.NONE, 0
    difference = (
        SCALE_RANK[requested_scale] - SCALE_RANK[current_scale]
    )
    if difference > 0:
        return ScaleJumpDirection.UPWARD, difference
    return ScaleJumpDirection.DOWNWARD, abs(difference)


def _route_scale_request(
    *,
    current_scale: ScaleLabel,
    requested_scale: ScaleLabel | None,
    direction: ScaleJumpDirection,
) -> tuple[ScaleAlignmentOutcome, AlgorithmName | None]:
    if direction is ScaleJumpDirection.NONE:
        return ScaleAlignmentOutcome.ALIGNED, None
    if direction is ScaleJumpDirection.DOWNWARD:
        return ScaleAlignmentOutcome.DEMOTION_RECOMMENDED, None
    if requested_scale is ScaleLabel.ARCHITECTURE:
        return ScaleAlignmentOutcome.ESCALATED, AlgorithmName.AEA
    if requested_scale is ScaleLabel.CONSTITUTIONAL:
        if SCALE_RANK[current_scale] >= SCALE_RANK[ScaleLabel.PRINCIPLE]:
            return ScaleAlignmentOutcome.ESCALATED, AlgorithmName.CGA
        return ScaleAlignmentOutcome.REJECTED, None
    return ScaleAlignmentOutcome.DELAYED, None


def _decision_from_assessment(
    assessment: ScaleAssessment,
    *,
    audit_id: str,
    decision_id: str,
) -> ReviewDecision:
    decision_type, status = _decision_route(assessment.outcome)
    return ReviewDecision(
        decision_id=decision_id,
        algorithm_name=AlgorithmName.MSSA,
        target_id=assessment.target_id,
        decision_type=decision_type,
        status=status,
        scores=ScoreBundle(
            multi_scale_coherence_score=(
                assessment.multi_scale_coherence_score
            ),
        ),
        rationale=_build_rationale(assessment),
        authorized=False,
        escalation_target=(
            assessment.escalation_target.value
            if assessment.escalation_target is not None
            else None
        ),
        audit_id=audit_id,
    )


def _decision_route(
    outcome: ScaleAlignmentOutcome,
) -> tuple[DecisionType, DecisionStatus]:
    if outcome is ScaleAlignmentOutcome.ALIGNED:
        return (
            DecisionType.APPROVE_WITH_MONITORING,
            DecisionStatus.MONITORING,
        )
    if outcome is ScaleAlignmentOutcome.DEMOTION_RECOMMENDED:
        return DecisionType.DEMOTE, DecisionStatus.PROVISIONAL
    if outcome is ScaleAlignmentOutcome.DELAYED:
        return DecisionType.DELAY, DecisionStatus.BLOCKED
    if outcome is ScaleAlignmentOutcome.REJECTED:
        return DecisionType.REJECT, DecisionStatus.FINAL
    return DecisionType.ESCALATE, DecisionStatus.ESCALATED


def _build_reasons(
    *,
    current_scale: ScaleLabel,
    candidate_status: CandidateStatus,
    requested_scale: ScaleLabel | None,
    direction: ScaleJumpDirection,
    distance: int,
    outcome: ScaleAlignmentOutcome,
) -> tuple[str, ...]:
    if requested_scale is None:
        return ("no scale-elevation candidacy was requested",)
    if direction is ScaleJumpDirection.NONE:
        return (
            "candidate request matches achieved scale but grants no authority",
        )
    if direction is ScaleJumpDirection.DOWNWARD:
        return (
            "candidate request is below achieved scale and requires "
            "demotion review",
        )
    if outcome is ScaleAlignmentOutcome.ESCALATED:
        return (
            f"{candidate_status.value} requests protected "
            f"{requested_scale.value} review from {current_scale.value}",
            "MSSA transfers unresolved review and grants no approval",
        )
    if outcome is ScaleAlignmentOutcome.REJECTED:
        return (
            "constitutional request bypasses required intermediate review "
            "layers",
        )
    return (
        f"unearned upward scale jump of {distance} level(s) is blocked",
    )


def _build_rationale(assessment: ScaleAssessment) -> str:
    threshold_result = (
        "passed" if assessment.threshold_check.result else "failed"
    )
    requested = (
        assessment.requested_scale.value
        if assessment.requested_scale is not None
        else "none"
    )
    escalation = (
        assessment.escalation_target.value
        if assessment.escalation_target is not None
        else "none"
    )
    return (
        f"MSSA outcome={assessment.outcome.value} for "
        f"{assessment.target_id}. Achieved scale="
        f"{assessment.current_scale.value}; candidate="
        f"{assessment.candidate_status.value}; requested scale={requested}; "
        f"direction={assessment.direction.value}; distance="
        f"{assessment.distance}. Multi-scale coherence score "
        f"{assessment.multi_scale_coherence_score:.3f} {threshold_result} "
        f"{assessment.threshold_check.threshold_name}="
        f"{assessment.threshold_check.threshold_value:.3f} "
        f"({assessment.threshold_check.direction}). Escalation target="
        f"{escalation}. Reasons: {'; '.join(assessment.reasons)}. "
        "Candidacy remains separate from achieved scale and authority; "
        "MSSA changed no metadata or graph state."
    )


def _validate_threshold_check(assessment: ScaleAssessment) -> None:
    check = assessment.threshold_check
    if not isinstance(check, ThresholdCheck):
        raise TypeError("threshold_check must be ThresholdCheck")
    if check.structure_id != assessment.target_id:
        raise ValueError("threshold_check must reference target_id")
    if check.threshold_name != "multi_scale_threshold":
        raise ValueError(
            "threshold_check must use multi_scale_threshold"
        )
    if (
        check.observed_value
        != assessment.multi_scale_coherence_score
    ):
        raise ValueError(
            "threshold observation must equal multi-scale coherence score"
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
    "CANDIDATE_REQUESTED_SCALES",
    "IDProvider",
    "ScaleAlignmentOutcome",
    "ScaleAssessment",
    "ScaleEvaluationError",
    "ScaleJumpDirection",
    "evaluate_scale_alignment",
    "requested_scale_for_candidate",
    "run_mssa_where_required",
]
