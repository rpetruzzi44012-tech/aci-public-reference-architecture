"""Visible architecture, governance, budget, and threshold state."""

from __future__ import annotations

from collections.abc import Mapping
from copy import deepcopy
from dataclasses import dataclass, field, fields
from types import MappingProxyType
from typing import TYPE_CHECKING, Literal

from .core import (
    AuditRecord,
    DiagnosticMixin,
    EscalationEvent,
    GraphUpdate,
    JSONValue,
    RollbackPoint,
    StateChange,
    SymbolicStructure,
)
from .enums import BudgetType, GovernanceMode
from .graphs import (
    AuthorityGraph,
    CoherenceGraph,
    EvidenceGraph,
    MemoryGraph,
    ScaleGraph,
)

if TYPE_CHECKING:
    from .registry import AlgorithmRegistry

ThresholdDirection = Literal["minimum_required", "maximum_allowed"]
BudgetPressureLevel = Literal["available", "low", "critical", "exhausted"]

LOW_BUDGET_BOUNDARY = 0.25
CRITICAL_BUDGET_BOUNDARY = 0.10

THRESHOLD_DIRECTIONS: Mapping[str, ThresholdDirection] = MappingProxyType(
    {
        "identity_threshold": "minimum_required",
        "stability_threshold": "minimum_required",
        "constitutional_risk_threshold": "maximum_allowed",
        "novelty_threshold": "maximum_allowed",
        "grounding_threshold": "minimum_required",
        "persistence_threshold": "minimum_required",
        "coherence_threshold": "maximum_allowed",
        "multi_scale_threshold": "minimum_required",
        "architectural_fitness_threshold": "minimum_required",
        "legitimacy_threshold": "minimum_required",
        "escalation_threshold": "maximum_allowed",
    }
)

THRESHOLD_MEANINGS: Mapping[str, str] = MappingProxyType(
    {
        "identity_threshold": "minimum identity continuity score",
        "stability_threshold": "minimum remaining stability capacity",
        "constitutional_risk_threshold": "maximum constitutional risk",
        "novelty_threshold": "maximum unresolved novelty pressure",
        "grounding_threshold": "minimum grounding score",
        "persistence_threshold": "minimum persistence score",
        "coherence_threshold": "maximum unresolved coherence pressure",
        "multi_scale_threshold": "minimum multi-scale coherence score",
        "architectural_fitness_threshold": "minimum architectural fitness",
        "legitimacy_threshold": "minimum governance legitimacy",
        "escalation_threshold": "maximum locally manageable review burden",
    }
)

_BUDGET_FIELDS: Mapping[BudgetType, str] = MappingProxyType(
    {
        BudgetType.STABILITY: "stability_budget",
        BudgetType.NOVELTY: "novelty_budget",
        BudgetType.VERIFICATION: "verification_budget",
        BudgetType.ATTENTION: "attention_budget",
        BudgetType.RECOVERY: "recovery_capacity",
    }
)

_BUDGET_ROUTES: Mapping[BudgetType, str] = MappingProxyType(
    {
        BudgetType.STABILITY: "stability_review",
        BudgetType.NOVELTY: "novelty_scope_reduction",
        BudgetType.VERIFICATION: "verification_delay",
        BudgetType.ATTENTION: "attention_scope_reduction",
        BudgetType.RECOVERY: "recovery_review",
    }
)


def _require_nonempty_text(value: str, field_name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a nonempty string")


def _require_normalized(value: float, field_name: str) -> None:
    if not isinstance(value, int | float) or isinstance(value, bool):
        raise TypeError(f"{field_name} must be numeric")
    if not 0.0 <= float(value) <= 1.0:
        raise ValueError(f"{field_name} must be in [0.0, 1.0]")


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


def _require_model_list(
    values: list[object],
    model_type: type[object],
    field_name: str,
) -> None:
    if not isinstance(values, list):
        raise TypeError(f"{field_name} must be a list")
    for position, value in enumerate(values):
        if not isinstance(value, model_type):
            raise TypeError(
                f"{field_name}[{position}] must be {model_type.__name__}"
            )


def _default_algorithm_registry() -> AlgorithmRegistry:
    from .registry import create_default_registry

    return create_default_registry()


@dataclass(slots=True)
class GovernanceState(DiagnosticMixin):
    """The active governance posture, distinct from authority relations."""

    governance_mode: GovernanceMode = GovernanceMode.NORMAL
    authority_graph: AuthorityGraph = field(default_factory=AuthorityGraph)
    active_vetoes: list[dict[str, JSONValue]] = field(default_factory=list)
    pending_escalations: list[EscalationEvent] = field(default_factory=list)
    governance_memory: list[dict[str, JSONValue]] = field(
        default_factory=list
    )

    def __post_init__(self) -> None:
        if not isinstance(self.governance_mode, GovernanceMode):
            raise TypeError("governance_mode must be GovernanceMode")
        if not isinstance(self.authority_graph, AuthorityGraph):
            raise TypeError("authority_graph must be AuthorityGraph")
        _require_record_list(self.active_vetoes, "active_vetoes")
        _require_model_list(
            self.pending_escalations,
            EscalationEvent,
            "pending_escalations",
        )
        _require_record_list(self.governance_memory, "governance_memory")


@dataclass(slots=True)
class BudgetState(DiagnosticMixin):
    """Normalized available capacities; 0.0 is exhausted and 1.0 is full."""

    stability_budget: float = 1.0
    novelty_budget: float = 1.0
    verification_budget: float = 1.0
    attention_budget: float = 1.0
    recovery_capacity: float = 1.0

    def __post_init__(self) -> None:
        for budget_field in fields(self):
            _require_normalized(
                getattr(self, budget_field.name),
                budget_field.name,
            )

    def values_by_type(self) -> dict[BudgetType, float]:
        return {
            budget_type: getattr(self, field_name)
            for budget_type, field_name in _BUDGET_FIELDS.items()
        }


@dataclass(slots=True)
class ThresholdState(DiagnosticMixin):
    """Provisional visible thresholds with externally declared direction."""

    identity_threshold: float = 0.80
    stability_threshold: float = 0.25
    constitutional_risk_threshold: float = 0.30
    novelty_threshold: float = 0.50
    grounding_threshold: float = 0.70
    persistence_threshold: float = 0.75
    coherence_threshold: float = 0.30
    multi_scale_threshold: float = 0.75
    architectural_fitness_threshold: float = 0.80
    legitimacy_threshold: float = 0.85
    escalation_threshold: float = 0.65

    def __post_init__(self) -> None:
        for threshold_field in fields(self):
            _require_normalized(
                getattr(self, threshold_field.name),
                threshold_field.name,
            )


@dataclass(slots=True)
class ArchitectureState(DiagnosticMixin):
    """The visible mutable domain state for one ACI prototype cycle."""

    state_id: str
    active_structures: dict[str, SymbolicStructure] = field(
        default_factory=dict
    )
    memory_graph: MemoryGraph = field(default_factory=MemoryGraph)
    evidence_graph: EvidenceGraph = field(default_factory=EvidenceGraph)
    coherence_graph: CoherenceGraph = field(default_factory=CoherenceGraph)
    scale_graph: ScaleGraph = field(default_factory=ScaleGraph)
    governance_state: GovernanceState = field(default_factory=GovernanceState)
    budgets: BudgetState = field(default_factory=BudgetState)
    thresholds: ThresholdState = field(default_factory=ThresholdState)
    algorithm_registry: AlgorithmRegistry = field(
        default_factory=_default_algorithm_registry
    )
    audit_log: list[AuditRecord] = field(default_factory=list)
    rollback_points: list[RollbackPoint] = field(default_factory=list)
    applied_graph_updates: list[GraphUpdate] = field(default_factory=list)
    monitoring_triggers: list[str] = field(default_factory=list)
    state_changes: list[StateChange] = field(default_factory=list)

    def __post_init__(self) -> None:
        _require_nonempty_text(self.state_id, "state_id")
        if not isinstance(self.active_structures, dict):
            raise TypeError("active_structures must be a dictionary")
        for structure_id, structure in self.active_structures.items():
            _require_nonempty_text(structure_id, "active_structures key")
            if not isinstance(structure, SymbolicStructure):
                raise TypeError(
                    "active_structures values must be SymbolicStructure"
                )
            if structure.structure_id != structure_id:
                raise ValueError(
                    "active structure key must match "
                    "SymbolicStructure.structure_id"
                )
        if not isinstance(self.memory_graph, MemoryGraph):
            raise TypeError("memory_graph must be MemoryGraph")
        if not isinstance(self.evidence_graph, EvidenceGraph):
            raise TypeError("evidence_graph must be EvidenceGraph")
        if not isinstance(self.coherence_graph, CoherenceGraph):
            raise TypeError("coherence_graph must be CoherenceGraph")
        if not isinstance(self.scale_graph, ScaleGraph):
            raise TypeError("scale_graph must be ScaleGraph")
        if not isinstance(self.governance_state, GovernanceState):
            raise TypeError("governance_state must be GovernanceState")
        if not isinstance(self.budgets, BudgetState):
            raise TypeError("budgets must be BudgetState")
        if not isinstance(self.thresholds, ThresholdState):
            raise TypeError("thresholds must be ThresholdState")
        from .registry import AlgorithmRegistry

        if not isinstance(self.algorithm_registry, AlgorithmRegistry):
            raise TypeError("algorithm_registry must be AlgorithmRegistry")
        _require_model_list(self.audit_log, AuditRecord, "audit_log")
        _require_model_list(
            self.rollback_points,
            RollbackPoint,
            "rollback_points",
        )
        _require_model_list(
            self.applied_graph_updates,
            GraphUpdate,
            "applied_graph_updates",
        )
        if not isinstance(self.monitoring_triggers, list):
            raise TypeError("monitoring_triggers must be a list")
        for position, trigger in enumerate(self.monitoring_triggers):
            _require_nonempty_text(
                trigger,
                f"monitoring_triggers[{position}]",
            )
        _require_model_list(
            self.state_changes,
            StateChange,
            "state_changes",
        )


@dataclass(frozen=True, slots=True)
class StateBaseline:
    """A logically read-only captured state that only returns deep copies."""

    source_state_id: str
    _snapshot: ArchitectureState = field(repr=False, compare=False)

    def __post_init__(self) -> None:
        _require_nonempty_text(self.source_state_id, "source_state_id")
        if not isinstance(self._snapshot, ArchitectureState):
            raise TypeError("_snapshot must be ArchitectureState")
        object.__setattr__(self, "_snapshot", clone_state(self._snapshot))

    def clone(self) -> ArchitectureState:
        return clone_state(self._snapshot)


def clone_state(state: ArchitectureState) -> ArchitectureState:
    """Return a fully isolated working copy of architecture state."""

    if not isinstance(state, ArchitectureState):
        raise TypeError("state must be ArchitectureState")
    return deepcopy(state)


def capture_baseline(state: ArchitectureState) -> StateBaseline:
    """Capture a private state copy that can create isolated working states."""

    if not isinstance(state, ArchitectureState):
        raise TypeError("state must be ArchitectureState")
    return StateBaseline(
        source_state_id=state.state_id,
        _snapshot=state,
    )


def classify_budget_capacity(value: float) -> BudgetPressureLevel:
    """Classify remaining capacity without consuming or restoring budget."""

    _require_normalized(value, "budget value")
    if value == 0.0:
        return "exhausted"
    if value <= CRITICAL_BUDGET_BOUNDARY:
        return "critical"
    if value <= LOW_BUDGET_BOUNDARY:
        return "low"
    return "available"


def budget_pressure(
    budgets: BudgetState,
) -> dict[BudgetType, BudgetPressureLevel]:
    """Expose pressure by budget domain for later routing decisions."""

    if not isinstance(budgets, BudgetState):
        raise TypeError("budgets must be BudgetState")
    return {
        budget_type: classify_budget_capacity(value)
        for budget_type, value in budgets.values_by_type().items()
    }


def budget_routing_signals(budgets: BudgetState) -> tuple[str, ...]:
    """Produce non-authorizing routing signals from current budget pressure."""

    pressures = budget_pressure(budgets)
    return tuple(
        f"{pressure}:{_BUDGET_ROUTES[budget_type]}"
        for budget_type, pressure in pressures.items()
        if pressure != "available"
    )


def threshold_direction(threshold_name: str) -> ThresholdDirection:
    """Return the explicit comparison direction for one threshold."""

    _require_nonempty_text(threshold_name, "threshold_name")
    try:
        return THRESHOLD_DIRECTIONS[threshold_name]
    except KeyError as error:
        raise KeyError(f"unknown threshold: {threshold_name}") from error


def threshold_meaning(threshold_name: str) -> str:
    """Return the declared v0.1 interpretation of one threshold."""

    _require_nonempty_text(threshold_name, "threshold_name")
    try:
        return THRESHOLD_MEANINGS[threshold_name]
    except KeyError as error:
        raise KeyError(f"unknown threshold: {threshold_name}") from error


def threshold_passes(
    thresholds: ThresholdState,
    threshold_name: str,
    observed_value: float,
) -> bool:
    """Evaluate a visible threshold without granting authority or mutating state."""

    if not isinstance(thresholds, ThresholdState):
        raise TypeError("thresholds must be ThresholdState")
    _require_normalized(observed_value, "observed_value")
    direction = threshold_direction(threshold_name)
    threshold_value = getattr(thresholds, threshold_name)
    if direction == "minimum_required":
        return observed_value >= threshold_value
    return observed_value <= threshold_value


def threshold_requires_review(
    thresholds: ThresholdState,
    threshold_name: str,
    observed_value: float,
) -> bool:
    """Expose a later-routing signal without performing the review."""

    return not threshold_passes(
        thresholds,
        threshold_name,
        observed_value,
    )


__all__ = [
    "ArchitectureState",
    "BudgetPressureLevel",
    "BudgetState",
    "CRITICAL_BUDGET_BOUNDARY",
    "GovernanceState",
    "LOW_BUDGET_BOUNDARY",
    "StateBaseline",
    "THRESHOLD_DIRECTIONS",
    "THRESHOLD_MEANINGS",
    "ThresholdDirection",
    "ThresholdState",
    "budget_pressure",
    "budget_routing_signals",
    "capture_baseline",
    "classify_budget_capacity",
    "clone_state",
    "threshold_direction",
    "threshold_meaning",
    "threshold_passes",
    "threshold_requires_review",
]
