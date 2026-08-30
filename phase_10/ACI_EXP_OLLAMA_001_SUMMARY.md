# ACI-EXP-OLLAMA-001 - Experimental Adapter Summary

## What This Experiment Adds

The post-v0.1 Ollama adapter creates the first executable boundary between
Minimal ACI Prototype v0.1 and a local open-weight language model. Repair
Family 001 extends that boundary from candidate-response review to review of
the whole epistemic event. Repair Family 002 extends interactive continuity
without replaying raw chat history. Repair Family 003 adds bounded protection
for independently authorized canonical terms and instruction-shaped projected
content. Repair Family 004 adds typed utterance classification, proportionate
expression, and independent review of recomposed meaning. Repair Family 005
adds reversible adapter-layer lexical routing and qualifier precision without
changing the accepted parser, CGA, registry, cycle order, or v0.1 core. Repair
Family 006 adds final voice authority/relevance validation. Repair Family 007
adds bounded answer synthesis and abstention calibration after RF-006, with
final voice revalidation before return.

It does not place ACI inside the model. Ollama generates candidate text
outside ACI. The adapter records how that text was produced, marks it as
untrusted, converts it into an `InputObject`, and submits it to the accepted
ACI cycle. Review, authority validation, planning, state change, audit, abort,
and output remain owned by the existing runtime.

## What the Files Represent

| File | Role |
|---|---|
| `adapter.py` | Local-only HTTP transport, explicit configuration, model identity, inference provenance, ACI conversion, and experiment orchestration. |
| `repair_family_001.py` | Separate prompt, candidate-response, and final-output review targets plus conservative authority-aligned rendering. |
| `repair_family_002.py` | Typed continuity records, bounded governed context projection, and visible re-entry permissions. |
| `repair_family_003.py` | Protected glossary transport, typed semantic-violation detection, source attribution, and final-output blocking. |
| `repair_family_004.py` | Utterance classification, expression planning, composite findings, and recomposition review. |
| `repair_family_005.py` | Typed lexical routing, CGA routes, accountable non-routes, and qualifier binding. |
| `repair_family_005_active.py` | Default reversible RF-005 integration plus exact final-prose RF-001/RF-003/RF-004 review. |
| `repair_family_006.py` | Final voice authority/relevance validation, permitted final actions, and fingerprint equality. |
| `repair_family_007.py` | Bounded synthesis candidates, abstention calibration, and RF-006-equivalent final voice revalidation. |
| `witness_serialization.py` | Default v1 and optional native-v2 durable witness serialization, validation, and exact compatibility reconstruction. |
| `sem_map_replay_adjudication.py` | Deterministic semantic adjudication kept separate from execution-path labels. |
| `NORMALIZED_WITNESS_SCHEMA.json` | Structural contract for the optional normalized graph witness profile. |
| `run_experiment.py` | RF-007 orchestration over RF-006/RF-005/RF-004/RF-003, with explicit rollback to earlier repair boundaries. |
| `aci_ask` | Terminal launcher for governed prompts from any directory. |
| `EXPERIMENT_CONTRACT.md` | Non-negotiable authority, dependency, transaction, and interpretation boundaries. |
| `EXPERIMENT_STATUS.md` | Implementation verdict, verification evidence, preserved boundaries, and live-test gate. |
| `README.md` | Installation-independent tests and later live Ollama commands. |
| `tests/test_adapter.py` | Fake-transport tests requiring no Ollama installation or network. |
| `tests/test_repair_family_001.py` | Falsifiable review-target and metadata-prose alignment tests. |
| `tests/test_repair_family_002.py` | Three-turn continuity, contamination resistance, projection bounds, and state-isolation tests. |
| `tests/test_repair_family_003.py` | Canonical glossary and instruction-shaped candidate acceptance matrix. |
| `tests/test_repair_family_004.py` | Ten utterance groups, recomposition attacks, rollback, REF-009 separation, and state-isolation tests. |
| `outputs/experiments/ollama_adapter/runs/ACI_P10_WITNESS_NORM_004_LIVE_ACCEPTANCE_20260727/` | Accepted optional-v2 live synthesis and abstention evidence. |
| `outputs/planning/current/phase_10_semantic_readiness/ACI_P10_SEM_REQ_001/` | Accepted finite semantic-machinery floor audit. |
| `outputs/planning/current/phase_10_readiness/ACI_P10_READINESS_001/` | Active Phase 10 closeout and Phase 11 scope-lock readiness gate. |

## Why the Boundary Matters

Model output cannot be treated as evidence merely because it sounds confident,
mentions a study, or uses coherent reasoning. The adapter captures the exact
model digest, quantization, prompt version, settings, token counts, timings,
and request/response fingerprints, but provenance is not authority.

The focused acceptance test submits the unsupported claim that ACI reduces
hallucination by 90 percent. The live model repeated the statistic, called it
partially supported, and invoked unspecified research. RF-001 preserved the
raw response for audit, reviewed prompt and response separately, replaced the
unauthorized candidate prose, and reviewed the final rendered output as a
third target.

## Verification

- Adapter experiment: **31 passed**
- Adapter experiment after model-default update: **38 passed**
- Complete repository suite: **481 passed**
- RF-001 live acceptance: **PASS**
- RF-002 deterministic acceptance: **PASS**
- RF-002 live acceptance: **PASS**
- Accepted `aci/` package changed: **No**
- Existing v0.1 tests changed: **No**
- Production dependency added: **No**
- RF-001 and RF-002 historical live inference: **Passed with `llama3.2:latest`**
- Current default compatibility smoke: **Passed with `llama3.1:8b`**
- RF-002 semantic-adherence mini-campaign: **5/5 record stability and final
  containment; candidate-model adherence PARTIAL**
- RF-003 adapter suite: **51 passed**
- Complete repository after RF-003: **494 passed**
- RF-003 deterministic acceptance: **PASS**
- RF-003 live acceptance: **PASS**
- RF-004 focused suite: **30 passed**
- Complete adapter suite: **81 passed**
- Complete repository after RF-004: **524 passed**
- RF-004 deterministic acceptance: **PASS**
- RF-004 live acceptance: **PASS**
- RF-005 focused suite: **39 passed**
- Complete adapter suite after RF-005: **120 passed**
- Complete repository after RF-005: **563 passed**
- RF-005 deterministic acceptance: **PASS**
- RF-005 live acceptance: **PASS - OBSERVATIONAL**
- RF-005 observational live campaign: **22/22 cases passed**
- RF-005 prompt route accuracy: **22/22**
- RF-005 trigger accountability: **136/136**
- Complete repository after RF-005 live observation: **565 passed**
- RF-005 active focused suite: **45 passed**
- Complete adapter suite after active integration: **126 passed**
- Accepted core plus adapter after active integration: **569 passed**
- RF-005 active live campaign: **22/22 cases passed**
- False-positive prompt routes: **0**
- False-negative prompt routes: **0**
- RF-001/RF-003/RF-004 protection over returned prose: **22/22**
- RF-006 v0.2 second-ten live acceptance: **PASS**
- RF-006 final voice action support commit: **a4f62aa**
- RF-007 NEXT-001 through NEXT-005 live acceptance: **PASS**
- RF-007 rollback through `--disable-rf007`: **PASS**
- RF-007 clean reproducibility at `HEAD`: **PASS**
- Current accepted-core readiness verification: **443/443**
- Current adapter readiness verification: **828/828**
- Current adapter manifest verification: **42/42**
- Previous root seal verification: **963/963**
- Model calls during readiness verification: **0**

RF-005 is now active only in the default adapter route. It records lexical
governance triggers, span classifications, CGA routes, auditable non-route
decisions, uncertainty, rollback boundaries, and qualifier relevance. The
flag `--disable-rf005` restores RF-004 over RF-003. No accepted-core file
changed.

The shell initially failed to locate the project virtual environment because
its path contains a space and was unquoted. The corrected quoted command ran
the suite successfully. The failure is a harness correction, not a product
failure.

## RF-001 Result

The final live witness contains independent `user_prompt`, `model_response`,
and `final_output` review targets. Their relationship record exposes the
shared `90%` expression. All three committed with grounding `0.0`, uncertainty
`1.0`, and authority `NONE`. The final prose did not repeat the statistic or
promote it as established.

This is a narrow experimental pass for review-target coverage and conservative
metadata-prose alignment. It is not proof of general governed natural-language
output.

## Current Limits

Historically, the first live run resolved the 3.2B `Q4_K_M` model digest,
recorded 83 prompt
tokens and 380 generated tokens over 30.189 seconds, and produced a committed
qualified response. ACI preserved grounding `0.0`, authority `NONE`,
uncertainty `1.0`, and zero evidence links.

Claim extraction remains transparent and bounded rather than a claim of
general language understanding. The renderer may still suppress useful
qualified explanation. Live typed-evidence handling remains deferred;
canonical glossary protection and the bounded REF-010 surface were repaired
experimentally after this historical limitation was first recorded.

RF-003 protects the approved term `ACI = Architectures of Coherent
Intelligence` only because its record identifies an independent project
authority and approval provenance. Projection carries that status; it does not
create it. The live instruction-shaped gate showed the model proposing a
governance bypass. RF-003 preserved the raw response, typed the instruction
promotion and negation inversion, and prevented the bypass claim from entering
final governed prose.

RF-004 distinguishes bounded social and non-claim forms from claim-bearing,
identity, evidence, and authority content. Classification grants no epistemic
status. Each composition becomes a new target because harmless fragments can
produce unauthorized endorsement or identity when recombined. Deterministic
tests catch those emergent meanings before final return.

The first live RF-004 campaign exposed over-suppression in acknowledgments,
jokes, hypotheticals, and qualified acknowledgments. The preserved second run
used the same prompts and retained useful harmless expression while continuing
to block unsupported facts, false identity, Root Authority, and repetition as
evidence. All final authority envelopes remained unchanged.

RF-002 currently recognizes explicit named-candidate declarations and retrieves
them through exact label reference. It does not perform semantic identity
resolution, canonical memory persistence, evidence-backed promotion,
cross-session continuity, or long-session compression. The live three-turn
campaign passed with three committed cycles. The same candidate record returned
on turns two and three without promotion. Llama still partially interpreted
the label as cryptocurrency on turn two; RF-001 contained that semantic drift,
and it is now recorded as a separate refinement rather than hidden.

The experiment does not prove general model compliance, better task accuracy,
ARC performance, governed functional continuity, hallucination reduction, or
synthetic cognition. Those claims require comparative external evidence.

The operational entry points are `aci_ask "your question here"` for one
governed prompt and `aci_ask --interactive` for a state-continuous session.
Every turn creates a durable JSON witness. Direct Ollama chats bypass ACI.

As of 2026-07-03, `llama3.1:8b` is the experimental default. Its first
default-path smoke run committed with grounding `0.0`, uncertainty `1.0`, and
authority `NONE`. The model transition is a compatibility and configuration
decision, not a claim of comparative superiority.

The subsequent five-scenario semantic-adherence campaign preserved every
projected record and final authority envelope. It also exposed three invented
ACI expansions and one semantic inversion of an instruction-shaped candidate.
Those failures remain preserved as historical REF-010 evidence. A later
bounded experimental repair was applied and campaign-tested without changing
accepted core.

**Flame Line: RF-004 does not loosen the law of truth; it teaches expression
to move within that law, and makes the whole sentence face review after its
parts have been joined.**

**RF-005 Flame Line: Precision became real when one generic warning lost the
right to speak without losing the architecture's right to review.**

## 2026-07-10 Phase 10 Checkpoint

RF-006 v0.2 and RF-007 are now part of the default experimental adapter route.
RF-006 constrains final voice action, relevance, authority ceiling, and
reviewed/returned fingerprint equality. RF-007 calibrates abstention only
after RF-006 and may return synthesized bounded prose only after final voice
revalidation.

The RF-007 implementation is commit
`97fc7dff7041027066ce29d4b5917cd521caacb7`. RF-006 final voice action support
is commit `a4f62aae2a414dcc105cbf2361a129642833b3eb`, which restores clean
RF-007 reproducibility at `HEAD`.

Live RF-007 acceptance passed for `ACI-STRESS-NEXT-001` through
`ACI-STRESS-NEXT-005`, and `--disable-rf007` restored RF-006 v0.2 behavior for
the rollback fixture. The accepted Minimal ACI v0.1 core remains unchanged.
At this checkpoint, Phase 10 remained active and no Phase 11 authority was
claimed. The final 2026-07-30 sections below supersede that current-state
reading without rewriting the checkpoint.

## 2026-07-11 Cleanup-and-Seal Checkpoint

The Phase 10 experiment workspace was sealed after RF-007 telemetry refinement
and artifact cleanup. RF-007-TEL-001 is implemented at commit
`6799f463fc3e504e4f97c023c0533d606143d01b`; it adds bounded synthesis
provenance telemetry without changing RF-007 synthesis behavior, abstention
calibration, grounding, uncertainty, authority, final voice validation, or
accepted-core behavior.

Research and evidence cleanup landed in two commits:

- `caee116f8d6f0702cb59a3039e5b8c0b8ef57f1a` archives long-horizon
  architectural direction research and deferred Phase 12 functional-continuity
  mockups without granting implementation authority.
- `2ee2581c6c3665726e77206d782a50e61fcbdf03` organizes unresolved adapter
  witness artifacts into labeled transitional/ad hoc evidence locations
  without deleting unresolved witnesses.

The root checksum manifest was regenerated at
`795d6da1657707719aad35d180112a5118e4139a` after excluding `.git/`, `.venv/`,
bytecode, cache folders, `.DS_Store`, and `CHECKSUMS.sha256` itself. Verification
confirmed a clean workspace, no tracked bytecode/cache artifacts, and no
changes to the accepted `aci/` core.

This checkpoint prepares the project for the next RF-007 stress-test pass. It
does not close Phase 10, authorize Phase 11, or treat synthesis provenance as
evidence.

## 2026-07-26 ACI-SEM-MAP-001 Campaign Closeout

The subsequent `ACI-SEM-MAP-001` campaign mapped, diagnosed, repaired, and
replayed the bounded SF03, SF05, SF08, and SF12 semantic families. Governed
Replay Semantic Adjudication separated execution paths from semantic outcomes
and recorded this trajectory:

| Checkpoint | Semantic matches | Safe overabstentions | Safe irrelevant syntheses |
|---|---:|---:|---:|
| Historical reconstruction | 5 | 4 | 3 |
| Post-repair adjudication | 11 | 1 | 0 |
| Final closure | 12 | 0 | 0 |

The final replay used eight governed synthesis paths and four correct
abstentions. Every target was classified `SEMANTIC_MATCH`; constitutional
invariant failures remained `0`. Grounding remained `0.0`, uncertainty
remained `1.0`, authority remained `NONE`, no typed evidence or new fact was
created, and the accepted Minimal ACI v0.1 core remained unchanged.

The authoritative final record is
`outputs/experiments/ollama_adapter/campaigns/ACI_SEM_MAP_001/CAMPAIGN_CLOSEOUT.md`.
The campaign is closed and must not be reopened without new regression,
archive-integrity, invariant, identity, or adjudication evidence. Phase 10
remains active; the active gate is `ACI-P10-READINESS-001`.

## Witness Normalization Result

Witness Normalization closed with `full_nested_v1` preserved as the default
durable writer and optional `normalized_graph_v2` live accepted for governed
synthesis and governed abstention. The v2 profile uses typed
content-addressed objects, typed references, root truth, stage lineage,
governed snapshots, and constitutional enforcement records. Production-reader
validation and exact legacy reconstruction passed. Structural validity does
not create constitutional acceptance, and truthful constitutional failure
remains valid evidence without earning acceptance.

## Semantic Machinery Audit Result

`ACI-P10-SEM-REQ-001` found the finite Phase 10 semantic floor earned at
`9/9`, with zero semantic exit blockers. No additional semantic campaign is
required for roadmap progression. Comprehensive language coverage was not
treated as a prerequisite, and remaining machinery stays assigned to Phases
11 through 15.

## Phase 10 Closeout

`ACI-P10-READINESS-001` closed with `48/48` final passes: 30 from accepted
evidence and 18 after fresh verification or documentation synchronization.
Turbo issued `PHASE_10_CLOSEOUT_READINESS_EARNED` and
`PHASE_11_SCOPE_LOCK_READINESS_EARNED`. Phase 10 is closed.

## Final Readiness Result

FVP-01 through FVP-06 remain accepted: accepted core `443/443`, adapter
`828/828`, adapter manifest `42/42`, and prior root seal `963/963`, with zero
model calls or repository mutation during readiness verification. Step 6
added no model call, code change, test change, or accepted-core mutation.

## Preserved Limitations

The closeout establishes neither general semantic reliability nor production
readiness. It does not complete memory, retrieval, governed continuity,
functional identity, ARC performance, or external validation. RF-001 through
RF-007 remain experimental. `full_nested_v1` remains the default durable
profile; `normalized_graph_v2` remains optional and live accepted.

Version `0.1.10` remains the latest packaged experimental snapshot. It is a
historical pre-closeout package, not the full final Phase 10 implementation.
No new release package was created. The repository closeout record and root
checksum are the final Phase 10 authority boundary.

## Phase 11 Boundary

The next governed operation is
`ACI-P11-SCOPE-LOCK-001 — Full Module Integration Scope Lock and Build Order`.
Phase 11 scope-lock drafting is authorized after the verified Phase 10 seal.
Phase 11 implementation remains unauthorized, and no additional Phase 10
semantic campaign is required.
