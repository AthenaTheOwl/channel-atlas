from __future__ import annotations

import argparse
import json
from pathlib import Path

from .graph import build_graph
from .loader import load_records
from .report import render_report, write_json, write_jsonl
from .validation import validate_citations

ROOT = Path(__file__).resolve().parents[2]


def build(quarter: str) -> dict[str, Path]:
    spvs, edges = load_records(ROOT / "data" / "fixtures" / f"{quarter}-spv-ledger.csv")
    spv_path = ROOT / "data" / "spv_records" / f"{quarter}.jsonl"
    edge_path = ROOT / "data" / "counterparty_edges" / f"{quarter}.jsonl"
    graph_path = ROOT / "reports" / f"{quarter}-spv-counterparty.graph.json"
    report_path = ROOT / "reports" / f"{quarter}-spv-counterparty.md"
    write_jsonl(spv_path, [item.to_dict() for item in spvs])
    write_jsonl(edge_path, [item.to_dict() for item in edges])
    write_json(graph_path, build_graph(spvs, edges))
    render_report(report_path, quarter, spvs, edges)
    validate_citations([spv_path, edge_path])
    return {"spv_path": spv_path, "edge_path": edge_path, "graph_path": graph_path, "report_path": report_path}


def validate_all() -> None:
    paths = list((ROOT / "data" / "spv_records").glob("*.jsonl")) + list(
        (ROOT / "data" / "counterparty_edges").glob("*.jsonl")
    )
    validate_citations(paths)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="channel-atlas")
    sub = parser.add_subparsers(dest="command", required=True)
    build_cmd = sub.add_parser("build")
    build_cmd.add_argument("--quarter", default="2026q2")
    sub.add_parser("validate")
    args = parser.parse_args(argv)
    if args.command == "build":
        paths = build(args.quarter)
        print(json.dumps({key: value.relative_to(ROOT).as_posix() for key, value in paths.items()}, sort_keys=True))
        return 0
    validate_all()
    print("valid: graph")
    return 0

