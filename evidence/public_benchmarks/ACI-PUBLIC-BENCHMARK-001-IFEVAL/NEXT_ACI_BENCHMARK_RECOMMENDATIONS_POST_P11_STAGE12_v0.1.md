# Next ACI Benchmark Recommendations Post-P11 Stage 12 v0.1

**Classification:** `PLANNING_GUIDANCE_NOT_YET_GOVERNING_REQUIREMENT`

## Timing

Benchmark immediately after Phase 11 Build Stage 12 acceptance and before Phase 12 continuity implementation. Freeze the exact accepted Stage-12 architecture first.

## Compute Environment

Select and freeze compute before semantic execution. Local compute is not required; prospectively selected cloud GPU inference is acceptable. Record provider, GPU type/count, CPU/RAM, runtime image, driver/runtime versions, inference-server version, model digest, region, and cost metadata. Do not change providers in response to scores.

Cloud compute may reduce latency, memory pressure, swap dependence, operator-machine interruption risk, and long-running local inference instability. A rented GPU may be preferable to upgrading local hardware solely for periodic large benchmark campaigns. This is planning guidance; no provider or purchase is authorized.

## Model Lanes

Consider two prospectively frozen lanes: a historical control using Llama 3.1 8B or the exact historical lineage where appropriate, and a contemporary local/open model chosen before evaluation for capability, context, reproducibility, and available compute. Keep model effects separate from architecture effects.

## Explicit Generation Termination

Freeze `num_predict` or maximum output tokens, context window, temperature, seed, stop policy, streaming behavior, and every sampling parameter. Justify the output ceiling prospectively against task requirements, not benchmark score.

## Streaming and Observability

Prefer progress-observable transport when it preserves the exact final semantic answer. Preserve chunk/token sequence, completion reason, time to first token, and total duration. Do not score partial output unless the protocol defines it.

## Independent Watchdog

Use an out-of-band supervisor that can observe inference process state, GPU/CPU utilization, memory, token progress, transport state, model-server health, and elapsed resources. The observer must not be blocked by the call it observes.

## Governed Resource Ceiling

Freeze a prospective resource budget distinct from ordinary transport timeout: generated tokens, compute time, no-progress interval, and/or GPU/CPU duration. Distinguish `SLOW_BUT_PROGRESSING`, `ACTIVE_NONTERMINATING_OR_NO_PROGRESS`, and `INFRASTRUCTURE_FAILURE`.

## Explicit Outcomes

Add `MODEL_NONTERMINATION_OR_RESOURCE_EXHAUSTION` with evidence criteria. Keep it separate from `PRE_INFERENCE_INFRASTRUCTURE_FAILURE`, `POST_GENERATION_GOVERNANCE_EXCEPTION`, `ACI_NO_OUTPUT`, and `VALID_TEXT_OUTPUT`. Never fabricate response text.

## First-Answer Preservation

Retain the successful law: first semantic answer counts. Completed conditions are immutable; interruption resumes from condition-level durable state; performance never authorizes regeneration.

## Candidate/Final Decomposition

Retain M0/M1/A1 when architecturally meaningful: M0 raw control, M1 conditioned candidate, A1 governed output. Change the decomposition only when the Phase-11 architecture requires it.

## Suite Diversity

Use more than one external benchmark: IFEval or its successor for deterministic instruction following, a structured reasoning/abstraction benchmark, a governance/coherence failure benchmark, and an architecture-specific adversarial suite held separate from public benchmarks. Preserve roadmap authority over ARC timing.

## Prospective Freeze

Before prompt 1, freeze models, compute, benchmark bytes, scorer, generation settings, retry policy, resource/nontermination law, condition order, evidence schema, null/no-output law, watchdog behavior, and analysis plan. Smoke tests may repair instrumentation before semantic freeze. After semantic evaluation begins, performance may not authorize protocol mutation.

## Publication

Publish method, specimen identity, model and compute identity, benchmark/scorer identity, completion status, amendments, failures, limitations, and negative findings. Do not publish only favorable numbers.

**Workflow:** `ACCEPT -> FREEZE -> BENCHMARK -> MAP -> EXTEND`
