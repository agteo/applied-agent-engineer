"""Automated Level 1 check: are these traces usable by Level 2?

    python -m acme_agent.check_traces traces/level-1.jsonl

Exit code 0 means another script can load every trace, every final answer
matches the contract, and every cited policy id exists. Failure messages name
the trace and the field, because "invalid trace" is not feedback.
"""

from __future__ import annotations

import sys
from pathlib import Path

from . import fixtures
from .schemas import FINAL_ANSWER_SCHEMA
from .trace import load_traces
from .validation import ValidationError, validate

MIN_TRACES = 20


def check(path: str | Path) -> list[str]:
    problems: list[str] = []
    traces = load_traces(path)
    known_ids = {section["source_id"] for section in fixtures.policy_sections()}

    if len(traces) < MIN_TRACES:
        problems.append(
            f"{path}: found {len(traces)} traces, Level 1 requires at least {MIN_TRACES}."
        )

    seen_ids: set[str] = set()
    for index, trace in enumerate(traces, start=1):
        label = f"{path}:{index} (task_id={trace.get('task_id')!r})"
        for field in ("task_id", "task", "agent_version", "model", "prompt_version", "steps", "metadata"):
            if field not in trace:
                problems.append(f"{label}: missing required trace field {field!r}.")
        seen_ids.add(trace.get("task_id", ""))

        if not trace.get("steps"):
            problems.append(f"{label}: has no steps.")

        answer = trace.get("final_answer")
        if answer is None:
            problems.append(
                f"{label}: no final answer (stop_reason="
                f"{trace.get('metadata', {}).get('stop_reason')!r})."
            )
            continue
        try:
            validate(answer, FINAL_ANSWER_SCHEMA, "final_answer")
        except ValidationError as error:
            problems.append(f"{label}: final answer breaks the contract: {error}")
            continue

        cited = {
            source_id
            for group in ("reimbursable_items", "non_reimbursable_items")
            for line in answer[group]
            for source_id in line["policy_source_ids"]
        }
        cited |= set(answer.get("cited_policy_source_ids", []))
        cited |= {
            source_id
            for entry in answer["approvals_required"]
            for source_id in entry.get("policy_source_ids", [])
        }
        for source_id in sorted(cited - known_ids):
            problems.append(f"{label}: cites unknown policy source id {source_id!r}.")

        total = round(sum(line["amount"] for line in answer["reimbursable_items"]), 2)
        if abs(total - answer["total_reimbursable"]) > 0.011:
            problems.append(
                f"{label}: total_reimbursable is {answer['total_reimbursable']} "
                f"but the line items sum to {total}."
            )

    if len(seen_ids) < len(traces):
        problems.append(f"{path}: task ids are not unique across traces.")

    return problems


def main(argv: list[str] | None = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    path = argv[0] if argv else "traces/level-1.jsonl"
    if not Path(path).exists():
        print(f"FAIL: {path} does not exist. Run: python run_agent.py --all", file=sys.stderr)
        return 2
    problems = check(path)
    if problems:
        print(f"FAIL: {len(problems)} problem(s) in {path}\n", file=sys.stderr)
        for problem in problems:
            print(f"  - {problem}", file=sys.stderr)
        return 1
    print(f"PASS: {path} is a valid Level 1 trace bundle.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
