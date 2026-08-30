# RF-005 Live Acceptance Results

## Verdict

`PASS` - narrow observational acceptance

## Campaign

- ID: `ACI-EXP-OLLAMA-RF005-LIVE-001`
- Model: `llama3.1:8b`
- Digest: `46e0c10c039e019119339687c3c1757cc81b9da49709a3b3924863ba87ca666e`
- Frozen cases: `22`
- Completed cases: `22`
- RF-005 influence on live route: none

## Results

- Expected prompt routes matched: `22/22`
- Lexical triggers across all four target layers: `136`
- CGA routes: `25`
- Typed non-route decisions: `87`
- Trigger-accountability failures: `0`
- Non-route approval promotions: `0`
- Non-route claims that governance risk was absent: `0`
- Model identity mismatches: `0`
- Final committed audit failures: `0`
- Final authority-envelope failures: `0`

Repository verification after adding the live-observation wrapper:

- RF-005 tests: `41 passed`;
- complete adapter suite: `122 passed`; and
- accepted core plus adapter: `565 passed`.

## Important Observation

Model responses sometimes introduced governance-relevant content even when the
prompt did not require CGA. RF-005 recorded those response-level routes
separately rather than copying the prompt route across the event. Final outputs
were evaluated independently and did not inherit response routes invisibly.

## Narrow Meaning

This PASS means the experiment-layer evaluator preserved the frozen routing
distinctions and Non-Route Accountability under live local-model pressure.

It does not mean:

- the accepted parser is repaired;
- RF-005 is approved for default `aci_ask` integration;
- arbitrary routing is solved;
- the model understands governance;
- CGA should be weakened; or
- governed functional continuity has been achieved.

**Flame Line:** RF-005 passed live observation not because governance appeared
less often, but because every appearance and every deliberate non-route left a
traceable reason for the gate it reached.
