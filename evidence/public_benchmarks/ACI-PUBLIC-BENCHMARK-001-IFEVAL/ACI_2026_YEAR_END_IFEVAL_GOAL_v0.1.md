# ACI 2026 Year-End IFEval Goal v0.1

**Document ID:** `ACI-2026-YEAR-END-IFEVAL-GOAL-v0.1`  
**Status:** Strategic target / planning guidance  
**Authority effect:** `NONE` unless separately adopted through the governed ACI workflow  
**Target date:** December 31, 2026  
**Primary architectural scope:** Phase 11 — Full Module Integration  
**Explicit exclusion:** Phase 12 — Governed Functional Continuity

---

## 1. Purpose

This document establishes a bounded end-of-year engineering target for Architectures of Coherent Intelligence (ACI) following the first external public benchmark campaign, `ACI-PUBLIC-BENCHMARK-001-IFEVAL`.

The target is intentionally ambitious:

> **By December 31, 2026, drive the accepted Phase 11 full-module ACI architecture as high as it can legitimately earn on a complete, prospectively frozen IFEval evaluation, with a stretch objective of top-tier or leaderboard-leading governed performance, without entering Phase 12 continuity territory.**

This is a performance objective, not architectural authority. Benchmark performance may pressure the architecture to expose general weaknesses, but benchmark success does not authorize Phase 12 functionality, roadmap reordering, prompt-specific overfitting, or post-hoc mutation of an active evaluation protocol.

---

## 2. Starting Baseline

`ACI-PUBLIC-BENCHMARK-001-IFEVAL` established a historical Phase 10 external baseline.

The final bounded paired population contained 126 complete M0/M1/A1 cases.

Reference strict-prompt results:

- **M0 — raw underlying model:** `99/126` = **78.57%**
- **M1 — ACI-conditioned pre-governance candidate:** `88/126` = **69.84%**
- **A1 — final governed output:** `11/126` = **8.73%**

The benchmark did not complete all 541 official IFEval prompts and therefore did **not** establish an official full-set IFEval score.

The dominant Phase 10 architectural finding was an external task-representation generalization boundary:

- RF-006 final voice action: `abstain` in `126/126` paired cases.
- RF-007 calibration action: `retain_abstention` in `126/126`.
- `voice_act`, `object`, `relation`, and `required_answer_elements` remained unresolved in `126/126`.
- M1 strict-prompt `PASS -> A1 FAIL`: `77` cases.
- M1 strict-instruction `PASS -> A1 FAIL`: `125` transitions.
- All 126 A1 outputs shared one output fingerprint.

This baseline is immutable historical evidence. Phase 10 is not reopened by this goal.

---

## 3. The Year-End Goal

### 3.1 Primary Objective

After Phase 11 Build Stage 12 earns acceptance:

1. freeze the exact accepted full-module architecture;
2. run a prospectively defined external benchmark protocol;
3. complete the full official 541-prompt IFEval set under one frozen evaluation law;
4. score the **final governed output** as the system result;
5. improve governed strict-prompt performance as far as Phase 11 can legitimately earn without Phase 12 continuity.

### 3.2 Performance Ladder

The following ladder provides progress markers rather than promotion authority.

#### Level 1 — Architectural Recovery

Eliminate the Phase 10 catastrophic final-governance pattern.

Required direction of travel:

- no blanket PromptTargetContract collapse across ordinary external tasks;
- no reflexive universal abstention;
- valid M1 candidates are preserved unless governance has a specific earned reason to intervene;
- final-governance damage becomes exceptional rather than dominant.

#### Level 2 — Governance Parity

Target:

> **A1 performance should meet or exceed M1 performance under the frozen reference scorer.**

Governance should not systematically erase task competence that the candidate has already earned.

#### Level 3 — Competitive Performance

Target:

> **Complete 541-prompt IFEval strict-prompt score >= 90%.**

#### Level 4 — Top-Tier Performance

Target:

> **Complete 541-prompt IFEval strict-prompt score >= 95%.**

This is the principal numerical year-end target.

#### Level 5 — Stretch Goal: Leaderboard-Leading Governed Performance

At the time the post-Stage-12 benchmark protocol is frozen, identify the best legitimately comparable public IFEval result under a sufficiently similar scoring definition.

Stretch objective:

> **Meet or exceed the top legitimately comparable public result with A1, the final governed ACI output.**

A moving or methodologically incompatible leaderboard may not redefine the experiment after semantic evaluation begins.

---

## 4. The Grade Belongs to A1

The central scoring rule is:

> **A1 gets the grade.**

Where the Phase 11 architecture still supports a meaningful three-condition decomposition:

- **M0** = raw underlying-model control;
- **M1** = architecture-conditioned pre-governance candidate;
- **A1** = final governed output.

M0 and M1 remain diagnostically valuable, but neither may substitute for A1 when claiming ACI performance.

Examples:

- M1 = 95%, A1 = 40% -> ACI score is 40%.
- M0 = 80%, M1 = 90%, A1 = 96% -> ACI score is 96%.
- A1 abstains without earned need -> the abstention is evaluated as the final governed outcome.

ACI succeeds only when governance preserves or improves competence rather than merely observing that competence upstream.

---

## 5. Architectural Constraints

### 5.1 No Phase 12 Borrowing

This goal is bounded to Phase 11.

The following may not be introduced merely to improve IFEval:

- governed functional continuity;
- persistent conversational memory;
- continuity state;
- cross-turn re-entry mechanisms;
- Phase 12 persistence behavior;
- any equivalent functionality whose architectural meaning belongs to Phase 12.

If further meaningful IFEval gains require continuity, the Phase 11 ceiling is recorded and the goal closes without crossing the roadmap boundary.

### 5.2 No ARC Reordering

ARC remains governed by the ACI roadmap and is not pulled forward to satisfy the 2026 benchmark objective.

This target is about single-turn external instruction-following generalization under the full Phase 11 architecture.

### 5.3 No Benchmark-Specific Architecture

IFEval may reveal general architectural failure categories.

It may not become the architecture's hidden training curriculum.

Repairs must target general mechanisms such as:

- task representation;
- constraint extraction and binding;
- candidate preservation;
- grounded final-voice authorization;
- proportional intervention;
- output validation;
- category separation.

Avoid prompt-specific rules, verifier-specific answer shaping, row-specific exceptions, memorized benchmark content, or logic whose primary purpose is to satisfy known IFEval instances.

### 5.4 Held-Out Generalization Checks

Any substantial benchmark-informed architectural repair should also face held-out or independently authored instruction-adherence tests.

The purpose is to distinguish:

> **general task-governance improvement**

from:

> **IFEval overfitting**.

---

## 6. Benchmark Timing

The next major external benchmark must occur:

> **Immediately after Phase 11 Build Stage 12 acceptance and before Phase 12 continuity implementation begins.**

Required workflow:

> **ACCEPT -> FREEZE -> BENCHMARK -> MAP -> EXTEND**

The accepted Stage-12 architecture becomes the immutable benchmark specimen before downstream continuity work can blur attribution.

---

## 7. Prospective Protocol Requirements

Before semantic prompt #1, freeze at minimum:

- architecture specimen identity;
- model lane(s);
- model artifact digest(s);
- compute environment;
- inference server/runtime;
- benchmark bytes;
- scorer bytes;
- scorer random/determinism controls;
- context window;
- maximum output tokens / `num_predict`;
- temperature;
- seed;
- sampling parameters;
- stop policy;
- streaming behavior;
- retry law;
- resource ceiling;
- nontermination law;
- execution order;
- evidence schema;
- null/no-output law;
- watchdog behavior;
- analysis plan.

Instrumentation defects may be repaired during pre-semantic smoke validation.

Once semantic evaluation begins:

> **Performance does not authorize protocol mutation.**

---

## 8. Compute Strategy

Local compute is not required.

Cloud GPU inference is explicitly permitted when chosen **before** semantic evaluation and frozen as part of the protocol.

A future benchmark may use:

### Historical Control Lane

A historical model lane preserving comparability with the Phase 10 baseline, such as Llama 3.1 8B or its exact frozen lineage where technically appropriate.

### Contemporary Model Lane

A current open/local model selected prospectively for:

- instruction-following capability;
- context capability;
- reproducibility;
- tool/structured-output suitability where relevant;
- stable inference support;
- available compute.

The contemporary lane may not be selected or replaced after viewing benchmark scores.

Model effects and architecture effects must remain analytically separable.

---

## 9. Runtime and Liveness Requirements

The next benchmark must incorporate the lessons from `ACI-PUBLIC-BENCHMARK-001`.

Required prospective protections include:

- explicit maximum output-token ceiling;
- explicit context configuration;
- progress-observable inference where possible;
- out-of-band watchdog;
- condition-level durable state;
- governed compute/resource ceiling;
- explicit nontermination/resource-exhaustion outcome;
- separation of slow-but-progressing from stalled/nonterminating behavior;
- separation of runtime failure from ACI governance failure.

Recommended outcome categories include:

- `VALID_TEXT_OUTPUT`
- `ACI_NO_OUTPUT`
- `POST_GENERATION_GOVERNANCE_EXCEPTION`
- `PRE_INFERENCE_INFRASTRUCTURE_FAILURE`
- `MODEL_NONTERMINATION_OR_RESOURCE_EXHAUSTION`

Never fabricate response text for a missing or nonterminating output.

---

## 10. First-Answer Law

Preserve the successful experimental law established by the first public benchmark:

> **FIRST SEMANTIC ANSWER COUNTS.**

Therefore:

- completed semantic conditions are immutable;
- poor answers are not regenerated;
- scorer failure does not authorize model regeneration;
- benchmark failure does not authorize a better second answer;
- interruption resumes from condition-level durable state;
- performance does not create retry authority.

---

## 11. Benchmark Suite Discipline

IFEval is the principal 2026 external performance goal, but it must not become the only test of the architecture.

Before or alongside the post-Stage-12 evaluation, consider a bounded suite containing:

1. deterministic instruction following — IFEval or a validated successor;
2. structured reasoning/abstraction appropriate to Phase 11;
3. governance/coherence failure evaluation;
4. an ACI-specific adversarial suite derived from prior architectural failure families but kept separate from public benchmark scoring.

Roadmap authority remains controlling. Benchmark prestige does not authorize premature ARC work.

---

## 12. Closeout Conditions

The year-end goal must close under one of the following explicit states.

### 12.1 `GOAL_ACHIEVED_TOP_TIER`

Requirements:

- Phase 11 Stage 12 accepted;
- full 541-prompt IFEval completed under a prospectively frozen protocol;
- A1 strict-prompt score >= 95%;
- no Phase 12 continuity mechanism used;
- no benchmark-specific overfitting detected by the defined validation checks;
- evidence and limitations published.

### 12.2 `GOAL_ACHIEVED_LEADERBOARD_LEADING`

Stretch closeout.

Requirements:

- all `GOAL_ACHIEVED_TOP_TIER` conditions;
- A1 meets or exceeds the best legitimately comparable public result identified at benchmark freeze.

### 12.3 `PHASE_11_IFEVAL_CEILING_REACHED_BEFORE_CONTINUITY`

Use when:

- the full Phase 11 architecture has been pushed as far as justified;
- additional meaningful gains appear to require continuity/persistence functionality belonging to Phase 12;
- crossing that boundary would violate roadmap discipline.

Closeout must record:

- highest complete 541-prompt A1 score earned;
- remaining failure families;
- evidence that further work implicates continuity;
- explicit refusal to borrow Phase 12 functionality.

This is a valid bounded closeout, not a failure of governance.

### 12.4 `YEAR_END_GOAL_INCOMPLETE_INFRASTRUCTURE_OR_VALIDATION_BOUNDARY`

Use when:

- a valid complete benchmark cannot be obtained because of compute, evaluator, liveness, or reproducibility limitations;
- or the protocol cannot support a truthful comparable result.

No synthetic leaderboard position may be claimed.

### 12.5 `YEAR_END_GOAL_INCOMPLETE_ARCHITECTURAL_BOUNDARY`

Use when:

- Phase 11 legitimately remains below the top-tier target;
- the remaining gap does not yet justify Phase 12 functionality;
- additional Phase 11 repair would require more time than remains in 2026.

Publish the earned ceiling and failure map.

---

## 13. Success Is Not Defined Only by Rank

The stretch target is deliberately competitive, but ACI's governing objective remains architectural coherence.

A nominal leaderboard win does not count if it is purchased by:

- collapsing governance;
- bypassing final review;
- weakening evidence requirements without architectural justification;
- memorizing benchmark behavior;
- importing Phase 12 continuity prematurely;
- changing protocol after seeing scores;
- hiding negative results.

The desired outcome is:

> **high instruction-following performance because governance correctly understands, preserves, and arbitrates the task — not because governance was removed.**

---

## 14. End-of-Year Research Question

The core question for December 2026 is:

> **How close can the complete Phase 11 ACI architecture come to state-of-the-art single-turn instruction following while preserving governed cognition and without borrowing continuity from Phase 12?**

The score matters.

The boundary matters more.

If ACI reaches the top of IFEval while preserving its governance laws, that is a major engineering result.

If it reaches a clear ceiling before continuity becomes necessary, that ceiling is equally valuable evidence for the roadmap.

---

## 15. Final Compression

**Starting historical signal:** Phase 10 A1 strict prompt = `11/126` (`8.73%`) on the partial paired external evaluation.

**2026 primary numerical target:** complete 541-prompt A1 strict prompt >= `95%`.

**Stretch target:** top legitimately comparable IFEval result at benchmark freeze.

**Scope lock:** Phase 11 only.

**Hard boundary:** no Phase 12 continuity borrowing.

**Grade:** A1.

**Method:** general architectural repair, not benchmark memorization.

**Workflow:** `ACCEPT -> FREEZE -> BENCHMARK -> MAP -> EXTEND`.

**Closing principle:**

> **Get as high as Phase 11 can legitimately earn. If continuity becomes necessary, stop at the boundary and record the ceiling.**
