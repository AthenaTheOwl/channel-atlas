from __future__ import annotations

import csv
import subprocess
import sys
from pathlib import Path

from src.channel_atlas.loader import load_records
from src.channel_atlas.validation import read_jsonl

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "data" / "fixtures" / "2026q3-spv-ledger.csv"
SPV_PATH = ROOT / "data" / "spv_records" / "2026q3.jsonl"
EDGE_PATH = ROOT / "data" / "counterparty_edges" / "2026q3.jsonl"
GRAPH_PATH = ROOT / "reports" / "2026q3-spv-counterparty.graph.json"


def _build_q3() -> None:
    subprocess.run(
        [sys.executable, "-m", "channel_atlas", "build", "--quarter", "2026q3"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )


def test_2026q3_build_is_deterministic() -> None:
    _build_q3()
    paths = [SPV_PATH, EDGE_PATH, GRAPH_PATH]
    first = {path.relative_to(ROOT).as_posix(): path.read_bytes() for path in paths}

    _build_q3()
    second = {path.relative_to(ROOT).as_posix(): path.read_bytes() for path in paths}

    assert second == first


def test_2026q3_fixture_and_records_have_expected_shape() -> None:
    _build_q3()
    with FIXTURE.open(encoding="utf-8", newline="") as handle:
        fixture_rows = list(csv.DictReader(handle))
    spvs, edges = load_records(FIXTURE)
    spv_rows = read_jsonl(SPV_PATH)
    edge_rows = read_jsonl(EDGE_PATH)

    assert len(fixture_rows) == 10
    assert len(spvs) == 5
    assert len(edges) == 10
    assert len(spv_rows) == 5
    assert len(edge_rows) == 10
    assert all(row["source_url"] for row in fixture_rows)
    assert all(item.source_filings[0].url for item in spvs)
    assert all(item.source_filings[0].url for item in edges)


def test_cli_show_renders_2026q3() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "channel_atlas", "show", "--quarter", "2026q3"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )

    assert "channel-atlas" in result.stdout
    assert "2026q3" in result.stdout
    assert "headline:" in result.stdout


def test_cli_show_unknown_quarter_fails_cleanly() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "channel_atlas", "show", "--quarter", "2099q9"],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )

    assert result.returncode == 1
    assert "no graph" in result.stderr
    assert "reports/2099q9-spv-counterparty.graph.json" in result.stderr
