"""Append-only dependent review context with isolated read views."""

from __future__ import annotations

from collections.abc import Callable, Iterable
from copy import deepcopy
from dataclasses import dataclass
from typing import Literal

from .core import (
    DiagnosticMixin,
    ReviewDecision,
    ScoreBundle,
    SymbolicStructure,
)
from .enums import AlgorithmName, DecisionStatus
from .state import ArchitectureState, clone_state

ScoreField = Literal[
    "grounding_score",
    "coherence_score",
    "persistence_score",
    "multi_scale_coherence_score",
    "stability_score",
    "novelty_score",
    "legitimacy_score",
    "confidence_score",
    "risk_score",
    "identity_risk_score",
    "constitutional_risk_score",
]

SCORE_FIELDS = frozenset(ScoreBundle.__dataclass_fields__)


class ReviewContextError(ValueError):
    """Raised when review provenance or target identity is invalid."""


class AlgorithmContractError(RuntimeError):
    """Raised when a reviewer returns or mutates outside its contract."""


@dataclass(frozen=True, slots=True)
class UnresolvedReviewItem(DiagnosticMixin):
    item_id: str
    target_id: str
    reason: str
    decision_ref: str | None = None

    def __post_init__(self) -> None:
        _require_nonempty_text(self.item_id, "item_id")
        _require_nonempty_text(self.target_id, "target_id")
        _require_nonempty_text(self.reason, "reason")
        if self.decision_ref is not None:
            _require_nonempty_text(self.decision_ref, "decision_ref")


@dataclass(frozen=True, slots=True)
class ReviewTraceEntry(DiagnosticMixin):
    sequence: int
    algorithm_name: AlgorithmName
    target_id: str
    decision_id: str

    def __post_init__(self) -> None:
        if not isinstance(self.sequence, int) or isinstance(self.sequence, bool):
            raise TypeError("sequence must be int")
        if self.sequence < 1:
            raise ValueError("sequence must be positive")
        if not isinstance(self.algorithm_name, AlgorithmName):
            raise TypeError("algorithm_name must be AlgorithmName")
        _require_nonempty_text(self.target_id, "target_id")
        _require_nonempty_text(self.decision_id, "decision_id")


@dataclass(slots=True)
class _ReviewCheckpoint:
    audit_id: str
    state_snapshot: ArchitectureState
    targets: dict[str, SymbolicStructure]
    decisions: list[ReviewDecision]
    unresolved_items: list[UnresolvedReviewItem]
    review_trace: list[ReviewTraceEntry]


class ReviewContext(DiagnosticMixin):
    """Read-isolated state plus append-only review evidence."""

    __slots__ = (
        "_audit_id",
        "_state_snapshot",
        "_targets",
        "_decisions",
        "_unresolved_items",
        "_review_trace",
    )

    def __init__(
        self,
        *,
        audit_id: str,
        architecture_state: ArchitectureState,
        targets: Iterable[SymbolicStructure],
        unresolved_items: Iterable[UnresolvedReviewItem] = (),
    ) -> None:
        _require_nonempty_text(audit_id, "audit_id")
        if not isinstance(architecture_state, ArchitectureState):
            raise TypeError("architecture_state must be ArchitectureState")

        target_index: dict[str, SymbolicStructure] = {}
        for position, target in enumerate(targets):
            if not isinstance(target, SymbolicStructure):
                raise TypeError(
                    f"targets[{position}] must be SymbolicStructure"
                )
            if target.structure_id in target_index:
                raise ReviewContextError(
                    f"duplicate target_id: {target.structure_id}"
                )
            target_index[target.structure_id] = deepcopy(target)

        self._audit_id = audit_id
        self._state_snapshot = clone_state(architecture_state)
        self._targets = target_index
        self._decisions: list[ReviewDecision] = []
        self._unresolved_items: list[UnresolvedReviewItem] = []
        self._review_trace: list[ReviewTraceEntry] = []
        for item in unresolved_items:
            self.record_unresolved(item)

    @property
    def audit_id(self) -> str:
        return self._audit_id

    @property
    def architecture_state(self) -> ArchitectureState:
        """Return an isolated read view, never the authoritative object."""

        return clone_state(self._state_snapshot)

    @property
    def architecture_state_ref(self) -> str:
        return self._state_snapshot.state_id

    @property
    def targets(self) -> tuple[SymbolicStructure, ...]:
        return tuple(deepcopy(target) for target in self._targets.values())

    @property
    def target_ids(self) -> tuple[str, ...]:
        return tuple(self._targets)

    @property
    def decisions(self) -> tuple[ReviewDecision, ...]:
        return tuple(deepcopy(decision) for decision in self._decisions)

    @property
    def unresolved_items(self) -> tuple[UnresolvedReviewItem, ...]:
        return tuple(self._unresolved_items)

    @property
    def review_trace(self) -> tuple[ReviewTraceEntry, ...]:
        return tuple(self._review_trace)

    def get_target(self, target_id: str) -> SymbolicStructure:
        _require_nonempty_text(target_id, "target_id")
        try:
            return deepcopy(self._targets[target_id])
        except KeyError as error:
            raise ReviewContextError(
                f"unknown target_id: {target_id}"
            ) from error

    def decisions_for(self, target_id: str) -> tuple[ReviewDecision, ...]:
        self.get_target(target_id)
        return tuple(
            deepcopy(decision)
            for decision in self._decisions
            if decision.target_id == target_id
        )

    def latest_by_algorithm(
        self,
        target_id: str,
        algorithm: AlgorithmName,
    ) -> ReviewDecision | None:
        self.get_target(target_id)
        if not isinstance(algorithm, AlgorithmName):
            raise TypeError("algorithm must be AlgorithmName")
        for decision in reversed(self._decisions):
            if (
                decision.target_id == target_id
                and decision.algorithm_name is algorithm
            ):
                return deepcopy(decision)
        return None

    def latest_score(
        self,
        target_id: str,
        algorithm: AlgorithmName,
        score_field: ScoreField,
    ) -> float | None:
        if score_field not in SCORE_FIELDS:
            raise ValueError(f"unknown score_field: {score_field}")
        decision = self.latest_by_algorithm(target_id, algorithm)
        if decision is None:
            return None
        return float(getattr(decision.scores, score_field))

    def latest_grounding(self, target_id: str) -> ReviewDecision | None:
        return self.latest_by_algorithm(target_id, AlgorithmName.GEA)

    def latest_coherence(self, target_id: str) -> ReviewDecision | None:
        return self.latest_by_algorithm(target_id, AlgorithmName.CRA)

    def latest_persistence(self, target_id: str) -> ReviewDecision | None:
        return self.latest_by_algorithm(target_id, AlgorithmName.PCA)

    def latest_scale(self, target_id: str) -> ReviewDecision | None:
        return self.latest_by_algorithm(target_id, AlgorithmName.MSSA)

    def has_blocking_decision(self, target_id: str) -> bool:
        blocking_statuses = {
            DecisionStatus.BLOCKED,
            DecisionStatus.ESCALATED,
            DecisionStatus.PENDING_REVIEW,
        }
        return any(
            decision.status in blocking_statuses
            for decision in self.decisions_for(target_id)
        )

    def append_decision(self, decision: ReviewDecision) -> None:
        self.append_decisions((decision,))

    def append_decisions(
        self,
        decisions: Iterable[ReviewDecision],
    ) -> None:
        pending = list(decisions)
        known_ids = {decision.decision_id for decision in self._decisions}
        validated: list[ReviewDecision] = []
        for position, decision in enumerate(pending):
            if not isinstance(decision, ReviewDecision):
                raise TypeError(
                    f"decisions[{position}] must be ReviewDecision"
                )
            self._validate_decision(decision, known_ids)
            known_ids.add(decision.decision_id)
            validated.append(deepcopy(decision))

        for decision in validated:
            self._decisions.append(decision)
            self._review_trace.append(
                ReviewTraceEntry(
                    sequence=len(self._review_trace) + 1,
                    algorithm_name=decision.algorithm_name,
                    target_id=decision.target_id,
                    decision_id=decision.decision_id,
                )
            )

    def record_unresolved(self, item: UnresolvedReviewItem) -> None:
        if not isinstance(item, UnresolvedReviewItem):
            raise TypeError("item must be UnresolvedReviewItem")
        if item.target_id not in self._targets:
            raise ReviewContextError(
                f"unknown target_id: {item.target_id}"
            )
        if any(
            existing.item_id == item.item_id
            for existing in self._unresolved_items
        ):
            raise ReviewContextError(
                f"duplicate unresolved item_id: {item.item_id}"
            )
        if (
            item.decision_ref is not None
            and item.decision_ref
            not in {decision.decision_id for decision in self._decisions}
        ):
            raise ReviewContextError(
                f"unknown decision_ref: {item.decision_ref}"
            )
        self._unresolved_items.append(item)

    def unresolved_for(
        self,
        target_id: str,
    ) -> tuple[UnresolvedReviewItem, ...]:
        self.get_target(target_id)
        return tuple(
            item
            for item in self._unresolved_items
            if item.target_id == target_id
        )

    def to_dict(self) -> dict[str, object]:
        return {
            "audit_id": self.audit_id,
            "architecture_state_ref": self.architecture_state_ref,
            "target_ids": list(self.target_ids),
            "decisions": [
                decision.to_dict() for decision in self._decisions
            ],
            "unresolved_items": [
                item.to_dict() for item in self._unresolved_items
            ],
            "review_trace": [
                entry.to_dict() for entry in self._review_trace
            ],
        }

    def _validate_decision(
        self,
        decision: ReviewDecision,
        known_ids: set[str],
    ) -> None:
        if decision.audit_id != self.audit_id:
            raise ReviewContextError(
                f"decision audit_id must reference {self.audit_id}"
            )
        if decision.target_id not in self._targets:
            raise ReviewContextError(
                f"unknown target_id: {decision.target_id}"
            )
        if decision.decision_id in known_ids:
            raise ReviewContextError(
                f"duplicate decision_id: {decision.decision_id}"
            )

    def _checkpoint(self) -> _ReviewCheckpoint:
        return _ReviewCheckpoint(
            audit_id=self._audit_id,
            state_snapshot=clone_state(self._state_snapshot),
            targets=deepcopy(self._targets),
            decisions=deepcopy(self._decisions),
            unresolved_items=list(self._unresolved_items),
            review_trace=list(self._review_trace),
        )

    def _restore(self, checkpoint: _ReviewCheckpoint) -> None:
        self._audit_id = checkpoint.audit_id
        self._state_snapshot = clone_state(checkpoint.state_snapshot)
        self._targets = deepcopy(checkpoint.targets)
        self._decisions = deepcopy(checkpoint.decisions)
        self._unresolved_items = list(checkpoint.unresolved_items)
        self._review_trace = list(checkpoint.review_trace)

    def _assert_contract_integrity(
        self,
        checkpoint: _ReviewCheckpoint,
    ) -> None:
        if (
            self._audit_id != checkpoint.audit_id
            or self._state_snapshot != checkpoint.state_snapshot
            or self._targets != checkpoint.targets
        ):
            raise AlgorithmContractError(
                "review algorithm mutated audit, state, or target inputs"
            )

        decision_count = len(checkpoint.decisions)
        unresolved_count = len(checkpoint.unresolved_items)
        trace_count = len(checkpoint.review_trace)
        if (
            len(self._decisions) < decision_count
            or self._decisions[:decision_count] != checkpoint.decisions
            or len(self._unresolved_items) < unresolved_count
            or self._unresolved_items[:unresolved_count]
            != checkpoint.unresolved_items
            or len(self._review_trace) < trace_count
            or self._review_trace[:trace_count] != checkpoint.review_trace
        ):
            raise AlgorithmContractError(
                "review algorithm altered existing review history"
            )

        if len(self._review_trace) != len(self._decisions):
            raise AlgorithmContractError(
                "review algorithm bypassed ordered decision tracing"
            )

        known_ids: set[str] = set()
        for sequence, (decision, trace) in enumerate(
            zip(self._decisions, self._review_trace, strict=True),
            start=1,
        ):
            self._validate_decision(decision, known_ids)
            known_ids.add(decision.decision_id)
            if trace != ReviewTraceEntry(
                sequence=sequence,
                algorithm_name=decision.algorithm_name,
                target_id=decision.target_id,
                decision_id=decision.decision_id,
            ):
                raise AlgorithmContractError(
                    "review algorithm corrupted ordered decision tracing"
                )

        unresolved_ids: set[str] = set()
        for item in self._unresolved_items:
            if item.item_id in unresolved_ids:
                raise AlgorithmContractError(
                    "review algorithm duplicated an unresolved item"
                )
            unresolved_ids.add(item.item_id)
            if item.target_id not in self._targets:
                raise AlgorithmContractError(
                    "review algorithm added an unresolved item for an "
                    "unknown target"
                )
            if (
                item.decision_ref is not None
                and item.decision_ref not in known_ids
            ):
                raise AlgorithmContractError(
                    "review algorithm added an unresolved item with an "
                    "unknown decision reference"
                )


ReviewAlgorithm = Callable[[ReviewContext], None]


def run_algorithm_where_required(
    context: ReviewContext,
    algorithm: ReviewAlgorithm,
) -> None:
    """Run a reviewer that may append evidence but may return no mutation."""

    if not isinstance(context, ReviewContext):
        raise TypeError("context must be ReviewContext")
    if not callable(algorithm):
        raise TypeError("algorithm must be callable")

    checkpoint = context._checkpoint()
    try:
        result = algorithm(context)
        if result is not None:
            raise AlgorithmContractError(
                "review algorithm must append decisions and return None"
            )
        context._assert_contract_integrity(checkpoint)
    except Exception:
        context._restore(checkpoint)
        raise


def _require_nonempty_text(value: str, field_name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ReviewContextError(
            f"{field_name} must be a nonempty string"
        )


__all__ = [
    "AlgorithmContractError",
    "ReviewAlgorithm",
    "ReviewContext",
    "ReviewContextError",
    "ReviewTraceEntry",
    "SCORE_FIELDS",
    "ScoreField",
    "UnresolvedReviewItem",
    "run_algorithm_where_required",
]
