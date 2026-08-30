"""Protected algorithm stubs for Minimal ACI Prototype v0.1.

IPA, SRA, NGSA, and AEA retain typed detection and routing boundaries without
claiming the full canonical capabilities their names represent. Each reviewer
may append a registry-valid ``ReviewDecision`` and may not mutate architecture
state, metadata, graphs, budgets, thresholds, or governance posture.
"""

from __future__ import annotations

import re
from collections.abc import Callable, Iterable, Mapping
from dataclasses import dataclass, field
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
    BudgetType,
    CandidateStatus,
    DecisionStatus,
    DecisionType,
    StructureType,
)
from ..metadata import ThresholdCheck, create_threshold_check
from ..review_context import ReviewContext, run_algorithm_where_required
from ..state import (
    ArchitectureState,
    BudgetPressureLevel,
    budget_pressure,
)

IDProvider = Callable[[], str]

_PRESSURED_BUDGET_LEVELS = frozenset({"low", "critical", "exhausted"})
_SEVERE_BUDGET_LEVELS = frozenset({"critical", "exhausted"})
_IDENTITY_RISK_PATTERNS: Mapping[str, tuple[str, ...]] = MappingProxyType(
    {
        "identity_risk": (
            r"\bidentity risk\b",
            r"\bidentity continuity (?:risk|failure|loss)\b",
        ),
        "identity_kernel_change": (
            r"\b(?:change|modify|replace|remove)\b.{0,30}\bidentity kernel\b",
        ),
        "invariant_loss": (
            r"\binvariant (?:loss|failure|removal)\b",
            r"\bremove\b.{0,30}\bprotected invariant\b",
        ),
        "lineage_loss": (
            r"\blineage (?:loss|break|failure)\b",
            r"\berase\b.{0,30}\blineage\b",
        ),
    }
)
_NOVELTY_PATTERNS = (
    r"\bnovel(?:ty)?\b",
    r"\bnew hypothesis\b",
    r"\bnew candidate\b",
    r"\bcounterfactual\b",
    r"\bwhat if\b",
)


class ProtectedStubError(RuntimeError):
    """Raised when a protected stub cannot issue a registered judgment."""


@dataclass(frozen=True, slots=True)
class StubReviewFixture(DiagnosticMixin):
    """Explicit trigger data for stable tests and structured callers."""

    target_id: str
    identity_risk_flags: tuple[str, ...] = ()
    novelty_claim: bool = False

    def __post_init__(self) -> None:
        _require_nonempty_text(self.target_id, "target_id")
        if not isinstance(self.identity_risk_flags, tuple):
            raise TypeError("identity_risk_flags must be a tuple")
        for position, flag in enumerate(self.identity_risk_flags):
            _require_nonempty_text(
                flag,
                f"identity_risk_flags[{position}]",
            )
        if len(self.identity_risk_flags) != len(
            set(self.identity_risk_flags)
        ):
            raise ValueError("identity_risk_flags must not contain duplicates")
        if not isinstance(self.novelty_claim, bool):
            raise TypeError("novelty_claim must be bool")


@dataclass(frozen=True, slots=True)
class ProtectedStubAssessment(DiagnosticMixin):
    """Transparent non-authorizing result from one limited stub review."""

    algorithm_name: AlgorithmName
    target_id: str
    triggered: bool
    signals: tuple[str, ...]
    decision_type: DecisionType | None
    status: DecisionStatus | None
    escalation_target: AlgorithmName | None
    budget_levels: tuple[str, ...] = ()
    threshold_checks: tuple[ThresholdCheck, ...] = ()
    scores: ScoreBundle = field(default_factory=ScoreBundle)

    def __post_init__(self) -> None:
        if self.algorithm_name not in {
            AlgorithmName.IPA,
            AlgorithmName.SRA,
            AlgorithmName.NGSA,
            AlgorithmName.AEA,
        }:
            raise ValueError("algorithm_name must identify a protected stub")
        _require_nonempty_text(self.target_id, "target_id")
        if not isinstance(self.triggered, bool):
            raise TypeError("triggered must be bool")
        _require_text_tuple(self.signals, "signals")
        if self.triggered != bool(self.signals):
            raise ValueError("triggered must be true exactly when signals exist")
        if self.triggered:
            if not isinstance(self.decision_type, DecisionType):
                raise TypeError("triggered assessment requires decision_type")
            if not isinstance(self.status, DecisionStatus):
                raise TypeError("triggered assessment requires status")
        elif (
            self.decision_type is not None
            or self.status is not None
            or self.escalation_target is not None
        ):
            raise ValueError("untriggered assessment cannot route a decision")
        if self.escalation_target is not None and not isinstance(
            self.escalation_target,
            AlgorithmName,
        ):
            raise TypeError(
                "escalation_target must be AlgorithmName or None"
            )
        if (
            self.decision_type is DecisionType.ESCALATE
        ) != (self.escalation_target is not None):
            raise ValueError(
                "only escalation decisions may name escalation_target"
            )
        _require_text_tuple(self.budget_levels, "budget_levels")
        if not isinstance(self.threshold_checks, tuple):
            raise TypeError("threshold_checks must be a tuple")
        for position, check in enumerate(self.threshold_checks):
            if not isinstance(check, ThresholdCheck):
                raise TypeError(
                    f"threshold_checks[{position}] must be ThresholdCheck"
                )
        if not isinstance(self.scores, ScoreBundle):
            raise TypeError("scores must be ScoreBundle")


def _default_id_provider() -> str:
    return f"decision-{uuid4()}"


def detect_identity_risk_flags(
    target: SymbolicStructure,
) -> tuple[str, ...]:
    """Return only transparent, explicit identity-risk markers."""

    if not isinstance(target, SymbolicStructure):
        raise TypeError("target must be SymbolicStructure")
    return tuple(
        flag
        for flag, patterns in _IDENTITY_RISK_PATTERNS.items()
        if any(
            re.search(pattern, target.content, re.IGNORECASE)
            for pattern in patterns
        )
    )


def detect_novelty_claim(target: SymbolicStructure) -> bool:
    """Detect a novelty request without generating or evaluating novelty."""

    if not isinstance(target, SymbolicStructure):
        raise TypeError("target must be SymbolicStructure")
    return (
        target.structure_type is StructureType.NOVELTY_CANDIDATE
        or any(
            re.search(pattern, target.content, re.IGNORECASE)
            for pattern in _NOVELTY_PATTERNS
        )
    )


def detect_architecture_candidate(target: SymbolicStructure) -> bool:
    """Detect architecture candidacy without changing achieved scale."""

    if not isinstance(target, SymbolicStructure):
        raise TypeError("target must be SymbolicStructure")
    return (
        target.structure_type is StructureType.ARCHITECTURAL_CANDIDATE
        or target.metadata.candidate_status
        is CandidateStatus.ARCHITECTURE_CANDIDATE
    )


def evaluate_ipa_stub(
    context: ReviewContext,
    target_id: str,
    *,
    fixture: StubReviewFixture | None = None,
) -> ProtectedStubAssessment:
    """Detect explicit identity risk and transfer it to CGA."""

    target, _ = _review_inputs(context, target_id, fixture)
    signals = _deduplicate(
        (
            *detect_identity_risk_flags(target),
            *(
                fixture.identity_risk_flags
                if fixture is not None
                else ()
            ),
        )
    )
    if not signals:
        return _untriggered(AlgorithmName.IPA, target_id)
    return ProtectedStubAssessment(
        algorithm_name=AlgorithmName.IPA,
        target_id=target_id,
        triggered=True,
        signals=signals,
        decision_type=DecisionType.ESCALATE,
        status=DecisionStatus.ESCALATED,
        escalation_target=AlgorithmName.CGA,
        scores=ScoreBundle(identity_risk_score=1.0),
    )


def evaluate_sra_stub(
    context: ReviewContext,
    target_id: str,
) -> ProtectedStubAssessment:
    """Detect visible pressure without regulating state or consuming budget."""

    target, state = _review_inputs(context, target_id, None)
    pressures = budget_pressure(state.budgets)
    stability_level = pressures[BudgetType.STABILITY]
    attention_level = pressures[BudgetType.ATTENTION]
    stability_check = create_threshold_check(
        state,
        structure_id=target.structure_id,
        threshold_name="stability_threshold",
        observed_value=state.budgets.stability_budget,
    )
    threshold_checks: list[ThresholdCheck] = [stability_check]
    signals: list[str] = []
    if not stability_check.result:
        signals.append("stability_budget_below_threshold")
    if attention_level in _PRESSURED_BUDGET_LEVELS:
        signals.append("attention_budget_pressure")

    coherence_pressure = state.coherence_graph.coherence_pressure
    if coherence_pressure is not None:
        coherence_check = create_threshold_check(
            state,
            structure_id=target.structure_id,
            threshold_name="coherence_threshold",
            observed_value=coherence_pressure,
        )
        escalation_check = create_threshold_check(
            state,
            structure_id=target.structure_id,
            threshold_name="escalation_threshold",
            observed_value=coherence_pressure,
        )
        threshold_checks.extend((coherence_check, escalation_check))
        if (
            state.coherence_graph.unresolved_tensions
            and not coherence_check.result
        ):
            signals.append("unresolved_tension_overload")

    signals_tuple = _deduplicate(signals)
    if not signals_tuple:
        return ProtectedStubAssessment(
            algorithm_name=AlgorithmName.SRA,
            target_id=target_id,
            triggered=False,
            signals=(),
            decision_type=None,
            status=None,
            escalation_target=None,
            budget_levels=_budget_levels(
                stability_level=stability_level,
                attention_level=attention_level,
            ),
            threshold_checks=tuple(threshold_checks),
        )

    severe_budget_pressure = (
        stability_level in _SEVERE_BUDGET_LEVELS
        or attention_level in _SEVERE_BUDGET_LEVELS
    )
    escalation_required = severe_budget_pressure or (
        coherence_pressure is not None
        and coherence_pressure > state.thresholds.escalation_threshold
    )
    return ProtectedStubAssessment(
        algorithm_name=AlgorithmName.SRA,
        target_id=target_id,
        triggered=True,
        signals=signals_tuple,
        decision_type=(
            DecisionType.ESCALATE
            if escalation_required
            else DecisionType.DELAY
        ),
        status=(
            DecisionStatus.ESCALATED
            if escalation_required
            else DecisionStatus.PENDING_REVIEW
        ),
        escalation_target=(
            AlgorithmName.CGA if escalation_required else None
        ),
        budget_levels=_budget_levels(
            stability_level=stability_level,
            attention_level=attention_level,
        ),
        threshold_checks=tuple(threshold_checks),
        scores=ScoreBundle(
            stability_score=state.budgets.stability_budget,
            risk_score=coherence_pressure or 0.0,
        ),
    )


def evaluate_ngsa_stub(
    context: ReviewContext,
    target_id: str,
    *,
    fixture: StubReviewFixture | None = None,
) -> ProtectedStubAssessment:
    """Recommend a sandbox for claimed novelty without creating novelty."""

    target, state = _review_inputs(context, target_id, fixture)
    novelty_claim = detect_novelty_claim(target) or (
        fixture.novelty_claim if fixture is not None else False
    )
    if not novelty_claim:
        return _untriggered(AlgorithmName.NGSA, target_id)
    pressures = budget_pressure(state.budgets)
    novelty_level = pressures[BudgetType.NOVELTY]
    stability_level = pressures[BudgetType.STABILITY]
    signals = ["novelty_claim"]
    if novelty_level in _PRESSURED_BUDGET_LEVELS:
        signals.append("novelty_budget_pressure")
    if stability_level in _PRESSURED_BUDGET_LEVELS:
        signals.append("stability_budget_pressure")
    return ProtectedStubAssessment(
        algorithm_name=AlgorithmName.NGSA,
        target_id=target_id,
        triggered=True,
        signals=tuple(signals),
        decision_type=DecisionType.SANDBOX,
        status=DecisionStatus.PROVISIONAL,
        escalation_target=None,
        budget_levels=(
            f"novelty:{novelty_level}",
            f"stability:{stability_level}",
        ),
    )


def evaluate_aea_stub(
    context: ReviewContext,
    target_id: str,
) -> ProtectedStubAssessment:
    """Route an architecture candidate without evaluating architectural fitness."""

    target, _ = _review_inputs(context, target_id, None)
    if not detect_architecture_candidate(target):
        return _untriggered(AlgorithmName.AEA, target_id)
    return ProtectedStubAssessment(
        algorithm_name=AlgorithmName.AEA,
        target_id=target_id,
        triggered=True,
        signals=("architecture_candidate",),
        decision_type=DecisionType.ESCALATE,
        status=DecisionStatus.ESCALATED,
        escalation_target=AlgorithmName.CGA,
    )


def run_ipa_stub_where_required(
    context: ReviewContext,
    fixtures: Iterable[StubReviewFixture] = (),
    *,
    id_provider: IDProvider = _default_id_provider,
) -> None:
    """Append IPA stub decisions only for explicit identity-risk triggers."""

    _run_stub(
        context,
        AlgorithmName.IPA,
        lambda review_context, target_id, fixture: evaluate_ipa_stub(
            review_context,
            target_id,
            fixture=fixture,
        ),
        fixtures=fixtures,
        id_provider=id_provider,
    )


def run_sra_stub_where_required(
    context: ReviewContext,
    *,
    id_provider: IDProvider = _default_id_provider,
) -> None:
    """Append SRA stub decisions only when visible pressure is present."""

    _run_stub(
        context,
        AlgorithmName.SRA,
        lambda review_context, target_id, fixture: evaluate_sra_stub(
            review_context,
            target_id,
        ),
        fixtures=(),
        id_provider=id_provider,
    )


def run_ngsa_stub_where_required(
    context: ReviewContext,
    fixtures: Iterable[StubReviewFixture] = (),
    *,
    id_provider: IDProvider = _default_id_provider,
) -> None:
    """Append NGSA stub sandbox recommendations for novelty claims."""

    _run_stub(
        context,
        AlgorithmName.NGSA,
        lambda review_context, target_id, fixture: evaluate_ngsa_stub(
            review_context,
            target_id,
            fixture=fixture,
        ),
        fixtures=fixtures,
        id_provider=id_provider,
    )


def run_aea_stub_where_required(
    context: ReviewContext,
    *,
    id_provider: IDProvider = _default_id_provider,
) -> None:
    """Append AEA stub decisions only for architecture candidates."""

    _run_stub(
        context,
        AlgorithmName.AEA,
        lambda review_context, target_id, fixture: evaluate_aea_stub(
            review_context,
            target_id,
        ),
        fixtures=(),
        id_provider=id_provider,
    )


def _run_stub(
    context: ReviewContext,
    algorithm_name: AlgorithmName,
    evaluator: Callable[
        [ReviewContext, str, StubReviewFixture | None],
        ProtectedStubAssessment,
    ],
    *,
    fixtures: Iterable[StubReviewFixture],
    id_provider: IDProvider,
) -> None:
    if not isinstance(context, ReviewContext):
        raise TypeError("context must be ReviewContext")
    if not callable(id_provider):
        raise TypeError("id_provider must be callable")
    fixture_index = _index_fixtures(fixtures, context)

    def reviewer(review_context: ReviewContext) -> None:
        state_view = review_context.architecture_state
        specification = state_view.algorithm_registry.get_spec(
            algorithm_name
        )
        for target in review_context.targets:
            if (
                target.structure_type
                not in specification.permitted_structure_types
            ):
                continue
            if review_context.latest_by_algorithm(
                target.structure_id,
                algorithm_name,
            ) is not None:
                continue
            assessment = evaluator(
                review_context,
                target.structure_id,
                fixture_index.get(target.structure_id),
            )
            if not assessment.triggered:
                continue
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
                raise ProtectedStubError(
                    f"{algorithm_name.name} stub produced a "
                    f"registry-invalid decision: {codes}"
                )
            review_context.append_decision(decision)

    run_algorithm_where_required(context, reviewer)


def _decision_from_assessment(
    assessment: ProtectedStubAssessment,
    *,
    audit_id: str,
    decision_id: str,
) -> ReviewDecision:
    if not assessment.triggered:
        raise ProtectedStubError(
            "an untriggered assessment cannot become a decision"
        )
    return ReviewDecision(
        decision_id=decision_id,
        algorithm_name=assessment.algorithm_name,
        target_id=assessment.target_id,
        decision_type=assessment.decision_type,
        status=assessment.status,
        scores=assessment.scores,
        rationale=_build_stub_rationale(assessment),
        authorized=False,
        escalation_target=(
            assessment.escalation_target.value
            if assessment.escalation_target is not None
            else None
        ),
        audit_id=audit_id,
    )


def _build_stub_rationale(
    assessment: ProtectedStubAssessment,
) -> str:
    signals = ", ".join(assessment.signals)
    budgets = (
        f"; budget levels: {', '.join(assessment.budget_levels)}"
        if assessment.budget_levels
        else ""
    )
    thresholds = (
        "; threshold checks: "
        + ", ".join(
            (
                f"{check.threshold_name}="
                f"{check.observed_value:.3f}/"
                f"{check.threshold_value:.3f}:"
                f"{'pass' if check.result else 'review'}"
            )
            for check in assessment.threshold_checks
        )
        if assessment.threshold_checks
        else ""
    )
    return (
        f"{assessment.algorithm_name.name} is a v0.1 stub; it detected "
        f"explicit routing signal(s): {signals}{budgets}{thresholds}. "
        "It has not performed full canonical review and grants no mutation, "
        "status elevation, or protected authority."
    )


def _review_inputs(
    context: ReviewContext,
    target_id: str,
    fixture: StubReviewFixture | None,
) -> tuple[SymbolicStructure, ArchitectureState]:
    if not isinstance(context, ReviewContext):
        raise TypeError("context must be ReviewContext")
    _require_nonempty_text(target_id, "target_id")
    if fixture is not None:
        if not isinstance(fixture, StubReviewFixture):
            raise TypeError("fixture must be StubReviewFixture or None")
        if fixture.target_id != target_id:
            raise ValueError("fixture target_id must match reviewed target")
    return context.get_target(target_id), context.architecture_state


def _index_fixtures(
    fixtures: Iterable[StubReviewFixture],
    context: ReviewContext,
) -> dict[str, StubReviewFixture]:
    if isinstance(fixtures, StubReviewFixture):
        raise TypeError("fixtures must be an iterable of StubReviewFixture")
    indexed: dict[str, StubReviewFixture] = {}
    for position, fixture in enumerate(fixtures):
        if not isinstance(fixture, StubReviewFixture):
            raise TypeError(
                f"fixtures[{position}] must be StubReviewFixture"
            )
        if fixture.target_id not in context.target_ids:
            raise ValueError(
                f"fixture references unknown target_id: {fixture.target_id}"
            )
        if fixture.target_id in indexed:
            raise ValueError(
                f"duplicate fixture target_id: {fixture.target_id}"
            )
        indexed[fixture.target_id] = fixture
    return indexed


def _untriggered(
    algorithm_name: AlgorithmName,
    target_id: str,
) -> ProtectedStubAssessment:
    return ProtectedStubAssessment(
        algorithm_name=algorithm_name,
        target_id=target_id,
        triggered=False,
        signals=(),
        decision_type=None,
        status=None,
        escalation_target=None,
    )


def _budget_levels(
    *,
    stability_level: BudgetPressureLevel,
    attention_level: BudgetPressureLevel,
) -> tuple[str, ...]:
    return (
        f"stability:{stability_level}",
        f"attention:{attention_level}",
    )


def _deduplicate(values: Iterable[str]) -> tuple[str, ...]:
    return tuple(dict.fromkeys(values))


def _require_text_tuple(
    values: tuple[str, ...],
    field_name: str,
) -> None:
    if not isinstance(values, tuple):
        raise TypeError(f"{field_name} must be a tuple")
    for position, value in enumerate(values):
        _require_nonempty_text(value, f"{field_name}[{position}]")


def _require_nonempty_text(value: str, field_name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a nonempty string")


__all__ = [
    "IDProvider",
    "ProtectedStubAssessment",
    "ProtectedStubError",
    "StubReviewFixture",
    "detect_architecture_candidate",
    "detect_identity_risk_flags",
    "detect_novelty_claim",
    "evaluate_aea_stub",
    "evaluate_ipa_stub",
    "evaluate_ngsa_stub",
    "evaluate_sra_stub",
    "run_aea_stub_where_required",
    "run_ipa_stub_where_required",
    "run_ngsa_stub_where_required",
    "run_sra_stub_where_required",
]
