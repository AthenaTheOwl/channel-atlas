# channel-atlas

A sponsor commits $2.4B to a Delaware LLC. The LLC signs a build-to-suit lease for a
data-center campus. None of it lands on the sponsor's balance sheet, and the four hops
from check to GPU sit in four separate filings. channel-atlas wires them into one graph.

## What it does

The financing that builds AI infrastructure mostly does not show up where you'd look
for it. It moves through SPVs, joint ventures, private credit, build-to-suit leases,
and note purchases — structures designed so the spend stays off the sponsor's books and
the exposure lands on an entity nobody has a name for yet. Reported capex understates
the real number by exactly the amount that took the off-balance-sheet route, and the
disclosures that would close the gap are scattered one per 8-K.

channel-atlas reads those disclosures into a counterparty graph: who funded which
vehicle, which campus or GPU fleet the money backs, and how much exposure piles up on
each receiving entity. Every node and every edge has to cite a source filing or it does
not enter the graph. v0.1 ships one quarter as a checked-in fixture ledger — six
entities, four financing edges, $7.05B disclosed. The model and the citation gate are
the point; the data adapter is deliberately small.

## Try it

One command, offline, no keys. It reads the committed graph and prints the ranked view:

```bash
python -m channel_atlas show
```

```
channel-atlas - AI-infra SPV financing graph (2026q2)

6 entities | 2 SPVs | 2 sponsors | 4 financing edges | $7.05B disclosed

financing edges, ranked by commitment:

   #     amount  type                  flow
  --  ---------  --------------------  ----------------------------------------
   1     $2.40B  sponsor_commitment    Apollo Infrastructure Credit -> Northlake AI Infrastructure LLC
   2     $1.80B  built_to_suit_lease   Northlake AI Infrastructure LLC -> CloudNorth Compute
   3     $1.60B  note_purchase         Brookfield Infrastructure -> Helios GPU Funding DAC
   4     $1.25B  gpu_lease             Helios GPU Funding DAC -> Frontier Model Hosting Co.

inbound exposure, ranked by receiving entity:

     $2.40B  Northlake AI Infrastructure LLC
     $1.80B  CloudNorth Compute
     $1.60B  Helios GPU Funding DAC
     $1.25B  Frontier Model Hosting Co.

headline: Northlake AI Infrastructure LLC is the single largest financing sink at $2.40B (34% of disclosed commitments). every edge cites a source filing.
```

Ranked by commitment, biggest check first, then the same money summed by where it lands.
The largest sink is where concentration risk would show up first.

## Live demo

Browse the same graph interactively:

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

The app reads `reports/2026q2-spv-counterparty.graph.json` directly (no network, no
secrets): ranked financing edges, inbound exposure by receiving entity, a
relationship-type filter, and a headline callout.

Deploy on Streamlit Cloud: repo `AthenaTheOwl/channel-atlas`, branch `main`, main file
`streamlit_app.py`.

<!-- live-url: https://share.streamlit.io/... (fill in after first deploy) -->

## How it connects

channel-atlas is the financing side of the same AI-infra demand curve the rest of the
cluster traces from other angles:

- [grid-silicon](https://github.com/AthenaTheOwl/grid-silicon) — scores how much of an
  announced datacenter load actually got energized, the power-side gap under the money.
- [interconnect-alpha](https://github.com/AthenaTheOwl/interconnect-alpha) — the
  survival model: probability a queued project ever reaches commercial operation.
- [chip-supply-chain-map](https://github.com/AthenaTheOwl/chip-supply-chain-map) /
  [fab-risk-radar](https://github.com/AthenaTheOwl/fab-risk-radar) — the silicon end of
  the GPU fleets this financing is collateralized against.

## Run it in full

```bash
# build the graph + report from the checked-in fixture ledger
python -m channel_atlas build --quarter 2026q2

# print a ranked, readable view of the committed graph (read-only, offline)
python -m channel_atlas show

# re-validate that every node and edge cites a source filing
python -m channel_atlas validate
```

`build` reads `data/fixtures/2026q2-spv-ledger.csv` and writes the SPV records,
counterparty edges, graph JSON, and markdown report. `validate` exits zero only when
every node and edge carries a filing citation.

## Layout

```
src/channel_atlas/    loader, graph build, report, show, validation, cli
data/fixtures/        the committed SPV ledger v0.1 ships
reports/              2026q2 graph JSON + markdown report
schemas/  specs/  decisions/  docs/  tests/
```

## License

MIT. See [LICENSE](LICENSE).
