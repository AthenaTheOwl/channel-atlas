from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

from src.channel_atlas.loader import load_records
from src.channel_atlas.show import counterparty_exposure, load_graph, rank_edges, render_show
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


def test_show_ranks_edges_descending() -> None:
    graph = load_graph()
    edges = rank_edges(graph)
    amounts = [e["commitment_amount"] for e in edges]
    assert amounts == sorted(amounts, reverse=True)
    assert amounts[0] == 2400000000.0


def test_show_exposure_concentration() -> None:
    exposure = counterparty_exposure(load_graph())
    assert exposure[0][0] == "Northlake AI Infrastructure LLC"
    assert exposure[0][1] == 2400000000.0


def test_show_renders_headline_and_table() -> None:
    out = render_show()
    assert "channel-atlas" in out
    assert "financing edges, ranked by commitment" in out
    assert "headline:" in out
    assert "$7.05B" in out


def test_citation_gate_rejects_missing_and_urlless_filings(tmp_path: Path) -> None:
    # Pins all()-not-any() plus the isinstance/bool(filings) guard in has_citation:
    # a row with no source_filings and a row whose filing lacks a url must both fail.
    missing = tmp_path / "missing.jsonl"
    missing.write_text(json.dumps({"id": "e1"}) + "\n", encoding="utf-8")
    with pytest.raises(ValueError):
        validate_citations([missing])

    empty = tmp_path / "empty.jsonl"
    empty.write_text(json.dumps({"id": "e2", "source_filings": []}) + "\n", encoding="utf-8")
    with pytest.raises(ValueError):
        validate_citations([empty])

    no_url = tmp_path / "no_url.jsonl"
    no_url.write_text(
        json.dumps({"id": "e3", "source_filings": [{"accession_number": "x"}]}) + "\n",
        encoding="utf-8",
    )
    with pytest.raises(ValueError):
        validate_citations([no_url])

    # One cited, one uncited: all() must reject; any() would wrongly accept.
    mixed = tmp_path / "mixed.jsonl"
    mixed.write_text(
        json.dumps(
            {"id": "e4", "source_filings": [{"url": "http://x"}, {"accession_number": "y"}]}
        )
        + "\n",
        encoding="utf-8",
    )
    with pytest.raises(ValueError):
        validate_citations([mixed])


def test_exposure_accumulates_multiple_inbound_edges() -> None:
    # Two edges into the same target must sum, not overwrite. The 2026q2 fixture
    # has one edge per target, so only a hand-built graph exercises the += path.
    graph = {
        "edges": [
            {"target": "Acme", "commitment_amount": 100.0},
            {"target": "Acme", "commitment_amount": 250.0},
            {"target": "Other", "commitment_amount": 50.0},
        ]
    }
    exposure = dict(counterparty_exposure(graph))
    assert exposure["Acme"] == 350.0
    assert exposure["Other"] == 50.0


def test_graph_node_kind_split() -> None:
    # Lock the kind classification: mislabeling SPV nodes as sponsor (or vice versa)
    # must fail. No other test reads node kinds.
    graph = json.loads((ROOT / "reports" / "2026q2-spv-counterparty.graph.json").read_text())
    kinds = [node["kind"] for node in graph["nodes"]]
    assert kinds.count("spv") == 2
    assert kinds.count("sponsor") == 2
    assert kinds.count("counterparty") == 2


def test_cli_show_runs_offline() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "channel_atlas", "show"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    assert "headline:" in result.stdout
    assert result.returncode == 0

