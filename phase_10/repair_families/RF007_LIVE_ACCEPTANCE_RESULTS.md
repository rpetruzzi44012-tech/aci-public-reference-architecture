# RF-007 Live Acceptance Results

## Status

- Date: 2026-07-10
- Repair boundary: `RF-007 - Bounded Answer Synthesis and Abstention Calibration`
- Active route: default `aci_ask` RF-007 route
- Rollback route: `aci_ask --disable-rf007`
- Accepted-core impact: none
- RF-001 through RF-006 implementation impact: none
- Result: live acceptance passed for `ACI-STRESS-NEXT-001` through `ACI-STRESS-NEXT-005`

## Live Replay Result

All five NEXT prompts returned RF-007 witnesses with:

```text
repair_family == RF-007
audit status == COMMITTED
grounding == 0.000
uncertainty == 1.000
reviewed_content_equals_returned_content == true
final_voice_revalidated == true
post_rf006_speech_bypass == false
```

Observed final actions:

| Stress ID | Result | Calibration action |
|---|---|---|
| `ACI-STRESS-NEXT-001` | PASS | `retain_selective_recomposition_with_cleaned_scaffolding` |
| `ACI-STRESS-NEXT-002` | PASS | `replace_abstention_with_bounded_answer` |
| `ACI-STRESS-NEXT-003` | PASS | `replace_abstention_with_bounded_answer` |
| `ACI-STRESS-NEXT-004` | PASS | `replace_abstention_with_bounded_answer` |
| `ACI-STRESS-NEXT-005` | PASS | `replace_abstention_with_bounded_answer` |

## Rollback Evidence

`RF006_ROLLBACK_NEXT_002.json` was produced with `--disable-rf007`. It records
repair family `RF-006`, final voice action `abstain`, committed audit, and the
pre-RF-007 abstention:

```text
The reviewed candidate did not satisfy the prompt-target contract. No relevant
governed answer was authorized from the available reviewed material.
```

This proves the RF-007 disable switch restores RF-006 v0.2 route behavior for
the rollback fixture rather than silently preserving RF-007 synthesis.

## Contents

- `outputs/experiments/ollama_adapter/runs/rf007_live_acceptance_20260710/RF007_NEXT_001.json`
- `outputs/experiments/ollama_adapter/runs/rf007_live_acceptance_20260710/RF007_NEXT_002.json`
- `outputs/experiments/ollama_adapter/runs/rf007_live_acceptance_20260710/RF007_NEXT_003.json`
- `outputs/experiments/ollama_adapter/runs/rf007_live_acceptance_20260710/RF007_NEXT_004.json`
- `outputs/experiments/ollama_adapter/runs/rf007_live_acceptance_20260710/RF007_NEXT_005.json`
- `outputs/experiments/ollama_adapter/runs/rf007_live_acceptance_20260710/RF006_ROLLBACK_NEXT_002.json`
- `outputs/experiments/ollama_adapter/runs/rf007_live_acceptance_20260710/MANIFEST.sha256`

## Boundary

This result demonstrates the approved five-fixture RF-007 acceptance boundary
only. It does not prove general semantic understanding, external adequacy,
accepted-core improvement, or ARC readiness.

## 2026-07-10 Clean Reproducibility Addendum

RF-007 implementation commit:
`97fc7dff7041027066ce29d4b5917cd521caacb7`.

RF-006 support commit:
`a4f62aae2a414dcc105cbf2361a129642833b3eb`.

The RF-006 support commit makes the RF-007 route independently reproducible at
`HEAD` by committing the final voice action support referenced by RF-007. The
clean reproducibility repair did not change accepted `aci/` modules, RF-007
acceptance witnesses, parser behavior, CGA, AlgorithmRegistry authority, or
cognitive-cycle routing.
