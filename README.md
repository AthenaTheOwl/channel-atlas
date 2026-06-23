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


v0.1 shipped and runs end to end. The entry command `python -m src.channel_atlas build` runs. See `specs/0002-design/` for the v0.1 scope and `STATUS.md` (where present) for the current state and next-feature queue.

## How to run

```bash
# build the graph + report from the checked-in fixture ledger
python -m channel_atlas build --quarter 2026q2

# print a ranked, readable view of the committed graph (read-only, offline)
python -m channel_atlas show

# re-validate that every node and edge cites a source filing
python -m channel_atlas validate
```

`show` reads `reports/2026q2-spv-counterparty.graph.json` and prints the
financing edges ranked by commitment, inbound exposure by receiving
entity, and a one-line headline naming the largest financing sink.

## live demo

Browse the same graph interactively:

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

The app reads `reports/2026q2-spv-counterparty.graph.json` directly
(no network, no secrets): ranked financing edges, inbound exposure by
receiving entity, a relationship-type filter, and a headline callout.

Deploy on Streamlit Cloud: repo `AthenaTheOwl/channel-atlas`, branch
`main`, main file `streamlit_app.py`.

<!-- live-url: https://share.streamlit.io/... (fill in after first deploy) -->

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
