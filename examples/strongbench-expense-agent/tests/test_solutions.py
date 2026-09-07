"""The reference solutions are course deliverables, so CI runs them.

A reference solution that no longer runs is worse than no reference solution:
the learner assumes their environment is broken.
"""

import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
SOLUTIONS = sorted(path.name for path in (ROOT / "solutions").glob("lab_*.py"))


def test_all_four_labs_have_a_reference_solution():
    assert len(SOLUTIONS) == 4, SOLUTIONS


@pytest.mark.parametrize("script", SOLUTIONS)
def test_solution_runs_clean(script):
    result = subprocess.run(
        [sys.executable, str(ROOT / "solutions" / script)],
        capture_output=True,
        text=True,
        cwd=ROOT,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_run_agent_cli_completes_every_task(tmp_path):
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "run_agent.py"),
            "--all",
            "--quiet",
            "--traces",
            str(tmp_path / "cli.jsonl"),
        ],
        capture_output=True,
        text=True,
        cwd=ROOT,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "22/22 tasks reached a valid final answer." in result.stdout
