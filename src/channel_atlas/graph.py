from __future__ import annotations

from .models import CounterpartyEdge, SpvRecord


def build_graph(spvs: list[SpvRecord], edges: list[CounterpartyEdge]) -> dict[str, object]:
    nodes: dict[str, dict[str, object]] = {}
    for spv in spvs:
        nodes[spv.legal_name] = {
            "id": spv.legal_name,
            "kind": "spv",
            "jurisdiction": spv.jurisdiction,
            "data_status": spv.data_status,
            "source_filings": [item.to_dict() for item in spv.source_filings],
        }
        nodes.setdefault(
            spv.sponsoring_filer,
            {"id": spv.sponsoring_filer, "kind": "sponsor", "source_filings": []},
        )
    graph_edges = []
    for edge in edges:
        nodes.setdefault(edge.from_entity, {"id": edge.from_entity, "kind": "counterparty"})
        nodes.setdefault(edge.to_entity, {"id": edge.to_entity, "kind": "counterparty"})
        graph_edges.append(
            {
                "id": edge.edge_id,
                "source": edge.from_entity,
                "target": edge.to_entity,
                "relationship_type": edge.relationship_type,
                "commitment_amount": edge.commitment_amount,
                "commitment_currency": edge.commitment_currency,
                "data_status": edge.data_status,
                "source_filings": [item.to_dict() for item in edge.source_filings],
            }
        )
    statuses = {spv.data_status for spv in spvs} | {edge.data_status for edge in edges}
    return {
        "data_status": statuses.pop() if len(statuses) == 1 else "mixed",
        "nodes": sorted(nodes.values(), key=lambda item: str(item["id"])),
        "edges": graph_edges,
    }

