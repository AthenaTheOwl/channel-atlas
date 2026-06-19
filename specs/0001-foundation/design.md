# Spec 0001 — Foundation design

## Shape

A Python CLI plus a small set of source adapters, a deterministic
graph builder, a report renderer, and a citation-audit gate. The
artifact is a markdown report and a Cytoscape JSON file, regenerated
quarterly.

## Components

### Ingest adapters (`src/channel_atlas/extract/`)

One adapter per public-source family. Each adapter is independent and
writes raw documents plus a normalized record list.

- `edgar.py` — pulls 8-K / 10-K filings via the SEC EDGAR HTTP API,
  resolves Item 1.01 (Material Definitive Agreement) and Item 2.03
  (Off-Balance-Sheet Arrangement) sections, extracts SPV references
  and counterparty names.
- `lp_disclosure.py` — pulls LP allocation disclosures from state
  pension funds (CalPERS, NYCRS, Texas Teachers), CPP Investment
  Board, and university endowments. Parses PDF tables.
- `ucc.py` — queries Delaware and Cayman UCC-1 financing-statement
  registries by debtor name; returns secured-party records.
- `spv_registry.py` — Cayman Registry of Companies and Delaware
  Division of Corporations lookup by entity name.
- `abs_prospectus.py` — pulls ABS shelf filings (S-1, 424B) and
  extracts data-center-collateral disclosures.

Each adapter writes:

- `data/raw/<source>/<accession_id>/document.pdf` (or `.html`)
- `data/raw/<source>/<accession_id>/extracted.json`
- An entry in `data/manifests/<source>-<run_id>.json`

### Graph builder (`src/channel_atlas/graph/build.py`)

Takes the union of normalized records, runs entity-resolution (a
simple deterministic name-canonicalization plus a hand-curated alias
table at `data/aliases.yaml`), composes nodes and edges, validates
against the JSON schemas, writes `data/spv_graph.json`.

Determinism: sort all node and edge lists by id before writing.

### Renderer (`src/channel_atlas/report/render.py`)

Reads `data/spv_graph.json`, produces:

- `reports/<year>-Q<n>-spv-counterparty.md` (narrative + tables)
- `reports/<year>-Q<n>-spv-counterparty.graph.json` (Cytoscape format)

The narrative is templated. Every claim in the narrative cites the
source filing by URL via inline footnotes.

### Citation audit (`eval/citation_faithfulness.py`)

Walks every node and every edge in `data/spv_graph.json`, asserts
that `source_filings[]` is non-empty and that every URL resolves to a
real SEC accession or state-registry record format. Fails on the
first missing citation.

## Data model

```
Node (Entity)
  - entity_id (canonical slug)
  - legal_name
  - entity_type ∈ {sponsor, hyperscaler, spv, datacenter_campus, gpu_fleet}
  - jurisdiction
  - source_filings[]

Edge (CounterpartyRelationship)
  - edge_id
  - from_entity → to_entity
  - relationship_type ∈ {finances, owns, leases_to, secures, sponsors}
  - commitment_amount / currency
  - disclosure_date
  - source_filings[]
```

## Out of scope for spec 0001

- A web frontend. The graph file plus the markdown report is the v0
  surface.
- Live ingest scheduling. Operator runs the CLI quarterly.
- Estimation of undisclosed deal sizes. Public-filings-only.
