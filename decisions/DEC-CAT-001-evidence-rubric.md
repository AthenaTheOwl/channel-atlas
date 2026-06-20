---
id: DEC-CAT-001-evidence-rubric
spec: specs/0002-design/
requirement: R-CAT-014
date: 2026-06-20
status: approved
reversible: true
decision: |
  Require every SPV node and counterparty edge to cite at least one public
  filing URL before it can enter the graph.
alternatives:
  - label: allow uncited seed rows
    rejected_because: |
      The graph would become a rumor ledger, which breaks the repo charter.
  - label: defer citation checks to report review
    rejected_because: |
      Missing citations should fail at data build time, before prose is written.
rationale: |
  Citation-bearing rows are easy to validate and let future adapters add source
  types without changing the graph contract.
evidence:
  - kind: spec
    ref: specs/0002-design/
rollback: |
  Replace the URL requirement with a richer source object only after every
  adapter emits the richer shape.
---

