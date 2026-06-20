# design - 0002-design

## shape

The v0.1 loop reads `data/fixtures/2026q2-spv-ledger.csv`, deduplicates
SPV records, emits cited edge rows, builds graph JSON, and renders one
markdown memo.

## non-goals

- live EDGAR fetch
- LP disclosure ingest
- UCC and registry search
- PDF output

