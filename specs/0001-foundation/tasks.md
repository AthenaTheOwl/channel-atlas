# Spec 0001 — Foundation tasks

Ordered task list for the first 2-3 PRs after the scaffold.

## PR 1 — schemas plus EDGAR adapter skeleton

- [ ] Add `pyproject.toml` declaring the `channel-atlas` package and
      its CLI entry point.
- [ ] Add `src/channel_atlas/__init__.py` with `__version__`.
- [ ] Add `schemas/spv_record.schema.json` matching R-CAT-002.
- [ ] Add `schemas/counterparty_edge.schema.json` matching R-CAT-003.
- [ ] Add `schemas/manifest.schema.json` for the per-source manifest.
- [ ] Add `src/channel_atlas/extract/edgar.py` with a fetch-and-cache
      function plus a stub `extract_8k_material_definitive` parser.
- [ ] Add one fixture filing at
      `tests/fixtures/edgar/0001045810-25-000123.html` (a real public
      filing checked in).
- [ ] Add `tests/test_edgar_extract.py` asserting the parser returns
      a non-empty record list against the fixture.
- [ ] Add `decisions/DEC-CAT-001-evidence-rubric.md`.

## PR 2 — graph builder plus citation audit gate

- [ ] Add `src/channel_atlas/graph/build.py` taking a list of records
      and producing a validated graph.
- [ ] Add `data/aliases.yaml` with seed entity aliases (Microsoft,
      Apollo, Blackstone, Brookfield, KKR, Carlyle, Meta, Amazon,
      Google, Oracle).
- [ ] Add `eval/citation_faithfulness.py` running R-CAT-004.
- [ ] Add `scripts/voice_lint.py` with the banned-term list.
- [ ] Wire `pytest` to exercise the graph builder against the EDGAR
      fixture record set.

## PR 3 — LP / UCC adapters plus first report skeleton

- [ ] Add `src/channel_atlas/extract/lp_disclosure.py` with a CalPERS
      adapter.
- [ ] Add `src/channel_atlas/extract/ucc.py` with a Delaware lookup.
- [ ] Add `src/channel_atlas/report/render.py` and one templated
      narrative section.
- [ ] Add `reports/2026-Q3-spv-counterparty.md` as a skeleton (no
      live data yet, all sections present, voice_lint clean).
- [ ] Add `docs/dev/running-the-pipeline.md` covering the operator
      CLI invocation order.
