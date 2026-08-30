"""Simplified Persistence and Consolidation Algorithm for ACI v0.1.

PCA recommends whether a persistence candidate may proceed, should remain only
in a non-authoritative archive, must wait, or must be rejected. It does not
write memory, update metadata, or apply state changes.
"""

from __future__ import annotations

from collections.abc import Callable
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
    CandidateStatus,
    DecisionStatus,
    DecisionType,
)
from ..metadata import ThresholdCheck, create_threshold_check
from ..registry import SCALE_RANK
from ..review_context import ReviewContext, run_algorithm_where_required
from ..state import ArchitectureState

IDProvider = Callable[[], str]

_GROUNDING_APPROVALS = frozenset(
    {
        DecisionType.APPROVE,
        DecisionType.APPROVE_WITH_MONITORING,
    }
)
_COHERENCE_APPROVALS = frozenset(
    {
        DecisionType.APPROVE,
        DecisionType.APPROVE_WITH_MONITORING,
    }
)
_BLOCKING_STATUSES = frozenset(
    {
        DecisionStatus.BLOCKED,
        DecisionStatus.ESCALATED,
        DecisionStatus.PENDING_REVIEW,
    }
)
_CONTRADICTION_DECISIONS = frozenset(
    {
        DecisionType.REPAIR,
        DecisionType.REJECT,
        DecisionType.RETRACT,
    }
)


class PersistenceEvaluationError(RuntimeError):
    """Raised when PCA cannot produce a valid registered judgment."""


@unique
class PersistenceOutcome(StrEnum):
    """Non-mutating PCA recommendation categories."""

    PERSIST_RECOMMENDED = "persistence_outcome.persist_recommended"
    ARCHIVE_RECOMMENDED = "persistence_outcome.archive_recommended"
    DELAYED = "persistence_outcome.delayed"
    REJECTED = "persistence_outcome.rejected"
    UNRESOLVED = "persistence_outcome.unresolved"


@dataclass(frozen=True, slots=True)
class PersistenceAssessment(DiagnosticMixin):
    """Typed gate result that grants no memory or mutation authority."""

    target_id: str
    outcome: PersistenceOutcome
    gea_decision_ref: str | None
    cra_decision_ref: str | None
    grounding_score: float
    coherence_score: float
    persistence_score: float
    grounding_check: ThresholdCheck
    persistence_check: ThresholdCheck
    grounding_eligible: bool
    coherence_eligible: bool
    candidate_eligible: bool
    audit_eligible: bool
    authority_eligible: bool
    disqualifying_contradiction: bool
    unresolved_dependency: bool
    reasons: tuple[str, ...]

    def __post_init__(self) -> None:
        _require_nonempty_text(self.target_id, "target_id")
        if not isinstance(self.outcome, PersistenceOutcome):
            raise TypeError("outcome must be PersistenceOutcome")
        _require_optional_reference(
            self.gea_decision_ref,
            "gea_decision_ref",
        )
        _require_optional_reference(
            self.cra_decision_ref,
            "cra_decision_ref",
        )
        for field_name in (
            "grounding_score",
            "coherence_score",
            "persistence_score",
        ):
            _require_normalized(getattr(self, field_name), field_name)
        _validate_threshold_check(
            self.grounding_check,
            target_id=self.target_id,
            threshold_name="grounding_threshold",
            observed_value=self.grounding_score,
        )
        _validate_threshold_check(
            self.persistence_check,
            target_id=self.target_id,
            threshold_name="persistence_threshold",
            observed_value=self.persistence_score,
        )
        for field_name in (
            "grounding_eligible",
            "coherence_eligible",
            "candidate_eligible",
            "audit_eligible",
            "authority_eligible",
            "disqualifying_contradiction",
            "unresolved_dependency",
        ):
            if not isinstance(getattr(self, field_name), bool):
                raise TypeError(f"{field_name} must be bool")
        if not isinstance(self.reasons, tuple) or not self.reasons:
            raise ValueError("reasons must be a nonempty tuple")
        for position, reason in enumerate(self.reasons):
            _require_nonempty_text(reason, f"reasons[{position}]")

        all_required_gates = (
            self.grounding_eligible
            and self.coherence_eligible
            and self.candidate_eligible
            and self.audit_eligible
            and self.authority_eligible
        )
        if self.outcome is PersistenceOutcome.PERSIST_RECOMMENDED and (
            not all_required_gates
            or not self.persistence_check.result
            or self.disqualifying_contradiction
            or self.unresolved_dependency
        ):
            raise ValueError(
                "persistence recommendation requires every gate and "
                "threshold to pass without contradiction or unresolved review"
            )


def _default_id_provider() -> str:
    return f"decision-{uuid4()}"


def evaluate_persistence_candidate(
    context: ReviewContext,
    target_id: str,
) -> PersistenceAssessment:
    """Evaluate explicit persistence gates using prior GEA and CRA decisions."""

    if not isinstance(context, ReviewContext):
        raise TypeError("context must be ReviewContext")
    _require_nonempty_text(target_id, "target_id")

    target = context.get_target(target_id)
    state_view = context.architecture_state
    gea_decision = context.latest_grounding(target_id)
    cra_decision = context.latest_coherence(target_id)

    grounding_score = (
        gea_decision.scores.grounding_score
        if gea_decision is not None
        else 0.0
    )
    coherence_score = (
        cra_decision.scores.coherence_score
        if cra_decision is not None
        else 0.0
    )
    grounding_check = create_threshold_check(
        state_view,
        structure_id=target_id,
        threshold_name="grounding_threshold",
        observed_value=grounding_score,
    )

    grounding_eligible = (
        gea_decision is not None
        and gea_decision.decision_type in _GROUNDING_APPROVALS
        and gea_decision.status not in _BLOCKING_STATUSES
        and grounding_check.result
    )
    linked_cra_tension = (
        cra_decision is not None
        and any(
            item.decision_ref == cra_decision.decision_id
            for item in context.unresolved_for(target_id)
        )
    )
    coherence_eligible = (
        cra_decision is not None
        and cra_decision.decision_type in _COHERENCE_APPROVALS
        and cra_decision.status not in _BLOCKING_STATUSES
        and not linked_cra_tension
    )
    candidate_eligible = (
        target.metadata.candidate_status
        is CandidateStatus.PERSISTENCE_CANDIDATE
    )
    audit_eligible = context.audit_id in target.metadata.audit_refs
    authority_eligible = _registry_authority_permits(
        state_view,
        target,
    )

    required_gates = (
        grounding_eligible,
        coherence_eligible,
        candidate_eligible,
        audit_eligible,
        authority_eligible,
    )
    persistence_score = sum(required_gates) / len(required_gates)
    persistence_check = create_threshold_check(
        state_view,
        structure_id=target_id,
        threshold_name="persistence_threshold",
        observed_value=persistence_score,
    )

    disqualifying_contradiction = (
        (
            gea_decision is not None
            and gea_decision.decision_type is DecisionType.REJECT
        )
        or (
            cra_decision is not None
            and cra_decision.decision_type in _CONTRADICTION_DECISIONS
        )
    )
    missing_dependency = gea_decision is None or cra_decision is None
    unresolved_dependency = (
        missing_dependency
        or linked_cra_tension
        or (
            gea_decision is not None
            and (
                gea_decision.status in _BLOCKING_STATUSES
                or gea_decision.decision_type
                in {DecisionType.DELAY, DecisionType.ESCALATE}
            )
        )
        or (
            cra_decision is not None
            and (
                cra_decision.status in _BLOCKING_STATUSES
                or cra_decision.decision_type
                in {DecisionType.DELAY, DecisionType.ESCALATE}
            )
        )
    )

    outcome = _route_outcome(
        grounding_eligible=grounding_eligible,
        coherence_eligible=coherence_eligible,
        candidate_eligible=candidate_eligible,
        audit_eligible=audit_eligible,
        authority_eligible=authority_eligible,
        persistence_threshold_passed=persistence_check.result,
        disqualifying_contradiction=disqualifying_contradiction,
        unresolved_dependency=unresolved_dependency,
    )
    reasons = _build_reasons(
        gea_decision=gea_decision,
        cra_decision=cra_decision,
        grounding_eligible=grounding_eligible,
        coherence_eligible=coherence_eligible,
        candidate_eligible=candidate_eligible,
        audit_eligible=audit_eligible,
        authority_eligible=authority_eligible,
        disqualifying_contradiction=disqualifying_contradiction,
        unresolved_dependency=unresolved_dependency,
    )
    return PersistenceAssessment(
        target_id=target_id,
        outcome=outcome,
        gea_decision_ref=(
            gea_decision.decision_id
            if gea_decision is not None
            else None
        ),
        cra_decision_ref=(
            cra_decision.decision_id
            if cra_decision is not None
            else None
        ),
        grounding_score=grounding_score,
        coherence_score=coherence_score,
        persistence_score=persistence_score,
        grounding_check=grounding_check,
        persistence_check=persistence_check,
        grounding_eligible=grounding_eligible,
        coherence_eligible=coherence_eligible,
        candidate_eligible=candidate_eligible,
        audit_eligible=audit_eligible,
        authority_eligible=authority_eligible,
        disqualifying_contradiction=disqualifying_contradiction,
        unresolved_dependency=unresolved_dependency,
        reasons=reasons,
    )


def run_pca_where_required(
    context: ReviewContext,
    *,
    id_provider: IDProvider = _default_id_provider,
) -> None:
    """Append registered PCA judgments for unreviewed persistence candidates."""

    if not isinstance(context, ReviewContext):
        raise TypeError("context must be ReviewContext")
    if not callable(id_provider):
        raise TypeError("id_provider must be callable")

    def reviewer(review_context: ReviewContext) -> None:
        state_view = review_context.architecture_state
        for target in review_context.targets:
            if (
                target.metadata.candidate_status
                is not CandidateStatus.PERSISTENCE_CANDIDATE
            ):
                continue
            if review_context.latest_persistence(
                target.structure_id
            ) is not None:
                continue

            assessment = evaluate_persistence_candidate(
                review_context,
                target.structure_id,
            )
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
                raise PersistenceEvaluationError(
                    "PCA produced a registry-invalid decision: "
                    f"{codes}"
                )
            review_context.append_decision(decision)

    run_algorithm_where_required(context, reviewer)


def _registry_authority_permits(
    architecture_state: ArchitectureState,
    target: SymbolicStructure,
) -> bool:
    spec = architecture_state.algorithm_registry.get_spec(
        AlgorithmName.PCA
    )
    return (
        target.structure_type in spec.permitted_structure_types
        and SCALE_RANK[target.metadata.scale_label]
        <= SCALE_RANK[spec.maximum_target_scale]
        and spec.state_mutation_prohibited
        and not spec.stub
        and not spec.coordinator
    )


def _route_outcome(
    *,
    grounding_eligible: bool,
    coherence_eligible: bool,
    candidate_eligible: bool,
    audit_eligible: bool,
    authority_eligible: bool,
    persistence_threshold_passed: bool,
    disqualifying_contradiction: bool,
    unresolved_dependency: bool,
) -> PersistenceOutcome:
    if disqualifying_contradiction:
        return PersistenceOutcome.REJECTED
    if unresolved_dependency:
        return PersistenceOutcome.UNRESOLVED
    if not candidate_eligible or not audit_eligible or not authority_eligible:
        return PersistenceOutcome.DELAYED
    if not grounding_eligible:
        return PersistenceOutcome.ARCHIVE_RECOMMENDED
    if not coherence_eligible:
        return PersistenceOutcome.UNRESOLVED
    if not persistence_threshold_passed:
        return PersistenceOutcome.DELAYED
    return PersistenceOutcome.PERSIST_RECOMMENDED


def _decision_from_assessment(
    assessment: PersistenceAssessment,
    *,
    audit_id: str,
    decision_id: str,
) -> ReviewDecision:
    decision_type, status = _decision_route(assessment.outcome)
    return ReviewDecision(
        decision_id=decision_id,
        algorithm_name=AlgorithmName.PCA,
        target_id=assessment.target_id,
        decision_type=decision_type,
        status=status,
        scores=ScoreBundle(
            grounding_score=assessment.grounding_score,
            coherence_score=assessment.coherence_score,
            persistence_score=assessment.persistence_score,
        ),
        rationale=_build_rationale(assessment),
        authorized=False,
        audit_id=audit_id,
    )


def _decision_route(
    outcome: PersistenceOutcome,
) -> tuple[DecisionType, DecisionStatus]:
    if outcome is PersistenceOutcome.PERSIST_RECOMMENDED:
        return DecisionType.PERSIST, DecisionStatus.PROVISIONAL
    if outcome is PersistenceOutcome.ARCHIVE_RECOMMENDED:
        return DecisionType.ARCHIVE, DecisionStatus.FINAL
    if outcome is PersistenceOutcome.REJECTED:
        return DecisionType.REJECT, DecisionStatus.FINAL
    if outcome is PersistenceOutcome.UNRESOLVED:
        return DecisionType.DELAY, DecisionStatus.PENDING_REVIEW
    return DecisionType.DELAY, DecisionStatus.BLOCKED


def _build_reasons(
    *,
    gea_decision: ReviewDecision | None,
    cra_decision: ReviewDecision | None,
    grounding_eligible: bool,
    coherence_eligible: bool,
    candidate_eligible: bool,
    audit_eligible: bool,
    authority_eligible: bool,
    disqualifying_contradiction: bool,
    unresolved_dependency: bool,
) -> tuple[str, ...]:
    reasons: list[str] = []
    if gea_decision is None:
        reasons.append("missing GEA decision")
    elif not grounding_eligible:
        reasons.append("GEA did not establish threshold-sufficient grounding")
    if cra_decision is None:
        reasons.append("missing CRA decision")
    elif not coherence_eligible:
        reasons.append(
            "CRA did not clear contradiction and unresolved-tension review"
        )
    if not candidate_eligible:
        reasons.append("target lacks explicit persistence candidacy")
    if not audit_eligible:
        reasons.append("target is not bound to the current pending audit")
    if not authority_eligible:
        reasons.append("PCA registry authority does not cover the target")
    if disqualifying_contradiction:
        reasons.append("a prior review records disqualifying contradiction")
    if unresolved_dependency:
        reasons.append("a required dependency remains unresolved")
    if not reasons:
        reasons.append("all required persistence-review gates passed")
    return tuple(reasons)


def _build_rationale(assessment: PersistenceAssessment) -> str:
    grounding_result = (
        "passed" if assessment.grounding_check.result else "failed"
    )
    persistence_result = (
        "passed" if assessment.persistence_check.result else "failed"
    )
    return (
        f"PCA outcome={assessment.outcome.value} for "
        f"{assessment.target_id}. GEA={assessment.gea_decision_ref}; "
        f"CRA={assessment.cra_decision_ref}. Grounding score "
        f"{assessment.grounding_score:.3f} {grounding_result} "
        f"{assessment.grounding_check.threshold_name}="
        f"{assessment.grounding_check.threshold_value:.3f} "
        f"({assessment.grounding_check.direction}). Persistence gate score "
        f"{assessment.persistence_score:.3f} {persistence_result} "
        f"{assessment.persistence_check.threshold_name}="
        f"{assessment.persistence_check.threshold_value:.3f} "
        f"({assessment.persistence_check.direction}). Gate results: "
        f"grounding={assessment.grounding_eligible}, "
        f"coherence={assessment.coherence_eligible}, "
        f"candidacy={assessment.candidate_eligible}, "
        f"audit={assessment.audit_eligible}, "
        f"registry_authority={assessment.authority_eligible}. "
        f"Reasons: {'; '.join(assessment.reasons)}. This is a review "
        "recommendation only: archive is non-authoritative, and PCA wrote "
        "neither memory nor metadata."
    )


def _validate_threshold_check(
    check: ThresholdCheck,
    *,
    target_id: str,
    threshold_name: str,
    observed_value: float,
) -> None:
    if not isinstance(check, ThresholdCheck):
        raise TypeError(f"{threshold_name} check must be ThresholdCheck")
    if check.structure_id != target_id:
        raise ValueError("threshold check must reference target_id")
    if check.threshold_name != threshold_name:
        raise ValueError(
            f"threshold check must use {threshold_name}"
        )
    if check.observed_value != observed_value:
        raise ValueError(
            "threshold check observed value must equal assessed score"
        )


def _require_nonempty_text(value: str, field_name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a nonempty string")


def _require_optional_reference(
    value: str | None,
    field_name: str,
) -> None:
    if value is not None:
        _require_nonempty_text(value, field_name)


def _require_normalized(value: float, field_name: str) -> None:
    if not isinstance(value, int | float) or isinstance(value, bool):
        raise TypeError(f"{field_name} must be numeric")
    if not 0.0 <= float(value) <= 1.0:
        raise ValueError(f"{field_name} must be in [0.0, 1.0]")


__all__ = [
    "IDProvider",
    "PersistenceAssessment",
    "PersistenceEvaluationError",
    "PersistenceOutcome",
    "evaluate_persistence_candidate",
    "run_pca_where_required",
]
