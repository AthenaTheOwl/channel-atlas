from __future__ import annotations

import csv
from pathlib import Path

from .models import CounterpartyEdge, SourceFiling, SpvRecord


def load_records(path: Path) -> tuple[list[SpvRecord], list[CounterpartyEdge]]:
    spvs: dict[str, SpvRecord] = {}
    edges: list[CounterpartyEdge] = []
    with path.open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            filing = SourceFiling(
                url=row["source_url"],
                accession_number=row["accession_number"],
                cited_at=row["cited_at"],
            )
            spvs[row["spv_id"]] = SpvRecord(
                spv_id=row["spv_id"],
                legal_name=row["legal_name"],
                jurisdiction=row["jurisdiction"],
                formation_date=row["formation_date"],
                sponsoring_filer=row["sponsoring_filer"],
                purpose_text=row["purpose_text"],
                source_filings=[filing],
            )
            edges.append(
                CounterpartyEdge(
                    edge_id=row["edge_id"],
                    from_entity=row["from_entity"],
                    to_entity=row["to_entity"],
                    relationship_type=row["relationship_type"],
                    commitment_amount=float(row["commitment_amount"]),
                    commitment_currency=row["commitment_currency"],
                    disclosure_date=row["disclosure_date"],
                    source_filings=[filing],
                )
            )
    return sorted(spvs.values(), key=lambda item: item.spv_id), sorted(
        edges, key=lambda item: item.edge_id
    )

