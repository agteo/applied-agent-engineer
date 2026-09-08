"""Deterministic checks for the Lab 1 module contract."""

from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
import sys
from typing import Any


TASKS = [
    "What is 47 plus 68?",
    "I spent $47 on parking and $68 on dinner. What is the total?",
    "Explain whether dinner is reimbursable.",
]


def _check(module: Any, check_id: str, title: str, fn) -> dict[str, Any]:
    try:
        passed, message = fn(module)
        return {"id": check_id, "title": title, "passed": bool(passed), "message": str(message)}
    except Exception as error:  # A learner exception is a failed check.
        return {"id": check_id, "title": title, "passed": False, "message": f"{type(error).__name__}: {error}"}


def check(module) -> list[dict]:
    """Grade a learner's Lab 1 module without raising."""
    def loops(mod):
        traces = [mod.run(task) for task in TASKS]
        valid = all(trace.get("stop_reason") and trace.get("steps") is not None for trace in traces)
        within_budget = all(len(trace["steps"]) <= 4 for trace in traces)
        return valid and within_budget, "All three tasks returned within max_steps with a stop_reason." if valid and within_budget else "Each task must return within max_steps and set stop_reason."

    def uses_tool(mod):
        traces = [mod.run(task) for task in TASKS]
        calls = [
            [step.get("tool_call", {}).get("name") for step in trace["steps"] if step.get("tool_call")]
            for trace in traces
        ]
        passed = all(calls[index] == ["calculator"] for index in (0, 1)) and calls[2] == []
        return passed, "Calculator is used for the first two tasks and not the third." if passed else f"Observed tool calls: {calls!r}"

    def uses_result(mod):
        answer = mod.run(TASKS[1]).get("final_answer") or ""
        return "115" in answer, "The final answer includes 115." if "115" in answer else "Task 2's final_answer must use the calculator result 115."

    def complete_trace(mod):
        traces = [mod.run(task) for task in TASKS]
        passed = all(
            trace.get("final_answer") is not None
            and all(
                "model_response" in step
                and ("tool_call" not in step or "observation" in step)
                and ("observation" not in step or "tool_call" in step)
                for step in trace["steps"]
            )
            for trace in traces
        )
        return passed, "Each trace records model responses, tool stages, and final_answer." if passed else "Every trace must record each stage and final_answer."

    def safe_tool(mod):
        result = mod.calculator("__import__('os')")
        passed = isinstance(result, dict) and "error" in result
        return passed, "Unsafe expressions return an error." if passed else "calculator must reject arbitrary code instead of evaluating it."

    return [
        _check(module, "loop-terminates", "The loop stops", loops),
        _check(module, "tool-when-needed", "The tool is called only when needed", uses_tool),
        _check(module, "answer-uses-result", "The final answer uses the tool result", uses_result),
        _check(module, "trace-is-complete", "The trace records each stage", complete_trace),
        _check(module, "tool-is-safe", "The calculator does not eval", safe_tool),
    ]


def _load_module(path: Path) -> Any:
    spec = importlib.util.spec_from_file_location("lab_01_submission", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load module from {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run deterministic checks for Lab 1.")
    parser.add_argument(
        "submission",
        nargs="?",
        default="starters/lab_01_minimal_agent_loop.py",
        help="Path to the learner's Lab 1 Python file.",
    )
    parser.add_argument("--json", action="store_true", help="Print machine-readable check results.")
    args = parser.parse_args(argv)

    submission = Path(args.submission)
    if not submission.is_absolute():
        submission = Path.cwd() / submission

    module = _load_module(submission)
    results = check(module)

    if args.json:
        print(json.dumps(results, indent=2))
    else:
        for result in results:
            status = "PASS" if result["passed"] else "FAIL"
            print(f"{status} {result['id']}: {result['message']}")

    return 0 if all(result["passed"] for result in results) else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
