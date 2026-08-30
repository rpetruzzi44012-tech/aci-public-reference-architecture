# Phase 11 Full Module Integration Test and Acceptance Plan

## Status

- Status: `APPROVED_SCOPE_LOCK`
- Original Phase 10 seal baseline: `41c95e422e71530c8e003484d04a1cf332c47fa6`
- Original draft commit: `0bf21c5f50c00d63594db3ea2fe13d908693d00d`
- Verified Step 1 audit head / Step 2 amendment baseline: `dd714801cc4d5ac2eed2e1dfd411a3d2c42b07b4`
- Step 2 commit binding: `CONTAINING_COMMIT`
- Type policy: `VERSIONED_PHASE11_CONTRACTS_WITH_EXPLICIT_V0_1_ADAPTERS`
- `STEP_2_AMENDMENT_COMPLETE: YES`
- `STEP_2A_RECONCILIATION_COMPLETE: YES`
- `TECHNICAL_BLOCKERS: 0`
- `TURBO_FINAL_REVIEW_REQUIRED: NO`
- `PHASE_11_SCOPE_LOCK_APPROVED: YES`
- `TEST_EXECUTION_AUTHORIZED: NO`
- `PHASE_11_IMPLEMENTATION_AUTHORIZED: NO`
- Live model campaign required: `NO`

The ten layers below are locked candidate implementation oracles. They can establish deterministic
conformance and expose architectural defects; they cannot prove external
adequacy, production fitness, consciousness, or later-phase capability.
Step 3 authorizes neither their execution nor runtime implementation.

## Oracle Principles

1. Every fixture names the module, algorithm, authority, state, graph, budget,
   threshold, audit, and expected category boundaries it exercises.
2. Deterministic identifier and clock providers are required.
3. Valid and invalid paths are equally first-class.
4. Algorithms are observed before application and must not mutate state.
5. Registry validation, planning, application, rollback, audit, and output are
   separately inspectable.
6. Failures preserve baseline-equivalent domain state and a truthful terminal
   audit.
7. v0.1 and Phase 11 are run separately; overlap differences require explicit
   authorization.
8. A model or adapter may be tested later only through a separate amendment.

## Layer 1 -- Static Contract Validation

Required checks:

- enum families remain separate, including candidate status, scale, authority,
  epistemic status, audit status, and governance mode;
- dataclass/schema construction rejects empty IDs, malformed references,
  invalid ranges, and incomplete typed results;
- imports preserve the accepted-core/Phase-11 package boundary;
- all eighteen module contracts and all nine registry entries exist;
- registry dependencies are acyclic and an algorithm cannot authorize itself;
- no Phase 11 runtime imports a Phase 12-15 delivery package;
- compatibility adapters reject lossy authority/evidence/audit conversions.
- Phase 11 runtime core imports no accepted v0.1 aggregate and v0.1 imports no
  Phase 11 package;
- stable values use closed enum mappings, unknown values fail closed, and
  forward conversion maps every field;
- compatibility-only, fixture-only, and serialization-evidence-only placement
  boundaries are enforced independently of semantic compatibility;
- complete durable records reject representative projections as runtime input
  or `_ref` targets, and every projection names exact omissions.
- `NoveltyCandidateProposal` fields equal the governing Step 1 field set
  exactly; missing or extra fields and `source_decision_ref` are rejected;
- every proposal has a non-null `audit_ref` to a pending audit that predates
  proposal construction;
- proposal-to-own-decision references and proposal/decision cycles are
  rejected, and projections cannot satisfy proposal references.

Pass oracle: static inspection and import tests report complete contracts, no
authority cycle, and no ambiguous `aci` package resolution.

## Layer 2 -- Focused Module Tests

One focused suite is required for every module:

| Module | Minimum oracle |
|---|---|
| 8.1 SymbolicStructure | typed state, relations, lineage refs, and review eligibility validate |
| 8.2 SymbolicMetadata | lifecycle transitions preserve status, risk, lineage, revision, and audit separation |
| 8.3 ArchitectureState | every domain is visible, clone-isolated, and baseline-comparable |
| 8.4 IdentityKernel | invariant impact and non-compensable failure are typed without functional-identity claims |
| 8.5 BudgetState | bounded visible budgets affect routing and authorized costs |
| 8.6 ThresholdState | named directional checks affect review but grant no status |
| 8.7 ReviewDecision | complete observational result, provenance, rationale, escalation, and no mutation |
| 8.8 AuditRecord | completed cycle has one terminal audit; audit candidate stays private; terminalization failure publishes none |
| 8.9 Graph Structures | five domains stay separate; cross-domain transfer is explicit |
| 8.10 GovernanceState | mode, veto, protected change, authority, and escalation remain distinct |
| 8.11 Algorithm Interface | isolated context, declared reads, complete result, no application |
| 8.12 AlgorithmRegistry | proposal, per-decision, AEA, CGA, and decision-set closure validate without a shared barrier |
| 8.13 Escalation Pathways | eleven internal, ten external/manual, and one bounded second-pass route remain finite and non-approving |
| 8.14 State Update Rules | closed decisions reach planning; admissibility precedes outcome-neutral routing and tentative application |
| 8.15 Rollback Points | reservation/readiness separate; low risk discards; high risk restores from the same-attempt record |
| 8.16 Integrated Cognitive Cycle | requirement derivation, six origins, review DAG, recovery, terminalization, and commit are ordered |
| 8.17 CycleResult | transaction axes remain separate; pre-application abort binds exact abort and zero-effect delta |
| 8.18 OutputObject | provisional output stays private; exact binding and explicit NO_OUTPUT prevent partial publication |

Pass oracle: every locked target has valid, invalid, boundary, and
serialization tests, and no Phase 11-owned module is represented only by a
routing stub.

## Layer 3 -- Algorithm Contract Tests

For each of IPA, SRA, NGSA, GEA, PCA, CRA, MSSA, AEA, and CGA require:

- valid and invalid typed inputs;
- only registered state, graph, budget, and threshold reads;
- required dependency decisions and deterministic ordering;
- below/at/above threshold behavior;
- permitted escalation and rejected escalation;
- zero direct state mutation;
- complete, registry-valid `ReviewDecision`;
- unchanged input fingerprints;
- explicit later-phase refusal.
- complete durable inputs only, backward-valid ordinary references, and no
  projection input;
- a newly discovered material review requirement opens a new bounded event
  rather than mutating the current requirement set.

Algorithm-specific oracles:

- IPA detects identity impact and non-compensable invariant failure without
  claiming cross-run identity;
- SRA selects bounded stabilization/recovery from visible state;
- NGSA emits exactly `proposal_id`, `source_input_refs`,
  `source_structure_refs`, `proposed_structure`, `provenance_refs`,
  `candidate_status`, `sandbox_scope`, `budget_observations`,
  `threshold_observations`, `containment_constraints`,
  `permitted_review_routes`, `prohibited_uses`, `no_new_authority`,
  `no_grounding_grant`, `no_persistence`, `not_active_state`, and `audit_ref`;
  rejects `source_decision_ref`; resolves `audit_ref` backward to the pending
  audit; constructs the proposal before its `ReviewDecision`; requires
  `ReviewDecision.proposal_refs` to reference the existing proposal; prohibits
  a proposal back-reference to its own decision; fixes the four final
  invariants true; requires no model; performs no direct mutation; and grants
  no novelty authority;
- GEA changes grounding only through valid EvidenceLink;
- PCA evaluates lineage/dependency/reconstruction without continuity;
- CRA preserves unresolved tension and grounding precedence;
- MSSA synchronizes scale without authority promotion;
- AEA consumes validated IPA, SRA, applicable domain decisions, and candidate
  identity without requiring prior CGA;
- CGA consumes validated upstream decisions, follows AEA when applicable, and
  enforces veto/protected-change/authority boundaries without amendment.

## Layer 4 -- Cross-Module Integration

Required seams:

- SymbolicStructure <-> SymbolicMetadata <-> ArchitectureState;
- metadata <-> evidence <-> five graph domains;
- AlgorithmRegistry <-> ReviewDecision <-> StateChangePlan;
- EscalationEvent <-> GovernanceState <-> registry scope;
- RollbackPoint <-> state update <-> StateDelta;
- AuditRecord <-> CycleResult <-> OutputObject;
- IdentityKernel <-> IPA <-> AEA <-> CGA.
- ReviewRequirementSet <-> per-decision validation <-> AEA/CGA validation <->
  decision-set closure <-> planner;
- StateChangePlan <-> CompositionAdmissibilityRecord <-> transaction route <->
  tentative application <-> terminal binding <-> authoritative commit.
- pending AuditRecord <-> NoveltyCandidateProposal <-> NGSA ReviewDecision <->
  proposal validation <-> per-decision validation. The proposal references the
  pending audit, the decision references the proposal, no proposal/decision
  cycle exists, and the terminal audit later binds both without rewriting the
  original lineage.

Pass oracle: each seam transfers only typed authorized information, preserves
reference integrity, and cannot manufacture evidence, persistence, scale,
authority, legitimacy, approval, or mutation.

## Layer 5 -- Transaction and Fault Injection

Inject transaction-boundary failures at exactly these owned stages:

1. central planning;
2. readiness-reservation creation;
3. composition-admissibility infrastructure;
4. readiness completion;
5. working-state application;
6. state-delta calculation;
7. provisional output construction;
8. audit candidate finalization;
9. output binding;
10. state-change/audit binding;
11. CycleResult candidate preparation;
12. terminal-binding validation;
13. working-copy discard;
14. rollback restoration;
15. aborted-result preparation;
16. aborted-result validation;
17. authoritative commit attempt.

Attack cases include registry identity/scope/scale/self-change attacks,
IdentityKernel non-compensable failures, constitutional veto, conflicting
plans, reference loss, double finalization, and post-plan failure.

Pass oracle: no unauthorized mutation leaks; high-risk application never
precedes same-attempt completed readiness; low-risk failure uses discard;
pre-application failure binds a complete zero-effect delta without fabricating
an application attempt; every completed cycle has exactly one terminal audit;
commit failure publishes no state, audit, output, CycleResult, or commit record.

Reference-temporality oracles require backward ordinary references, existing
typed reservation-only future completion, reservation consumption or
cancellation, declared lifecycle-only nulls, and rejection of fabricated
completed records.

## Layer 6 -- Category-Collapse Regression

The accepted v0.1 suite remains independently runnable. Phase 11 adds explicit
regressions that refuse:

- speculation -> knowledge;
- coherence -> evidence;
- evidence -> persistence;
- memory -> invariant;
- scale -> authority;
- authority -> legitimacy;
- usefulness -> constitutional approval;
- candidacy -> achieved status;
- review -> mutation;
- escalation -> approval;
- output -> truth;
- rollback -> approval;
- audit reservation -> audit completion;
- provenance -> typed evidence;
- IdentityKernel record -> functional identity.

Pass oracle: every protected distinction has a positive separation test and an
adversarial collapse test.

## Layer 7 -- Differential Compatibility

Run matching deterministic fixtures against accepted v0.1 and the Phase 11
package where contracts overlap:

- parsing and metadata initialization;
- GEA, PCA, CRA, MSSA, and CGA decisions;
- registry validation;
- planning/application;
- audit/output binding;
- committed and aborted integrated cycles.

Classify differences as `UNCHANGED`, `AUTHORIZED_EXTENSION`,
`INTENTIONAL_REJECTION`, or `REGRESSION`. Any unclassified difference blocks
passage. Phase 11-only fields must not retrofit or mutate v0.1.

## Layer 8 -- Full ICC Acceptance

At least twelve deterministic scenarios are required:

1. ordinary governed cycle;
2. evidence-driven grounding cycle;
3. coherence-tension cycle;
4. sandboxed novelty cycle;
5. persistence-review cycle;
6. scale-conflict cycle;
7. identity-risk cycle;
8. architectural-candidate cycle;
9. constitutional-governance cycle;
10. recursive-escalation cycle;
11. rollback cycle;
12. fault-aborted cycle.

Every scenario must bind target structures, module route, nine-algorithm
applicability, state reads, decisions, registry results, plan, rollback,
effects, delta, audit, output, unresolved items, and escalation. A module may
be legitimately non-applicable only when that decision is typed and witnessed;
silent omission fails.

Review applicability is field-derived. Tests cover IdentityKernel, budget/
threshold/recovery, evidence, persistence, coherence, scale, architecture, and
protected/governance dimensions as representative and nonexhaustive classes;
direct and NGSA origins; independent architectural/protected dimensions; and
new-event routing when a material requirement appears after closure.

Composition-admissibility tests cover positive reviewer/domain/risk coverage,
missing IPA/SRA/AEA/CGA, missing GEA/PCA/CRA/MSSA, unreviewed affected domains,
risk/route mismatch, missing rollback obligations, raw input leakage, planner
authority expansion, additional-review, and rejected-no-application results.
Transaction-axis tests keep selected route, selection status, application
disposition, transaction status, recovery mechanism, and derived terminal
outcome independent across successful/aborted no-application, low-risk, and
high-risk cases.

The sandboxed-novelty scenario proves that the pending audit exists before the
proposal, the proposal field set is exact, `proposal.audit_ref` is
backward-valid, the NGSA decision references the proposal, no proposal-to-own-
decision back-reference exists, and downstream reviewers consume only the
validated proposal and validated decision records.

Pass oracle: the scenario set collectively exercises all eighteen modules,
nine algorithms, twelve SM-11 capabilities, committed and aborted paths, and
all protected category boundaries.

## Layer 9 -- Evidence and Witness Integrity

The approved evidence-envelope policy permits candidate conformance,
fault-injection, witness, manifest, and acceptance records to bind
deterministic module/test results and carry either:

1. existing v1 witness material;
2. optional `normalized_graph_v2` negotiated per writer/reader.

The concrete Phase 11 envelope schema must be frozen before P11-STAGE-11.
This policy requires no live model campaign and does not silently make v2 the
default.

Requirements regardless of profile:

- source, execution, review, and returned-content identities are explicit;
- manifest/checksum validation is deterministic;
- no provenance field is treated as typed evidence;
- no optional v2 field becomes mandatory for v1 readers;
- failure artifacts are truthful and do not masquerade as completed results;
- no live model call is needed for deterministic acceptance.

Stage 10 may execute deterministic internal ICC tests over typed results.
Stage 11 cannot begin until the concrete envelope schema is frozen. Profile
selection grants no model-call, implementation, acceptance, or content
authority; v1 remains supported, and optional v2 remains explicitly negotiated
rather than silently becoming the default.

Pass oracle: every acceptance artifact resolves to exact source/test/release
bytes and remains semantically non-authorizing.

### Adapter Bridge Oracle

- no Phase 10 adapter import or bridge is eligible before successful
  deterministic P11-STAGE-11 conformance;
- any post-Stage-11 bridge is optional, requires separate authorization, and
  is no earlier than P11-STAGE-12 or a post-Phase-11 operation;
- Phase 11 acceptance remains possible without a bridge;
- a bridge cannot alter deterministic Stage 1-11 evidence or promote Phase 10
  experimental authority;
- removing a later bridge cannot change accepted v0.1 or the deterministic
  Phase 11 package.

## Layer 10 -- Final Acceptance

Final acceptance requires:

- every module meets its approved target disposition;
- no Phase 11-owned stub remains;
- all nine algorithms meet their locked targets;
- all twelve SM-11 capabilities pass their oracles;
- all twenty scope-lock exit criteria are evidenced;
- all Phase 11 suites and the independent accepted v0.1 suite pass;
- no blocking decision remains;
- no Phase 12-15 outcome is claimed;
- documentation, traceability, rollback instructions, and versioned release
  package are complete;
- clean-checkout reproducibility succeeds;
- Turbo performs an independent final acceptance review.
- accepted v0.1 is independently executable and reproducibly archived.

Passage is a bounded Phase 11 integration result. It does not promote the
experimental adapter, establish external validity, or authorize Phase 12.

## Step 1 Closure Oracle Index

The ten layers collectively require these exact closure oracles:

- lossy reverse-conversion rejection;
- projection non-referenceability;
- one base-validation instance per decision;
- field-derived reviewer applicability;
- no model requirement for NGSA;
- selected route independent of transaction result;
- `CycleTerminalizationFailure` is a finite nonrecursive sink with zero
  partial publication.

## Test Ownership by Proposed Stage

| Stage | New primary layers | Cumulative requirement |
|---|---|---|
| P11-STAGE-01 | Layer 1 import/topology | accepted v0.1 runnable |
| P11-STAGE-02 | Layers 1-2 shared contracts | Stages 1-2 + v0.1 |
| P11-STAGE-03 | Layers 1-2 state foundations/graph primitives | Stages 1-3 + v0.1 |
| P11-STAGE-04 | Layers 2, 4 aggregate state/relations | Stages 1-4 + collapse controls |
| P11-STAGE-05 | Layers 1, 3-4 registry/closure/admissibility | Stages 1-5 + registry attacks |
| P11-STAGE-06 | Layers 2, 4-5 transaction infrastructure | Stages 1-6 + audit/recovery/terminalization |
| P11-STAGE-07 | Layers 3, 7 domain reviewers | Stages 1-7 + differential |
| P11-STAGE-08 | Layer 3 identity/stability/novelty/architecture | eight non-CGA reviewer suites |
| P11-STAGE-09 | Layers 3-4 terminal CGA/DAG closure | all nine reviewer suites |
| P11-STAGE-10 | Layers 4-5, 8 full ICC | all modules/algorithms |
| P11-STAGE-11 | Layers 5-9 conformance/fault injection | full Phase 11 + v0.1 |
| P11-STAGE-12 | Layer 10 acceptance/archive | frozen-byte reproducibility |

## Stop Conditions

Stop and route for review if an oracle:

- relies on model prose when a deterministic typed fixture can test the claim;
- approves the same implementation choice it was written to justify without a
  counterexample;
- requires accepted-core mutation;
- cannot distinguish interface, semantic, authority, or infrastructure
  failure;
- treats audit, provenance, coherence, or authority as truth;
- introduces a Phase 12-15 requirement;
- weakens a registry, rollback, audit, evidence, or category boundary.

- `STEP_2_AMENDMENT_COMPLETE: YES`
- `STEP_2A_RECONCILIATION_COMPLETE: YES`
- `TECHNICAL_BLOCKERS: 0`
- `TURBO_FINAL_REVIEW_REQUIRED: NO`
- `PHASE_11_SCOPE_LOCK_APPROVED: YES`
- `TEST_EXECUTION_AUTHORIZED: NO`
- `PHASE_11_IMPLEMENTATION_AUTHORIZED: NO`
- `P11_STAGE_01_IMPLEMENTATION_AUTHORIZED: NO`
- `PHASE_12_CONTINUITY_AUTHORIZED: NO`
- `PHASE_13_FUNCTIONAL_IDENTITY_AUTHORIZED: NO`
- `PHASE_14_ARC_AUTHORIZED: NO`
- `PHASE_15_EXTERNAL_VALIDATION_AUTHORIZED: NO`
