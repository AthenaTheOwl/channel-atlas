# acceptance - 0002-design

Accepted when:

- `python -m channel_atlas build --quarter 2026q2` writes all four artifacts.
- `python -m channel_atlas validate` passes.
- `python scripts/validate_schemas.py` passes.
- `python scripts/check_citation_faithfulness.py` passes.
- `python -m pytest tests/ -q` passes.

