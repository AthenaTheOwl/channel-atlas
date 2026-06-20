from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.channel_atlas.validation import validate_citations  # noqa: E402


def main() -> int:
    paths = list((ROOT / "data" / "spv_records").glob("*.jsonl")) + list(
        (ROOT / "data" / "counterparty_edges").glob("*.jsonl")
    )
    validate_citations(paths)
    print("citation_faithfulness OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())

