"""Enforceable procedural authority registry for Minimal ACI v0.1."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from types import MappingProxyType
from typing import Any

from .core import DiagnosticMixin, ReviewDecision, SymbolicStructure
from .enums import (
    AlgorithmName,
    AuthorityLevel,
    DecisionStatus,
    DecisionType,
    ScaleLabel,
    StructureType,
)

REGISTRY_CHANGE_KINDS = (
    "registry_entry",
    "authority",
    "threshold",
    "escalation_pathway",
    "call_order",
)

SCALE_RANK = {
    ScaleLabel.OBSERVATION: 0,
    ScaleLabel.CLAIM: 1,
    ScaleLabel.HYPOTHESIS: 2,
    ScaleLabel.MEMORY: 3,
    ScaleLabel.PRINCIPLE: 4,
    ScaleLabel.ARCHITECTURE: 5,
    ScaleLabel.CONSTITUTIONAL: 6,
}

AUTHORITY_RANK = {
    AuthorityLevel.NONE: 0,
    AuthorityLevel.TEMPORARY_USE: 1,
    AuthorityLevel.ACTIVE_REASONING: 2,
    AuthorityLevel.MEMORY_INFLUENCE: 3,
    AuthorityLevel.ARCHITECTURAL_INFLUENCE: 4,
    AuthorityLevel.INVARIANT_CONSTRAINT: 5,
    AuthorityLevel.CONSTITUTIONAL_AUTHORITY: 6,
}

STUB_DECISION_TYPES = (
    DecisionType.SANDBOX,
    DecisionType.DELAY,
    DecisionType.ESCALATE,
)


def _require_nonempty_text(value: str, field_name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a nonempty string")


def _require_bool(value: bool, field_name: str) -> None:
    if not isinstance(value, bool):
        raise TypeError(f"{field_name} must be bool")


def _require_enum_tuple(
    values: tuple[object, ...],
    enum_type: type[object],
    field_name: str,
    *,
    allow_empty: bool = False,
) -> None:
    if not isinstance(values, tuple):
        raise TypeError(f"{field_name} must be a tuple")
    if not values and not allow_empty:
        raise ValueError(f"{field_name} cannot be empty")
    for position, value in enumerate(values):
        if not isinstance(value, enum_type):
            raise TypeError(
                f"{field_name}[{position}] must be {enum_type.__name__}"
            )
    if len(values) != len(set(values)):
        raise ValueError(f"{field_name} must not contain duplicates")


@dataclass(frozen=True, slots=True)
class AlgorithmSpec(DiagnosticMixin):
    """An algorithm's explicit review scope and authority boundary."""

    algorithm_name: AlgorithmName
    purpose: str
    permitted_structure_types: tuple[StructureType, ...]
    permitted_decision_types: tuple[DecisionType, ...]
    authority_level: AuthorityLevel
    maximum_target_scale: ScaleLabel
    permitted_escalation_targets: tuple[AlgorithmName, ...]
    protected: bool
    stub: bool
    state_mutation_prohibited: bool = True
    coordinator: bool = False

    def __post_init__(self) -> None:
        if not isinstance(self.algorithm_name, AlgorithmName):
            raise TypeError("algorithm_name must be AlgorithmName")
        _require_nonempty_text(self.purpose, "purpose")
        _require_enum_tuple(
            self.permitted_structure_types,
            StructureType,
            "permitted_structure_types",
        )
        _require_enum_tuple(
            self.permitted_decision_types,
            DecisionType,
            "permitted_decision_types",
            allow_empty=self.coordinator,
        )
        if not isinstance(self.authority_level, AuthorityLevel):
            raise TypeError("authority_level must be AuthorityLevel")
        if not isinstance(self.maximum_target_scale, ScaleLabel):
            raise TypeError("maximum_target_scale must be ScaleLabel")
        _require_enum_tuple(
            self.permitted_escalation_targets,
            AlgorithmName,
            "permitted_escalation_targets",
            allow_empty=True,
        )
        _require_bool(self.protected, "protected")
        _require_bool(self.stub, "stub")
        _require_bool(
            self.state_mutation_prohibited,
            "state_mutation_prohibited",
        )
        _require_bool(self.coordinator, "coordinator")
        if self.algorithm_name in self.permitted_escalation_targets:
            raise ValueError("algorithm cannot escalate to itself")
        if self.coordinator and self.algorithm_name is not AlgorithmName.ICC:
            raise ValueError("only ICC may be registered as coordinator")
        if self.coordinator and self.stub:
            raise ValueError("coordinator cannot be a reviewer stub")
        if self.coordinator and self.permitted_decision_types:
            raise ValueError("coordinator cannot issue review decisions")
        if not self.coordinator and not self.state_mutation_prohibited:
            raise ValueError("reviewers must prohibit direct state mutation")
        if self.stub and not set(self.permitted_decision_types).issubset(
            STUB_DECISION_TYPES
        ):
            raise ValueError(
                "stub decisions are limited to sandbox, delay, or escalation"
            )


@dataclass(frozen=True, slots=True)
class RegistryChangeRequest(DiagnosticMixin):
    """A visible but non-applicable v0.1 request to change procedural power."""

    request_id: str
    proposer_algorithm: AlgorithmName
    target_algorithm: AlgorithmName
    change_kind: str
    reason: str
    audit_ref: str | None = None

    def __post_init__(self) -> None:
        _require_nonempty_text(self.request_id, "request_id")
        if not isinstance(self.proposer_algorithm, AlgorithmName):
            raise TypeError("proposer_algorithm must be AlgorithmName")
        if not isinstance(self.target_algorithm, AlgorithmName):
            raise TypeError("target_algorithm must be AlgorithmName")
        _require_nonempty_text(self.change_kind, "change_kind")
        if self.change_kind not in REGISTRY_CHANGE_KINDS:
            raise ValueError(f"unsupported change_kind: {self.change_kind}")
        _require_nonempty_text(self.reason, "reason")
        if self.audit_ref is not None:
            _require_nonempty_text(self.audit_ref, "audit_ref")


@dataclass(frozen=True, slots=True)
class ValidationIssue(DiagnosticMixin):
    code: str
    message: str
    field_name: str | None = None

    def __post_init__(self) -> None:
        _require_nonempty_text(self.code, "code")
        _require_nonempty_text(self.message, "message")
        if self.field_name is not None:
            _require_nonempty_text(self.field_name, "field_name")


@dataclass(frozen=True, slots=True)
class DecisionValidationResult(DiagnosticMixin):
    decision_id: str
    target_id: str
    algorithm_identity: str
    accepted: bool
    issues: tuple[ValidationIssue, ...]

    def __post_init__(self) -> None:
        _require_nonempty_text(self.decision_id, "decision_id")
        _require_nonempty_text(self.target_id, "target_id")
        _require_nonempty_text(self.algorithm_identity, "algorithm_identity")
        _require_bool(self.accepted, "accepted")
        if not isinstance(self.issues, tuple):
            raise TypeError("issues must be a tuple")
        for position, issue in enumerate(self.issues):
            if not isinstance(issue, ValidationIssue):
                raise TypeError(
                    f"issues[{position}] must be ValidationIssue"
                )
        if self.accepted == bool(self.issues):
            raise ValueError("accepted must be true exactly when issues are empty")

    @property
    def reason_codes(self) -> tuple[str, ...]:
        return tuple(issue.code for issue in self.issues)


@dataclass(frozen=True, slots=True)
class AlgorithmRegistry(DiagnosticMixin):
    """The complete v0.1 procedural authority map."""

    algorithms: Mapping[AlgorithmName, AlgorithmSpec]

    def __post_init__(self) -> None:
        if not isinstance(self.algorithms, Mapping):
            raise TypeError("algorithms must be a mapping")
        algorithms = dict(self.algorithms)
        for algorithm_name, spec in algorithms.items():
            if not isinstance(algorithm_name, AlgorithmName):
                raise TypeError("algorithm keys must be AlgorithmName")
            if not isinstance(spec, AlgorithmSpec):
                raise TypeError("algorithm values must be AlgorithmSpec")
            if spec.algorithm_name is not algorithm_name:
                raise ValueError(
                    "registry key must match AlgorithmSpec.algorithm_name"
                )

        required = set(AlgorithmName)
        missing = required.difference(algorithms)
        if missing:
            missing_names = ", ".join(
                sorted(algorithm.name for algorithm in missing)
            )
            raise ValueError(f"registry missing algorithms: {missing_names}")

        for spec in algorithms.values():
            for escalation_target in spec.permitted_escalation_targets:
                if escalation_target not in algorithms:
                    raise ValueError(
                        "escalation target must be registered: "
                        f"{escalation_target.name}"
                    )

        icc = algorithms[AlgorithmName.ICC]
        if not icc.coordinator or not icc.protected:
            raise ValueError("ICC must be a protected coordinator")
        object.__setattr__(
            self,
            "algorithms",
            MappingProxyType(algorithms),
        )

    def __deepcopy__(self, memo: dict[int, Any]) -> "AlgorithmRegistry":
        return self

    def get_spec(self, algorithm_name: AlgorithmName) -> AlgorithmSpec:
        if not isinstance(algorithm_name, AlgorithmName):
            raise TypeError("algorithm_name must be AlgorithmName")
        return self.algorithms[algorithm_name]

    def validate_decision(
        self,
        decision: ReviewDecision,
        target: SymbolicStructure,
        *,
        change_request: RegistryChangeRequest | None = None,
    ) -> DecisionValidationResult:
        return validate_review_decision(
            self,
            decision,
            target,
            change_request=change_request,
        )


def _parse_algorithm_reference(value: str | None) -> AlgorithmName | None:
    if value is None:
        return None
    try:
        return AlgorithmName(value)
    except ValueError:
        try:
            return AlgorithmName[value]
        except KeyError:
            return None


def validate_review_decision(
    registry: AlgorithmRegistry,
    decision: ReviewDecision,
    target: SymbolicStructure,
    *,
    change_request: RegistryChangeRequest | None = None,
) -> DecisionValidationResult:
    """Return all authority violations without mutating or dropping a decision."""

    if not isinstance(registry, AlgorithmRegistry):
        raise TypeError("registry must be AlgorithmRegistry")
    if not isinstance(decision, ReviewDecision):
        raise TypeError("decision must be ReviewDecision")
    if not isinstance(target, SymbolicStructure):
        raise TypeError("target must be SymbolicStructure")
    if change_request is not None and not isinstance(
        change_request,
        RegistryChangeRequest,
    ):
        raise TypeError("change_request must be RegistryChangeRequest or None")

    issues: list[ValidationIssue] = []
    algorithm_value = decision.algorithm_name
    if isinstance(algorithm_value, AlgorithmName):
        algorithm_identity = algorithm_value.value
        spec = registry.algorithms.get(algorithm_value)
    else:
        algorithm_identity = str(algorithm_value).strip() or "<empty>"
        spec = None

    if spec is None:
        issues.append(
            ValidationIssue(
                code="unregistered_algorithm",
                message="decision algorithm identity is not registered",
                field_name="algorithm_name",
            )
        )

    if decision.target_id != target.structure_id:
        issues.append(
            ValidationIssue(
                code="target_id_mismatch",
                message="decision target does not match reviewed structure",
                field_name="target_id",
            )
        )

    if spec is not None:
        if spec.coordinator:
            issues.append(
                ValidationIssue(
                    code="coordinator_not_reviewer",
                    message="ICC coordinates review and cannot issue ReviewDecision",
                    field_name="algorithm_name",
                )
            )
        if target.structure_type not in spec.permitted_structure_types:
            issues.append(
                ValidationIssue(
                    code="target_type_not_permitted",
                    message=(
                        f"{spec.algorithm_name.name} cannot review "
                        f"{target.structure_type.name}"
                    ),
                    field_name="structure_type",
                )
            )
        if not isinstance(decision.decision_type, DecisionType):
            issues.append(
                ValidationIssue(
                    code="invalid_decision_type",
                    message="decision type is not a DecisionType",
                    field_name="decision_type",
                )
            )
        elif decision.decision_type not in spec.permitted_decision_types:
            issues.append(
                ValidationIssue(
                    code="decision_type_not_permitted",
                    message=(
                        f"{spec.algorithm_name.name} cannot issue "
                        f"{decision.decision_type.name}"
                    ),
                    field_name="decision_type",
                )
            )
        if (
            SCALE_RANK[target.metadata.scale_label]
            > SCALE_RANK[spec.maximum_target_scale]
        ):
            issues.append(
                ValidationIssue(
                    code="target_scale_exceeds_authority",
                    message=(
                        f"{target.metadata.scale_label.name} exceeds "
                        f"{spec.algorithm_name.name} maximum target scale "
                        f"{spec.maximum_target_scale.name}"
                    ),
                    field_name="scale_label",
                )
            )

        escalating = (
            decision.decision_type is DecisionType.ESCALATE
            or decision.status is DecisionStatus.ESCALATED
        )
        if (
            not escalating
            and AUTHORITY_RANK[target.metadata.authority_level]
            > AUTHORITY_RANK[spec.authority_level]
        ):
            issues.append(
                ValidationIssue(
                    code="target_authority_exceeds_algorithm",
                    message=(
                        f"{target.metadata.authority_level.name} exceeds "
                        f"{spec.algorithm_name.name} authority "
                        f"{spec.authority_level.name}"
                    ),
                    field_name="authority_level",
                )
            )
        escalation_target = _parse_algorithm_reference(
            decision.escalation_target
        )
        if escalating:
            if escalation_target is None:
                issues.append(
                    ValidationIssue(
                        code="invalid_escalation_target",
                        message="escalation target is not a registered identity",
                        field_name="escalation_target",
                    )
                )
            elif escalation_target not in spec.permitted_escalation_targets:
                issues.append(
                    ValidationIssue(
                        code="escalation_target_not_permitted",
                        message=(
                            f"{spec.algorithm_name.name} cannot escalate to "
                            f"{escalation_target.name}"
                        ),
                        field_name="escalation_target",
                    )
                )
        elif decision.escalation_target is not None:
            issues.append(
                ValidationIssue(
                    code="unexpected_escalation_target",
                    message="non-escalation decision names an escalation target",
                    field_name="escalation_target",
                )
            )

        if spec.stub:
            if decision.status is DecisionStatus.FINAL:
                issues.append(
                    ValidationIssue(
                        code="stub_cannot_finalize",
                        message="stub reviewer cannot issue a final decision",
                        field_name="status",
                    )
                )
            if decision.authorized:
                issues.append(
                    ValidationIssue(
                        code="stub_cannot_authorize",
                        message="stub reviewer cannot claim authorization",
                        field_name="authorized",
                    )
                )
        if not spec.state_mutation_prohibited:
            issues.append(
                ValidationIssue(
                    code="reviewer_mutation_not_prohibited",
                    message="reviewer specification permits state mutation",
                    field_name="state_mutation_prohibited",
                )
            )

    if change_request is not None:
        if change_request.proposer_algorithm is not algorithm_value:
            issues.append(
                ValidationIssue(
                    code="change_proposer_mismatch",
                    message="change proposer does not match decision algorithm",
                    field_name="proposer_algorithm",
                )
            )
        if change_request.proposer_algorithm is change_request.target_algorithm:
            issues.append(
                ValidationIssue(
                    code="self_modification_prohibited",
                    message=(
                        "algorithm cannot modify its own registry entry, "
                        "authority, threshold, or pathway"
                    ),
                    field_name="target_algorithm",
                )
            )
        target_spec = registry.algorithms[change_request.target_algorithm]
        if target_spec.protected:
            issues.append(
                ValidationIssue(
                    code="protected_algorithm_change_prohibited",
                    message="protected algorithm changes require later governance",
                    field_name="target_algorithm",
                )
            )
        if (
            change_request.target_algorithm is AlgorithmName.ICC
            and change_request.change_kind in {
                "authority",
                "escalation_pathway",
                "call_order",
            }
        ):
            issues.append(
                ValidationIssue(
                    code="icc_change_prohibited",
                    message="ordinary algorithms cannot modify ICC authority or call order",
                    field_name="target_algorithm",
                )
            )
        issues.append(
            ValidationIssue(
                code="direct_registry_change_prohibited",
                message=(
                    "v0.1 records registry change requests but does not apply "
                    "them directly"
                ),
                field_name="change_request",
            )
        )

    return DecisionValidationResult(
        decision_id=decision.decision_id,
        target_id=target.structure_id,
        algorithm_identity=algorithm_identity,
        accepted=not issues,
        issues=tuple(issues),
    )


def create_default_registry() -> AlgorithmRegistry:
    """Create the complete deterministic v0.1 registry."""

    all_structure_types = tuple(StructureType)
    algorithms = {
        AlgorithmName.IPA: AlgorithmSpec(
            algorithm_name=AlgorithmName.IPA,
            purpose="Detect identity-relevant risk and route protected review.",
            permitted_structure_types=(
                StructureType.ARCHITECTURAL_CANDIDATE,
                StructureType.GOVERNANCE_OBJECT,
                StructureType.CONSTITUTIONAL_OBJECT,
                StructureType.MEMORY_CANDIDATE,
                StructureType.PERSISTENT_KNOWLEDGE,
            ),
            permitted_decision_types=STUB_DECISION_TYPES,
            authority_level=AuthorityLevel.INVARIANT_CONSTRAINT,
            maximum_target_scale=ScaleLabel.CONSTITUTIONAL,
            permitted_escalation_targets=(AlgorithmName.CGA,),
            protected=True,
            stub=True,
        ),
        AlgorithmName.SRA: AlgorithmSpec(
            algorithm_name=AlgorithmName.SRA,
            purpose="Detect stability pressure and route recovery review.",
            permitted_structure_types=(
                StructureType.NOVELTY_CANDIDATE,
                StructureType.COHERENCE_TENSION,
                StructureType.SCALE_CONFLICT,
                StructureType.ARCHITECTURAL_CANDIDATE,
                StructureType.GOVERNANCE_OBJECT,
            ),
            permitted_decision_types=STUB_DECISION_TYPES,
            authority_level=AuthorityLevel.ACTIVE_REASONING,
            maximum_target_scale=ScaleLabel.ARCHITECTURE,
            permitted_escalation_targets=(
                AlgorithmName.IPA,
                AlgorithmName.CGA,
            ),
            protected=True,
            stub=True,
        ),
        AlgorithmName.NGSA: AlgorithmSpec(
            algorithm_name=AlgorithmName.NGSA,
            purpose="Sandbox novelty without granting earned status.",
            permitted_structure_types=(
                StructureType.QUESTION,
                StructureType.HYPOTHESIS,
                StructureType.NOVELTY_CANDIDATE,
                StructureType.COHERENCE_TENSION,
            ),
            permitted_decision_types=STUB_DECISION_TYPES,
            authority_level=AuthorityLevel.TEMPORARY_USE,
            maximum_target_scale=ScaleLabel.HYPOTHESIS,
            permitted_escalation_targets=(
                AlgorithmName.GEA,
                AlgorithmName.CRA,
                AlgorithmName.SRA,
                AlgorithmName.MSSA,
            ),
            protected=True,
            stub=True,
        ),
        AlgorithmName.GEA: AlgorithmSpec(
            algorithm_name=AlgorithmName.GEA,
            purpose="Evaluate grounding without creating persistence.",
            permitted_structure_types=(
                StructureType.CLAIM,
                StructureType.HYPOTHESIS,
                StructureType.EVIDENCE_ITEM,
                StructureType.MEMORY_CANDIDATE,
                StructureType.PERSISTENT_KNOWLEDGE,
            ),
            permitted_decision_types=(
                DecisionType.APPROVE,
                DecisionType.APPROVE_WITH_MONITORING,
                DecisionType.SANDBOX,
                DecisionType.REVISE,
                DecisionType.DELAY,
                DecisionType.DEMOTE,
                DecisionType.REJECT,
                DecisionType.ESCALATE,
            ),
            authority_level=AuthorityLevel.ACTIVE_REASONING,
            maximum_target_scale=ScaleLabel.MEMORY,
            permitted_escalation_targets=(
                AlgorithmName.CRA,
                AlgorithmName.PCA,
                AlgorithmName.CGA,
            ),
            protected=True,
            stub=False,
        ),
        AlgorithmName.PCA: AlgorithmSpec(
            algorithm_name=AlgorithmName.PCA,
            purpose="Govern persistence, archive, demotion, and retraction.",
            permitted_structure_types=(
                StructureType.CLAIM,
                StructureType.HYPOTHESIS,
                StructureType.MEMORY_CANDIDATE,
                StructureType.PERSISTENT_KNOWLEDGE,
                StructureType.COHERENCE_TENSION,
            ),
            permitted_decision_types=(
                DecisionType.APPROVE_WITH_MONITORING,
                DecisionType.REVISE,
                DecisionType.DELAY,
                DecisionType.DEMOTE,
                DecisionType.PERSIST,
                DecisionType.ARCHIVE,
                DecisionType.RETRACT,
                DecisionType.REJECT,
                DecisionType.ESCALATE,
            ),
            authority_level=AuthorityLevel.MEMORY_INFLUENCE,
            maximum_target_scale=ScaleLabel.MEMORY,
            permitted_escalation_targets=(
                AlgorithmName.GEA,
                AlgorithmName.CRA,
                AlgorithmName.MSSA,
                AlgorithmName.CGA,
            ),
            protected=True,
            stub=False,
        ),
        AlgorithmName.CRA: AlgorithmSpec(
            algorithm_name=AlgorithmName.CRA,
            purpose="Review contradiction and preserve or repair tension.",
            permitted_structure_types=(
                StructureType.CLAIM,
                StructureType.HYPOTHESIS,
                StructureType.COHERENCE_TENSION,
                StructureType.MEMORY_CANDIDATE,
                StructureType.PERSISTENT_KNOWLEDGE,
                StructureType.SCALE_CONFLICT,
            ),
            permitted_decision_types=(
                DecisionType.APPROVE_WITH_MONITORING,
                DecisionType.REPAIR,
                DecisionType.REVISE,
                DecisionType.DELAY,
                DecisionType.DEMOTE,
                DecisionType.REJECT,
                DecisionType.ESCALATE,
            ),
            authority_level=AuthorityLevel.ACTIVE_REASONING,
            maximum_target_scale=ScaleLabel.PRINCIPLE,
            permitted_escalation_targets=(
                AlgorithmName.GEA,
                AlgorithmName.PCA,
                AlgorithmName.MSSA,
                AlgorithmName.CGA,
            ),
            protected=True,
            stub=False,
        ),
        AlgorithmName.MSSA: AlgorithmSpec(
            algorithm_name=AlgorithmName.MSSA,
            purpose="Review scale labels and detect authority drift.",
            permitted_structure_types=(
                StructureType.CLAIM,
                StructureType.HYPOTHESIS,
                StructureType.MEMORY_CANDIDATE,
                StructureType.PERSISTENT_KNOWLEDGE,
                StructureType.SCALE_CONFLICT,
                StructureType.ARCHITECTURAL_CANDIDATE,
                StructureType.GOVERNANCE_OBJECT,
                StructureType.CONSTITUTIONAL_OBJECT,
            ),
            permitted_decision_types=(
                DecisionType.APPROVE_WITH_MONITORING,
                DecisionType.REVISE,
                DecisionType.DELAY,
                DecisionType.DEMOTE,
                DecisionType.PROMOTE_CANDIDATE,
                DecisionType.REJECT,
                DecisionType.ESCALATE,
            ),
            authority_level=AuthorityLevel.ARCHITECTURAL_INFLUENCE,
            maximum_target_scale=ScaleLabel.CONSTITUTIONAL,
            permitted_escalation_targets=(
                AlgorithmName.PCA,
                AlgorithmName.AEA,
                AlgorithmName.CGA,
            ),
            protected=True,
            stub=False,
        ),
        AlgorithmName.AEA: AlgorithmSpec(
            algorithm_name=AlgorithmName.AEA,
            purpose="Detect architectural change and route protected review.",
            permitted_structure_types=(
                StructureType.ARCHITECTURAL_CANDIDATE,
                StructureType.PERSISTENT_KNOWLEDGE,
                StructureType.SCALE_CONFLICT,
                StructureType.GOVERNANCE_OBJECT,
            ),
            permitted_decision_types=STUB_DECISION_TYPES,
            authority_level=AuthorityLevel.ARCHITECTURAL_INFLUENCE,
            maximum_target_scale=ScaleLabel.ARCHITECTURE,
            permitted_escalation_targets=(
                AlgorithmName.IPA,
                AlgorithmName.SRA,
                AlgorithmName.CGA,
            ),
            protected=True,
            stub=True,
        ),
        AlgorithmName.CGA: AlgorithmSpec(
            algorithm_name=AlgorithmName.CGA,
            purpose="Review vetoes, escalation, legitimacy, and constitutional risk.",
            permitted_structure_types=(
                StructureType.GOVERNANCE_OBJECT,
                StructureType.CONSTITUTIONAL_OBJECT,
                StructureType.ARCHITECTURAL_CANDIDATE,
                StructureType.SCALE_CONFLICT,
                StructureType.PERSISTENT_KNOWLEDGE,
                StructureType.COHERENCE_TENSION,
            ),
            permitted_decision_types=(
                DecisionType.APPROVE,
                DecisionType.APPROVE_WITH_MONITORING,
                DecisionType.SANDBOX,
                DecisionType.REVISE,
                DecisionType.DELAY,
                DecisionType.DEMOTE,
                DecisionType.PERSIST,
                DecisionType.ARCHIVE,
                DecisionType.RETRACT,
                DecisionType.REJECT,
                DecisionType.ROLLBACK,
                DecisionType.ESCALATE,
                DecisionType.AMENDMENT_REVIEW,
            ),
            authority_level=AuthorityLevel.CONSTITUTIONAL_AUTHORITY,
            maximum_target_scale=ScaleLabel.CONSTITUTIONAL,
            permitted_escalation_targets=(),
            protected=True,
            stub=False,
        ),
        AlgorithmName.ICC: AlgorithmSpec(
            algorithm_name=AlgorithmName.ICC,
            purpose="Coordinate the governed cycle without acting as a reviewer.",
            permitted_structure_types=all_structure_types,
            permitted_decision_types=(),
            authority_level=AuthorityLevel.ACTIVE_REASONING,
            maximum_target_scale=ScaleLabel.CONSTITUTIONAL,
            permitted_escalation_targets=tuple(
                algorithm_name
                for algorithm_name in AlgorithmName
                if algorithm_name is not AlgorithmName.ICC
            ),
            protected=True,
            stub=False,
            state_mutation_prohibited=True,
            coordinator=True,
        ),
    }
    return AlgorithmRegistry(algorithms=algorithms)


__all__ = [
    "AUTHORITY_RANK",
    "AlgorithmRegistry",
    "AlgorithmSpec",
    "DecisionValidationResult",
    "REGISTRY_CHANGE_KINDS",
    "RegistryChangeRequest",
    "SCALE_RANK",
    "STUB_DECISION_TYPES",
    "ValidationIssue",
    "create_default_registry",
    "validate_review_decision",
]
