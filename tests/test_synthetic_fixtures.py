from __future__ import annotations

import csv
import json
import re
import subprocess
import sys
from pathlib import Path

import pytest

from src.channel_atlas.loader import load_records
from src.channel_atlas.report import SYNTHETIC_NOTICE
from src.channel_atlas.show import render_show
from src.channel_atlas.validation import read_jsonl

ROOT = Path(__file__).resolve().parents[1]
QUARTERS = ("2026q2", "2026q3")
# Real firms that earlier fixtures and specs named as sponsors or research targets.
# The fixtures are invented and the specs use placeholders; no real firm may appear
# beside an invented deal and amount or as an uncited research target.
REAL_FIRMS = (
    "Apollo", "Blackstone", "Brookfield", "KKR", "Carlyle",
    "Microsoft", "Meta", "Amazon", "Google", "Oracle",
)


def _derived(quarter: str) -> list[Path]:
    return [
        ROOT / "data" / "spv_records" / f"{quarter}.jsonl",
        ROOT / "data" / "counterparty_edges" / f"{quarter}.jsonl",
        ROOT / "reports" / f"{quarter}-spv-counterparty.graph.json",
        ROOT / "reports" / f"{quarter}-spv-counterparty.md",
    ]


def _published(quarter: str) -> list[Path]:
    return [ROOT / "data" / "fixtures" / f"{quarter}-spv-ledger.csv", *_derived(quarter)]


@pytest.mark.parametrize("quarter", QUARTERS)
def test_no_real_firm_is_named_as_a_fixture_sponsor(quarter: str) -> None:
    for path in [*_published(quarter), ROOT / "README.md", ROOT / "streamlit_app.py"]:
        text = path.read_text(encoding="utf-8")
        for firm in REAL_FIRMS:
            assert firm not in text, f"{path.relative_to(ROOT)} names {firm}"


def test_specs_and_docs_name_no_real_firm_as_a_target() -> None:
    paths = sorted((ROOT / "specs").rglob("*.md")) + sorted((ROOT / "docs").rglob("*.md"))
    assert paths
    for path in paths:
        text = path.read_text(encoding="utf-8")
        for firm in REAL_FIRMS:
            assert re.search(rf"\b{firm}\b", text) is None, f"{path.relative_to(ROOT)} names {firm}"


@pytest.mark.parametrize("quarter", QUARTERS)
def test_every_fixture_row_and_derived_record_is_marked_synthetic(quarter: str) -> None:
    with (ROOT / "data" / "fixtures" / f"{quarter}-spv-ledger.csv").open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    assert rows and all(row["data_status"] == "synthetic" for row in rows)
    spv_path, edge_path, graph_path, report_path = _derived(quarter)
    assert all(row["data_status"] == "synthetic" for row in read_jsonl(spv_path))
    assert all(row["data_status"] == "synthetic" for row in read_jsonl(edge_path))
    graph = json.loads(graph_path.read_text(encoding="utf-8"))
    assert graph["data_status"] == "synthetic"
    assert all(edge["data_status"] == "synthetic" for edge in graph["edges"])
    assert SYNTHETIC_NOTICE in report_path.read_text(encoding="utf-8")
    assert "illustrative synthetic fixture" in render_show(graph_path, quarter)


def test_readme_says_the_data_is_illustrative_and_synthetic() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "Illustrative, synthetic data." in readme
    assert "data_status: synthetic" in readme


@pytest.mark.parametrize("status", ["", "real", "SYNTHETIC "])
def test_loader_refuses_a_row_without_a_known_status(tmp_path: Path, status: str) -> None:
    source = ROOT / "data" / "fixtures" / "2026q2-spv-ledger.csv"
    with source.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    rows[1]["data_status"] = status
    ledger = tmp_path / "ledger.csv"
    with ledger.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    with pytest.raises(ValueError, match=r"ledger.csv:3: data_status must be one of"):
        load_records(ledger)


def test_loader_refuses_a_ledger_without_the_column(tmp_path: Path) -> None:
    ledger = tmp_path / "ledger.csv"
    source = (ROOT / "data" / "fixtures" / "2026q2-spv-ledger.csv").read_text(encoding="utf-8")
    ledger.write_text(
        "\n".join(line.rsplit(",", 1)[0] for line in source.splitlines() if line) + "\n",
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="data_status"):
        load_records(ledger)


@pytest.mark.parametrize("quarter", QUARTERS)
def test_committed_outputs_match_the_build(quarter: str) -> None:
    # The derived files are regenerated with `python -m channel_atlas build`,
    # never hand-edited: a fresh build must leave them byte-identical.
    before = {path: path.read_bytes() for path in _derived(quarter)}
    subprocess.run(
        [sys.executable, "-m", "channel_atlas", "build", "--quarter", quarter],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    assert {path: path.read_bytes() for path in _derived(quarter)} == before
