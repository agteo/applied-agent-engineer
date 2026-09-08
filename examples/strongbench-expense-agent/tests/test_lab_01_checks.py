"""The Lab 1 reference solution must satisfy the learner-facing checks."""

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_reference_solution_passes_lab_01_checks():
    solution = load_module(ROOT / "solutions" / "lab_01_minimal_agent_loop.py", "lab_01_solution")
    checks = load_module(ROOT / "checks" / "lab_01.py", "lab_01_checks")
    results = checks.check(solution)
    assert [result["id"] for result in results] == [
        "loop-terminates",
        "tool-when-needed",
        "answer-uses-result",
        "trace-is-complete",
        "tool-is-safe",
    ]
    assert all(result["passed"] for result in results), results


def test_starter_exists_and_fails_lab_01_checks_usefully():
    starter = load_module(ROOT / "starters" / "lab_01_minimal_agent_loop.py", "lab_01_starter")
    checks = load_module(ROOT / "checks" / "lab_01.py", "lab_01_checks_starter")
    results = checks.check(starter)

    assert [result["id"] for result in results] == [
        "loop-terminates",
        "tool-when-needed",
        "answer-uses-result",
        "trace-is-complete",
        "tool-is-safe",
    ]
    assert any(not result["passed"] for result in results)
    assert all(result["message"] for result in results)
