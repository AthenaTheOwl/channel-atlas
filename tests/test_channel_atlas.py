from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from src.channel_atlas.loader import load_records
from src.channel_atlas.validation import read_jsonl, validate_citations

ROOT = Path(__file__).resolve().parents[1]


def test_fixture_loads_spvs_and_edges() -> None:
    spvs, edges = load_records(ROOT / "data" / "fixtures" / "2026q2-spv-ledger.csv")
    assert len(spvs) == 2
    assert len(edges) == 4
    assert all(item.source_filings for item in spvs)
    assert all(item.source_filings for item in edges)


def test_cli_builds_graph_and_report() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "channel_atlas", "build", "--quarter", "2026q2"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    payload = json.loads(result.stdout)
    assert (ROOT / payload["graph_path"]).is_file()
    assert (ROOT / payload["report_path"]).is_file()
    validate_citations([ROOT / payload["spv_path"], ROOT / payload["edge_path"]])


def test_graph_has_cited_edges() -> None:
    graph = json.loads((ROOT / "reports" / "2026q2-spv-counterparty.graph.json").read_text())
    assert graph["nodes"]
    assert graph["edges"]
    assert all(edge["source_filings"] for edge in graph["edges"])


def test_outputs_are_jsonl() -> None:
    assert read_jsonl(ROOT / "data" / "counterparty_edges" / "2026q2.jsonl")

