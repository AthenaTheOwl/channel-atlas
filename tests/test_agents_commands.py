from __future__ import annotations

import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FENCE = re.compile(r"```(?:bash|sh)\n(.*?)```", re.S)
SCRIPT = re.compile(r"^\s*(?:uv run )?python3? (\S+\.py)\b", re.M)


def _agents_scripts() -> list[str]:
    text = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
    return [path for block in FENCE.findall(text) for path in SCRIPT.findall(block)]


def test_every_script_command_in_agents_md_exists() -> None:
    scripts = _agents_scripts()
    assert "scripts/voice_lint.py" in scripts
    missing = [path for path in scripts if not (ROOT / path).is_file()]
    assert missing == []


def test_every_agents_md_script_exits_zero() -> None:
    for path in _agents_scripts():
        completed = subprocess.run(
            [sys.executable, path], cwd=ROOT, text=True, capture_output=True, check=False
        )
        assert completed.returncode == 0, (path, completed.stderr)


def test_voice_lint_fails_on_a_banned_term(tmp_path: Path) -> None:
    shutil.copy(ROOT / "README.md", tmp_path / "README.md")
    (tmp_path / "reports").mkdir()
    (tmp_path / "reports" / "q.md").write_text("A seamless SPV.\nPlain line.\n", encoding="utf-8")
    completed = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "voice_lint.py"), str(tmp_path)],
        text=True,
        capture_output=True,
        check=False,
    )
    assert completed.returncode == 1
    assert "reports/q.md:1: banned term: seamless" in completed.stderr
