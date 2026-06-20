from __future__ import annotations

import json
from pathlib import Path

from .models import CounterpartyEdge, SpvRecord


def write_jsonl(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, sort_keys=True) + "\n")


def write_json(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def render_report(path: Path, quarter: str, spvs: list[SpvRecord], edges: list[CounterpartyEdge]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    total = sum(edge.commitment_amount for edge in edges)
    lines = [
        f"# ChannelAtlas SPV counterparty graph - {quarter}",
        "",
        f"Fixture-backed graph with {len(spvs)} SPVs and {len(edges)} financing edges.",
        f"Total disclosed fixture commitments: {total:,.0f} USD.",
        "",
        "## SPVs",
        "",
    ]
    for spv in spvs:
        lines.extend(
            [
                f"### {spv.legal_name}",
                "",
                f"- jurisdiction: {spv.jurisdiction}",
                f"- sponsor: {spv.sponsoring_filer}",
                f"- purpose: {spv.purpose_text}",
                f"- source: {spv.source_filings[0].url}",
                "",
            ]
        )
    lines.extend(["## edges", ""])
    for edge in edges:
        lines.extend(
            [
                f"- {edge.from_entity} -> {edge.to_entity}: "
                f"{edge.commitment_amount:,.0f} {edge.commitment_currency} "
                f"({edge.relationship_type}, {edge.source_filings[0].url})"
            ]
        )
    lines.extend(
        [
            "",
            "## methodology",
            "",
            "Each node and edge must cite at least one public filing URL. v0.1 uses a checked-in fixture ledger and deterministic graph build.",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")

