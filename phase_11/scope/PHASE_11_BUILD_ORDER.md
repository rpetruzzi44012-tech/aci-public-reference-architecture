# Phase 11 Full Module Integration Build Order

## Status and Reading Rule

- Status: `APPROVED_SCOPE_LOCK`
- Original Phase 10 seal baseline: `41c95e422e71530c8e003484d04a1cf332c47fa6`
- Original draft commit: `0bf21c5f50c00d63594db3ea2fe13d908693d00d`
- Verified Step 1 audit head / Step 2 amendment baseline: `dd714801cc4d5ac2eed2e1dfd411a3d2c42b07b4`
- Step 2 commit binding: `CONTAINING_COMMIT`
- Proposed stages: 12
- Type policy: `VERSIONED_PHASE11_CONTRACTS_WITH_EXPLICIT_V0_1_ADAPTERS`
- `STEP_2_AMENDMENT_COMPLETE: YES`
- `TECHNICAL_BLOCKERS: 0`
- `TURBO_FINAL_REVIEW_REQUIRED: NO`
- `PHASE_11_SCOPE_LOCK_APPROVED: YES`
- `PHASE_11_IMPLEMENTATION_AUTHORIZED: NO`
- `P11_STAGE_01_CONTRACT_DRAFTING_AUTHORIZED: YES_AFTER_VERIFIED_SEAL`
- `P11_STAGE_01_IMPLEMENTATION_AUTHORIZED: NO`
- `PHASE_12_CONTINUITY_AUTHORIZED: NO`
- `PHASE_13_FUNCTIONAL_IDENTITY_AUTHORIZED: NO`
- `PHASE_14_ARC_AUTHORIZED: NO`
- `PHASE_15_EXTERNAL_VALIDATION_AUTHORIZED: NO`

This dependency-derived sequence is not canon-section order. The twelve-stage
order is locked, but no stage is authorized for implementation. Drafting the
P11-STAGE-01 implementation contract is the next authorized operation after
the verified seal. Passing or drafting one stage never authorizes another;
any order amendment requires a separately authorized scope-lock amendment.
Accepted v0.1 remains independently executable and reproducibly archived.

## P11-STAGE-01 -- Integration Topology and Compatibility Scaffold

- **Purpose:** establish package, import, version, type-policy, adapter, and differential boundaries without runtime behavior.
- **Modules:** 8.1-8.18 as ownership declarations only.
- **Algorithms:** all nine as interface declarations only.
- **Prerequisites:** approved `P11-DEC-001`, `P11-DEC-002`, `P11-DEC-003`, and `P11-DEC-004`, plus a separately approved Stage 1 implementation contract.
- **Authorized paths:** proposed `aci_prototype/aci_phase11/`, `aci_prototype/tests_phase11/`, package metadata, and explicit compatibility adapters after separate authorization.
- **Prohibited paths:** accepted v0.1 runtime/tests, Phase 10 evidence, and Phase 12-15 delivery packages.
- **Artifacts:** import law, version identity, placement classes, closed wire mappings, and differential scaffold.
- **Focused tests:** import isolation; no v0.1 aggregate imports in Phase 11 runtime core; no reverse import; unknown enum and lossy reverse-conversion rejection.
- **Cumulative tests:** accepted v0.1 independent execution and archive verification plus the static scaffold.
- **Exit invariant:** Phase 11 imports beside v0.1 without mutation, shadowing, or authority transfer.
- **Rollback point:** remove or disable the isolated package and restore the pre-stage manifest.
- **Stop conditions:** circular import, aggregate reuse, accepted-core mutation, or ambiguous authority.
- **Authority after passage:** scaffold conformance only; no module or algorithm acceptance.

## P11-STAGE-02 -- Core Symbolic and Shared Result Contracts

- **Purpose:** establish shared enums, value contracts, SymbolicStructure, SymbolicMetadata, ReviewDecision, CycleResult and OutputObject bases, and durable-record/projection bases.
- **Modules:** 8.1, 8.2, 8.7, and base contracts for 8.17-8.18.
- **Algorithms:** none executed; all nine signatures modeled.
- **Prerequisites:** `P11-STAGE-01`.
- **Authorized paths:** Phase 11 value, structure, metadata, durable-record, projection, result, and output contracts.
- **Prohibited paths:** algorithm execution, registry activation, state application, continuity types, and model integration.
- **Artifacts:** typed bases, validation rules, reference vocabulary, and serialization boundaries.
- **Focused tests:** enum separation; metadata lifecycle; complete ReviewDecision; projection omissions/non-authority; result/output bases; conversion rejection.
- **Cumulative tests:** Stages 1-2 plus accepted v0.1 execution and archive checks.
- **Exit invariant:** later modules can name complete durable inputs and observational outputs without transaction logic.
- **Rollback point:** package-only return to Stage 1.
- **Stop conditions:** projection accepted as durable input/reference, category collapse, or output treated as truth.
- **Authority after passage:** typed-contract candidacy only.

## P11-STAGE-03 -- State Foundations and Graph Primitives

- **Purpose:** define IdentityKernel, BudgetState, ThresholdState, governance primitives, five graph-domain types, relation primitives, candidate-origin values, and ReviewRequirementSet grammar constituents.
- **Modules:** 8.4-8.6, graph primitives for 8.9, and governance/review primitives for 8.3, 8.7, and 8.10.
- **Algorithms:** signatures/read contracts only.
- **Prerequisites:** `P11-STAGE-02` and approved `P11-DEC-007`, `P11-DEC-008`, and `P11-DEC-010` policies.
- **Authorized paths:** Phase 11 identity, budget, threshold, graph, relation, candidate-origin, and review-requirement primitives.
- **Prohibited paths:** aggregate ArchitectureState, cross-run identity, persistent storage, learned thresholds, constitutional amendment, and direct mutation.
- **Artifacts:** primitive state domains, five graph containers, relation types, six candidate origins, and field grammar.
- **Focused tests:** invariants, budget/threshold bounds, graph separation, relation typing, candidate-origin non-authority, and representative/nonexhaustive review derivation.
- **Cumulative tests:** Stages 1-3 plus accepted v0.1.
- **Exit invariant:** graph primitives precede aggregate state and every primitive preserves its distinct status domain.
- **Rollback point:** restore the Stage 2 type set.
- **Stop conditions:** functional-identity claims, hidden state, status transfer, or non-isolatable primitives.
- **Authority after passage:** primitive-contract conformance only.

## P11-STAGE-04 -- Integrated ArchitectureState, GovernanceState, and Cross-Domain Relations

- **Purpose:** integrate complete ArchitectureState, GovernanceState, GraphSet, cross-domain relations, clone, baseline, fingerprint, and comparison behavior.
- **Modules:** 8.3, 8.9 integration, and 8.10.
- **Algorithms:** read contracts only.
- **Prerequisites:** `P11-STAGE-03`.
- **Authorized paths:** Phase 11 aggregate state, governance state, graph integration, and comparison code.
- **Prohibited paths:** AuthorityGraph/GovernanceState collapse, direct application, persistence database, or implicit cross-domain transfer.
- **Artifacts:** full integrated state with isolated working copy and baseline equivalence.
- **Focused tests:** visible-domain completeness, clone isolation, fingerprint equivalence, cross-domain rejection, and governance/authority separation.
- **Cumulative tests:** Stages 1-4 plus accepted category-collapse tests.
- **Exit invariant:** authoritative and tentative working state are distinguishable and terminalization failure cannot alter authoritative state.
- **Rollback point:** restore Stage 3 primitives without aggregate integration.
- **Stop conditions:** leaked mutation, missing domain, or implicit status transfer.
- **Authority after passage:** aggregate-state conformance only.

## P11-STAGE-05 -- Algorithm Interface and Registry Authority

- **Purpose:** establish algorithm interface, immutable registry, proposal and decision validation, decision-set closure, planning contract, rollback reservation obligation, and composition admissibility without application.
- **Modules:** 8.7, 8.11, 8.12, and Stage 5 planning responsibilities of 8.14.
- **Algorithms:** all nine as registered contracts.
- **Prerequisites:** `P11-STAGE-04` and approved algorithm completion depth.
- **Authorized paths:** ReviewContext, AlgorithmSpec, registry, proposal validation, per-decision/AEA/CGA validation, closure, planner, reservation obligation, and CompositionAdmissibilityRecord.
- **Prohibited paths:** mutable registry, raw proposal/decision planning input, working-state application, self-validation, and shared executable validation barrier.
- **Artifacts:** relationship-class DAG, one validation instance per decision, closed decision set, plan contract, and admissibility statuses.
- **Focused tests:** registration attacks; DAG acyclicity; raw-input rejection; AEA/CGA dependency validation; closure; planner non-broadening; positive and negative admissibility.
- **Cumulative tests:** Stages 1-5 plus accepted registry behavior.
- **Exit invariant:** only one closed validated decision set may reach planning, and admissibility grants route eligibility only.
- **Rollback point:** deactivate the Phase 11 registry and planning contracts.
- **Stop conditions:** authority cycle, mutable registry, unregistered review, raw input leakage, or planner authority expansion.
- **Authority after passage:** registry and planning eligibility only; no application authority.

## P11-STAGE-06 -- Audit, Escalation, State Update, and Rollback Infrastructure

- **Purpose:** implement audit, escalation, tentative application, recovery, private terminal construction, terminal validation, and authoritative commit infrastructure.
- **Modules:** 8.8, 8.13, Stage 6 application responsibilities of 8.14, and 8.15.
- **Algorithms:** deterministic validated-decision fixtures only.
- **Prerequisites:** `P11-STAGE-05` and the approved `P11-DEC-007` and `P11-DEC-008` policies.
- **Authorized paths:** audit state machine; eleven internal and ten manual routes; bounded second pass; reservation/readiness; tentative application; delta; provisional output/audit/CycleResult; discard/restoration; pre-application abort; terminal binding; commit/failure records.
- **Prohibited paths:** reviewer mutation, application before admissibility/readiness, durable/crash-safe claims, partial publication, and unbounded recursion.
- **Artifacts:** RollbackReadinessReservation/Record, PreApplicationAbortRecord, PrivateStateDeltaRecord, AuthoritativeCommitRecord, CycleTerminalizationFailure, and exactly-once completed-cycle audit logic.
- **Focused tests:** route map; backward refs; reservation lifecycle; all pre-application and private-pipeline failures; discard/restoration; zero-effect delta; baseline equivalence; commit atomicity; terminal failure sink.
- **Cumulative tests:** Stages 1-6 plus accepted transaction/audit suites.
- **Exit invariant:** effects remain private until one authoritative commit; every completed cycle has one terminal audit; terminalization failure publishes nothing.
- **Rollback point:** restore Stage 5 with no Phase 11 application engine.
- **Stop conditions:** partial publication, double finalization, leaked mutation, wrong recovery mechanism, forward reference, or escalation treated as approval.
- **Authority after passage:** central engine can apply tentatively; final authority exists only at AuthoritativeTransactionCommit.

## P11-STAGE-07 -- Domain Reviewer Expansion

- **Purpose:** expand GEA, PCA, CRA, and MSSA to complete Phase 11 review contracts.
- **Modules:** 8.2, 8.5-8.7, 8.9-8.13.
- **Algorithms:** GEA, PCA, CRA, MSSA.
- **Prerequisites:** `P11-STAGE-06`.
- **Authorized paths:** Phase 11 domain-reviewer implementations, deterministic fixtures, and focused tests.
- **Prohibited paths:** CGA completion, unrestricted retrieval, continuity, scale-based authority, direct mutation, or commit ownership.
- **Artifacts:** four full domain reviewers with typed escalation and validation.
- **Focused tests:** evidence links; lineage/reconstruction; coherence/tension; scale conflict; budget/threshold boundaries; unchanged inputs; no mutation.
- **Cumulative tests:** Stages 1-7 plus accepted v0.1 differential overlap.
- **Exit invariant:** four reviewers return complete registry-valid observational decisions and preserve all category boundaries.
- **Rollback point:** deactivate expanded reviewers and retain Stage 6 fixtures.
- **Stop conditions:** hidden evidence, status transfer, reviewer application, or unclassified behavioral divergence.
- **Authority after passage:** four bounded reviewer contracts within the draft package only.

## P11-STAGE-08 -- Identity, Stability, Novelty, and Architectural Reviewers

- **Purpose:** implement IPA, SRA, NGSA, NoveltyCandidateProposal, candidate routing, and AEA after validated prerequisites.
- **Modules:** 8.4-8.7, 8.10-8.13, and 8.15.
- **Algorithms:** IPA, SRA, NGSA, AEA.
- **Prerequisites:** `P11-STAGE-07`, active IdentityKernel, and approved `P11-DEC-009` algorithm completion depth.
- **Authorized paths:** Phase 11 IPA/SRA/NGSA/AEA, proposal type, deterministic sandbox/candidate fixtures, and tests.
- **Prohibited paths:** prior-CGA dependency for AEA, autonomous generation, model requirement, novelty promotion, cross-run identity, planning, application, or mutation.
- **Artifacts:** seventeen-field proposal with four fixed invariants and four observational reviewers.
- **Focused tests:** identity impact; stability/recovery; proposal validation; no novelty authority; AEA after validated IPA/SRA/domain/candidate identity; escalation map.
- **Cumulative tests:** Stages 1-8 and all eight non-CGA reviewer suites.
- **Exit invariant:** AEA consumes every applicable validated prerequisite and no protected reviewer remains a routing-only stub.
- **Rollback point:** deactivate the four reviewers without claiming completion.
- **Stop conditions:** functional-identity claim, model dependency, novelty authority, prior CGA requirement, or reviewer-owned plan/application.
- **Authority after passage:** eight bounded reviewers; no terminal constitutional closure.

## P11-STAGE-09 -- Terminal CGA and Reviewer-DAG Closure

- **Purpose:** implement terminal CGA, CGA validation, complete escalation map, all-reviewer decision-set closure, and DAG conformance.
- **Modules:** 8.7, 8.10-8.13, and review-facing 8.16 contracts.
- **Algorithms:** CGA plus all applicable validated upstream decisions.
- **Prerequisites:** `P11-STAGE-08`.
- **Authorized paths:** Phase 11 CGA, terminal constitutional routing, decision validation/closure, escalation configuration, and conformance tests.
- **Prohibited paths:** constitutional amendment machinery, CGA as upstream dependency of IPA/SRA/NGSA/AEA, application, or authority creation.
- **Artifacts:** terminal constitutional reviewer, validated CGA record, complete reviewer DAG, and closed applicable decision set.
- **Focused tests:** terminal ordering; veto/protected effects; no amendment; all relationship classes; bounded second pass; missing or raw dependency rejection.
- **Cumulative tests:** Stages 1-9 and all nine reviewer suites.
- **Exit invariant:** every applicable decision is individually validated, CGA follows AEA when required, and closure is planning eligibility only.
- **Rollback point:** deactivate CGA and withhold reviewer-DAG closure.
- **Stop conditions:** authority cycle, prior-CGA dependency, amendment application, missing reviewer, or closure treated as approval.
- **Authority after passage:** closed review candidate only; no state-application authority.

## P11-STAGE-10 -- Full Integrated Cognitive Cycle

- **Purpose:** orchestrate requirement derivation, candidate/proposal routing, review validation, planning, admissibility, outcome-neutral routing, tentative application, recovery, terminalization, and authoritative commit.
- **Modules:** 8.1-8.18.
- **Algorithms:** all nine.
- **Prerequisites:** `P11-STAGE-09` and approved `P11-DEC-007` bounded recursion policy.
- **Authorized paths:** Phase 11 ICC, route configuration, transaction engine integration, result/output binding, and deterministic scenarios.
- **Prohibited paths:** adapter bridge, live model dependency, concurrency, unbounded recursion, continuity state, or partial publication.
- **Artifacts:** full ordered ICC, route trace, committed/aborted candidates, and terminal failure path.
- **Focused tests:** six candidate origins; eight representative review classes; no/additional/application routes; low/high recovery; all failure stages; exact audit/output/result binding.
- **Cumulative tests:** Stages 1-10, all algorithms, and accepted v0.1 differential suite.
- **Exit invariant:** one deterministic ICC may exercise every applicable component and either publish one coherent terminal set or nothing.
- **Rollback point:** disable Phase 11 ICC while retaining independently tested modules/reviewers.
- **Stop conditions:** missing route, loop, output/audit mismatch, direct mutation, fabricated reference, partial publication, or later-phase dependency.
- **Authority after passage:** integrated-cycle candidate only.

## P11-STAGE-11 -- Full-Module Conformance and Fault-Injection Acceptance

- **Purpose:** attempt to falsify full integration across contracts, transactions, categories, compatibility, and finite failure boundaries.
- **Modules:** 8.1-8.18.
- **Algorithms:** all nine.
- **Prerequisites:** `P11-STAGE-10` and the approved `P11-DEC-005` evidence-profile policy with its concrete schema frozen before this stage.
- **Authorized paths:** Phase 11 oracle package, deterministic fixtures, fault harness, differential report, and candidate witnesses.
- **Prohibited paths:** adapter promotion, mandatory live model campaign, release promotion, or Phase 12-15 claims.
- **Artifacts:** conformance matrix, seventeen-stage fault results, category-collapse and differential reports, and candidate acceptance ledger.
- **Focused tests:** ten-layer plan including reference temporality, registry attacks, admissibility, transaction axes, restoration equivalence, exact terminal binding, and witness integrity.
- **Cumulative tests:** the complete Phase 11 suite and independently executable accepted v0.1 suite.
- **Exit invariant:** 18 modules, 9 algorithms, 12 capabilities, and all exit requirements pass with zero technical blocker and no accepted-core regression.
- **Rollback point:** reject candidate acceptance and return to Stage 10 for bounded repair.
- **Stop conditions:** flaky/self-confirming oracle, accepted-core regression, evidence ambiguity, scope drift, or unresolved technical defect.
- **Authority after passage:** evidence package ready for independent Turbo review only.

## P11-STAGE-12 -- Final Phase 11 Acceptance, Archive, and Release Boundary

- **Purpose:** freeze candidate evidence, prove reproducibility, preserve provenance, and obtain independent Turbo acceptance without silent canonical promotion.
- **Modules:** 8.1-8.18.
- **Algorithms:** all nine.
- **Prerequisites:** `P11-STAGE-11`, zero technical blockers, and all frozen scope-lock policies satisfied by evidence.
- **Authorized paths:** Phase 11 status/acceptance documents, versioned archive, manifests/checksums, and release metadata after separate authorization.
- **Prohibited paths:** v0.1 mutation, silent canonical promotion, Phase 12 work, public/reference claims, or production deployment.
- **Artifacts:** final traceability, acceptance record, reproducible release archive, rollback instructions, and independent Turbo decision.
- **Focused tests:** release-content/hash verification, clean-checkout reproduction, independent Phase 11 import, and accepted v0.1 execution plus archive verification.
- **Cumulative tests:** frozen-byte Phase 11 suite and accepted v0.1 suite.
- **Exit invariant:** all exit criteria are evidenced and Turbo separately accepts or rejects the candidate.
- **Rollback point:** archive a rejected/superseded candidate and keep v0.1 canonical.
- **Stop conditions:** checksum, reproduction, evidence, scope, or authority-marker failure.
- **Authority after passage:** only authority explicitly granted by a later Turbo acceptance; this candidate grants none.

## Global Ordering Constraints

- Graph primitives precede integrated aggregate state.
- Types precede algorithms; validation and closure precede planning.
- Composition admissibility precedes route selection and tentative application.
- AEA follows validated IPA/SRA and applicable domain review; CGA follows AEA when applicable.
- Full ICC follows complete reviewer-DAG closure.
- No adapter bridge precedes deterministic Stage 11 conformance.
- `P11-DEC-011` is an enforced exclusion, never an approval prerequisite.
- No Phase 12 continuity object appears in this sequence.
- Every stage requires separate authorization and focused plus cumulative passage.
- Accepted v0.1 remains independently executable and reproducibly archived throughout.
