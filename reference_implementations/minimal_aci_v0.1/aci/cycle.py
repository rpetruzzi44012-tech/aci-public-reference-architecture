"""Transactional orchestration for the Minimal ACI v0.1 cognitive cycle.

The cycle coordinates existing modules. It does not reproduce parsing,
review, planning, mutation, audit, or output rules owned elsewhere.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping
from copy import deepcopy
from dataclasses import dataclass, field, replace
from datetime import datetime, timezone
from uuid import uuid4

from .algorithms.cga import GovernanceReviewFixture, run_cga_where_required
from .algorithms.cra import (
    PropositionComparisonFixture,
    run_cra_where_required,
)
from .algorithms.gea import run_gea_where_required
from .algorithms.mssa import run_mssa_where_required
from .algorithms.pca import run_pca_where_required
from .algorithms.stubs import (
    StubReviewFixture,
    run_aea_stub_where_required,
    run_ipa_stub_where_required,
    run_ngsa_stub_where_required,
    run_sra_stub_where_required,
)
from .audit import (
    AbortedAuditData,
    CommittedAuditData,
    bind_audit_reference_to_state_change,
    capture_baseline_fingerprint,
    capture_baseline_reference,
    create_pending_audit,
    finalize_aborted_audit,
    finalize_committed_audit,
)
from .core import (
    AuditRecord,
    CycleResult,
    InputObject,
    JSONValue,
    StateChangePlan,
    SymbolicStructure,
)
from .enums import AlgorithmName
from .metadata import MetadataInitializationResult, assign_initial_scale_labels
from .output import (
    bind_audit_ref_to_output,
    generate_provisional_authorized_output,
)
from .parser import (
    StructuredParseFixture,
    parse_input_into_symbolic_structures,
    parse_structured_fixtures,
)
from .registry import RegistryChangeRequest
from .review_context import ReviewContext
from .state import ArchitectureState, capture_baseline, clone_state
from .state_update import (
    apply_state_change_plan,
    calculate_state_delta,
    plan_authorized_state_changes,
)

CycleIDProvider = Callable[[str], str]
CycleTimeProvider = Callable[[], str]
FaultInjector = Callable[[str], None]


class IntegratedCycleError(RuntimeError):
    """Raised when orchestration detects an invalid transaction boundary."""


@dataclass(frozen=True, slots=True)
class StructuredCycleInput:
    """Explicit parser fixtures for stable full-cycle acceptance tests."""

    input_id: str
    fixtures: tuple[StructuredParseFixture, ...]

    def __post_init__(self) -> None:
        _require_nonempty_text(self.input_id, "input_id")
        _require_tuple_members(
            self.fixtures,
            StructuredParseFixture,
            "fixtures",
        )
        if not self.fixtures:
            raise ValueError("fixtures cannot be empty")
        fixture_input_ids = [
            fixture.input_id for fixture in self.fixtures
        ]
        if len(fixture_input_ids) != len(set(fixture_input_ids)):
            raise ValueError(
                "structured cycle fixture input IDs must be unique"
            )


@dataclass(frozen=True, slots=True)
class CycleReviewConfiguration:
    """Explicit fixtures for v0.1 reviewers that require structured input."""

    ngsa_fixtures: tuple[StubReviewFixture, ...] = ()
    cra_comparisons: tuple[PropositionComparisonFixture, ...] = ()
    ipa_fixtures: tuple[StubReviewFixture, ...] = ()
    cga_fixtures: tuple[GovernanceReviewFixture, ...] = ()
    registry_change_requests: Mapping[str, RegistryChangeRequest] = field(
        default_factory=dict
    )

    def __post_init__(self) -> None:
        _require_tuple_members(
            self.ngsa_fixtures,
            StubReviewFixture,
            "ngsa_fixtures",
        )
        _require_tuple_members(
            self.cra_comparisons,
            PropositionComparisonFixture,
            "cra_comparisons",
        )
        _require_tuple_members(
            self.ipa_fixtures,
            StubReviewFixture,
            "ipa_fixtures",
        )
        _require_tuple_members(
            self.cga_fixtures,
            GovernanceReviewFixture,
            "cga_fixtures",
        )
        if not isinstance(self.registry_change_requests, Mapping):
            raise TypeError("registry_change_requests must be a mapping")
        for decision_id, request in self.registry_change_requests.items():
            _require_nonempty_text(decision_id, "registry decision ID")
            if not isinstance(request, RegistryChangeRequest):
                raise TypeError(
                    "registry_change_requests values must be "
                    "RegistryChangeRequest"
                )


# Fault points are test seams between authoritative orchestration stages.
# No fault point runs after the prepared result becomes authoritative.
CYCLE_FAULT_POINTS = (
    "audit_reserved",
    "working_state_cloned",
    "input_parsed",
    "metadata_initialized",
    "review_context_created",
    "review_ngsa",
    "review_gea",
    "review_cra",
    "review_sra",
    "review_ipa",
    "review_pca",
    "review_mssa",
    "review_aea",
    "review_cga",
    "plan_created",
    "plan_applied",
    "delta_calculated",
    "provisional_output_generated",
    "commit_candidate_finalized",
    "output_bound",
    "state_changes_bound",
    "audit_appended",
    "cycle_result_prepared",
)


def _default_id_provider(kind: str) -> str:
    _require_nonempty_text(kind, "identifier kind")
    return f"{kind}-{uuid4()}"


def _default_time_provider() -> str:
    return datetime.now(timezone.utc).isoformat()


def run_integrated_cognitive_cycle(
    architecture_state: ArchitectureState,
    input_value: InputObject | str | StructuredCycleInput,
    *,
    review_configuration: CycleReviewConfiguration | None = None,
    id_provider: CycleIDProvider = _default_id_provider,
    time_provider: CycleTimeProvider = _default_time_provider,
    fault_injector: FaultInjector | None = None,
) -> CycleResult:
    """Run one logically atomic ACI cycle against an isolated working state.

    Runtime-only v0.1 guarantees logical exception safety. It does not claim
    process-crash durability or durable transaction recovery.
    """

    if not isinstance(architecture_state, ArchitectureState):
        raise TypeError("architecture_state must be ArchitectureState")
    if not isinstance(
        input_value,
        (InputObject, str, StructuredCycleInput),
    ):
        raise TypeError(
            "input_value must be InputObject, str, or StructuredCycleInput"
        )
    if review_configuration is None:
        review_configuration = CycleReviewConfiguration()
    if not isinstance(review_configuration, CycleReviewConfiguration):
        raise TypeError(
            "review_configuration must be CycleReviewConfiguration"
        )
    if not callable(id_provider):
        raise TypeError("id_provider must be callable")
    if not callable(time_provider):
        raise TypeError("time_provider must be callable")
    if fault_injector is not None and not callable(fault_injector):
        raise TypeError("fault_injector must be callable or None")

    cycle_id = _next_id(id_provider, "cycle")
    normalized_input = _normalize_input(input_value, id_provider)
    baseline = capture_baseline(architecture_state)
    baseline_state = baseline.clone()
    pending_audit = create_pending_audit(
        cycle_id=cycle_id,
        input_ref=normalized_input.input_id,
        baseline_state_ref=capture_baseline_reference(baseline),
        baseline_fingerprint=capture_baseline_fingerprint(baseline),
        id_provider=_kind_provider(id_provider, "audit"),
        time_provider=time_provider,
    )
    if any(
        audit.audit_id == pending_audit.audit_id
        for audit in baseline_state.audit_log
    ):
        raise IntegratedCycleError(
            f"audit ID already exists: {pending_audit.audit_id}"
        )

    working_state: ArchitectureState | None = None
    initialized_structures: tuple[SymbolicStructure, ...] = ()
    metadata_result: MetadataInitializationResult | None = None
    context: ReviewContext | None = None
    plan: StateChangePlan | None = None
    invoked_algorithms = [AlgorithmName.ICC]
    failure_stage = "audit_reserved"

    try:
        _checkpoint(fault_injector, failure_stage)

        failure_stage = "working_state_cloned"
        working_state = baseline.clone()
        working_state.audit_log.append(deepcopy(pending_audit))
        _checkpoint(fault_injector, failure_stage)

        failure_stage = "input_parsed"
        parsed_structures = _parse_cycle_input(
            normalized_input,
            pending_audit.audit_id,
            id_provider,
        )
        _checkpoint(fault_injector, failure_stage)

        failure_stage = "metadata_initialized"
        metadata_result = assign_initial_scale_labels(
            parsed_structures,
            working_state,
        )
        initialized_structures = metadata_result.structures
        _register_cycle_structures(working_state, initialized_structures)
        _checkpoint(fault_injector, failure_stage)

        failure_stage = "review_context_created"
        context = ReviewContext(
            audit_id=pending_audit.audit_id,
            architecture_state=working_state,
            targets=initialized_structures,
        )
        _checkpoint(fault_injector, failure_stage)

        failure_stage = "review_ngsa"
        invoked_algorithms.append(AlgorithmName.NGSA)
        run_ngsa_stub_where_required(
            context,
            review_configuration.ngsa_fixtures,
            id_provider=_kind_provider(id_provider, "decision"),
        )
        _checkpoint(fault_injector, failure_stage)

        failure_stage = "review_gea"
        invoked_algorithms.append(AlgorithmName.GEA)
        run_gea_where_required(
            context,
            id_provider=_kind_provider(id_provider, "decision"),
        )
        _checkpoint(fault_injector, failure_stage)

        failure_stage = "review_cra"
        invoked_algorithms.append(AlgorithmName.CRA)
        run_cra_where_required(
            context,
            review_configuration.cra_comparisons,
            decision_id_provider=_kind_provider(id_provider, "decision"),
            unresolved_id_provider=_kind_provider(id_provider, "unresolved"),
        )
        _checkpoint(fault_injector, failure_stage)

        failure_stage = "review_sra"
        invoked_algorithms.append(AlgorithmName.SRA)
        run_sra_stub_where_required(
            context,
            id_provider=_kind_provider(id_provider, "decision"),
        )
        _checkpoint(fault_injector, failure_stage)

        failure_stage = "review_ipa"
        invoked_algorithms.append(AlgorithmName.IPA)
        run_ipa_stub_where_required(
            context,
            review_configuration.ipa_fixtures,
            id_provider=_kind_provider(id_provider, "decision"),
        )
        _checkpoint(fault_injector, failure_stage)

        failure_stage = "review_pca"
        invoked_algorithms.append(AlgorithmName.PCA)
        run_pca_where_required(
            context,
            id_provider=_kind_provider(id_provider, "decision"),
        )
        _checkpoint(fault_injector, failure_stage)

        failure_stage = "review_mssa"
        invoked_algorithms.append(AlgorithmName.MSSA)
        run_mssa_where_required(
            context,
            id_provider=_kind_provider(id_provider, "decision"),
        )
        _checkpoint(fault_injector, failure_stage)

        failure_stage = "review_aea"
        invoked_algorithms.append(AlgorithmName.AEA)
        run_aea_stub_where_required(
            context,
            id_provider=_kind_provider(id_provider, "decision"),
        )
        _checkpoint(fault_injector, failure_stage)

        failure_stage = "review_cga"
        invoked_algorithms.append(AlgorithmName.CGA)
        run_cga_where_required(
            context,
            review_configuration.cga_fixtures,
            id_provider=_kind_provider(id_provider, "decision"),
        )
        _checkpoint(fault_injector, failure_stage)

        failure_stage = "plan_created"
        plan = plan_authorized_state_changes(
            context,
            working_state.algorithm_registry,
            registry_change_requests=(
                review_configuration.registry_change_requests
            ),
            id_provider=_kind_provider(id_provider, "plan"),
        )
        _checkpoint(fault_injector, failure_stage)

        failure_stage = "plan_applied"
        working_state = apply_state_change_plan(
            working_state,
            plan,
            pending_audit.audit_id,
        )
        _checkpoint(fault_injector, failure_stage)

        failure_stage = "delta_calculated"
        state_delta = calculate_state_delta(
            baseline_state,
            working_state,
        )
        _checkpoint(fault_injector, failure_stage)

        failure_stage = "provisional_output_generated"
        provisional_output = generate_provisional_authorized_output(
            context,
            plan,
            id_provider=_kind_provider(id_provider, "output"),
        )
        _checkpoint(fault_injector, failure_stage)

        # Finalize a private candidate first. The authoritative PENDING audit
        # remains abortable until every post-finalization binding is proven.
        failure_stage = "commit_candidate_finalized"
        committed_audit = finalize_committed_audit(
            deepcopy(pending_audit),
            CommittedAuditData(
                target_structure_ids=[
                    structure.structure_id
                    for structure in initialized_structures
                ],
                created_structures=list(initialized_structures),
                algorithms_invoked=invoked_algorithms,
                decisions=list(context.decisions),
                accepted_plan_items=plan.changes,
                rejected_plan_items=[],
                state_change_plan=plan,
                graph_updates=plan.graph_updates,
                budget_effects=_budget_effects(plan),
                threshold_effects=[
                    check.to_dict()
                    for check in metadata_result.threshold_checks
                ],
                rollback_points_created=plan.rollback_points,
                state_delta=state_delta,
                provisional_output_ref=(
                    provisional_output.output_id
                    if provisional_output is not None
                    else None
                ),
                unresolved_tensions=_unresolved_ids(context),
                escalation_events=plan.escalation_events,
            ),
            time_provider=time_provider,
        )
        _checkpoint(fault_injector, failure_stage)

        failure_stage = "output_bound"
        committed_output = bind_audit_ref_to_output(
            provisional_output,
            committed_audit,
        )
        _checkpoint(fault_injector, failure_stage)

        failure_stage = "state_changes_bound"
        working_state.state_changes = [
            bind_audit_reference_to_state_change(change, committed_audit)
            if change.audit_ref == committed_audit.audit_id
            else change
            for change in working_state.state_changes
        ]
        _checkpoint(fault_injector, failure_stage)

        failure_stage = "audit_appended"
        _replace_pending_audit(working_state, committed_audit)
        _checkpoint(fault_injector, failure_stage)

        failure_stage = "cycle_result_prepared"
        result = CycleResult.committed(
            cycle_id=cycle_id,
            updated_state=working_state,
            audit_record=committed_audit,
            output=committed_output,
            unresolved_items=_unresolved_ids(context),
            escalation_events=plan.escalation_events,
            monitoring_triggers=_new_monitoring_triggers(
                baseline_state,
                working_state,
            ),
        )
        _checkpoint(fault_injector, failure_stage)
        return result
    except Exception as error:
        return _abort_cycle(
            cycle_id=cycle_id,
            pending_audit=pending_audit,
            baseline_state=baseline_state,
            failure_stage=failure_stage,
            error=error,
            initialized_structures=initialized_structures,
            context=context,
            plan=plan,
            invoked_algorithms=invoked_algorithms,
            time_provider=time_provider,
        )


def _abort_cycle(
    *,
    cycle_id: str,
    pending_audit: AuditRecord,
    baseline_state: ArchitectureState,
    failure_stage: str,
    error: Exception,
    initialized_structures: tuple[SymbolicStructure, ...],
    context: ReviewContext | None,
    plan: StateChangePlan | None,
    invoked_algorithms: list[AlgorithmName],
    time_provider: CycleTimeProvider,
) -> CycleResult:
    recovered_state = clone_state(baseline_state)
    decisions = list(context.decisions) if context is not None else []
    unresolved_items = (
        _unresolved_ids(context) if context is not None else []
    )
    escalation_events = (
        list(plan.escalation_events) if plan is not None else []
    )
    error_text = f"{type(error).__name__}: {error}"
    if not str(error):
        error_text = type(error).__name__
    aborted_audit = finalize_aborted_audit(
        pending_audit,
        AbortedAuditData(
            failure_stage=failure_stage,
            error=error_text,
            target_structure_ids=[
                structure.structure_id
                for structure in initialized_structures
            ],
            algorithms_invoked=invoked_algorithms,
            decisions=decisions,
            rejected_plan_items=[],
            state_change_plan=plan,
            unresolved_tensions=unresolved_items,
            escalation_events=escalation_events,
        ),
        time_provider=time_provider,
    )
    recovered_state.audit_log.append(deepcopy(aborted_audit))
    return CycleResult.aborted(
        cycle_id=cycle_id,
        audit_record=aborted_audit,
        error=error_text,
        updated_state=recovered_state,
        output=None,
        unresolved_items=unresolved_items,
        escalation_events=escalation_events,
        monitoring_triggers=[],
    )


def _normalize_input(
    input_value: InputObject | str | StructuredCycleInput,
    id_provider: CycleIDProvider,
) -> InputObject | StructuredCycleInput:
    if isinstance(input_value, StructuredCycleInput):
        return deepcopy(input_value)
    if isinstance(input_value, InputObject):
        return deepcopy(input_value)
    return InputObject(
        input_id=_next_id(id_provider, "input"),
        content=input_value,
        source="cycle-string",
    )


def _parse_cycle_input(
    input_value: InputObject | StructuredCycleInput,
    audit_id: str,
    id_provider: CycleIDProvider,
) -> list[SymbolicStructure]:
    structure_id_provider = _kind_provider(id_provider, "structure")
    if isinstance(input_value, StructuredCycleInput):
        fixtures = tuple(
            replace(
                fixture,
                audit_ref=_validated_fixture_audit_ref(
                    fixture,
                    audit_id,
                ),
            )
            for fixture in input_value.fixtures
        )
        return parse_structured_fixtures(
            fixtures,
            id_provider=structure_id_provider,
        )
    return parse_input_into_symbolic_structures(
        _bind_input_to_pending_audit(input_value, audit_id),
        id_provider=structure_id_provider,
    )


def _validated_fixture_audit_ref(
    fixture: StructuredParseFixture,
    audit_id: str,
) -> str:
    if fixture.audit_ref is not None and fixture.audit_ref != audit_id:
        raise IntegratedCycleError(
            "structured fixture audit_ref conflicts with the current "
            "PENDING audit"
        )
    return audit_id


def _bind_input_to_pending_audit(
    input_object: InputObject,
    audit_id: str,
) -> InputObject:
    if (
        input_object.audit_ref is not None
        and input_object.audit_ref != audit_id
    ):
        raise IntegratedCycleError(
            "input audit_ref conflicts with the current PENDING audit"
        )
    return replace(input_object, audit_ref=audit_id)


def _register_cycle_structures(
    state: ArchitectureState,
    structures: tuple[SymbolicStructure, ...],
) -> None:
    for structure in structures:
        if structure.structure_id in state.active_structures:
            raise IntegratedCycleError(
                f"structure ID already exists: {structure.structure_id}"
            )
        state.active_structures[structure.structure_id] = deepcopy(structure)


def _replace_pending_audit(
    state: ArchitectureState,
    committed_audit: AuditRecord,
) -> None:
    matching = [
        position
        for position, audit in enumerate(state.audit_log)
        if audit.audit_id == committed_audit.audit_id
    ]
    if len(matching) != 1:
        raise IntegratedCycleError(
            "working state must contain exactly one matching audit reservation"
        )
    state.audit_log[matching[0]] = deepcopy(committed_audit)


def _budget_effects(
    plan: StateChangePlan,
) -> list[dict[str, JSONValue]]:
    return [
        {
            "change_id": change.change_id,
            "target_id": change.target_id,
            **deepcopy(change.payload),
        }
        for change in plan.changes
        if change.change_type == "budget_effect"
    ]


def _unresolved_ids(context: ReviewContext) -> list[str]:
    return [item.item_id for item in context.unresolved_items]


def _new_monitoring_triggers(
    baseline: ArchitectureState,
    working_state: ArchitectureState,
) -> list[str]:
    baseline_triggers = set(baseline.monitoring_triggers)
    return [
        trigger
        for trigger in working_state.monitoring_triggers
        if trigger not in baseline_triggers
    ]


def _checkpoint(
    fault_injector: FaultInjector | None,
    fault_point: str,
) -> None:
    if fault_injector is not None:
        fault_injector(fault_point)


def _kind_provider(
    id_provider: CycleIDProvider,
    kind: str,
) -> Callable[[], str]:
    return lambda: _next_id(id_provider, kind)


def _next_id(id_provider: CycleIDProvider, kind: str) -> str:
    value = id_provider(kind)
    _require_nonempty_text(value, f"{kind} identifier")
    return value


def _require_tuple_members(
    values: tuple,
    model_type: type,
    field_name: str,
) -> None:
    if not isinstance(values, tuple):
        raise TypeError(f"{field_name} must be a tuple")
    for position, value in enumerate(values):
        if not isinstance(value, model_type):
            raise TypeError(
                f"{field_name}[{position}] must be {model_type.__name__}"
            )


def _require_nonempty_text(value: str, field_name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a nonempty string")


__all__ = [
    "CYCLE_FAULT_POINTS",
    "CycleIDProvider",
    "CycleReviewConfiguration",
    "FaultInjector",
    "IntegratedCycleError",
    "StructuredCycleInput",
    "run_integrated_cognitive_cycle",
]
