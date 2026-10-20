# ChannelAtlas SPV counterparty graph - 2026q2

> Illustrative synthetic fixture. Every sponsor, SPV, counterparty, amount and filing link here is invented; none describes a real transaction or firm.

Fixture-backed graph with 2 SPVs and 4 financing edges.
Total disclosed fixture commitments: 7,050,000,000 USD.

## SPVs

### Northlake AI Infrastructure LLC

- jurisdiction: Delaware
- sponsor: Fixture Sponsor Alpha Credit
- data status: synthetic
- purpose: Finance a data-center campus lease and GPU collateral pool
- source: https://www.sec.gov/Archives/edgar/data/0000000000/fixture-northlake.htm

### Helios GPU Funding DAC

- jurisdiction: Ireland
- sponsor: Fixture Sponsor Beta Infrastructure
- data status: synthetic
- purpose: Hold secured notes backed by accelerator leases
- source: https://www.sec.gov/Archives/edgar/data/0000000000/fixture-helios.htm

## edges

- Fixture Sponsor Alpha Credit -> Northlake AI Infrastructure LLC: 2,400,000,000 USD (sponsor_commitment, https://www.sec.gov/Archives/edgar/data/0000000000/fixture-northlake.htm)
- Northlake AI Infrastructure LLC -> CloudNorth Compute: 1,800,000,000 USD (built_to_suit_lease, https://www.sec.gov/Archives/edgar/data/0000000000/fixture-northlake.htm)
- Fixture Sponsor Beta Infrastructure -> Helios GPU Funding DAC: 1,600,000,000 USD (note_purchase, https://www.sec.gov/Archives/edgar/data/0000000000/fixture-helios.htm)
- Helios GPU Funding DAC -> Frontier Model Hosting Co.: 1,250,000,000 USD (gpu_lease, https://www.sec.gov/Archives/edgar/data/0000000000/fixture-helios.htm)

## methodology

Each node and edge must cite at least one public filing URL. v0.1 uses a checked-in fixture ledger and deterministic graph build.
