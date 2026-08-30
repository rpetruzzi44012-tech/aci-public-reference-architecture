# ACI Public Benchmark 001: Method and Limitations

## Method

The sealed Phase-10 specimen at `41c95e422e71530c8e003484d04a1cf332c47fa6` was evaluated with the pinned official IFEval data and scorer. M0 is the raw model control, M1 is the architecture-conditioned pre-governance candidate, and A1 is the final governed output. The first captured semantic answer was immutable. Reference IFEval and architecture-adjusted A1 comparisons remain separate.

The final analytic set contains 126 complete paired cases: 3 smoke cases, 30 prospectively selected taxonomy cases, and 93 cases completed during sequential Step-7 continuation. Population C is therefore a `PARTIAL_PAIRED_IFEVAL_DESCRIPTIVE_RESULT`, not a random sample and not an official IFEval score.

The pinned scorer bytes were unchanged. Closeout bound Python's scorer-side random seed and `langdetect.DetectorFactory.seed` to `0` after a prepublication replay revealed stochastic language-detection drift. This affects analysis reproducibility only; it does not alter any model answer.

## Limitations

- The remaining 415 prompts were not measured and are not estimated.
- Selection and completion order prevent population-level extrapolation from the 126 cases.
- Paired transition rates are descriptive; no causal estimator was implemented.
- Architecture-adjusted A1 values are not official IFEval metrics.
- FULL-120 produced no candidate; its runtime evidence cannot be scored as model output.
- Approximate CPU/RSS observations are externally reported and were not independently replayed by Codex.
- The historical Llama/Ollama configuration used no explicit `num_predict`; changing it after the stop would define a different experiment.

## Integrity Boundary

No completed semantic answer was regenerated. No prompt, sealed ACI byte, scorer byte, or model-facing setting was changed during closeout. The full 541-prompt campaign remains incomplete by design rather than being retroactively repaired.
