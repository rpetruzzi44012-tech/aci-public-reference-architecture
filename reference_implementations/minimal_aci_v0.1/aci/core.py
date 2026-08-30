"""Core passive data contracts for Minimal ACI Prototype v0.1."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field, fields, is_dataclass
from enum import StrEnum
from typing import TYPE_CHECKING, Any, TypeVar

from .enums import (
    AlgorithmName,
    AuditStatus,
    AuthorityLevel,
    CandidateStatus,
    CycleStatus,
    DecisionStatus,
    DecisionType,
    EpistemicStatus,
    EscalationUrgency,
    GraphName,
    GraphUpdateType,
    GovernanceMode,
    OutputType,
    ScaleLabel,
    StructureType,
    SymbolicState,
)

if TYPE_CHECKING:
    from .registry import DecisionValidationResult

JSONValue = str | int | float | bool | None | list["JSONValue"] | dict[str, "JSONValue"]

_EnumT = TypeVar("_EnumT", bound=StrEnum)


def _serialize(value: Any) -> Any:
    if isinstance(value, StrEnum):
        return value.value
    if is_dataclass(value):
        return {
            data_field.name: _serialize(getattr(value, data_field.name))
            for data_field in fields(value)
        }
    if isinstance(value, list):
        return [_serialize(item) for item in value]
    if isinstance(value, tuple):
        return [_serialize(item) for item in value]
    if isinstance(value, Mapping):
        return {str(_serialize(key)): _serialize(item) for key, item in value.items()}
    return value


def _require_nonempty_text(value: str, field_name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a nonempty string")


def _require_optional_nonempty_text(value: str | None, field_name: str) -> None:
    if value is not None:
        _require_nonempty_text(value, field_name)


def _require_bool(value: bool, field_name: str) -> None:
    if not isinstance(value, bool):
        raise TypeError(f"{field_name} must be bool")


def _require_enum(value: object, enum_type: type[_EnumT], field_name: str) -> None:
    if not isinstance(value, enum_type):
        raise TypeError(f"{field_name} must be {enum_type.__name__}")


def _require_score(value: float, field_name: str) -> None:
    if not isinstance(value, int | float) or isinstance(value, bool):
        raise TypeError(f"{field_name} must be a numeric score")
    if not 0.0 <= float(value) <= 1.0:
        raise ValueError(f"{field_name} must be in [0.0, 1.0]")


def _require_mapping(value: dict[str, JSONValue], field_name: str) -> None:
    if not isinstance(value, dict):
        raise TypeError(f"{field_name} must be a dictionary")
    for key in value:
        _require_nonempty_text(key, f"{field_name} key")


def _require_ref_list(values: list[str], field_name: str) -> None:
    if not isinstance(values, list):
        raise TypeError(f"{field_name} must be a list")
    for index, value in enumerate(values):
        _require_nonempty_text(value, f"{field_name}[{index}]")


def _require_enum_list(values: list[StrEnum], enum_type: type[_EnumT], field_name: str) -> None:
    if not isinstance(values, list):
        raise TypeError(f"{field_name} must be a list")
    for index, value in enumerate(values):
        _require_enum(value, enum_type, f"{field_name}[{index}]")


def _require_model_list(values: list[object], model_type: type[object], field_name: str) -> None:
    if not isinstance(values, list):
        raise TypeError(f"{field_name} must be a list")
    for index, value in enumerate(values):
        if not isinstance(value, model_type):
            raise TypeError(f"{field_name}[{index}] must be {model_type.__name__}")


class DiagnosticMixin:
    """Small diagnostic serializer for tests, logs, and audit-readable output."""

    def to_dict(self) -> dict[str, Any]:
        serialized = _serialize(self)
        if not isinstance(serialized, dict):
            raise TypeError("diagnostic serialization did not produce a dictionary")
        return serialized


@dataclass(slots=True)
class InputObject(DiagnosticMixin):
    input_id: str
    content: str
    source: str = "user"
    context_refs: list[str] = field(default_factory=list)
    audit_ref: str | None = None

    def __post_init__(self) -> None:
        _require_nonempty_text(self.input_id, "input_id")
        if not isinstance(self.content, str):
            raise TypeError("content must be a string")
        _require_nonempty_text(self.source, "source")
        _require_ref_list(self.context_refs, "context_refs")
        _require_optional_nonempty_text(self.audit_ref, "audit_ref")


@dataclass(slots=True)
class ScoreBundle(DiagnosticMixin):
    grounding_score: float = 0.0
    coherence_score: float = 0.0
    persistence_score: float = 0.0
    multi_scale_coherence_score: float = 0.0
    stability_score: float = 0.0
    novelty_score: float = 0.0
    legitimacy_score: float = 0.0
    confidence_score: float = 0.0
    risk_score: float = 0.0
    identity_risk_score: float = 0.0
    constitutional_risk_score: float = 0.0

    def __post_init__(self) -> None:
        for score_field in fields(self):
            _require_score(getattr(self, score_field.name), score_field.name)


@dataclass(slots=True)
class SymbolicMetadata(DiagnosticMixin):
    origin: str
    epistemic_status: EpistemicStatus
    scale_label: ScaleLabel
    candidate_status: CandidateStatus
    authority_level: AuthorityLevel
    grounding_score: float = 0.0
    coherence_score: float = 0.0
    persistence_score: float = 0.0
    uncertainty: float = 1.0
    audit_refs: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        _require_nonempty_text(self.origin, "origin")
        _require_enum(self.epistemic_status, EpistemicStatus, "epistemic_status")
        _require_enum(self.scale_label, ScaleLabel, "scale_label")
        _require_enum(self.candidate_status, CandidateStatus, "candidate_status")
        _require_enum(self.authority_level, AuthorityLevel, "authority_level")
        _require_score(self.grounding_score, "grounding_score")
        _require_score(self.coherence_score, "coherence_score")
        _require_score(self.persistence_score, "persistence_score")
        _require_score(self.uncertainty, "uncertainty")
        _require_ref_list(self.audit_refs, "audit_refs")


@dataclass(slots=True)
class SymbolicStructure(DiagnosticMixin):
    structure_id: str
    content: str
    structure_type: StructureType
    current_state: SymbolicState
    metadata: SymbolicMetadata

    def __post_init__(self) -> None:
        _require_nonempty_text(self.structure_id, "structure_id")
        if not isinstance(self.content, str):
            raise TypeError("content must be a string")
        _require_enum(self.structure_type, StructureType, "structure_type")
        _require_enum(self.current_state, SymbolicState, "current_state")
        if not isinstance(self.metadata, SymbolicMetadata):
            raise TypeError("metadata must be SymbolicMetadata")


@dataclass(slots=True)
class ReviewDecision(DiagnosticMixin):
    decision_id: str
    algorithm_name: AlgorithmName
    target_id: str
    decision_type: DecisionType
    status: DecisionStatus
    scores: ScoreBundle
    rationale: str
    authorized: bool
    escalation_target: str | None = None
    audit_id: str | None = None
    recommended_governance_mode: GovernanceMode | None = None
    output_block_recommended: bool = False

    def __post_init__(self) -> None:
        _require_nonempty_text(self.decision_id, "decision_id")
        _require_enum(self.algorithm_name, AlgorithmName, "algorithm_name")
        _require_nonempty_text(self.target_id, "target_id")
        _require_enum(self.decision_type, DecisionType, "decision_type")
        _require_enum(self.status, DecisionStatus, "status")
        if not isinstance(self.scores, ScoreBundle):
            raise TypeError("scores must be ScoreBundle")
        _require_nonempty_text(self.rationale, "rationale")
        _require_bool(self.authorized, "authorized")
        _require_optional_nonempty_text(self.escalation_target, "escalation_target")
        _require_optional_nonempty_text(self.audit_id, "audit_id")
        if self.recommended_governance_mode is not None:
            _require_enum(
                self.recommended_governance_mode,
                GovernanceMode,
                "recommended_governance_mode",
            )
        _require_bool(
            self.output_block_recommended,
            "output_block_recommended",
        )
        if (
            self.decision_type is DecisionType.ESCALATE
            or self.status is DecisionStatus.ESCALATED
        ) and self.escalation_target is None:
            raise ValueError("escalated decisions require escalation_target")


@dataclass(slots=True)
class AuditRecord(DiagnosticMixin):
    audit_id: str
    status: AuditStatus
    cycle_id: str | None = None
    input_ref: str | None = None
    baseline_state_ref: str | None = None
    baseline_fingerprint: str | None = None
    started_at: str | None = None
    finalized_at: str | None = None
    target_structure_ids: list[str] = field(default_factory=list)
    created_structures: list[SymbolicStructure] = field(default_factory=list)
    algorithms_invoked: list[AlgorithmName] = field(default_factory=list)
    decisions: list[ReviewDecision] = field(default_factory=list)
    accepted_plan_items: list[StateChange] = field(default_factory=list)
    rejected_plan_items: list[StateChange] = field(default_factory=list)
    state_change_plan: StateChangePlan | None = None
    graph_updates: list[GraphUpdate] = field(default_factory=list)
    budget_effects: list[dict[str, JSONValue]] = field(default_factory=list)
    threshold_effects: list[dict[str, JSONValue]] = field(default_factory=list)
    rollback_points_created: list[RollbackPoint] = field(default_factory=list)
    state_delta: StateDelta | None = None
    provisional_output_ref: str | None = None
    unresolved_tensions: list[str] = field(default_factory=list)
    escalation_events: list[EscalationEvent] = field(default_factory=list)
    decision_refs: list[str] = field(default_factory=list)
    state_change_refs: list[str] = field(default_factory=list)
    graph_update_refs: list[str] = field(default_factory=list)
    escalation_refs: list[str] = field(default_factory=list)
    rollback_refs: list[str] = field(default_factory=list)
    output_refs: list[str] = field(default_factory=list)
    failure_stage: str | None = None
    error: str | None = None

    def __post_init__(self) -> None:
        _require_nonempty_text(self.audit_id, "audit_id")
        _require_enum(self.status, AuditStatus, "status")
        _require_optional_nonempty_text(self.cycle_id, "cycle_id")
        _require_optional_nonempty_text(self.input_ref, "input_ref")
        _require_optional_nonempty_text(self.baseline_state_ref, "baseline_state_ref")
        _require_optional_nonempty_text(
            self.baseline_fingerprint,
            "baseline_fingerprint",
        )
        _require_optional_nonempty_text(self.started_at, "started_at")
        _require_optional_nonempty_text(self.finalized_at, "finalized_at")
        _require_ref_list(self.target_structure_ids, "target_structure_ids")
        _require_model_list(
            self.created_structures,
            SymbolicStructure,
            "created_structures",
        )
        _require_enum_list(
            self.algorithms_invoked,
            AlgorithmName,
            "algorithms_invoked",
        )
        _require_model_list(self.decisions, ReviewDecision, "decisions")
        _require_model_list(
            self.accepted_plan_items,
            StateChange,
            "accepted_plan_items",
        )
        _require_model_list(
            self.rejected_plan_items,
            StateChange,
            "rejected_plan_items",
        )
        if self.state_change_plan is not None and not isinstance(
            self.state_change_plan,
            StateChangePlan,
        ):
            raise TypeError(
                "state_change_plan must be StateChangePlan or None"
            )
        _require_model_list(self.graph_updates, GraphUpdate, "graph_updates")
        if not isinstance(self.budget_effects, list):
            raise TypeError("budget_effects must be a list")
        for index, effect in enumerate(self.budget_effects):
            _require_mapping(effect, f"budget_effects[{index}]")
        if not isinstance(self.threshold_effects, list):
            raise TypeError("threshold_effects must be a list")
        for index, effect in enumerate(self.threshold_effects):
            _require_mapping(effect, f"threshold_effects[{index}]")
        _require_model_list(
            self.rollback_points_created,
            RollbackPoint,
            "rollback_points_created",
        )
        if self.state_delta is not None and not isinstance(
            self.state_delta,
            StateDelta,
        ):
            raise TypeError("state_delta must be StateDelta or None")
        _require_optional_nonempty_text(
            self.provisional_output_ref,
            "provisional_output_ref",
        )
        _require_ref_list(self.unresolved_tensions, "unresolved_tensions")
        _require_model_list(
            self.escalation_events,
            EscalationEvent,
            "escalation_events",
        )
        _require_optional_nonempty_text(self.failure_stage, "failure_stage")
        _require_optional_nonempty_text(self.error, "error")
        _require_ref_list(self.decision_refs, "decision_refs")
        _require_ref_list(self.state_change_refs, "state_change_refs")
        _require_ref_list(self.graph_update_refs, "graph_update_refs")
        _require_ref_list(self.escalation_refs, "escalation_refs")
        _require_ref_list(self.rollback_refs, "rollback_refs")
        _require_ref_list(self.output_refs, "output_refs")
        if self.status is AuditStatus.PENDING:
            if (
                self.finalized_at is not None
                or self.failure_stage is not None
                or self.error is not None
                or self.state_delta is not None
                or self.state_change_plan is not None
            ):
                raise ValueError(
                    "pending audit cannot be finalized, failed, or contain a delta"
                )
        elif self.status is AuditStatus.COMMITTED:
            if self.finalized_at is None:
                raise ValueError("committed audit requires finalized_at")
            if self.failure_stage is not None or self.error is not None:
                raise ValueError(
                    "committed audit cannot contain failure data"
                )
        elif self.status is AuditStatus.ABORTED:
            if (
                self.finalized_at is None
                or self.failure_stage is None
                or self.error is None
            ):
                raise ValueError(
                    "aborted audit requires finalized_at, failure_stage, and error"
                )
            if (
                self.created_structures
                or self.accepted_plan_items
                or self.graph_updates
                or self.budget_effects
                or self.threshold_effects
                or self.rollback_points_created
                or self.state_delta is not None
                or self.provisional_output_ref is not None
                or self.state_change_refs
                or self.graph_update_refs
                or self.rollback_refs
                or self.output_refs
            ):
                raise ValueError(
                    "aborted audit cannot contain committed domain effects"
                )


@dataclass(slots=True)
class StateChange(DiagnosticMixin):
    change_id: str
    target_id: str
    change_type: str
    decision_ref: str
    audit_ref: str
    payload: dict[str, JSONValue] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_nonempty_text(self.change_id, "change_id")
        _require_nonempty_text(self.target_id, "target_id")
        _require_nonempty_text(self.change_type, "change_type")
        _require_nonempty_text(self.decision_ref, "decision_ref")
        _require_nonempty_text(self.audit_ref, "audit_ref")
        _require_mapping(self.payload, "payload")


@dataclass(slots=True)
class EscalationEvent(DiagnosticMixin):
    escalation_id: str
    target_id: str
    reason: str
    urgency: EscalationUrgency
    decision_ref: str
    from_algorithm: AlgorithmName | None = None
    from_domain: str | None = None
    to_algorithm: AlgorithmName | None = None
    to_domain: str | None = None
    resolved: bool = False
    audit_ref: str | None = None

    def __post_init__(self) -> None:
        _require_nonempty_text(self.escalation_id, "escalation_id")
        _require_nonempty_text(self.target_id, "target_id")
        _require_nonempty_text(self.reason, "reason")
        _require_enum(self.urgency, EscalationUrgency, "urgency")
        _require_nonempty_text(self.decision_ref, "decision_ref")
        if self.from_algorithm is not None:
            _require_enum(self.from_algorithm, AlgorithmName, "from_algorithm")
        _require_optional_nonempty_text(self.from_domain, "from_domain")
        if self.to_algorithm is not None:
            _require_enum(self.to_algorithm, AlgorithmName, "to_algorithm")
        _require_optional_nonempty_text(self.to_domain, "to_domain")
        _require_bool(self.resolved, "resolved")
        _require_optional_nonempty_text(self.audit_ref, "audit_ref")
        source_count = int(self.from_algorithm is not None) + int(self.from_domain is not None)
        target_count = int(self.to_algorithm is not None) + int(self.to_domain is not None)
        if source_count != 1:
            raise ValueError("escalation requires exactly one source algorithm or domain")
        if target_count != 1:
            raise ValueError("escalation requires exactly one target algorithm or domain")


@dataclass(slots=True)
class RollbackPoint(DiagnosticMixin):
    rollback_id: str
    state_ref: str
    affected_structures: list[str]
    affected_graphs: list[GraphName]
    reason_created: str
    audit_ref: str
    valid_until: str | None = None

    def __post_init__(self) -> None:
        _require_nonempty_text(self.rollback_id, "rollback_id")
        _require_nonempty_text(self.state_ref, "state_ref")
        _require_ref_list(self.affected_structures, "affected_structures")
        _require_enum_list(self.affected_graphs, GraphName, "affected_graphs")
        _require_nonempty_text(self.reason_created, "reason_created")
        _require_nonempty_text(self.audit_ref, "audit_ref")
        _require_optional_nonempty_text(self.valid_until, "valid_until")
        if not self.affected_structures and not self.affected_graphs:
            raise ValueError("rollback point must scope at least one structure or graph")


@dataclass(slots=True)
class GraphUpdate(DiagnosticMixin):
    update_id: str
    graph_name: GraphName
    update_type: GraphUpdateType
    affected_nodes: list[str]
    affected_edges: list[str]
    decision_ref: str
    audit_ref: str
    payload: dict[str, JSONValue] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_nonempty_text(self.update_id, "update_id")
        _require_enum(self.graph_name, GraphName, "graph_name")
        _require_enum(self.update_type, GraphUpdateType, "update_type")
        _require_ref_list(self.affected_nodes, "affected_nodes")
        _require_ref_list(self.affected_edges, "affected_edges")
        _require_nonempty_text(self.decision_ref, "decision_ref")
        _require_nonempty_text(self.audit_ref, "audit_ref")
        _require_mapping(self.payload, "payload")
        if not self.affected_nodes and not self.affected_edges:
            raise ValueError("graph update must name affected nodes or edges")


@dataclass(slots=True)
class StateChangePlan(DiagnosticMixin):
    plan_id: str
    decision_refs: list[str]
    changes: list[StateChange] = field(default_factory=list)
    graph_updates: list[GraphUpdate] = field(default_factory=list)
    rollback_points: list[RollbackPoint] = field(default_factory=list)
    escalation_events: list[EscalationEvent] = field(default_factory=list)
    validation_results: list["DecisionValidationResult"] = field(
        default_factory=list
    )
    rejected_decisions: list[ReviewDecision] = field(default_factory=list)
    no_op_items: list[ReviewDecision] = field(default_factory=list)
    rationale: list[str] = field(default_factory=list)
    authorized: bool = True
    audit_ref: str | None = None

    def __post_init__(self) -> None:
        _require_nonempty_text(self.plan_id, "plan_id")
        _require_ref_list(self.decision_refs, "decision_refs")
        _require_model_list(self.changes, StateChange, "changes")
        _require_model_list(self.graph_updates, GraphUpdate, "graph_updates")
        _require_model_list(self.rollback_points, RollbackPoint, "rollback_points")
        _require_model_list(self.escalation_events, EscalationEvent, "escalation_events")
        from .registry import DecisionValidationResult

        _require_model_list(
            self.validation_results,
            DecisionValidationResult,
            "validation_results",
        )
        _require_model_list(
            self.rejected_decisions,
            ReviewDecision,
            "rejected_decisions",
        )
        _require_model_list(
            self.no_op_items,
            ReviewDecision,
            "no_op_items",
        )
        _require_ref_list(self.rationale, "rationale")
        _require_bool(self.authorized, "authorized")
        _require_optional_nonempty_text(self.audit_ref, "audit_ref")
        if self.authorized != bool(self.decision_refs):
            raise ValueError(
                "authorized must be true exactly when decision_refs exist"
            )

        accepted_refs = set(self.decision_refs)
        if len(accepted_refs) != len(self.decision_refs):
            raise ValueError("decision_refs must not contain duplicates")
        for collection_name, collection in (
            ("changes", self.changes),
            ("graph_updates", self.graph_updates),
            ("escalation_events", self.escalation_events),
        ):
            for item in collection:
                if item.decision_ref not in accepted_refs:
                    raise ValueError(
                        f"{collection_name} must reference an accepted decision"
                    )
                if (
                    self.audit_ref is not None
                    and item.audit_ref != self.audit_ref
                ):
                    raise ValueError(
                        f"{collection_name} audit_ref must match plan audit_ref"
                    )
        if self.audit_ref is not None:
            for rollback_point in self.rollback_points:
                if rollback_point.audit_ref != self.audit_ref:
                    raise ValueError(
                        "rollback_points audit_ref must match plan audit_ref"
                    )

        rejected_refs = {
            decision.decision_id for decision in self.rejected_decisions
        }
        no_op_refs = {
            decision.decision_id for decision in self.no_op_items
        }
        if len(rejected_refs) != len(self.rejected_decisions):
            raise ValueError(
                "rejected_decisions must not contain duplicate IDs"
            )
        if len(no_op_refs) != len(self.no_op_items):
            raise ValueError("no_op_items must not contain duplicate IDs")
        if (
            accepted_refs.intersection(rejected_refs)
            or accepted_refs.intersection(no_op_refs)
            or rejected_refs.intersection(no_op_refs)
        ):
            raise ValueError(
                "accepted, rejected, and no-op decisions must remain separate"
            )


@dataclass(slots=True)
class StateDelta(DiagnosticMixin):
    delta_id: str
    before_state_ref: str
    after_state_ref: str
    audit_ref: str
    applied_change_ids: list[str] = field(default_factory=list)
    graph_update_ids: list[str] = field(default_factory=list)
    escalation_ids: list[str] = field(default_factory=list)
    rollback_ids: list[str] = field(default_factory=list)
    domain_changes: dict[str, JSONValue] = field(default_factory=dict)
    audit_log_changed: bool = False
    audit_log_before_refs: list[str] = field(default_factory=list)
    audit_log_after_refs: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        _require_nonempty_text(self.delta_id, "delta_id")
        _require_nonempty_text(self.before_state_ref, "before_state_ref")
        _require_nonempty_text(self.after_state_ref, "after_state_ref")
        _require_nonempty_text(self.audit_ref, "audit_ref")
        _require_ref_list(self.applied_change_ids, "applied_change_ids")
        _require_ref_list(self.graph_update_ids, "graph_update_ids")
        _require_ref_list(self.escalation_ids, "escalation_ids")
        _require_ref_list(self.rollback_ids, "rollback_ids")
        _require_mapping(self.domain_changes, "domain_changes")
        _require_bool(self.audit_log_changed, "audit_log_changed")
        _require_ref_list(
            self.audit_log_before_refs,
            "audit_log_before_refs",
        )
        _require_ref_list(
            self.audit_log_after_refs,
            "audit_log_after_refs",
        )
        if (
            self.audit_log_before_refs != self.audit_log_after_refs
            and not self.audit_log_changed
        ):
            raise ValueError(
                "a changed audit reference sequence requires "
                "audit_log_changed"
            )


@dataclass(slots=True)
class EpistemicMarker(DiagnosticMixin):
    """Per-structure output status without collapsing review dimensions."""

    structure_id: str
    epistemic_status: EpistemicStatus
    scale_label: ScaleLabel
    candidate_status: CandidateStatus
    authority_level: AuthorityLevel
    grounding_score: float = 0.0
    coherence_score: float = 0.0
    uncertainty: float = 1.0
    decision_refs: list[str] = field(default_factory=list)
    decision_statuses: list[DecisionStatus] = field(default_factory=list)

    def __post_init__(self) -> None:
        _require_nonempty_text(self.structure_id, "structure_id")
        _require_enum(
            self.epistemic_status,
            EpistemicStatus,
            "epistemic_status",
        )
        _require_enum(self.scale_label, ScaleLabel, "scale_label")
        _require_enum(
            self.candidate_status,
            CandidateStatus,
            "candidate_status",
        )
        _require_enum(
            self.authority_level,
            AuthorityLevel,
            "authority_level",
        )
        _require_score(self.grounding_score, "grounding_score")
        _require_score(self.coherence_score, "coherence_score")
        _require_score(self.uncertainty, "uncertainty")
        _require_ref_list(self.decision_refs, "decision_refs")
        _require_enum_list(
            self.decision_statuses,
            DecisionStatus,
            "decision_statuses",
        )
        if len(self.decision_refs) != len(set(self.decision_refs)):
            raise ValueError("decision_refs must not contain duplicates")
        if len(self.decision_statuses) != len(set(self.decision_statuses)):
            raise ValueError(
                "decision_statuses must not contain duplicates"
            )


@dataclass(slots=True)
class OutputObject(DiagnosticMixin):
    output_id: str
    output_type: OutputType
    content: str | None = None
    supporting_structure_ids: list[str] = field(default_factory=list)
    supporting_decision_ids: list[str] = field(default_factory=list)
    epistemic_markers: list[EpistemicMarker] = field(default_factory=list)
    epistemic_status: EpistemicStatus = EpistemicStatus.UNKNOWN
    decision_status: DecisionStatus = DecisionStatus.PROVISIONAL
    scale_label: ScaleLabel = ScaleLabel.OBSERVATION
    authority_level: AuthorityLevel = AuthorityLevel.NONE
    grounding_score: float = 0.0
    coherence_score: float = 0.0
    uncertainty: float = 1.0
    unresolved_tensions: list[str] = field(default_factory=list)
    pending_escalation_ids: list[str] = field(default_factory=list)
    audit_ref: str | None = None
    audit_finalized: bool = False

    def __post_init__(self) -> None:
        _require_nonempty_text(self.output_id, "output_id")
        _require_enum(self.output_type, OutputType, "output_type")
        if self.content is not None and not isinstance(self.content, str):
            raise TypeError("content must be a string or None")
        _require_ref_list(self.supporting_structure_ids, "supporting_structure_ids")
        _require_ref_list(
            self.supporting_decision_ids,
            "supporting_decision_ids",
        )
        _require_model_list(
            self.epistemic_markers,
            EpistemicMarker,
            "epistemic_markers",
        )
        _require_enum(self.epistemic_status, EpistemicStatus, "epistemic_status")
        _require_enum(self.decision_status, DecisionStatus, "decision_status")
        _require_enum(self.scale_label, ScaleLabel, "scale_label")
        _require_enum(self.authority_level, AuthorityLevel, "authority_level")
        _require_score(self.grounding_score, "grounding_score")
        _require_score(self.coherence_score, "coherence_score")
        _require_score(self.uncertainty, "uncertainty")
        _require_ref_list(self.unresolved_tensions, "unresolved_tensions")
        _require_ref_list(
            self.pending_escalation_ids,
            "pending_escalation_ids",
        )
        _require_optional_nonempty_text(self.audit_ref, "audit_ref")
        _require_bool(self.audit_finalized, "audit_finalized")
        if self.audit_finalized and self.audit_ref is None:
            raise ValueError("finalized output requires audit_ref")
        if (
            self.output_type is OutputType.NO_OUTPUT
            and self.content is not None
        ):
            raise ValueError("NO_OUTPUT cannot contain content")
        if (
            self.output_type is not OutputType.NO_OUTPUT
            and self.content is None
        ):
            raise ValueError("authorized external output requires content")
        if len(self.supporting_structure_ids) != len(
            set(self.supporting_structure_ids)
        ):
            raise ValueError(
                "supporting_structure_ids must not contain duplicates"
            )
        if len(self.supporting_decision_ids) != len(
            set(self.supporting_decision_ids)
        ):
            raise ValueError(
                "supporting_decision_ids must not contain duplicates"
            )
        if len(self.pending_escalation_ids) != len(
            set(self.pending_escalation_ids)
        ):
            raise ValueError(
                "pending_escalation_ids must not contain duplicates"
            )
        marker_ids = [
            marker.structure_id
            for marker in self.epistemic_markers
        ]
        if len(marker_ids) != len(set(marker_ids)):
            raise ValueError(
                "epistemic_markers must contain one marker per structure"
            )
        if not set(marker_ids).issubset(self.supporting_structure_ids):
            raise ValueError(
                "epistemic markers must reference supporting structures"
            )


@dataclass(slots=True)
class CycleResult(DiagnosticMixin):
    cycle_id: str
    status: CycleStatus
    audit_record: AuditRecord
    output: OutputObject | None = None
    updated_state: Any | None = None
    unresolved_items: list[str] = field(default_factory=list)
    escalation_events: list[EscalationEvent] = field(default_factory=list)
    monitoring_triggers: list[str] = field(default_factory=list)
    error: str | None = None

    @classmethod
    def committed(
        cls,
        *,
        cycle_id: str,
        updated_state: Any,
        audit_record: AuditRecord,
        output: OutputObject | None = None,
        unresolved_items: list[str] | None = None,
        escalation_events: list[EscalationEvent] | None = None,
        monitoring_triggers: list[str] | None = None,
    ) -> "CycleResult":
        return cls(
            cycle_id=cycle_id,
            status=CycleStatus.COMMITTED,
            audit_record=audit_record,
            output=output,
            updated_state=updated_state,
            unresolved_items=list(unresolved_items or []),
            escalation_events=list(escalation_events or []),
            monitoring_triggers=list(monitoring_triggers or []),
            error=None,
        )

    @classmethod
    def aborted(
        cls,
        *,
        cycle_id: str,
        audit_record: AuditRecord,
        error: str,
        updated_state: Any | None = None,
        output: OutputObject | None = None,
        unresolved_items: list[str] | None = None,
        escalation_events: list[EscalationEvent] | None = None,
        monitoring_triggers: list[str] | None = None,
    ) -> "CycleResult":
        return cls(
            cycle_id=cycle_id,
            status=CycleStatus.ABORTED,
            audit_record=audit_record,
            output=output,
            updated_state=updated_state,
            unresolved_items=list(unresolved_items or []),
            escalation_events=list(escalation_events or []),
            monitoring_triggers=list(monitoring_triggers or []),
            error=error,
        )

    def __post_init__(self) -> None:
        _require_nonempty_text(self.cycle_id, "cycle_id")
        _require_enum(self.status, CycleStatus, "status")
        if not isinstance(self.audit_record, AuditRecord):
            raise TypeError("audit_record must be AuditRecord")
        if self.output is not None and not isinstance(self.output, OutputObject):
            raise TypeError("output must be OutputObject or None")
        _require_ref_list(self.unresolved_items, "unresolved_items")
        _require_model_list(self.escalation_events, EscalationEvent, "escalation_events")
        _require_ref_list(self.monitoring_triggers, "monitoring_triggers")
        _require_optional_nonempty_text(self.error, "error")
        if self.status is CycleStatus.COMMITTED:
            if self.audit_record.status is not AuditStatus.COMMITTED:
                raise ValueError("committed cycle requires committed audit")
            if self.updated_state is None:
                raise ValueError("committed cycle requires updated_state")
            if self.error is not None:
                raise ValueError("committed cycle cannot contain error")
            if self.output is not None:
                if (
                    not self.output.audit_finalized
                    or self.output.audit_ref
                    != self.audit_record.audit_id
                ):
                    raise ValueError(
                        "committed cycle output requires finalized matching "
                        "audit linkage"
                    )
                if (
                    self.output.output_id
                    not in self.audit_record.output_refs
                ):
                    raise ValueError(
                        "committed audit must witness returned output"
                    )
        elif self.status is CycleStatus.ABORTED:
            if self.audit_record.status is not AuditStatus.ABORTED:
                raise ValueError("aborted cycle requires aborted audit")
            if self.error is None:
                raise ValueError("aborted cycle requires error")
            if self.output is not None:
                raise ValueError("aborted cycle cannot contain output")


__all__ = [
    "AuditRecord",
    "CycleResult",
    "EpistemicMarker",
    "EscalationEvent",
    "GraphUpdate",
    "InputObject",
    "OutputObject",
    "ReviewDecision",
    "RollbackPoint",
    "ScoreBundle",
    "StateChange",
    "StateChangePlan",
    "StateDelta",
    "SymbolicMetadata",
    "SymbolicStructure",
]
