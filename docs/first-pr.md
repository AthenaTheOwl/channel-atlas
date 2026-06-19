# First PR after the scaffold

This document names the literal first PR after the repo scaffold lands.
The goal: land the package skeleton, the two schemas, and one working
EDGAR adapter against a single checked-in fixture filing. Nothing more.

## Scope

Branch name: `feat/0001-edgar-schemas`

### Files added

- `pyproject.toml` — declares the `channel-atlas` package, the CLI
  entry point `channel-atlas = "channel_atlas.cli:main"`, and dev
  dependencies (pytest, jsonschema, beautifulsoup4, lxml, click).
- `src/channel_atlas/__init__.py` — sets `__version__ = "0.0.1"`.
- `src/channel_atlas/cli.py` — Click app with one no-op command
  `version`.
- `schemas/spv_record.schema.json` — matches R-CAT-002.
- `schemas/counterparty_edge.schema.json` — matches R-CAT-003.
- `schemas/manifest.schema.json` — per-source ingest manifest.
- `src/channel_atlas/extract/__init__.py`
- `src/channel_atlas/extract/edgar.py` — `fetch_filing(accession_id)`
  function that reads from `data/cache/edgar/` if present (the only
  mode supported in this PR), plus
  `extract_8k_material_definitive(html)` that returns a list of
  candidate SPV-record dicts.
- `tests/fixtures/edgar/0001045810-25-000123/document.html` — one
  real Microsoft 8-K filing checked in for offline testing.
- `tests/test_edgar_extract.py` — asserts that the parser produces at
  least one record against the fixture and that each record validates
  against `schemas/spv_record.schema.json`.
- `decisions/DEC-CAT-001-evidence-rubric.md` — names what counts as
  a primary source and the precedence order.

### Files NOT touched

- `reports/` — empty until PR 3.
- `eval/` — empty until PR 2.
- `src/channel_atlas/graph/` — empty until PR 2.

## Verification

```bash
uv pip install -e .[dev]
python -m channel_atlas version
# expect: channel-atlas 0.0.1

uv run pytest
# expect: tests/test_edgar_extract.py collects 2 tests, both pass

python -c "import json, jsonschema; \
  s=json.load(open('schemas/spv_record.schema.json')); \
  jsonschema.Draft202012Validator.check_schema(s); \
  print('spv_record schema OK')"
```

## Out of scope for this PR

- The graph builder (PR 2).
- LP / UCC / SPV-registry / ABS adapters (PR 3 and beyond).
- The voice_lint script (PR 2).
- Live EDGAR fetch — this PR reads from a checked-in fixture only.
- Any actual report content.
