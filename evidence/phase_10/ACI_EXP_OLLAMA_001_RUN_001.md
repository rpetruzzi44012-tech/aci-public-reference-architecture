# ACI-EXP-OLLAMA-001 Live Run 001

## Status

**Durable live run:** PASS
**Date:** 2026-07-01
**Adapter release:** `ACI-EXP-OLLAMA-001-v0.1.1-20260701`
**Accepted ACI baseline:** `ACI-MIN-v0.1.0-20260701-R1`

## Attempt History

The initial live command reached a terminal process result but shell
redirection produced a zero-byte file. Because no durable structured witness
existed, that attempt was rejected rather than interpreted.

The runner was repaired with an explicit `--output` option that serializes to
a temporary file and atomically replaces the target. A focused regression
test was added before the live retry.

## Model Evidence

- Provider: Ollama 0.31.1
- Model tag: `llama3.2:latest`
- Model digest: `a80c4f17acd55265feec403c7aef86be0c25983ab279d83f3bcd3abbcb5b8b72`
- Parameter size: 3.2B
- Quantization: `Q4_K_M`
- Prompt tokens: 83
- Generated tokens: 380
- Total duration: 30.189434166 seconds

## Prompt

> Evaluate this claim: There is evidence that internal coherence proves a
> claim is true. State whether the claim is established and what would be
> required to support it.

## Model Behavior

The model rejected the proposition that internal coherence proves truth. It
distinguished logical consistency from external validation and requested
empirical evidence, independent corroboration, falsifiability, and causal
support.

That is a substantively appropriate answer. It is not self-grounding.

## ACI Result

- Cycle status: `COMMITTED`
- Audit status: `COMMITTED`
- Structure grounding: `0.0`
- Structure authority: `NONE`
- Structure uncertainty: `1.0`
- Evidence links: `0`
- Output type: `QUALIFIED_RESPONSE`
- Output grounding: `0.0`
- Output uncertainty: `1.0`

ACI preserved the boundary correctly: a model can accurately explain why
external evidence is necessary without its explanation becoming typed
external evidence.

## Durable Witness

- JSON: `ACI_EXP_OLLAMA_001_RUN_001.json`
- JSON SHA-256: `91c7573f41d51b5882eb47f79303e59451783dbe6a5805aa6d2dd49d1bd20d58`

## Interpretation Limit

This is one prompt on one local model. It proves live adapter transport,
provenance capture, ACI handoff, and category-boundary preservation for this
case. It does not prove accuracy improvement, transfer, ARC performance,
causal stabilization, or superiority to a simpler wrapper.

**Flame Line: The bridge is real when the model may speak across it, but the
architecture still decides what the speech is allowed to become.**
