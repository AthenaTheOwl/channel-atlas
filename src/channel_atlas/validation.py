from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def has_citation(row: dict[str, Any]) -> bool:
    filings = row.get("source_filings")
    return isinstance(filings, list) and bool(filings) and all(item.get("url") for item in filings)


def validate_citations(paths: list[Path]) -> None:
    for path in paths:
        for row in read_jsonl(path):
            if not has_citation(row):
                raise ValueError(f"{path}: row lacks source filing: {row}")

