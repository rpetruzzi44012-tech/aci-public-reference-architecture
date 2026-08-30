# Minimal ACI Prototype v0.1 Final Acceptance Record

## Acceptance Decision

**PASS**

Minimal ACI Prototype v0.1 satisfies its bounded acceptance standard:
foundational distinctions survive parsing, review, authority validation,
planned mutation, working-copy application, audit, abort, and output.

This decision establishes contract acceptance for v0.1. It does not claim
general intelligence, full Phase 8 implementation, ARC capability,
consciousness, production security, or external adequacy.

## Findings

### [P1, repaired] Amendment review planned a deferred mutation

CGA correctly returned `AMENDMENT_REVIEW`, but planning converted that review
into `governance_mode_change`, an operation deliberately deferred by the
application layer. A protected output-rule request therefore aborted during
application instead of committing a governed output block.

Repair: amendment review now plans the supported `delay` effect at
`aci/state_update.py:1879`, preserving the CGA decision without mutating
governance. The full-cycle regression at
`tests/test_integrated_cycle.py:259` requires `COMMITTED`, typed `NO_OUTPUT`,
unchanged `governance.normal`, a delay plan, and scoped rollback.

### [P1, repaired] Scale demotion also changed authority

The scale-demotion operation reduced both `ScaleLabel` and `AuthorityLevel`.
That was conservative but still coupled categories the Scope Lock declares
independent.

Repair: `aci/state_update.py:905` now changes only achieved scale and its
paired scale-graph witness. The regression at
`tests/test_state_update_application.py:410` proves authority remains
unchanged. Any authority demotion now requires a separate authorized path.

### [P1, repaired] Aborted cycle results could contain output

The integrated cycle returned no output on abort, but the `CycleResult` model
allowed callers to construct an aborted result containing an `OutputObject`.
That weakened the abort/output boundary at the type-contract level.

Repair: `aci/core.py:883` rejects any output when cycle status is `ABORTED`.
The lifecycle regression at `tests/test_enums_and_models.py:718` proves the
invalid construction fails.

### Remaining acceptance blockers

None found after repair and complete reverification.

## Boundary Audit

| Audited boundary | Result | Primary implementation and test witness |
|---|---|---|
| Category collapse | PASS | Separate enum families in `aci/enums.py`; twelve full-cycle boundaries in `tests/test_category_collapse.py:225`. |
| Graph-domain collapse | PASS | Five distinct containers in `aci/graphs.py:30`; cross-domain snapshot enforcement in `aci/state_update.py:1032`. |
| Missing graph decision/audit references | PASS | Required fields in `aci/core.py:479`; application validation in `aci/state_update.py:632`; audit reference validation in `aci/audit.py:103`. |
| Hidden reviewer state mutation | PASS | Deep-copied review inputs and contract rollback in `aci/review_context.py:99` and `aci/review_context.py:352`. |
| Registry bypass | PASS within the integrated runtime | Registry validation precedes planning at `aci/state_update.py:214`; application requires preserved accepted validation at `aci/state_update.py:576`. |
| Incomplete audit lifecycle | PASS | Pending reservation at `aci/audit.py:262`; exactly-once terminal checks at `aci/audit.py:81`; committed/aborted transitions at `aci/audit.py:284` and `aci/audit.py:357`. |
| Abort leakage | PASS for handled in-process failures | Baseline recovery at `aci/cycle.py:479`; named fault families in `tests/test_cycle_transaction.py`. |
| Untyped grounding | PASS | Immutable typed link at `aci/evidence.py:41`; verified-link-only eligibility at `aci/evidence.py:153`; GEA lookup at `aci/algorithms/gea.py:104`. |
| Candidate/scale collapse | PASS | Separate metadata fields at `aci/core.py:157`; conservative initialization at `aci/metadata.py:132`; MSSA comparison without promotion at `aci/algorithms/mssa.py:173`. |
| Scale/authority collapse | PASS after repair | Scale-only demotion at `aci/state_update.py:905`; regression at `tests/test_state_update_application.py:410`. |
| Escalation/approval collapse | PASS | Typed unresolved event at `aci/core.py:421`; pending-only planning at `aci/state_update.py:309`; full-cycle boundary at `tests/test_category_collapse.py:448`. |
| Implicit budget or threshold behavior | PASS for v0.1 | Explicit state at `aci/state.py:163` and `aci/state.py:187`; named directional checks at `aci/state.py:366`. |
| Unscoped rollback | PASS | Model rejects empty scope at `aci/core.py:456`; application requires matching high-risk scope at `aci/state_update.py:646`. |
| Output overreach | PASS after repair | Least-authoritative selection at `aci/output.py:307`; committed binding at `aci/output.py:393`; abort-output rejection at `aci/core.py:883`. |
| Misleading stub authority | PASS | Registry prohibits stub finalization/authorization at `aci/registry.py:452`; explicit capability disclaimer at `aci/algorithms/stubs.py:569`. |
| Undocumented canon changes | PASS | Treatment corrections in `TREATMENT_MATRIX.md`, implementation status in `CANON_TO_CODE_STATUS.md`, and 29 decisions in `DECISION_LEDGER.md`. |

The registry and mutation checks protect the integrated ACI workflow, not an
adversarial Python process. Public dataclasses and mutable state are not a
cryptographic or process-isolation security boundary.

## Phase 8-to-v0.1 Acceptance Matrix

| Phase 8 module | Treatment | Acceptance result |
|---|---|---|
| 8.1 SymbolicStructure | Implemented | PASS |
| 8.2 SymbolicMetadata | Implemented / simplified | PASS |
| 8.3 ArchitectureState | Implemented / simplified | PASS |
| 8.4 IdentityKernel | Stubbed / deferred | PASS as bounded |
| 8.5 BudgetState | Simplified | PASS |
| 8.6 ThresholdState | Simplified | PASS |
| 8.7 ReviewDecision | Implemented / simplified | PASS |
| 8.8 AuditRecord | Implemented / extended | PASS |
| 8.9 Graph Structures | Implemented / simplified | PASS |
| 8.10 GovernanceState | Implemented / simplified | PASS |
| 8.11 Algorithm Interface | Implemented / simplified | PASS |
| 8.12 AlgorithmRegistry | Implemented | PASS |
| 8.13 Escalation Pathways | Implemented / simplified | PASS |
| 8.14 State Update Rules | Implemented | PASS |
| 8.15 Rollback Points | Implemented / simplified | PASS |
| 8.16 Integrated Cognitive Cycle | Implemented / corrected | PASS |
| 8.17 CycleResult | Implemented / extended | PASS after repair |
| 8.18 OutputObject | Implemented / simplified | PASS |

### Additional v0.1 contracts

| Treatment | Accepted contracts |
|---|---|
| **Implemented** | `EvidenceObject`, immutable `EvidenceLink`, `CandidateStatus`, `ReviewContext`, `StateChangePlan`, `StateDelta`, `EscalationEvent`, `GraphUpdate`, transactional audit extensions. |
| **Simplified** | GEA, CRA, PCA, MSSA, CGA, five graph containers, governance, budgets, thresholds, escalation, rollback scope, and prose output. |
| **Stubbed** | IPA, SRA, NGSA, and AEA detect and route only; full `IdentityKernel` continuity remains represented but unimplemented. |
| **Deferred** | General semantic parsing, source retrieval, learned calibration, durable state/audit/rollback, recursive escalation, positive legitimacy evidence, full identity continuity, novelty generation, architectural evolution, autonomous self-modification, ARC solving, and production governance. |

## Verification

- Focused acceptance regression:
  `135 passed`
- Complete suite:
  `443 passed in 1.60s`
- Runtime:
  Python 3.12.13
- Test runner:
  pytest 8.4.2
- Example runner:
  four scenarios completed
  - committed qualified response;
  - committed escalation notice;
  - committed governance-blocked `NO_OUTPUT`;
  - aborted cycle with no output or state delta.
- Protected amendment probe:
  `cycle.committed`, `audit.committed`, `output.no_output`,
  unchanged `governance.normal`, planned `delay`.
- Phase 8 checksum:
  `b4349325600d282ed1b2b78bc148a6e4ca1a410e27f7f8fba938b1d3eacb5f47`
- Stage evidence:
  23 stage summaries present and Build Stages 0-22 recorded `PASSED`.

## Decision-Ledger Summary

- `DEC-0001` through `DEC-0007`: scope, naming, data-model, graph,
  transaction, and audit foundations.
- `DEC-0008` through `DEC-0013`: authority registry, parser, metadata,
  ReviewContext, typed grounding, and structured coherence boundaries.
- `DEC-0014` through `DEC-0020`: persistence, FUC alignment, scale,
  legitimacy, and protected-stub reductions.
- `DEC-0021` through `DEC-0025`: planning precedence, isolated application,
  output binding, integrated transaction, and complete plan witnessing.
- `DEC-0026` through `DEC-0028`: structured acceptance inputs, transaction
  hardening, and Stage 22 archive compression.
- `DEC-0029`: final acceptance repairs preserving scale/authority,
  abort/output, and review/mutation distinctions.

No implementation divergence found during acceptance remains undocumented.

## Known Limitations

1. Runtime-only logical exception safety is not process-crash durability.
2. Failure while aborted-audit finalization itself is unavailable cannot
   produce a second audited result.
3. State, audit, graph, and rollback records are not durably persisted.
4. Raw lexical persistence input still delays because v0.1 GEA reviews claims
   and hypotheses while the parser creates `MEMORY_CANDIDATE`.
5. CRA uses explicit normalized propositions, not general semantic
   contradiction detection.
6. Positive constitutional legitimacy has no typed evidence model.
7. Budgets, thresholds, and scores are provisional and uncalibrated.
8. IPA, SRA, NGSA, and AEA remain protected routing stubs.
9. The internal object model trusts the current Python process; it is not
   tamper-resistant or a production authorization boundary.
10. Self-authored tests demonstrate contract conformance, not independent
    intelligence, transfer, ARC performance, or production adequacy.

## Accepted Archive

- Archive version identifier: `ACI-MIN-v0.1.0-20260701-R1`
- Release file:
  `outputs/releases/stage_22/current/Minimal_ACI_Prototype_v0.1_Build_Stage_22_v1.1.zip`
- Prior Stage 22 archive revision:
  preserved under `outputs/releases/stage_22/superseded/`
- Integrity:
  SHA-256 sidecar and root checksum manifest are required and verified.

## Final Verdict

**Minimal ACI Prototype v0.1: PASS**

The prototype does not prove that ACI is intelligent. It proves the narrower
claim it was built to test: within its declared runtime boundary, a symbolic
form cannot silently become evidence, memory, architecture, authority,
approval, truth, or committed state without crossing the corresponding typed,
reviewed, authorized, planned, and audited boundary.
