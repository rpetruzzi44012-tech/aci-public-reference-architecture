"""Simplified Constitutional Governance Algorithm for ACI v0.1.

CGA reviews legitimacy, authority conflicts, vetoes, escalation, protected
changes, and output risk. It recommends governance posture through typed
decisions but never changes GovernanceState or any other architecture state.
"""

from __future__ import annotations

import re
from collections.abc import Callable, Iterable, Mapping
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
    AuthorityLevel,
    CandidateStatus,
    DecisionStatus,
    DecisionType,
    GovernanceMode,
    StructureType,
)
from ..metadata import ThresholdCheck, create_threshold_check
from ..registry import RegistryChangeRequest
from ..review_context import ReviewContext, run_algorithm_where_required
from ..state import ArchitectureState

IDProvider = Callable[[], str]

_DEPENDENCY_ALGORITHMS = (
    AlgorithmName.MSSA,
    AlgorithmName.AEA,
    AlgorithmName.IPA,
)
_BLOCKING_STATUSES = frozenset(
    {
        DecisionStatus.BLOCKED,
        DecisionStatus.ESCALATED,
        DecisionStatus.PENDING_REVIEW,
    }
)
_MODE_SEVERITY = {
    GovernanceMode.NORMAL: 0,
    GovernanceMode.CAUTION: 1,
    GovernanceMode.CONSTITUTIONAL_RISK: 2,
    GovernanceMode.AMENDMENT_REVIEW: 3,
    GovernanceMode.EMERGENCY: 4,
    GovernanceMode.LOCKDOWN: 5,
}
_MODE_RISK_SCORES = {
    GovernanceMode.NORMAL: 0.0,
    GovernanceMode.CAUTION: 0.25,
    GovernanceMode.CONSTITUTIONAL_RISK: 0.65,
    GovernanceMode.AMENDMENT_REVIEW: 0.75,
    GovernanceMode.EMERGENCY: 0.90,
    GovernanceMode.LOCKDOWN: 1.0,
}


class GovernanceEvaluationError(RuntimeError):
    """Raised when CGA cannot produce a valid registered judgment."""


@unique
class GovernanceClaimKind(StrEnum):
    GENERAL = "governance_claim.general"
    UTILITY = "governance_claim.utility"
    POPULARITY = "governance_claim.popularity"
    REPETITION = "governance_claim.repetition"
    COHERENCE = "governance_claim.coherence"
    ARCHITECTURAL_SUCCESS = "governance_claim.architectural_success"
    AUTHORITY_ELEVATION = "governance_claim.authority_elevation"
    REGISTRY_CHANGE = "governance_claim.registry_change"
    OUTPUT_RULE_CHANGE = "governance_claim.output_rule_change"
    OUTPUT_BLOCK = "governance_claim.output_block"
    AMENDMENT = "governance_claim.amendment"
    EMERGENCY = "governance_claim.emergency"
    LOCKDOWN = "governance_claim.lockdown"


_CLAIM_PATTERNS: Mapping[
    GovernanceClaimKind,
    tuple[str, ...],
] = MappingProxyType(
    {
        GovernanceClaimKind.GENERAL: (
            r"\bgovern(?:ance|ed|ing)?\b",
            r"\bconstitution(?:al|ally)?\b",
            r"\blegitima(?:cy|te)\b",
            r"\bveto\b",
        ),
        GovernanceClaimKind.UTILITY: (
            r"\buseful(?:ness)?\b",
            r"\butility\b",
            r"\bbeneficial\b",
            r"\befficient\b",
        ),
        GovernanceClaimKind.POPULARITY: (
            r"\bpopular(?:ity)?\b",
            r"\bwidely accepted\b",
            r"\bconsensus\b",
        ),
        GovernanceClaimKind.REPETITION: (
            r"\brepeat(?:ed|edly|s|ition)?\b",
            r"\brecurr(?:ing|ed|ence)\b",
            r"\bmany times\b",
            r"\bcorpus\b",
        ),
        GovernanceClaimKind.COHERENCE: (
            r"\bcoheren(?:t|ce)\b",
            r"\binternally consistent\b",
        ),
        GovernanceClaimKind.ARCHITECTURAL_SUCCESS: (
            r"\bsuccessful architecture\b",
            r"\barchitecture succeeded\b",
            r"\barchitecture worked\b",
        ),
        GovernanceClaimKind.AUTHORITY_ELEVATION: (
            r"\bgrant\b.{0,30}\bauthority\b",
            r"\belevat(?:e|ion)\b.{0,30}\bauthority\b",
            r"\bconstitutional authority\b",
            r"\bmake\b.{0,40}\bconstitutional\b",
        ),
        GovernanceClaimKind.REGISTRY_CHANGE: (
            r"\balgorithm registry\b",
            r"\balgorithm authority\b",
            r"\bcall order\b",
        ),
        GovernanceClaimKind.OUTPUT_RULE_CHANGE: (
            r"\boutput rule\b",
            r"\boutput policy\b",
            r"\bchange\b.{0,30}\boutput\b",
        ),
        GovernanceClaimKind.OUTPUT_BLOCK: (
            r"\bblock\b.{0,20}\boutput\b",
            r"\bno output\b",
            r"\bsuppress\b.{0,20}\boutput\b",
        ),
        GovernanceClaimKind.AMENDMENT: (r"\bamend(?:ment|ed|ing)?\b",),
        GovernanceClaimKind.EMERGENCY: (r"\bemergency\b",),
        GovernanceClaimKind.LOCKDOWN: (r"\blockdown\b",),
    }
)


@dataclass(frozen=True, slots=True)
class GovernanceReviewFixture(DiagnosticMixin):
    """Structured governance signals for stable boundary tests and callers."""

    target_id: str
    claim_kinds: tuple[GovernanceClaimKind, ...] = ()
    requested_authority: AuthorityLevel | None = None
    requested_mode: GovernanceMode | None = None
    registry_change_request: RegistryChangeRequest | None = None

    def __post_init__(self) -> None:
        _require_nonempty_text(self.target_id, "target_id")
        if not isinstance(self.claim_kinds, tuple):
            raise TypeError("claim_kinds must be a tuple")
        for position, claim_kind in enumerate(self.claim_kinds):
            if not isinstance(claim_kind, GovernanceClaimKind):
                raise TypeError(
                    f"claim_kinds[{position}] must be GovernanceClaimKind"
                )
        if len(self.claim_kinds) != len(set(self.claim_kinds)):
            raise ValueError("claim_kinds must not contain duplicates")
        if self.requested_authority is not None and not isinstance(
            self.requested_authority,
            AuthorityLevel,
        ):
            raise TypeError(
                "requested_authority must be AuthorityLevel or None"
            )
        if self.requested_mode is not None and not isinstance(
            self.requested_mode,
            GovernanceMode,
        ):
            raise TypeError("requested_mode must be GovernanceMode or None")
        if (
            self.registry_change_request is not None
            and not isinstance(
                self.registry_change_request,
                RegistryChangeRequest,
            )
        ):
            raise TypeError(
                "registry_change_request must be RegistryChangeRequest "
                "or None"
            )


@dataclass(frozen=True, slots=True)
class VetoFinding(DiagnosticMixin):
    """Visible interpretation of one active-veto record."""

    record_ref: str
    veto_id: str | None
    target_scope: str | None
    issuing_domain: str | None
    reason: str | None
    protected: bool
    audit_ref: str | None
    scoped: bool
    auditable: bool

    def __post_init__(self) -> None:
        _require_nonempty_text(self.record_ref, "record_ref")
        for field_name in (
            "veto_id",
            "target_scope",
            "issuing_domain",
            "reason",
            "audit_ref",
        ):
            value = getattr(self, field_name)
            if value is not None:
                _require_nonempty_text(value, field_name)
        for field_name in ("protected", "scoped", "auditable"):
            if not isinstance(getattr(self, field_name), bool):
                raise TypeError(f"{field_name} must be bool")

    @property
    def reviewable(self) -> bool:
        return self.scoped and self.auditable


@dataclass(frozen=True, slots=True)
class GovernanceAssessment(DiagnosticMixin):
    """Typed non-mutating constitutional governance judgment."""

    target_id: str
    claim_kinds: tuple[GovernanceClaimKind, ...]
    legitimacy_score: float
    constitutional_risk_score: float
    legitimacy_check: ThresholdCheck
    constitutional_risk_check: ThresholdCheck
    recommended_mode: GovernanceMode
    output_block_recommended: bool
    veto_findings: tuple[VetoFinding, ...]
    pending_escalation_refs: tuple[str, ...]
    dependency_decision_refs: tuple[str, ...]
    registry_issue_codes: tuple[str, ...]
    authority_edge_refs: tuple[str, ...]
    unauthorized_authority_elevation: bool
    protected_change_requested: bool
    review_required: bool
    reasons: tuple[str, ...]

    def __post_init__(self) -> None:
        _require_nonempty_text(self.target_id, "target_id")
        if not isinstance(self.claim_kinds, tuple):
            raise TypeError("claim_kinds must be a tuple")
        for claim_kind in self.claim_kinds:
            if not isinstance(claim_kind, GovernanceClaimKind):
                raise TypeError(
                    "claim_kinds values must be GovernanceClaimKind"
                )
        _require_normalized(self.legitimacy_score, "legitimacy_score")
        _require_normalized(
            self.constitutional_risk_score,
            "constitutional_risk_score",
        )
        _validate_threshold_check(
            self.legitimacy_check,
            target_id=self.target_id,
            threshold_name="legitimacy_threshold",
            observed_value=self.legitimacy_score,
        )
        _validate_threshold_check(
            self.constitutional_risk_check,
            target_id=self.target_id,
            threshold_name="constitutional_risk_threshold",
            observed_value=self.constitutional_risk_score,
        )
        if not isinstance(self.recommended_mode, GovernanceMode):
            raise TypeError("recommended_mode must be GovernanceMode")
        for field_name in (
            "output_block_recommended",
            "unauthorized_authority_elevation",
            "protected_change_requested",
            "review_required",
        ):
            if not isinstance(getattr(self, field_name), bool):
                raise TypeError(f"{field_name} must be bool")
        if not isinstance(self.veto_findings, tuple):
            raise TypeError("veto_findings must be a tuple")
        for finding in self.veto_findings:
            if not isinstance(finding, VetoFinding):
                raise TypeError("veto_findings values must be VetoFinding")
        for field_name in (
            "pending_escalation_refs",
            "dependency_decision_refs",
            "registry_issue_codes",
            "authority_edge_refs",
            "reasons",
        ):
            _require_reference_tuple(getattr(self, field_name), field_name)
        if not self.reasons:
            raise ValueError("reasons cannot be empty")


def _default_id_provider() -> str:
    return f"decision-{uuid4()}"


def detect_governance_claims(
    target: SymbolicStructure,
) -> tuple[GovernanceClaimKind, ...]:
    """Detect transparent lexical and structural governance claims."""

    if not isinstance(target, SymbolicStructure):
        raise TypeError("target must be SymbolicStructure")
    detected: set[GovernanceClaimKind] = set()
    if target.structure_type in {
        StructureType.GOVERNANCE_OBJECT,
        StructureType.CONSTITUTIONAL_OBJECT,
    }:
        detected.add(GovernanceClaimKind.GENERAL)
    if (
        target.metadata.candidate_status
        is CandidateStatus.CONSTITUTIONAL_CANDIDATE
    ):
        detected.add(GovernanceClaimKind.AUTHORITY_ELEVATION)
    for claim_kind, patterns in _CLAIM_PATTERNS.items():
        if any(
            re.search(pattern, target.content, re.IGNORECASE)
            for pattern in patterns
        ):
            detected.add(claim_kind)
    return tuple(
        claim_kind
        for claim_kind in GovernanceClaimKind
        if claim_kind in detected
    )


def evaluate_governance(
    context: ReviewContext,
    target_id: str,
    *,
    fixture: GovernanceReviewFixture | None = None,
) -> GovernanceAssessment:
    """Review legitimacy and governance risk without changing state."""

    if not isinstance(context, ReviewContext):
        raise TypeError("context must be ReviewContext")
    _require_nonempty_text(target_id, "target_id")
    if fixture is not None:
        if not isinstance(fixture, GovernanceReviewFixture):
            raise TypeError("fixture must be GovernanceReviewFixture or None")
        if fixture.target_id != target_id:
            raise ValueError("fixture target_id must match reviewed target")

    target = context.get_target(target_id)
    state_view = context.architecture_state
    governance = state_view.governance_state
    claim_kinds = _merge_claim_kinds(
        detect_governance_claims(target),
        fixture.claim_kinds if fixture is not None else (),
    )
    requested_authority = _requested_authority(target, fixture)
    authority_edge_refs = _matching_authority_edges(
        state_view,
        target_id,
        requested_authority,
    )
    unauthorized_authority_elevation = (
        requested_authority is not None
        and target.metadata.authority_level is not requested_authority
        and not authority_edge_refs
    )

    veto_findings = _veto_findings_for_target(state_view, target_id)
    dependency_decisions = _dependency_decisions(context, target_id)
    dependency_decision_refs = tuple(
        decision.decision_id for decision in dependency_decisions
    )
    escalation_decision_refs = tuple(
        decision.decision_id
        for decision in context.decisions_for(target_id)
        if decision.algorithm_name is not AlgorithmName.CGA
        and (
            decision.decision_type is DecisionType.ESCALATE
            or decision.status is DecisionStatus.ESCALATED
        )
    )
    state_escalation_refs = tuple(
        event.escalation_id
        for event in governance.pending_escalations
        if event.target_id == target_id and not event.resolved
    )
    pending_escalation_refs = _deduplicate(
        (*escalation_decision_refs, *state_escalation_refs)
    )
    registry_issue_codes = _registry_findings(
        state_view,
        target,
        dependency_decisions,
        fixture.registry_change_request if fixture is not None else None,
        context.audit_id,
    )
    protected_change_requested = (
        GovernanceClaimKind.OUTPUT_RULE_CHANGE in claim_kinds
        or (
            fixture is not None
            and fixture.registry_change_request is not None
            and state_view.algorithm_registry.get_spec(
                fixture.registry_change_request.target_algorithm
            ).protected
        )
    )
    high_risk_dependency = any(
        decision.status in _BLOCKING_STATUSES
        for decision in dependency_decisions
    )
    protected_reviewable_veto = any(
        finding.protected and finding.reviewable
        for finding in veto_findings
    )
    requested_mode = (
        fixture.requested_mode
        if fixture is not None
        else _mode_requested_by_claims(claim_kinds)
    )
    recommended_mode = _recommend_mode(
        current_mode=governance.governance_mode,
        requested_mode=requested_mode,
        protected_change_requested=protected_change_requested,
        has_veto=bool(veto_findings),
        has_pending_escalation=bool(pending_escalation_refs),
        unauthorized_authority_elevation=(
            unauthorized_authority_elevation
        ),
        has_registry_issues=bool(registry_issue_codes),
        high_risk_dependency=high_risk_dependency,
        protected_reviewable_veto=protected_reviewable_veto,
        has_claim=bool(claim_kinds),
    )

    legitimacy_score = 0.0
    constitutional_risk_score = _MODE_RISK_SCORES[recommended_mode]
    legitimacy_check = create_threshold_check(
        state_view,
        structure_id=target_id,
        threshold_name="legitimacy_threshold",
        observed_value=legitimacy_score,
    )
    constitutional_risk_check = create_threshold_check(
        state_view,
        structure_id=target_id,
        threshold_name="constitutional_risk_threshold",
        observed_value=constitutional_risk_score,
    )
    review_required = bool(
        claim_kinds
        or veto_findings
        or pending_escalation_refs
        or dependency_decisions
        or registry_issue_codes
        or governance.governance_mode is not GovernanceMode.NORMAL
    )
    output_block_recommended = (
        GovernanceClaimKind.OUTPUT_BLOCK in claim_kinds
        or protected_change_requested
        or bool(veto_findings)
        or bool(pending_escalation_refs)
        or unauthorized_authority_elevation
        or recommended_mode
        in {
            GovernanceMode.CONSTITUTIONAL_RISK,
            GovernanceMode.EMERGENCY,
            GovernanceMode.AMENDMENT_REVIEW,
            GovernanceMode.LOCKDOWN,
        }
    )
    return GovernanceAssessment(
        target_id=target_id,
        claim_kinds=claim_kinds,
        legitimacy_score=legitimacy_score,
        constitutional_risk_score=constitutional_risk_score,
        legitimacy_check=legitimacy_check,
        constitutional_risk_check=constitutional_risk_check,
        recommended_mode=recommended_mode,
        output_block_recommended=output_block_recommended,
        veto_findings=veto_findings,
        pending_escalation_refs=pending_escalation_refs,
        dependency_decision_refs=dependency_decision_refs,
        registry_issue_codes=registry_issue_codes,
        authority_edge_refs=authority_edge_refs,
        unauthorized_authority_elevation=(
            unauthorized_authority_elevation
        ),
        protected_change_requested=protected_change_requested,
        review_required=review_required,
        reasons=_build_reasons(
            claim_kinds=claim_kinds,
            recommended_mode=recommended_mode,
            veto_findings=veto_findings,
            pending_escalation_refs=pending_escalation_refs,
            registry_issue_codes=registry_issue_codes,
            unauthorized_authority_elevation=(
                unauthorized_authority_elevation
            ),
            protected_change_requested=protected_change_requested,
            output_block_recommended=output_block_recommended,
        ),
    )


def run_cga_where_required(
    context: ReviewContext,
    fixtures: Iterable[GovernanceReviewFixture] = (),
    *,
    id_provider: IDProvider = _default_id_provider,
) -> None:
    """Append registered CGA decisions for governance-relevant targets."""

    if not isinstance(context, ReviewContext):
        raise TypeError("context must be ReviewContext")
    if not callable(id_provider):
        raise TypeError("id_provider must be callable")
    fixture_index = _index_fixtures(fixtures, context)

    def reviewer(review_context: ReviewContext) -> None:
        state_view = review_context.architecture_state
        specification = state_view.algorithm_registry.get_spec(
            AlgorithmName.CGA
        )
        for target in review_context.targets:
            if (
                target.structure_type
                not in specification.permitted_structure_types
            ):
                continue
            if review_context.latest_by_algorithm(
                target.structure_id,
                AlgorithmName.CGA,
            ) is not None:
                continue
            assessment = evaluate_governance(
                review_context,
                target.structure_id,
                fixture=fixture_index.get(target.structure_id),
            )
            if not assessment.review_required:
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
                raise GovernanceEvaluationError(
                    "CGA produced a registry-invalid decision: "
                    f"{codes}"
                )
            review_context.append_decision(decision)

    run_algorithm_where_required(context, reviewer)


def _requested_authority(
    target: SymbolicStructure,
    fixture: GovernanceReviewFixture | None,
) -> AuthorityLevel | None:
    if fixture is not None and fixture.requested_authority is not None:
        return fixture.requested_authority
    if (
        target.metadata.candidate_status
        is CandidateStatus.CONSTITUTIONAL_CANDIDATE
    ):
        return AuthorityLevel.CONSTITUTIONAL_AUTHORITY
    return None


def _matching_authority_edges(
    state: ArchitectureState,
    target_id: str,
    requested_authority: AuthorityLevel | None,
) -> tuple[str, ...]:
    if requested_authority is None:
        return ()
    matches: list[str] = []
    for position, edge in enumerate(
        state.governance_state.authority_graph.authority_edges
    ):
        edge_authority = edge.get("authority_level")
        if (
            edge.get("target_id") == target_id
            and edge_authority
            in {requested_authority.value, requested_authority.name}
            and edge.get("authorized") is True
            and _optional_text(edge.get("audit_ref")) is not None
        ):
            matches.append(
                _record_ref(edge, "edge_id", "authority-edge", position)
            )
    return tuple(matches)


def _veto_findings_for_target(
    state: ArchitectureState,
    target_id: str,
) -> tuple[VetoFinding, ...]:
    findings: list[VetoFinding] = []
    for position, veto in enumerate(
        state.governance_state.active_vetoes
    ):
        target_scope = _optional_text(veto.get("target_id"))
        if target_scope not in {None, "*", target_id}:
            continue
        veto_id = _optional_text(veto.get("veto_id"))
        issuing_domain = _optional_text(veto.get("issuing_domain"))
        reason = _optional_text(veto.get("reason"))
        audit_ref = _optional_text(veto.get("audit_ref"))
        findings.append(
            VetoFinding(
                record_ref=_record_ref(
                    veto,
                    "veto_id",
                    "active-veto",
                    position,
                ),
                veto_id=veto_id,
                target_scope=target_scope,
                issuing_domain=issuing_domain,
                reason=reason,
                protected=veto.get("protected") is True,
                audit_ref=audit_ref,
                scoped=target_scope is not None,
                auditable=audit_ref is not None,
            )
        )
    return tuple(findings)


def _dependency_decisions(
    context: ReviewContext,
    target_id: str,
) -> tuple[ReviewDecision, ...]:
    decisions: list[ReviewDecision] = []
    for algorithm in _DEPENDENCY_ALGORITHMS:
        decision = context.latest_by_algorithm(target_id, algorithm)
        if decision is not None:
            decisions.append(decision)
    return tuple(decisions)


def _registry_findings(
    state: ArchitectureState,
    target: SymbolicStructure,
    dependency_decisions: tuple[ReviewDecision, ...],
    change_request: RegistryChangeRequest | None,
    audit_id: str,
) -> tuple[str, ...]:
    issues: list[str] = []
    for decision in dependency_decisions:
        validation = state.algorithm_registry.validate_decision(
            decision,
            target,
        )
        issues.extend(validation.reason_codes)
    if change_request is not None:
        target_spec = state.algorithm_registry.get_spec(
            change_request.target_algorithm
        )
        if change_request.proposer_algorithm is change_request.target_algorithm:
            issues.append("self_modification_prohibited")
        if target_spec.protected:
            issues.append("protected_algorithm_change_requires_governance")
        if change_request.audit_ref != audit_id:
            issues.append("registry_change_audit_mismatch")
        issues.append("direct_registry_change_prohibited")
    return _deduplicate(issues)


def _recommend_mode(
    *,
    current_mode: GovernanceMode,
    requested_mode: GovernanceMode | None,
    protected_change_requested: bool,
    has_veto: bool,
    has_pending_escalation: bool,
    unauthorized_authority_elevation: bool,
    has_registry_issues: bool,
    high_risk_dependency: bool,
    protected_reviewable_veto: bool,
    has_claim: bool,
) -> GovernanceMode:
    candidate = GovernanceMode.NORMAL
    severe_basis = protected_reviewable_veto and (
        high_risk_dependency or has_registry_issues
    )
    if requested_mode is GovernanceMode.LOCKDOWN and severe_basis:
        candidate = GovernanceMode.LOCKDOWN
    elif (
        requested_mode is GovernanceMode.EMERGENCY
        and (protected_reviewable_veto or high_risk_dependency)
    ):
        candidate = GovernanceMode.EMERGENCY
    elif protected_change_requested:
        candidate = GovernanceMode.AMENDMENT_REVIEW
    elif (
        has_veto
        or has_pending_escalation
        or unauthorized_authority_elevation
        or has_registry_issues
        or high_risk_dependency
        or requested_mode
        in {GovernanceMode.EMERGENCY, GovernanceMode.LOCKDOWN}
    ):
        candidate = GovernanceMode.CONSTITUTIONAL_RISK
    elif has_claim:
        candidate = GovernanceMode.CAUTION
    return max(
        (current_mode, candidate),
        key=lambda mode: _MODE_SEVERITY[mode],
    )


def _decision_from_assessment(
    assessment: GovernanceAssessment,
    *,
    audit_id: str,
    decision_id: str,
) -> ReviewDecision:
    decision_type, status = _decision_route(
        assessment.recommended_mode
    )
    return ReviewDecision(
        decision_id=decision_id,
        algorithm_name=AlgorithmName.CGA,
        target_id=assessment.target_id,
        decision_type=decision_type,
        status=status,
        scores=ScoreBundle(
            legitimacy_score=assessment.legitimacy_score,
            constitutional_risk_score=(
                assessment.constitutional_risk_score
            ),
        ),
        rationale=_build_rationale(assessment),
        authorized=False,
        audit_id=audit_id,
        recommended_governance_mode=assessment.recommended_mode,
        output_block_recommended=(
            assessment.output_block_recommended
        ),
    )


def _decision_route(
    mode: GovernanceMode,
) -> tuple[DecisionType, DecisionStatus]:
    if mode is GovernanceMode.AMENDMENT_REVIEW:
        return (
            DecisionType.AMENDMENT_REVIEW,
            DecisionStatus.PENDING_REVIEW,
        )
    if mode is GovernanceMode.LOCKDOWN:
        return DecisionType.REJECT, DecisionStatus.BLOCKED
    if mode in {
        GovernanceMode.CONSTITUTIONAL_RISK,
        GovernanceMode.EMERGENCY,
    }:
        return DecisionType.DELAY, DecisionStatus.BLOCKED
    return DecisionType.DELAY, DecisionStatus.PENDING_REVIEW


def _build_reasons(
    *,
    claim_kinds: tuple[GovernanceClaimKind, ...],
    recommended_mode: GovernanceMode,
    veto_findings: tuple[VetoFinding, ...],
    pending_escalation_refs: tuple[str, ...],
    registry_issue_codes: tuple[str, ...],
    unauthorized_authority_elevation: bool,
    protected_change_requested: bool,
    output_block_recommended: bool,
) -> tuple[str, ...]:
    reasons = [
        "v0.1 has no typed positive legitimacy evidence; utility, "
        "popularity, repetition, coherence, and local success add none"
    ]
    rhetorical = tuple(
        claim_kind.value
        for claim_kind in claim_kinds
        if claim_kind
        in {
            GovernanceClaimKind.UTILITY,
            GovernanceClaimKind.POPULARITY,
            GovernanceClaimKind.REPETITION,
            GovernanceClaimKind.COHERENCE,
            GovernanceClaimKind.ARCHITECTURAL_SUCCESS,
        }
    )
    if rhetorical:
        reasons.append(
            "non-legitimating claims were preserved: "
            + ", ".join(rhetorical)
        )
    if veto_findings:
        reasons.append(
            f"{len(veto_findings)} active veto record(s) require review"
        )
    if any(not finding.reviewable for finding in veto_findings):
        reasons.append("an active veto is unscoped or unauditable")
    if pending_escalation_refs:
        reasons.append(
            "pending escalation transfers review but grants no approval"
        )
    if registry_issue_codes:
        reasons.append(
            "registry findings: " + ", ".join(registry_issue_codes)
        )
    if unauthorized_authority_elevation:
        reasons.append("requested authority elevation is unauthorized")
    if protected_change_requested:
        reasons.append(
            "protected registry or output-rule change requires governance"
        )
    if output_block_recommended:
        reasons.append("output block is recommended pending resolution")
    reasons.append(
        f"recommended governance posture is {recommended_mode.value}"
    )
    return tuple(reasons)


def _build_rationale(assessment: GovernanceAssessment) -> str:
    legitimacy_result = (
        "passed" if assessment.legitimacy_check.result else "failed"
    )
    risk_result = (
        "passed"
        if assessment.constitutional_risk_check.result
        else "failed"
    )
    return (
        f"CGA recommends {assessment.recommended_mode.value} for "
        f"{assessment.target_id}; output_block="
        f"{assessment.output_block_recommended}. Legitimacy score "
        f"{assessment.legitimacy_score:.3f} {legitimacy_result} "
        f"{assessment.legitimacy_check.threshold_name}="
        f"{assessment.legitimacy_check.threshold_value:.3f} "
        f"({assessment.legitimacy_check.direction}). Constitutional risk "
        f"{assessment.constitutional_risk_score:.3f} {risk_result} "
        f"{assessment.constitutional_risk_check.threshold_name}="
        f"{assessment.constitutional_risk_check.threshold_value:.3f} "
        f"({assessment.constitutional_risk_check.direction}). Vetoes="
        f"{tuple(f.record_ref for f in assessment.veto_findings)}; "
        f"pending escalations={assessment.pending_escalation_refs}; "
        f"dependency decisions={assessment.dependency_decision_refs}; "
        f"authority edges={assessment.authority_edge_refs}; registry "
        f"findings={assessment.registry_issue_codes}. Reasons: "
        f"{'; '.join(assessment.reasons)}. CGA issued review only and "
        "changed no governance, authority, output, or architecture state."
    )


def _merge_claim_kinds(
    first: tuple[GovernanceClaimKind, ...],
    second: tuple[GovernanceClaimKind, ...],
) -> tuple[GovernanceClaimKind, ...]:
    combined = set(first).union(second)
    return tuple(kind for kind in GovernanceClaimKind if kind in combined)


def _mode_requested_by_claims(
    claim_kinds: tuple[GovernanceClaimKind, ...],
) -> GovernanceMode | None:
    if GovernanceClaimKind.LOCKDOWN in claim_kinds:
        return GovernanceMode.LOCKDOWN
    if GovernanceClaimKind.EMERGENCY in claim_kinds:
        return GovernanceMode.EMERGENCY
    if GovernanceClaimKind.AMENDMENT in claim_kinds:
        return GovernanceMode.AMENDMENT_REVIEW
    return None


def _index_fixtures(
    fixtures: Iterable[GovernanceReviewFixture],
    context: ReviewContext,
) -> dict[str, GovernanceReviewFixture]:
    if isinstance(fixtures, GovernanceReviewFixture):
        raise TypeError("fixtures must be an iterable of fixtures")
    result: dict[str, GovernanceReviewFixture] = {}
    for position, fixture in enumerate(fixtures):
        if not isinstance(fixture, GovernanceReviewFixture):
            raise TypeError(
                f"fixtures[{position}] must be GovernanceReviewFixture"
            )
        context.get_target(fixture.target_id)
        if fixture.target_id in result:
            raise GovernanceEvaluationError(
                f"duplicate fixture target_id: {fixture.target_id}"
            )
        result[fixture.target_id] = fixture
    return result


def _record_ref(
    record: dict[str, object],
    key: str,
    prefix: str,
    position: int,
) -> str:
    return _optional_text(record.get(key)) or f"{prefix}-{position}"


def _optional_text(value: object) -> str | None:
    if isinstance(value, str) and value.strip():
        return value
    return None


def _deduplicate(values: Iterable[str]) -> tuple[str, ...]:
    return tuple(dict.fromkeys(values))


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


def _require_reference_tuple(
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


def _require_normalized(value: float, field_name: str) -> None:
    if not isinstance(value, int | float) or isinstance(value, bool):
        raise TypeError(f"{field_name} must be numeric")
    if not 0.0 <= float(value) <= 1.0:
        raise ValueError(f"{field_name} must be in [0.0, 1.0]")


__all__ = [
    "GovernanceAssessment",
    "GovernanceClaimKind",
    "GovernanceEvaluationError",
    "GovernanceReviewFixture",
    "IDProvider",
    "VetoFinding",
    "detect_governance_claims",
    "evaluate_governance",
    "run_cga_where_required",
]
