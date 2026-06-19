# Spec 0001 — Foundation acceptance

## What "v0 done" means

Spec 0001 is closed when all of the following hold:

1. The three PRs in `tasks.md` are merged.
2. The package installs cleanly: `uv pip install -e .` (or
   `python -m pip install -e .`) succeeds on a fresh venv.
3. `python -m channel_atlas --help` prints the CLI surface.
4. The full local-gates suite passes against the checked-in fixtures.
5. A first skeleton report at
   `reports/2026-Q3-spv-counterparty.md` exists, passes voice_lint,
   and renders without error.

## Commands to run

```bash
uv pip install -e .[dev]
python -m channel_atlas --help

uv run pytest
python scripts/voice_lint.py
python eval/citation_faithfulness.py --graph data/spv_graph.json
python scripts/validate_schemas.py
```

## Gates

| Gate | Source | Blocks merge when |
|---|---|---|
| pytest | `tests/` | any test fails |
| voice_lint | `scripts/voice_lint.py` | any banned term in `reports/` or `README.md` |
| citation_faithfulness | `eval/citation_faithfulness.py` | any node or edge lacks `source_filings[]` |
| schema validation | `scripts/validate_schemas.py` | any record fails its JSON schema |

## What v0 explicitly does NOT include

- Live ingest on a cron. Operator runs the CLI by hand.
- Web frontend. Markdown plus Cytoscape JSON only.
- Estimation of undisclosed deal sizes.
- Equity-side or credit-rating commentary.
