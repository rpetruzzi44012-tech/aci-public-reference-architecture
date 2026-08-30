# RF-005 Approval Record

## Decision

- Repair: `RF-005 Lexical Routing and Review-Path Precision`
- Date: 2026-07-04
- Status: `APPROVED FOR EXPERIMENTAL IMPLEMENTATION`
- Ownership boundary: staged option 4 only
- Accepted-core impact: none authorized
- Live acceptance: blocked until deterministic fixtures pass

## Approved Tightening

### Non-Route Accountability Invariant

When a protected reviewer is not invoked despite a lexical trigger, the
witness must preserve the trigger, span classification, non-route rationale,
uncertainty status, and rollback boundary. Non-invocation must never be treated
as approval, irrelevance by default, or evidence that governance risk was
absent.

## Approved Gates

Joseph approved:

1. exact RF-005 scope;
2. six governing invariants;
3. routing vocabulary and span model;
4. conservative uncertainty policy;
5. qualifier-to-span and qualifier-to-decision binding;
6. twelve deterministic test groups;
7. live protocol with `llama3.1:8b` frozen unless separately recorded;
8. separate false-positive and false-negative scoring;
9. staged option 4 only;
10. no accepted-core impact;
11. rollback boundary; and
12. narrow acceptance meaning.

## Prohibited Changes

This approval does not authorize modification of:

- `aci/parser.py`;
- CGA implementation or legitimacy rules;
- AlgorithmRegistry authority;
- accepted cycle review order;
- accepted structure construction; or
- any other Minimal ACI v0.1 core module.

## Required Sequence

```text
amend specification
  -> implement experimental evaluator
  -> pass deterministic fixtures
  -> review evidence
  -> only then begin live acceptance
```

**Flame Line:** A reviewer left unused must leave a record of why the gate did
not open, because silence at a protected boundary is a decision, not an
absence.
