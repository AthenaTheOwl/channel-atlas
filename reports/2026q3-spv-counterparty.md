# ChannelAtlas SPV counterparty graph - 2026q3

Fixture-backed graph with 5 SPVs and 10 financing edges.
Total disclosed fixture commitments: 13,865,000,000 USD.

## SPVs

### Meridian Compute Trust LLC

- jurisdiction: Delaware
- sponsor: Kestrel Infrastructure Partners
- purpose: Finance shell capacity leases for AI training campuses
- source: https://www.sec.gov/Archives/edgar/data/0000000000/fixture-meridian.htm

### Blue Mesa Accelerator Funding DAC

- jurisdiction: Ireland
- sponsor: Stonebridge Digital Credit
- purpose: Hold secured notes backed by accelerator purchase agreements
- source: https://www.sec.gov/Archives/edgar/data/0000000000/fixture-blue-mesa.htm

### Cascadia Data Center JV LP

- jurisdiction: Delaware
- sponsor: Ridgewater Infrastructure
- purpose: Fund build to suit data center shells for inference workloads
- source: https://www.sec.gov/Archives/edgar/data/0000000000/fixture-cascadia.htm

### LumenPeak AI Lease Trust

- jurisdiction: Cayman Islands
- sponsor: Harborlight Asset Management
- purpose: Acquire lease receivables from liquid cooled GPU clusters
- source: https://www.sec.gov/Archives/edgar/data/0000000000/fixture-lumenpeak.htm

### Silverrail Compute Finance LLC

- jurisdiction: Delaware
- sponsor: Tanager Private Credit
- purpose: Provide term loans secured by AI colocation contracts
- source: https://www.sec.gov/Archives/edgar/data/0000000000/fixture-silverrail.htm

## edges

- Kestrel Infrastructure Partners -> Meridian Compute Trust LLC: 2,100,000,000 USD (sponsor_commitment, https://www.sec.gov/Archives/edgar/data/0000000000/fixture-meridian.htm)
- Meridian Compute Trust LLC -> Aurora Model Systems: 1,700,000,000 USD (capacity_lease, https://www.sec.gov/Archives/edgar/data/0000000000/fixture-meridian.htm)
- Stonebridge Digital Credit -> Blue Mesa Accelerator Funding DAC: 1,450,000,000 USD (note_purchase, https://www.sec.gov/Archives/edgar/data/0000000000/fixture-blue-mesa.htm)
- Blue Mesa Accelerator Funding DAC -> Vantage Cloud Services: 1,325,000,000 USD (gpu_lease, https://www.sec.gov/Archives/edgar/data/0000000000/fixture-blue-mesa.htm)
- Ridgewater Infrastructure -> Cascadia Data Center JV LP: 1,800,000,000 USD (equity_commitment, https://www.sec.gov/Archives/edgar/data/0000000000/fixture-cascadia.htm)
- Cascadia Data Center JV LP -> Cedar River Compute: 1,550,000,000 USD (built_to_suit_lease, https://www.sec.gov/Archives/edgar/data/0000000000/fixture-cascadia.htm)
- Harborlight Asset Management -> LumenPeak AI Lease Trust: 950,000,000 USD (warehouse_facility, https://www.sec.gov/Archives/edgar/data/0000000000/fixture-lumenpeak.htm)
- LumenPeak AI Lease Trust -> Northstar Inference Labs: 825,000,000 USD (receivable_purchase, https://www.sec.gov/Archives/edgar/data/0000000000/fixture-lumenpeak.htm)
- Tanager Private Credit -> Silverrail Compute Finance LLC: 1,175,000,000 USD (term_loan, https://www.sec.gov/Archives/edgar/data/0000000000/fixture-silverrail.htm)
- Silverrail Compute Finance LLC -> Eastgate Cloud Operations: 990,000,000 USD (colocation_financing, https://www.sec.gov/Archives/edgar/data/0000000000/fixture-silverrail.htm)

## methodology

Each node and edge must cite at least one public filing URL. v0.1 uses a checked-in fixture ledger and deterministic graph build.
