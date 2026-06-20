# requirements - 0002-design

## scope

v0.1 ships one fixture-backed SPV counterparty graph and markdown memo.
The goal is cited graph output, not live EDGAR coverage.

## requirements

- R-CAT-013: `python -m channel_atlas build --quarter 2026q2` writes
  SPV records, counterparty edges, graph JSON, and a markdown report.
- R-CAT-014: Every SPV and edge row carries at least one public filing URL.
- R-CAT-015: The graph build is deterministic for the fixture input.
- R-CAT-016: `scripts/validate_schemas.py` validates all committed rows.
- R-CAT-017: `scripts/check_citation_faithfulness.py` fails on missing citations.

