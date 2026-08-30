# RF-002 Acceptance Record

## Verdict

**Implementation: PASS**

**Deterministic acceptance: PASS**

**Live three-turn acceptance: PASS**

## Identity

- Repair: `RF-002 Interactive Context and Governed Continuity Projection`
- Date: 2026-07-02
- Release: `ACI-EXP-OLLAMA-001-v0.1.4-20260702`
- Accepted core baseline: `ACI-MIN-v0.1.0-20260701-R1`
- Core runtime changes: none

## Deterministic Findings

The required three-turn Stability Token fixture proves:

- turn one sends no prior context;
- explicit candidate declaration creates one stable continuity record;
- turns two and three send only a typed governed projection;
- raw prior model prose is not replayed;
- the full prior prompt is not replayed;
- ArchitectureState identifiers and internal event records are not projected;
- candidate identity and content remain stable;
- grounding remains `0.0`;
- uncertainty remains `1.0`;
- authority remains `NONE`;
- achieved scale does not rise;
- allowed and prohibited uses are sent explicitly;
- instruction-shaped candidate content is quoted as untrusted data;
- projection item and character bounds are visible;
- omissions remain inspectable; and
- RF-001 continues to govern the whole current event and final prose.

## Verification

```text
Adapter experiment tests: 37 passed
Accepted core tests:       443 passed
Combined verification:     480 passed
Bytecode compilation:      PASS
```

## Live Findings

The three-turn campaign ran against `llama3.2:latest`, digest
`a80c4f17acd55265feec403c7aef86be0c25983ab279d83f3bcd3abbcb5b8b72`,
quantized `Q4_K_M`.

| Turn | Projection | Prompt tokens | Generated tokens | Result |
|---|---:|---:|---:|---|
| 1 | 0 records | 86 | 333 | committed |
| 2 | 1 record | 346 | 263 | committed |
| 3 | 1 record | 349 | 115 | committed |

All formal assertions passed:

- cycle and audit status committed on every turn;
- audit counts accumulated as one, two, and three;
- raw chat history was never replayed;
- the same record ID and exact candidate content returned on turns two and
  three;
- the record remained candidate-only, grounding `0.0`, uncertainty `1.0`,
  authority `NONE`, and scale `CLAIM`;
- final outputs retained grounding `0.0`, uncertainty `1.0`, and authority
  `NONE`; and
- turn three's model response reproduced the projection's allowed and
  prohibited uses.

The turn-two model response partially reinterpreted Stability Token as a
cryptocurrency and assigned an unsupported internal grounding value of
`0.500`. RF-001 contained that overreach: it remained raw candidate text, did
not alter the continuity record, and did not enter final governed output.

This establishes narrow governed re-entry, not general semantic fidelity or
governed functional continuity.

## Witnesses

- `ACI_OLLAMA_20260702T224256430512Z_001.json`
- `ACI_OLLAMA_20260702T224335862628Z_002.json`
- `ACI_OLLAMA_20260702T224416417273Z_003.json`

SHA-256 values:

- `0871421721e2d580c99d9b2147689ad357133a2372883e6f2de71163c5ea968a`
- `a368dab8e2dd7d93322a2a97f750fa05e19b364a4989d1c7d37bd18ad24a665a`
- `01e03eecbf87f5a67cbf345504b2032c1a78b84e91ada9d96c4e2e74dcb6d1dc`

## Remaining Limits

- explicit named-candidate syntax only;
- exact-label retrieval only;
- no semantic entity resolution;
- no contradiction-aware record merge;
- no typed-evidence promotion path;
- no canonical memory-graph persistence;
- no cross-session continuity;
- no long-session compression; and
- no demonstration of governed functional continuity.

**Flame Line:** Continuity passed because the prior candidate returned with
its identity intact and its authority unchanged, even when the model tried to
reinterpret the form around it.
