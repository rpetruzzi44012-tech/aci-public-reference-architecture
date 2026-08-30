# ACI Public Benchmark 001: IFEval

## Purpose

This collection preserves the origin, method, earned evidence, closeout, and
future planning lessons from the first public external evaluation of
Architectures of Coherent Intelligence.

The measured subject was the immutable Phase 10 specimen at commit
`41c95e422e71530c8e003484d04a1cf332c47fa6`, tree
`af2e6e558a85b505316779ef497a49ed949c7f70`, using the frozen
`llama3.1:8b` model artifact.

## Research Disposition

`BENCHMARK_MEASUREMENT_TERMINATED_INCOMPLETE_BY_FROZEN_CONFIGURATION_LIVENESS_BOUNDARY`

The intended 541-prompt campaign did not complete, and no official full-set
IFEval score is claimed. The campaign earned 126 complete paired M0/M1/A1
cases. Its prospectively selected 30-prompt taxonomy pilot covered 25/25
instruction IDs and 9/9 broad families. Population C is nonrandom partial
paired evidence and does not estimate the missing 415 prompts.

Reference strict-prompt results for the 126 complete pairs were:

- M0 raw model control: `99/126` (`78.57%`)
- M1 ACI-conditioned candidate: `88/126` (`69.84%`)
- A1 final governed output: `11/126` (`8.73%`)

## Findings

The architectural and runtime findings remain separate.

The architectural evidence supports an external task-representation boundary:
RF-006 abstained in 126/126 cases, RF-007 retained abstention in 126/126, and
the four observed PromptTargetContract dimensions remained unresolved in all
126 cases. All A1 outputs shared one fingerprint. This is descriptive evidence,
not a population-wide or causal proof.

The runtime evidence classifies FULL-120 as
`STRONG_EVIDENCE_OF_PATHOLOGICAL_ACTIVE_GENERATION_WITHOUT_TERMINAL_CANDIDATE`,
not proven literal nontermination. It produced no measured semantic answer.

The closeout bound scorer-side Python and language-detection random seeds to
zero after reproducibility replay exposed score drift. Scorer bytes and model
answers remained unchanged.

## Contents

- `ACI_PUBLIC_BENCHMARK_001_ORIGINAL_OUTLINE.md` - byte-exact pre-execution
  planning and experimental design artifact.
- `ACI_PUBLIC_BENCHMARK_001_FINAL_REPORT.md` - human-readable closeout.
- `ACI_PUBLIC_BENCHMARK_001_FINAL_SUMMARY.json` - earned metrics and paired
  analyses.
- `ACI_PUBLIC_BENCHMARK_001_METHOD_AND_LIMITATIONS.md` - method and claim
  boundaries.
- `ACI_PUBLIC_BENCHMARK_001_ARCHITECTURAL_FINDINGS.json` - Phase 10 witness
  findings.
- `ACI_PUBLIC_BENCHMARK_001_RUNTIME_AND_LIVENESS_FINDINGS.json` - transport
  and liveness findings.
- `ACI_PUBLIC_BENCHMARK_001_EVIDENCE_MANIFEST.json` - evidence-chain identity.
- `BENCHMARK_CARD_FINAL.json` - final benchmark metadata and disposition.
- `NEXT_ACI_BENCHMARK_RECOMMENDATIONS_POST_P11_STAGE12_v0.1.md` - planning
  guidance for the next prospectively frozen benchmark.
- `ACI_2026_YEAR_END_IFEVAL_GOAL_v0.1.md` - strategic Phase 11 target with
  `authority_effect=NONE`.
- `ACI_PUBLIC_BENCHMARK_001_FINAL_PUBLICATION_PACKAGE.zip` and sidecar - compact
  closeout carrier.
- `MANIFEST.sha256` - repository-byte checksums for this collection, excluding
  the manifest itself.

## Authority Boundary

This archive does not reopen or repair Phase 10. It does not change Phase 11
implementation authority, authorize Phase 12 continuity, or make the year-end
goal canonical. The goal remains:

`status=STRATEGIC_TARGET_PLANNING_GUIDANCE`

`authority_effect=NONE`

`phase_scope=PHASE_11_ONLY`

`phase_12_continuity_borrowing=PROHIBITED`

`A1_IS_GRADED_SYSTEM_OUTPUT=true`

The future workflow lesson is:

`ACCEPT -> FREEZE -> BENCHMARK -> MAP -> EXTEND`
