# Minimal ACI Prototype v0.1

This directory is a curated public projection of the accepted Minimal ACI Prototype v0.1 archive.

## Identity

- Project component: Minimal ACI Prototype v0.1.
- Accepted archive: `ACI-MIN-v0.1.0-20260701-R1`.
- Role: the first accepted executable ACI baseline.
- Projection status: selected implementation, tests, examples, and acceptance-facing documentation from the accepted archive.

Minimal ACI v0.1 was designed to test foundational architectural boundaries rather than implement the full Phase 8 canon. Its principal surfaces include:

- typed symbolic structures;
- separation of evidence from coherence, memory, scale, and authority;
- governed review and decision records;
- immutable and transactional state transitions;
- finalized audit lifecycle;
- bounded coherence repair;
- an integrated governed cycle;
- explicit resistance to category collapse.

## Public Projection Notice

> This directory is a curated public projection of the accepted Minimal ACI v0.1 archive. Retained implementation, tests, examples, and acceptance-facing documentation preserve their authenticated source bytes. The original accepted README and selected internal governance records are preserved in private project provenance but are not reproduced as public bodies because they contain private-workspace references or internal development machinery not required to run or evaluate the accepted prototype.

## Quick Start

From the public repository root:

```bash
cd reference_implementations/minimal_aci_v0.1
python3.11 -m venv .venv
.venv/bin/python -m pip install "pytest>=8,<9"
.venv/bin/python -m pytest -p no:cacheprovider
.venv/bin/python -m examples.run_minimal_cycle
```

## Public Documentation

- [Final acceptance record](docs/FINAL_ACCEPTANCE_RECORD_v0.1.md)
- [Version notes](docs/VERSION_NOTES_v0.1.md)
- [Final coherence review](docs/FINAL_COHERENCE_REVIEW.md)
- [Canon-to-code status](docs/CANON_TO_CODE_STATUS.md)

The accepted private archive contains additional development and governance records that are not part of this curated projection.

## Authority Boundary

This generated README is public navigation, not canonical architecture or an acceptance source. It does not replace the accepted archive, alter Minimal ACI v0.1 acceptance, or grant new implementation authority. Source provenance remains bound through the public provenance and projection manifests.
