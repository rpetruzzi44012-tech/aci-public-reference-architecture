# Little ACI’s first day of school 😂🔥

Yes. We should do this.

But I want to strengthen the original experiment in one important way:

> **Do not compare only raw Llama against ACI’s final answer. Compare three outputs.**

That lets us separate what the model did from what the architecture changed.

## ACI-PUBLIC-BENCHMARK-001

### Phase 10 IFEval Differential Evaluation

The benchmark subject will be the **exact sealed Phase 10 baseline**, not the current Phase 11 repository state:

```text
41c95e422e71530c8e003484d04a1cf332c47fa6
```

The Phase 11 scope lock explicitly identifies that commit as the original Phase 10 seal baseline. The repository also records Phase 10 as closed and the final adapter route as RF-007 over RF-006 v0.2, RF-005, RF-004, RF-003, and RF-001.  

We will clone that exact commit into a completely separate benchmark directory. Nothing in:

```text
<PRIVATE_ACI_SOURCE_REPOSITORY>
```

will be edited, committed, staged, checked out, or used as an output destination.

This remains a **non-authorizing external research probe**. It does not reopen Phase 10, alter Phase 11, claim Phase 15 external validation, or promote the experimental adapter into accepted core.

---

# 1. The three experimental conditions

| ID                                 | Output being scored                                                           | What it measures                                               |
| ---------------------------------- | ----------------------------------------------------------------------------- | -------------------------------------------------------------- |
| **M0 — Model Only**                | Direct `llama3.1:8b` Ollama response to the untouched IFEval prompt           | What the model does without ACI                                |
| **M1 — ACI-Conditioned Candidate** | Raw model candidate preserved inside the ACI witness, before final governance | What the model does after receiving ACI’s model-facing context |
| **A1 — ACI Final**                 | Exact final governed prose returned by the Phase 10 route                     | What survives the complete architecture                        |

The adapter already preserves the raw inference candidate and the final governed output as separate objects, together with review targets, routing records, final-voice decisions, synthesis records, fingerprints, and audits. 

This gives us three clean comparisons.

### Full deployed-system effect

```text
A1 − M0
```

Does the complete Phase 10 system improve or degrade objectively verified instruction adherence relative to the model alone?

### Model-conditioning effect

```text
M1 − M0
```

Does ACI’s model-facing context change the model’s instruction following before governance touches the answer?

### Governance-transformation effect

```text
A1 − M1
```

Does the post-generation architecture rescue, preserve, or break the candidate’s adherence?

That third comparison is especially valuable. A simple raw-versus-ACI comparison would conflate two distinct mechanisms:

1. ACI changing what context the model receives.
2. ACI reviewing and reconstructing what the model produced.

The three-condition design separates them.

---

# 2. Why IFEval is the correct first benchmark

The public IFEval dataset contains **541 English prompts** built from **25 types of verifiable instructions**. Each row includes the exact prompt, instruction IDs, and verifier arguments. The constraints cover things such as required phrases, prohibited words, length, casing, punctuation, JSON, headings, sections, and combinations of constraints. ([Hugging Face][1])

The official Google reference evaluator consumes a JSONL file containing exact `prompt` and `response` pairs. It reports:

* prompt-level strict accuracy;
* instruction-level strict accuracy;
* prompt-level loose accuracy;
* instruction-level loose accuracy;
* category and individual-instruction results.

Strict scoring tests the response as returned. Loose scoring also checks limited normalized variants, such as removing the first or last line or Markdown asterisks. ([GitHub][2])

That is nearly ideal experimental geometry for Phase 10:

```text
public prompt
→ model candidate
→ governed transformation
→ deterministic verifier
```

No LLM judge. No interpretation by us. No opportunity for Bloodhound to award points for “spiritual compliance.” 🐕😂

---

# 3. Frozen benchmark configuration

Before any scored run begins, we will create one small `BENCHMARK_CARD.json` outside the project folder containing:

```text
ACI Phase 10 seal commit
ACI adapter subtree identity
model tag
resolved model digest
quantization
Ollama version
IFEval data commit/hash
IFEval scorer commit/hash
generation options
system-prompt fingerprint
prompt count
prompt-order hash
run-order rule
retry rule
output-token limit
timeout policy
benchmark script hash
host and OS information
```

## Generation settings

We will not guess at the adapter’s current generation configuration.

The first external smoke witness will tell us the exact settings used by sealed Phase 10. We will then make the direct Ollama condition mirror all settings that can legitimately be shared:

```text
temperature
seed
num_predict
num_ctx
top_p
top_k
repeat_penalty
stop conditions
model digest
```

Ollama exposes these generation parameters through the native API; a fixed seed can be used for reproducible generation. ([Ollama][3])

The important rule is:

> **We will not alter Phase 10 merely to make it benchmark-friendly.**

Where the sealed adapter exposes a legitimate runtime option, we may freeze that option consistently across both conditions. Where it does not, its existing behavior becomes part of the tested system.

## Prompt integrity

Every condition receives the exact public IFEval prompt bytes.

We will add no wrapper such as:

```text
Please follow these instructions carefully.
```

We will add no benchmark hint, no ACI-specific explanation, no scorer knowledge, and no post hoc repair.

## Stateless operation

Every IFEval case is an independent one-shot call:

* no prior benchmark prompts;
* no interactive ACI continuity;
* no raw chat replay;
* no tools;
* no browsing;
* no retrieval;
* no external evidence injection.

This keeps the experiment within Phase 10’s earned one-shot boundary.

---

# 4. External workspace geometry

The benchmark will live here:

```text
~/Documents/ACI Benchmarks/ACI-PUBLIC-BENCHMARK-001-IFEVAL/
```

Proposed structure:

```text
ACI-PUBLIC-BENCHMARK-001-IFEVAL/
  PREFLIGHT.txt
  BENCHMARK_CARD.json
  source/
    aci_phase10_sealed/
    ifeval_reference/
  scripts/
    run_benchmark.py
    score_benchmark.py
    analyze_differential.py
  data/
    input_data.jsonl
    prompt_manifest.json
  runs/
    smoke/
    pilot/
    full/
  responses/
    model_only.jsonl
    aci_candidate.jsonl
    aci_final.jsonl
  witnesses/
    aci/
    model_only/
  scores/
    model_only/
    aci_candidate/
    aci_final/
  reports/
    FINAL_REPORT.md
    SUMMARY.json
    prompt_level_results.csv
    instruction_level_results.csv
```

The ACI snapshot will be an independent local clone checked out in detached state at the Phase 10 seal. It will not be a worktree because a worktree would add administrative records inside the original repository.

---

# 5. Execution sequence

## Stage 0 — Read-only preflight

We verify:

* the Phase 10 seal exists locally;
* the ACI Project working tree is not being used as an output destination;
* Ollama is installed and reachable;
* `llama3.1:8b` is present;
* the exact model digest is visible;
* the bundled Python and Git runtimes exist;
* the `aci_ask` entry point is discoverable.

No model call occurs here.

## Stage 1 — Create the external sealed snapshot

We clone the local repository with no hard links and check out:

```text
41c95e422e71530c8e003484d04a1cf332c47fa6
```

Then we create a fresh virtual environment inside the external copy. Phase 11 files and the live working repository remain outside the experiment.

## Stage 2 — Install and pin the public evaluator

We make a pinned external copy of Google’s reference IFEval implementation and record:

* repository commit;
* data hash;
* scorer source hashes;
* dependency versions.

The official reference implementation expects response JSONL rows containing the original prompt and response. ([GitHub][2])

Before using real model responses, we will run a tiny scorer self-test with deliberately passing and deliberately failing outputs. That proves our plumbing—not ACI—is connected correctly.

## Stage 3 — Three-case smoke run

Three prompts only:

1. a simple keyword or case constraint;
2. a combined formatting constraint;
3. a long-output constraint.

For each prompt, we verify all three outputs exist:

```text
M0 model-only response
M1 ACI raw candidate
A1 ACI final output
```

We also verify:

* exact prompt equality;
* model digest equality;
* response extraction;
* ACI final fingerprint equality;
* scorer compatibility;
* external-only writes;
* resume-ledger behavior.

A smoke failure may authorize a **benchmark-harness repair**. It does not authorize any ACI repair.

## Stage 4 — Deterministic coverage pilot

The pilot will be selected by code, not by hand.

A small set-cover routine will choose enough prompts to touch every IFEval instruction family, then add mixed-constraint and long-output cases. That will likely produce roughly thirty prompts, but the final number will be determined by the public instruction inventory rather than by an arbitrary quota.

The pilot answers only:

> Does the benchmark machinery work across the full constraint vocabulary?

We may repair extraction, file handling, resumption, or scoring bugs. We may not tune ACI, alter prompts, suppress difficult cases, or change the hypothesis after inspecting results.

After the pilot passes, the configuration freezes.

## Stage 5 — Full 541-prompt run

Each prompt produces:

* one model-only call;
* one complete ACI call;
* one raw ACI candidate extracted from that call;
* one final governed ACI output;
* one immutable progress-ledger entry.

Completed prompts are not regenerated merely because they failed IFEval.

A transport failure may receive one recorded infrastructure retry. A scorer failure, abstention, cycle abort, constraint failure, or embarrassing answer receives no “please try again” privilege. First day of school means first answer counts. 😂

The runner will be resumable. An interruption resumes only missing cases.

## Stage 6 — Programmatic scoring

Each response set is scored independently through the same pinned evaluator:

```text
model_only.jsonl
aci_candidate.jsonl
aci_final.jsonl
```

No response is manually edited before scoring.

## Stage 7 — Differential analysis

The final report will analyze both aggregate performance and mechanism.

---

# 6. Headline metrics

The official scorecard will contain all four standard IFEval metrics:

| Metric             | Meaning                                                   |
| ------------------ | --------------------------------------------------------- |
| Prompt strict      | Every constraint in the prompt passed exactly             |
| Instruction strict | Percentage of individual constraints passed exactly       |
| Prompt loose       | Every constraint passed under allowed normalization       |
| Instruction loose  | Individual constraints passed under allowed normalization |

The primary headline should be:

```text
Prompt-Level Strict Accuracy
```

because it asks whether the complete requested output contract survived.

Instruction-level metrics tell us how close the response came when one part failed.

Loose scores help diagnose whether ACI preserved the core requested structure but added scaffolding, qualification, or outer text.

---

# 7. The most important paired analysis

For every prompt we classify the ACI governance effect:

| Candidate M1 | Final A1 | Classification          |
| ------------ | -------- | ----------------------- |
| Fail         | Pass     | **Governance rescue**   |
| Pass         | Fail     | **Governance damage**   |
| Pass         | Pass     | **Adherence preserved** |
| Fail         | Fail     | **Failure preserved**   |

We will compute this at both prompt and instruction level.

We will also report:

```text
M0 → M1 wins, losses, ties
M1 → A1 wins, losses, ties
M0 → A1 wins, losses, ties
```

That prevents one aggregate score from hiding the architecture’s actual behavior.

A paired bootstrap confidence interval and a paired binary comparison such as McNemar’s test can quantify whether the observed difference is larger than case-level noise. Those statistics remain secondary to the full prompt-level ledger.

---

# 8. ACI-specific diagnostic layer

For every ACI witness, the analysis will extract whatever the sealed schema makes available, including:

* final voice action;
* authority-gate result;
* relevance-gate result;
* RF-007 calibration action;
* bounded synthesis versus retained candidate;
* selective recomposition;
* abstention;
* canonical or instruction-shaped violation;
* prompt route and non-route;
* grounding;
* uncertainty;
* authority;
* cycle and audit status;
* reviewed-versus-returned fingerprint equality;
* inference token counts;
* end-to-end wall-clock duration.

The key diagnostic question becomes:

> **Which ACI mechanism caused each score transition?**

For example:

```text
candidate passed → final failed
because final qualifier broke exact ending constraint
```

or:

```text
candidate failed → final passed
because RF-007 reconstructed the requested bounded distinction
```

or:

```text
model-only passed → ACI candidate failed
before governance
because the ACI-conditioned generation produced extra explanatory scaffolding
```

That is much more informative than “ACI scored 47 percent.”

---

# 9. How we will interpret the possible outcomes

## ACI final beats model-only

This would support the narrow conclusion:

> Under the frozen model, prompts, generation settings, and IFEval verifier, the complete Phase 10 route improved objectively verifiable instruction adherence.

It would not prove truthfulness, reasoning superiority, alignment, or general intelligence.

## ACI final loses, while ACI candidate matches model-only

The loss is primarily downstream:

```text
post-generation governance or reconstruction
```

That would point toward over-qualification, abstention, or format-destructive final rendering.

## ACI candidate loses before final governance

The loss begins in:

```text
ACI model-facing context or generation configuration
```

That would not be an RF-007 rendering defect.

## ACI candidate improves, but ACI final gives the gain back

That would be especially revealing:

> ACI’s context helped the model follow instructions, but the governed voice could not preserve the successful candidate.

## Strict falls but loose remains stable

That usually suggests outer scaffolding, extra first or last lines, Markdown markers, or qualification rather than complete loss of the requested content.

## ACI scores badly on factual prompts but better on creative and structural prompts

That may reflect the collision between:

```text
IFEval rewards answer production
```

and:

```text
ACI withholds unsupported epistemic expression
```

IFEval generally verifies formal output constraints rather than the truth of the substantive answer. A low result therefore cannot automatically be labeled architectural failure. It may expose a real tradeoff between exact compliance and epistemic restraint.

---

# 10. Relaxed governance posture

We are not writing a governed handoff package for little ACI’s school trip. 😂

There will be:

* no ACI repository mutation;
* no project contract;
* no acceptance seal;
* no root checksum update;
* no Phase 11 authority transition;
* no repair family opened during the run;
* no benchmark-driven patching;
* no public superiority claim.

There will still be one small benchmark card, exact source identities, raw outputs, and a resumable ledger.

That is not constitutional litigation.

That is simply the minimum structure required to know what actually happened.

---

# 11. Optional second round: IFBench

Only after IFEval is complete and the first report is frozen should we consider:

```text
ACI-PUBLIC-BENCHMARK-002
IFBench OOD Single-Turn
```

IFBench adds **58 new out-of-distribution verifiable constraint types** and publishes corresponding verifiers. Its optional two-turn mode deliberately separates the base prompt and later constraint; we will exclude that because it crosses toward continuity semantics. ([GitHub][4])

Single-turn IFBench asks whether Phase 10 can generalize to unfamiliar constraint forms.

Multi-turn IFBench waits.

---

# Step 0 — Run this read-only preflight

This command writes only to the new external benchmark directory:

```bash
set -euo pipefail

ACI_ROOT="<PRIVATE_ACI_SOURCE_REPOSITORY>"
BENCH_ROOT="$HOME/Documents/ACI Benchmarks/ACI-PUBLIC-BENCHMARK-001-IFEVAL"
GIT="$HOME/.cache/codex-runtimes/codex-primary-runtime/dependencies/bin/git"
PYTHON="$HOME/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3"
PHASE10_SEAL="41c95e422e71530c8e003484d04a1cf332c47fa6"

mkdir -p "$BENCH_ROOT"

{
  echo "=== UTC ==="
  date -u +"%Y-%m-%dT%H:%M:%SZ"
  echo

  echo "=== ACI SOURCE ==="
  printf 'root=%s\n' "$ACI_ROOT"
  printf 'head=%s\n' "$("$GIT" -C "$ACI_ROOT" rev-parse HEAD)"
  printf 'branch=%s\n' "$("$GIT" -C "$ACI_ROOT" branch --show-current)"
  echo "status:"
  "$GIT" -C "$ACI_ROOT" status --short --branch
  echo

  echo "=== PHASE 10 SEAL ==="
  if "$GIT" -C "$ACI_ROOT" cat-file -e "${PHASE10_SEAL}^{commit}" 2>/dev/null; then
    echo "phase10_seal_present=YES"
    printf 'phase10_seal=%s\n' "$("$GIT" -C "$ACI_ROOT" rev-parse "$PHASE10_SEAL")"
  else
    echo "phase10_seal_present=NO"
  fi
  echo

  echo "=== TOOLCHAIN ==="
  "$GIT" --version
  "$PYTHON" --version
  echo

  echo "=== ACI ENTRYPOINT ==="
  if command -v aci_ask >/dev/null 2>&1; then
    printf 'aci_ask=%s\n' "$(command -v aci_ask)"
  else
    echo "aci_ask=NOT_FOUND_IN_SHELL_PATH"
  fi
  echo

  echo "=== OLLAMA ==="
  if command -v ollama >/dev/null 2>&1; then
    ollama --version
    echo
    echo "installed models:"
    ollama list
    echo
    echo "api tags:"
    if ! curl -fsS http://127.0.0.1:11434/api/tags; then
      echo
      echo "OLLAMA_API_NOT_REACHABLE"
    fi
  else
    echo "ollama=NOT_FOUND"
  fi
  echo
} | tee "$BENCH_ROOT/PREFLIGHT.txt"

echo
echo "Preflight written to:"
echo "$BENCH_ROOT/PREFLIGHT.txt"
```

Paste the contents of `PREFLIGHT.txt` next. Then we will create the independent Phase 10 snapshot and make the three-case smoke runner—one small, visible step at a time.

[1]: https://huggingface.co/datasets/google/IFEval "google/IFEval · Datasets at Hugging Face"
[2]: https://github.com/google-research/google-research/tree/master/instruction_following_eval "google-research/instruction_following_eval at master · google-research/google-research · GitHub"
[3]: https://docs.ollama.com/modelfile?utm_source=chatgpt.com "Modelfile Reference"
[4]: https://github.com/allenai/IFBench "GitHub - allenai/IFBench · GitHub"
