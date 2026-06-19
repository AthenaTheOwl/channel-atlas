# ChannelAtlas

Open catalog of hyperscaler off-balance-sheet AI-infra financing. A
structured database of every JV, SPV, private-credit, leasing,
build-to-suit, and sale-leaseback structure financing AI infrastructure
(Apollo, Blackstone, Brookfield, KKR, Carlyle), tied to the specific
data-center campuses and GPU fleets they back.

## What this is

Hyperscaler debt issuance hit 108B USD in 2025, 3.4x the prior average.
Anthropic financed TPUs via 35B USD of private credit. Reported 2026
capex figures understate true AI-infra spend by an off-balance-sheet
share that nobody has fused into a single counterparty graph.

ChannelAtlas is the place that fusion happens. The first artifact is a
public PDF report covering every disclosed AI-infra SPV / JV /
private-credit deal in 2024-2026, with a counterparty graph rendered in
Cytoscape, tied to the specific data-center campuses where the financing
lands.

Buyers: credit hedge funds, equity L/S desks, Fortune 500 CFOs
assessing supplier-concentration risk, sovereign wealth fund
infrastructure teams, S&P and Moody's analysts.

## Status

v0 scaffold. No implementation yet. This repo holds the README, the
license, the operating contract for AI agents, the first foundation
spec (requirements, design, tasks, acceptance), and the literal first PR
plan in `docs/first-pr.md`. The next merge lands the schema and the
ingest skeleton for one filer.

## How to run

Placeholder. The first runnable surface will land in the first PR after
this scaffold, described in `docs/first-pr.md`. The longer-term run
contract will land in spec `0002-*` once `0001-foundation` is closed
out.

Once implemented, the entry point will be something like:

```bash
uv run channel-atlas ingest --filer apollo --window 2024-01:2026-06
uv run channel-atlas render --graph data/spv_graph.json --out reports/
```

## Layout

```
channel-atlas/
  README.md                          # this file
  LICENSE                            # MIT
  AGENTS.md                          # operating contract for AI agents
  .gitignore
  specs/
    0001-foundation/
      requirements.md                # R-CAT-NNN requirements
      design.md                      # architecture sketch
      tasks.md                       # ordered task list for first 2-3 PRs
      acceptance.md                  # what v0 done means
  docs/
    first-pr.md                      # the literal first PR after scaffold
```

Downstream additions named by the foundation spec:

```
  src/channel_atlas/
    extract/edgar.py                 # citation-faithful 8-K / 10-K extraction
    extract/lp_disclosure.py         # state pension / CalPERS / CPP LP filings
    extract/ucc.py                   # UCC-1 financing statements
    extract/spv_registry.py          # Cayman / Delaware SPV lookups
    extract/abs_prospectus.py        # ABS shelf filings
    graph/build.py                   # counterparty graph build
    graph/cytoscape_export.py        # render-ready JSON
    report/render.py                 # markdown / PDF report
  schemas/
    spv_record.schema.json
    counterparty_edge.schema.json
  data/
    raw/                             # gitignored
    cache/                           # gitignored
    spv_graph_2024_2026.json         # checked-in artifact for the first report
  reports/
    2026-Q3-spv-counterparty.md      # the first published report
  eval/
    citation_faithfulness.py         # gate: every edge has a SEC / filing URL
  decisions/
    DEC-CAT-001-evidence-rubric.md
```

## Voice and gates

See `AGENTS.md`. Plain assertions. No "leverage", "demonstrates",
"synergy", "seamless", "cutting-edge", "best-in-class". No antithetical
reversals as a structural device. Every counterparty edge cites the
source filing.

## License

MIT. See [LICENSE](LICENSE).
