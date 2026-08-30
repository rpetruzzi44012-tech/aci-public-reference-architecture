# Minimal ACI Prototype v0.1 - Scope Lock

## Document Status

- ACI phase: Phase 9
- Build stage: 0
- Prototype: Minimal ACI Prototype v0.1
- Status: Locked for implementation
- Date: 2026-06-21
- Governing canon: Phase 8 Full Pseudocode Module Canon
- Canon SHA-256: `b4349325600d282ed1b2b78bc148a6e4ca1a410e27f7f8fba938b1d3eacb5f47`
- Canonical name: Architectures of Coherent Intelligence (ACI)

## Purpose

Minimal ACI Prototype v0.1 is the smallest executable harness capable of testing whether ACI can preserve category distinctions across parsing, metadata, review, authority validation, planned mutation, audit, rollback, and output.

Its first duty is not autonomous intelligence. Its first duty is to prevent category collapse.

## Locked Technical Choices

- Python 3.11 or newer
- Modular repository
- Standard-library dataclasses and enums
- pytest for testing
- Runtime-only state
- Structured `OutputObject`
- Deterministic identifier providers in tests
- Typed graph containers backed by plain dictionaries and lists
- No production dependency without an approved decision-ledger entry
- pytest is the only pre-authorized development dependency

## Repository Boundary

The prototype lives in `aci_prototype/`.

```text
aci_prototype/
  README.md
  pyproject.toml
  aci/
    __init__.py
    enums.py
    core.py
    evidence.py
    graphs.py
    state.py
    registry.py
    parser.py
    metadata.py
    review_context.py
    audit.py
    state_update.py
    output.py
    cycle.py
    algorithms/
      __init__.py
      gea.py
      cra.py
      pca.py
      mssa.py
      cga.py
      stubs.py
  tests/
    test_enums_and_models.py
    test_evidence_boundary.py
    test_graph_separation.py
    test_state_isolation.py
    test_parser_boundary.py
    test_registry_authority.py
    test_review_dependencies.py
    test_category_collapse.py
    test_cycle_transaction.py
    test_output.py
  examples/
    run_minimal_cycle.py
  docs/
    SCOPE_LOCK.md
    CANON_MANIFEST.md
    BUILD_STAGE_MAP.md
    TREATMENT_MATRIX.md
    DECISION_LEDGER.md
    STAGE_STATUS.md
  canon/
    README.md
```

Stage 0 creates documentation and project metadata only. Runtime Python files begin in Build Stage 1.

## v0.1 Implements

- Typed symbolic structures and conservative metadata
- Typed evidence objects and evidence links
- Five distinct minimal graph domains
- Visible architecture state
- Minimal governance, budget, and threshold state
- Review decisions with status, named scores, rationale, and escalation
- Enforced algorithm registry
- Shared review context
- Simplified GEA, CRA, PCA, MSSA, and CGA
- Typed escalation events, graph updates, and rollback points
- State-change planning separated from application
- Copy-on-write logical transactions
- Pending, committed, and aborted audit lifecycle
- Structured cycle result and epistemically constrained output
- Category-collapse, authority, dependency, and transaction tests

## v0.1 Simplifies

- Graphs use typed containers backed by dictionaries and lists
- Metadata omits full lineage and risk machinery
- Governance preserves mode, authority graph, vetoes, escalation, and minimal precedent only
- Budgets are normalized state variables with simple routing effects
- Thresholds are explicit state variables with provisional calibration
- Escalation is typed and pending but not recursively resolved
- Rollback uses copy-on-write plus scoped in-memory rollback points
- Output is text content plus structured status markers
- State update supports only operations required by the first test harness

## v0.1 Stubs

- Identity Preservation Algorithm (IPA)
- Stability Regulation Algorithm (SRA)
- Novelty Generation and Sandboxing Algorithm (NGSA)
- Architectural Evolution Algorithm (AEA)
- Full IdentityKernel continuity modeling
- Advanced stability, novelty, verification, attention, and recovery dynamics
- Advanced rollback restoration

Stubs may detect and route. They may not claim complete review or authorize protected mutation.

## v0.1 Defers

- Autonomous reasoning and self-modification
- General semantic parsing and contradiction detection
- Full graph algorithms
- Full recursive escalation engine
- Persistent database or file-backed state
- Crash-safe write-ahead audit
- Durable rollback restoration
- Threshold learning and calibration
- Constitutional amendment machinery
- Production governance
- ARC task representation and solving
- Performance optimization

Deferred roles remain explicit. They must not be silently collapsed into implemented modules.

## Non-Negotiable Boundaries

### No Category Collapse

The prototype must preserve these distinctions:

- speculation is not grounded knowledge;
- coherence is not evidence;
- evidence is not persistence;
- memory is not invariant;
- usefulness is not legitimacy;
- scale is not authority;
- candidacy is not achieved status;
- review is not mutation;
- escalation is not approval;
- output is not truth;
- audit reservation is not audit completion;
- rollback is not approval;
- failed transformation is not legitimate state change.

### Typed Evidence

Only a typed `EvidenceLink` to an identifiable `EvidenceObject` may affect grounding. Evidential language such as “evidence,” “because,” “study,” or “proves” may create review intent but cannot create evidence.

### Candidate and Scale Separation

`CandidateStatus` records requested elevation. `ScaleLabel` records achieved scale. Candidate status grants no scale or authority.

### Five Graph Domains

The following remain separate:

1. `MemoryGraph`
2. `EvidenceGraph`
3. `CoherenceGraph`
4. `ScaleGraph`
5. `AuthorityGraph`

A cross-graph effect requires explicit routing. Every `GraphUpdate` references its authorizing `ReviewDecision` and audit.

### Governance State

Minimal `GovernanceState` preserves:

- explicit governance mode;
- `AuthorityGraph`;
- active, scoped vetoes;
- unresolved pending escalations;
- minimal governance precedent.

`AuthorityGraph` defines relations. `GovernanceState` records the active authority posture. They are not interchangeable.

### Budget and Threshold State

Minimal `BudgetState` contains normalized:

- stability budget;
- novelty budget;
- verification budget;
- attention budget;
- recovery capacity.

Minimal `ThresholdState` contains named values for identity, stability, constitutional risk, novelty, grounding, persistence, coherence, multi-scale review, architectural fitness, legitimacy, and escalation.

Budgets and thresholds are state variables. Algorithms read them through state; they do not hide or silently rewrite them. Passing a threshold does not independently grant authority.

### Algorithm Contract

Algorithms:

- receive explicit state, target structures, and review context;
- read metadata and prior decisions;
- append typed `ReviewDecision` objects;
- preserve decision status, named scores, rationale, and escalation;
- declare review limitations;
- never mutate architecture state, graphs, governance, budgets, thresholds, or authoritative metadata.

### Registry Enforcement

Every decision is checked for:

- registered algorithm identity;
- eligible target type;
- permitted decision type;
- maximum target scale;
- permitted escalation target;
- stub or protected status;
- self-modification prohibition.

Unregistered or unauthorized decisions remain visible for audit but cannot enter a state-change plan. ICC is a protected registered coordinator.

### Review and Mutation Separation

The pipeline is:

`ReviewDecision -> registry validation -> StateChangePlan -> working-state application -> StateDelta`

Review never directly mutates state. Rejected decisions remain auditable.

### Escalation

`EscalationEvent` preserves source, target, structure, reason, urgency, pending status, decision reference, and audit reference. Escalation transfers unresolved authority and never grants approval. Loops and registry-inconsistent paths are rejected.

### Rollback

High-risk plans create scoped `RollbackPoint` objects before application. Copy-on-write protects the cycle baseline. Rollback restores domain state but never erases the history of the attempt.

### Audit Lifecycle

Every logical cycle creates a `PENDING` `AuditRecord` at entry. It finalizes exactly once as:

- `COMMITTED`, after plan application, state delta, and provisional output are complete; or
- `ABORTED`, after failure, with no surviving attempted domain mutation.

Committed outputs and state changes reference the finalized audit. Runtime-only v0.1 guarantees logical exception safety, not process-crash durability.

## Canonical Transaction Order

1. Capture immutable baseline.
2. Create pending audit.
3. Clone working state.
4. Parse input.
5. Initialize metadata and candidate intent.
6. Create review context.
7. Run registered reviews in governed order.
8. Validate and accumulate decisions.
9. Resolve conflicts and create state-change plan.
10. Create required rollback points.
11. Apply authorized graph, governance, budget, and domain changes to working copy.
12. Compute state delta.
13. Generate provisional authorized output.
14. Finalize committed audit.
15. Bind audit to output, state changes, graph updates, escalations, and rollback points.
16. Append audit and return committed cycle result.
17. On failure, discard working copy, preserve baseline domain state, append aborted audit, and return aborted cycle result.

## Success Standard

v0.1 succeeds only if the complete test suite demonstrates that its foundational distinctions survive parsing, review, authority validation, planned mutation, audit, abort, and output.

Passing self-authored tests does not prove external adequacy. Later phases must compare against simpler baselines and external tasks.

## Scope Change Rule

Any change to a locked choice or foundational boundary requires:

1. a decision-ledger entry;
2. affected canon and stage references;
3. alternatives and rationale;
4. test and rollback consequences;
5. Joseph’s approval when the change alters governing intent.

Implementation may expose ambiguity. It may not silently resolve philosophical ambiguity as code.

## Environment Prerequisite

The macOS system shims cannot execute without Apple command-line developer
tools, but the Codex bundled runtime provides Python 3.12.13 and Git. The
workspace was initialized as a Git repository on branch `main`. On 2026-06-22,
a project-local `.venv` was created and pytest 8.4.2 was installed, satisfying
the Build Stage 1 test-runner prerequisite. The virtual environment is ignored
by Git. This is environment setup, not a scope change or production dependency.

## Exit Condition Assessment

No unresolved naming, scope, transaction, evidence, authority, or foundational data-model ambiguity remains in the v0.1 contract. Calibration values and detailed enum membership may be implemented conservatively within the locked category boundaries and tested in their assigned stages.
