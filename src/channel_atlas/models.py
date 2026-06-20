from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class SourceFiling:
    url: str
    accession_number: str
    cited_at: str

    def to_dict(self) -> dict[str, str]:
        return asdict(self)


@dataclass(frozen=True)
class SpvRecord:
    spv_id: str
    legal_name: str
    jurisdiction: str
    formation_date: str
    sponsoring_filer: str
    purpose_text: str
    source_filings: list[SourceFiling]

    def to_dict(self) -> dict[str, object]:
        payload = asdict(self)
        payload["source_filings"] = [item.to_dict() for item in self.source_filings]
        return payload


@dataclass(frozen=True)
class CounterpartyEdge:
    edge_id: str
    from_entity: str
    to_entity: str
    relationship_type: str
    commitment_amount: float
    commitment_currency: str
    disclosure_date: str
    source_filings: list[SourceFiling]

    def to_dict(self) -> dict[str, object]:
        payload = asdict(self)
        payload["source_filings"] = [item.to_dict() for item in self.source_filings]
        return payload

