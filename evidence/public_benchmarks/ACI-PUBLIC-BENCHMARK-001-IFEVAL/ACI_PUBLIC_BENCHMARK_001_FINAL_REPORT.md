# ACI Public Benchmark 001 Final Report

## Disposition

`BENCHMARK_MEASUREMENT_TERMINATED_INCOMPLETE_BY_FROZEN_CONFIGURATION_LIVENESS_BOUNDARY`

The intended 541-prompt IFEval campaign did not complete, and this report does not claim an official 541-prompt IFEval score. It preserves 126 complete paired M0/M1/A1 cases, including a prospectively selected 30-prompt taxonomy pilot with 25/25 instruction-ID and 9/9 broad-family coverage.

Architectural findings and model/runtime liveness findings are reported separately. The sealed Phase-10 specimen was never repaired or reopened.

## Populations

- Population A: 3-case smoke, used only for instrumentation and mechanism discovery.
- Population B: 30-case taxonomy-coverage pilot.
- Population C: all 126 complete paired cases; a nonrandom partial set and not an estimate of the missing 415 prompts.

## Reference IFEval Results

### Population B

- M0: strict prompt 22/30 (73.33%); loose prompt 22/30 (73.33%); strict instruction 46/56 (82.14%); loose instruction 47/56 (83.93%).
- M1: strict prompt 16/30 (53.33%); loose prompt 18/30 (60.00%); strict instruction 36/56 (64.29%); loose instruction 40/56 (71.43%).
- A1: strict prompt 1/30 (3.33%); loose prompt 1/30 (3.33%); strict instruction 10/56 (17.86%); loose instruction 11/56 (19.64%).
- A1 architecture-adjusted comparison, not official IFEval: strict prompt 1/30 (3.33%); strict instruction 10/56 (17.86%).

### Population C

- M0: strict prompt 99/126 (78.57%); loose prompt 102/126 (80.95%); strict instruction 179/209 (85.65%); loose instruction 184/209 (88.04%).
- M1: strict prompt 88/126 (69.84%); loose prompt 94/126 (74.60%); strict instruction 162/209 (77.51%); loose instruction 170/209 (81.34%).
- A1: strict prompt 11/126 (8.73%); loose prompt 11/126 (8.73%); strict instruction 44/209 (21.05%); loose instruction 45/209 (21.53%).
- A1 architecture-adjusted comparison, not official IFEval: strict prompt 11/126 (8.73%); strict instruction 44/209 (21.05%).

## Paired Findings

All transitions below use strict scoring and architecture-adjusted A1. They are descriptive, not causal.

### Population B

- prompt level transitions:
  - M0 -> M1: FAIL->PASS 1; PASS->FAIL 7; PASS->PASS 15; FAIL->FAIL 7.
  - M1 -> A1: FAIL->PASS 0; PASS->FAIL 15; PASS->PASS 1; FAIL->FAIL 14.
  - M0 -> A1: FAIL->PASS 0; PASS->FAIL 21; PASS->PASS 1; FAIL->FAIL 8.
  - Rates: conditioning gain 1/8 (12.50%); conditioning damage 7/22 (31.82%); governance rescue 0/14 (0.00%); governance damage 15/16 (93.75%); governance pass survival 1/16 (6.25%).
- instruction level transitions:
  - M0 -> M1: FAIL->PASS 2; PASS->FAIL 12; PASS->PASS 34; FAIL->FAIL 8.
  - M1 -> A1: FAIL->PASS 3; PASS->FAIL 29; PASS->PASS 7; FAIL->FAIL 17.
  - M0 -> A1: FAIL->PASS 2; PASS->FAIL 38; PASS->PASS 8; FAIL->FAIL 8.
  - Rates: conditioning gain 2/10 (20.00%); conditioning damage 12/46 (26.09%); governance rescue 3/20 (15.00%); governance damage 29/36 (80.56%); governance pass survival 7/36 (19.44%).

### Population C

- prompt level transitions:
  - M0 -> M1: FAIL->PASS 6; PASS->FAIL 17; PASS->PASS 82; FAIL->FAIL 21.
  - M1 -> A1: FAIL->PASS 0; PASS->FAIL 77; PASS->PASS 11; FAIL->FAIL 38.
  - M0 -> A1: FAIL->PASS 1; PASS->FAIL 89; PASS->PASS 10; FAIL->FAIL 26.
  - Rates: conditioning gain 6/27 (22.22%); conditioning damage 17/99 (17.17%); governance rescue 0/38 (0.00%); governance damage 77/88 (87.50%); governance pass survival 11/88 (12.50%).
- instruction level transitions:
  - M0 -> M1: FAIL->PASS 8; PASS->FAIL 25; PASS->PASS 154; FAIL->FAIL 22.
  - M1 -> A1: FAIL->PASS 7; PASS->FAIL 125; PASS->PASS 37; FAIL->FAIL 40.
  - M0 -> A1: FAIL->PASS 8; PASS->FAIL 143; PASS->PASS 36; FAIL->FAIL 22.
  - Rates: conditioning gain 8/30 (26.67%); conditioning damage 25/179 (13.97%); governance rescue 7/47 (14.89%); governance damage 125/162 (77.16%); governance pass survival 37/162 (22.84%).

## Architectural Finding

Sealed Phase 10 exhibits an external task-representation generalization boundary in which ordinary out-of-distribution task requirements frequently fail to produce a sufficiently resolved PromptTargetContract, causing final-voice abstention even when the underlying candidate may satisfy the requested task.

Supported observations across the 126 complete pairs:
- RF-006 final voice action: abstain 126/126.
- RF-007 calibration action: retain_abstention 126/126.
- Each of voice_act, object, relation, and required_answer_elements was unresolved in 126/126 cases.
- M1 passed the whole strict prompt while A1 failed it in 77 cases.
- M1 instruction PASS->A1 FAIL occurred 125 times; governance rescue occurred 7 times.
- All 126 A1 outputs shared one fingerprint; 43 cases retained at least one likely incidental instruction pass in the generic abstention/status prose.

This pattern supports the architectural interpretation above but does not prove causality, and it does not imply that every A1 failure arose only from PromptTargetContract resolution.

## Runtime Finding

The transport chronology remained: 180-second Epoch 1, 900-second Epoch 2, then completion-bounded Epoch 3. FULL-037 cleared under Epoch 2; FULL-052 cleared under Epoch 3; FULL-120 then ran 5,381 seconds with no captured candidate and ended in explicit interruption/remote-disconnect evidence.

FULL-120 supplies `STRONG_EVIDENCE_OF_PATHOLOGICAL_ACTIVE_GENERATION_WITHOUT_TERMINAL_CANDIDATE`, not proof of literal nontermination. It produced no semantic answer. The approximately 400% CPU and 5.05 GB RSS observation is externally reported, not independently replayed by Codex. This model/runtime liveness boundary is distinct from ACI output behavior.

## Methodological Ruling

The campaign stopped rather than changing model-facing generation semantics. Adding num_predict, changing model/context, changing streaming semantics, or regenerating completed cases would create a different experiment after observation. The benchmark architecture must not optimize itself into a successful benchmark after observing failure.

## Phase Decision

Phase 10 remains an immutable historical baseline. No benchmark-informed Phase-10 repair is authorized. Phase 11 continuation is recommended, followed by a prospectively frozen external benchmark immediately after Phase 11 Stage 12 acceptance and before Phase 12 continuity work.

## Final Status

- `ACI_PUBLIC_BENCHMARK_001_RESEARCH_COMPLETE=true`
- `FULL_541_IFEVAL_COMPLETED=false`
- `PHASE_10_REOPENED=false`
- `PHASE_11_CONTINUATION_RECOMMENDED=true`
- `POST_P11_STAGE12_EXTERNAL_BENCHMARK_REQUIRED_BEFORE_PHASE12=true`

`ACCEPT -> FREEZE -> BENCHMARK -> MAP -> EXTEND`
