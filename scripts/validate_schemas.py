from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read_jsonl(path: Path) -> list[object]:
    rows = []
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def main() -> int:
    try:
        import jsonschema
    except ImportError as exc:
        raise SystemExit("jsonschema is required") from exc
    spv_schema = json.loads((ROOT / "schemas" / "spv_record.schema.json").read_text(encoding="utf-8"))
    edge_schema = json.loads((ROOT / "schemas" / "counterparty_edge.schema.json").read_text(encoding="utf-8"))
    jsonschema.validators.validator_for(spv_schema).check_schema(spv_schema)
    jsonschema.validators.validator_for(edge_schema).check_schema(edge_schema)
    for path in (ROOT / "data" / "spv_records").glob("*.jsonl"):
        for row in read_jsonl(path):
            jsonschema.validate(row, spv_schema)
    for path in (ROOT / "data" / "counterparty_edges").glob("*.jsonl"):
        for row in read_jsonl(path):
            jsonschema.validate(row, edge_schema)
    print("validate_schemas OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())

