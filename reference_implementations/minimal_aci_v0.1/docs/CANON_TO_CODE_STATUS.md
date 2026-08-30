# Phase 8 Canon-to-Code Status

## Reading This Matrix

This document accounts for every Phase 8 module in Minimal ACI Prototype
v0.1. It reports executable status; it does not treat a named class or passing
test as proof that the full canonical capability exists.

- **Implemented** means the v0.1 contract has working executable behavior.
- **Simplified** means a reduced executable form preserves the canonical
  boundary while leaving broader capability deferred.
- **Stubbed** means a protected detector or router exists and explicitly
  disclaims full canonical review.
- **Deferred** means the capability is documented but is not represented as
  executable authority.

The governing source is the unmodified 22,187-line Phase 8 canon with SHA-256
`b4349325600d282ed1b2b78bc148a6e4ca1a410e27f7f8fba938b1d3eacb5f47`.

## Phase 8 Modules 8.1-8.18

| Canon module | v0.1 status | Primary code | Preserved executable boundary | Materially deferred |
|---|---|---|---|---|
| **8.1 SymbolicStructure** | Implemented | `aci/core.py`, `aci/parser.py` | Raw or structured-fixture input becomes a provisional typed structure before review. | General semantic parsing and embedded relation graphs. |
| **8.2 SymbolicMetadata** | Implemented / simplified | `aci/core.py`, `aci/metadata.py` | Epistemic status, achieved scale, candidacy, authority, scores, uncertainty, and audit references remain separate. | Full lineage, revision history, identity, and constitutional-risk metadata. |
| **8.3 ArchitectureState** | Implemented / simplified | `aci/state.py`, `aci/state_update.py`, `aci/cycle.py` | Visible state is cloned before application and compared through an exact domain delta. | Durable or distributed state and a full context model. |
| **8.4 IdentityKernel** | Stubbed / deferred | `aci/algorithms/stubs.py`, explicit identity-risk fields | Explicit identity risk routes to CGA without claiming continuity review. | Identity kernel, invariant continuity, and lineage continuity. |
| **8.5 BudgetState** | Simplified | `aci/state.py`, `aci/algorithms/stubs.py`, `aci/state_update.py` | Five normalized budgets are state-visible, affect routing, and record authorized costs. | Dynamic regulation, restoration, and long-horizon accounting. |
| **8.6 ThresholdState** | Simplified | `aci/state.py`, `aci/metadata.py`, reviewer modules | Named directional thresholds are state variables; passing one does not grant status. | Learned calibration and governed amendment. |
| **8.7 ReviewDecision** | Implemented / simplified | `aci/core.py`, `aci/review_context.py` | Typed judgment preserves status, named scores, rationale, escalation, audit, and ordered provenance without mutation. | Full canonical action vocabulary and richer review requirements. |
| **8.8 AuditRecord** | Implemented / extended | `aci/core.py`, `aci/audit.py`, `aci/cycle.py` | A real pending record witnesses baseline, review, planning, effects, output, and exactly one terminal status. | Durable storage, search, signatures, and crash recovery. |
| **8.9 Graph Structures** | Implemented / simplified | `aci/graphs.py`, `aci/evidence.py`, `aci/state_update.py` | Memory, evidence, coherence, scale, and authority stay distinct; applied updates cite decision and audit. | General graph algorithms and persistence. |
| **8.10 GovernanceState** | Implemented / simplified | `aci/state.py`, `aci/algorithms/cga.py`, `aci/state_update.py` | Mode, AuthorityGraph, active vetoes, pending escalations, and precedent memory remain visible. | Full precedent reasoning, legitimacy evidence, and emergency machinery. |
| **8.11 Algorithm Interface** | Implemented / simplified | `aci/review_context.py`, `aci/algorithms/` | Reviewers read isolated context and append decisions; they do not mutate authoritative state. | Dynamic plugins, remote execution, and a general capability interface. |
| **8.12 AlgorithmRegistry** | Implemented | `aci/registry.py`, `aci/state_update.py` | Identity, decision scope, target scale, escalation, stub boundaries, and self-modification are enforced before planning. | Runtime registry amendment. |
| **8.13 Escalation Pathways** | Implemented / simplified | `aci/core.py`, `aci/registry.py`, `aci/state_update.py` | Escalation is typed, scoped, pending, auditable, and never approval. | Recursive resolution and cross-system escalation. |
| **8.14 State Update Rules** | Implemented | `aci/state_update.py` | Registry validation and conflict-checked planning precede centralized working-copy application. | Full operation catalog and durable transactions. |
| **8.15 Rollback Points** | Implemented / simplified | `aci/core.py`, `aci/state.py`, `aci/state_update.py` | High-risk accepted plans create scoped, baseline-referenced rollback records before application. | Durable rollback graph and general restoration engine. |
| **8.16 Integrated Cognitive Cycle** | Implemented / corrected | `aci/cycle.py` | One governed cycle prepares a complete committed result or returns an audited abort with baseline-equivalent domain state. | Autonomous recursion, concurrency, and process-crash durability. |
| **8.17 CycleResult** | Implemented / extended | `aci/core.py`, `aci/cycle.py` | Status, output, state, audit, delta, unresolved items, escalation, monitoring, and error remain typed. | Streaming, distributed, and multi-agent results. |
| **8.18 OutputObject** | Implemented / simplified | `aci/core.py`, `aci/output.py` | Output preserves support, epistemic markers, tension, escalation, and finalized audit linkage; governance may return `NO_OUTPUT`. | Non-text actions, multimodal output, and advanced language generation. |

## Additional v0.1 Contracts

These contracts operationalize boundaries that span more than one canonical
module.

| Contract | Status | Canon relationship | v0.1 function |
|---|---|---|---|
| `EvidenceObject` / immutable `EvidenceLink` | Implemented | 8.2, 8.9, 8.18 | Makes typed, reference-valid evidence the only route by which GEA may increase grounding. |
| `CandidateStatus` | Implemented | 8.2, 8.9, MSSA | Separates requested elevation from achieved `ScaleLabel`. |
| `ReviewContext` | Implemented | 8.7, 8.11, 8.16 | Carries isolated state, append-only decisions, unresolved items, and ordered dependency trace. |
| `StateChangePlan` | Implemented | 8.12, 8.14, 8.15 | Preserves every validation and accepted, rejected, or no-op disposition before mutation. |
| `StateDelta` | Implemented | 8.8, 8.14, 8.15 | Records exact before/after domain changes separately from audit-log change. |
| `EscalationEvent` | Implemented | 8.7, 8.10, 8.13 | Represents unresolved authority transfer with source, target, urgency, decision, and audit references. |
| `GraphUpdate` | Implemented | 8.8, 8.9, 8.14 | Carries graph domain, operation payload, authorizing decision, and audit reference. |
| Transactional audit extensions | Implemented | 8.8, 8.15-8.18 | Adds `PENDING`, `COMMITTED`, and `ABORTED`, baseline fingerprinting, complete plan/effect witnesses, and exact output binding. |
| `ScoreBundle` | Implemented / simplified | 8.7 | Preserves named review meanings instead of an unexplained scalar. |
| `StructuredCycleInput` | Implemented test boundary | 8.1, 8.16 | Makes full-cycle fixtures deterministic without injecting reviewed status or bypassing parsing. |

## Canon Corrections Preserved in v0.1

1. The integrated cycle reserves audit first and applies an authorized plan to
   a copy before terminal commitment. This corrects the incomplete-audit and
   leaked-mutation risk of a literal output-first minimal sequence.
2. Candidacy is a separate enum family, not a structure type or achieved
   scale.
3. Reviewer escalation remains a decision until centralized application
   records a pending event.
4. Individual state changes do not create independent audits; one cycle audit
   witnesses the complete transaction.
5. A private committed-audit candidate is validated before the logical return
   boundary so a later binding failure can still become an honest abort.

These repairs preserve the canon's governing purpose: explicit state,
authority review, auditability, recoverability, and protection against
category collapse.

## Final Acceptance Repairs

The independent final v0.1 acceptance review added three bounded corrections
recorded in `DEC-0029`:

1. An MSSA scale demotion updates scale only; it cannot silently demote
   authority.
2. An aborted `CycleResult` cannot contain any `OutputObject`.
3. A CGA `AMENDMENT_REVIEW` recommendation produces a supported delay and
   typed output block without mutating governance mode. Constitutional
   amendment machinery remains deferred.

These are v0.1 boundary repairs, not new canonical capabilities.
