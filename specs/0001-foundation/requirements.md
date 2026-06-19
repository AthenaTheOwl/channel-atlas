# Spec 0001 — Foundation requirements

The first spec for ChannelAtlas. Names the schemas, the ingest
surfaces, the graph model, the report shape, and the citation
discipline that every downstream PR has to honor.

## Requirements

- **R-CAT-001** — The repo MUST expose a `channel-atlas` Python
  package with a `__version__` string and a CLI entry point
  registered under that name.

- **R-CAT-002** — An SPV record MUST conform to
  `schemas/spv_record.schema.json` with fields: `spv_id`, `legal_name`,
  `jurisdiction`, `formation_date`, `sponsoring_filer`, `purpose_text`,
  `source_filings[]` (each with `url`, `accession_number`, `cited_at`).

- **R-CAT-003** — A counterparty edge MUST conform to
  `schemas/counterparty_edge.schema.json` with fields: `edge_id`,
  `from_entity`, `to_entity`, `relationship_type`, `commitment_amount`,
  `commitment_currency`, `disclosure_date`, `source_filings[]`.

- **R-CAT-004** — Every node and edge in the published graph MUST cite
  at least one public filing URL. A node without a citation fails the
  citation-faithfulness gate and blocks merge.

- **R-CAT-005** — The ingest layer MUST be split per source: EDGAR
  8-K / 10-K, LP disclosures, UCC-1 filings, SPV registries, ABS
  prospectuses. Each adapter lives under `src/channel_atlas/extract/`
  and writes raw artifacts under `data/raw/<source>/<accession_id>/`.

- **R-CAT-006** — The graph build step MUST be deterministic given the
  same input set. Re-running the build on identical inputs produces a
  byte-identical `data/spv_graph.json`.

- **R-CAT-007** — The report renderer MUST produce a single markdown
  file at `reports/<year>-Q<n>-spv-counterparty.md` plus a Cytoscape
  JSON sidecar at `reports/<year>-Q<n>-spv-counterparty.graph.json`.

- **R-CAT-008** — Voice gate: the report MUST pass `voice_lint`.
  Banned terms include "leverage", "seamless", "best-in-class",
  "synergy", "cutting-edge", "demonstrates" (used as filler).

- **R-CAT-009** — The first published report MUST cover the window
  2024-01 through 2026-06 and include at minimum: Apollo, Blackstone,
  Brookfield, KKR, Carlyle as sponsoring counterparties on the
  private-credit side; Microsoft, Meta, Amazon, Google, Oracle on the
  hyperscaler side.

- **R-CAT-010** — The repo MUST include a `decisions/` directory and a
  `DEC-CAT-001-evidence-rubric.md` entry that documents what counts as
  a primary source and the precedence order when sources conflict.

- **R-CAT-011** — All ingest scripts MUST cache raw documents under
  `data/cache/` (gitignored) and emit a manifest at
  `data/manifests/<source>-<run_id>.json` that lists every retrieved
  filing, its hash, and the retrieval timestamp.

- **R-CAT-012** — No live network access at gate time. All gates run
  against checked-in fixtures. Live ingest is a separate operator-run
  command.
