"""Voice gate (R-CAT-008): fail when a banned term appears in the published prose.

Scope, per specs/0001-foundation/acceptance.md: README.md and every markdown
report under reports/. "demonstrates" used as filler is also on the R-CAT-008
list, but filler cannot be told apart from a literal use by a word match, so
it is left to review.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

BANNED_FAIL = (
    "best-in-class",
    "cutting-edge",
    "leverage",
    "seamless",
    "synergy",
)
_PATTERN = re.compile(r"\b(" + "|".join(re.escape(term) for term in BANNED_FAIL) + r")", re.IGNORECASE)


def scanned_files(root: Path = ROOT) -> list[Path]:
    readme = root / "README.md"
    return ([readme] if readme.is_file() else []) + sorted((root / "reports").rglob("*.md"))


def find_violations(root: Path = ROOT) -> list[str]:
    violations: list[str] = []
    for path in scanned_files(root):
        for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            for match in _PATTERN.finditer(line):
                violations.append(f"{path.relative_to(root).as_posix()}:{number}: banned term: {match.group(1).lower()}")
    return violations


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    root = Path(args[0]).resolve() if args else ROOT
    violations = find_violations(root)
    for violation in violations:
        print(violation, file=sys.stderr)
    if violations:
        return 1
    print(f"voice_lint OK ({len(scanned_files(root))} file(s))")
    return 0


if __name__ == "__main__":
    sys.exit(main())
