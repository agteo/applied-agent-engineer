#!/usr/bin/env python3
"""Run the Acme Expense Agent.

    python run_agent.py --task "I spent $47 on parking and $68 on dinner."
    python run_agent.py --all                       # the 22 manual Level 1 tasks
    python run_agent.py --all --model claude-sonnet-5

The default model is `scripted`, a deterministic offline planner. It needs no
API key and no network, so `--all` always works. Pass a real model name to use
the Anthropic adapter (requires `anthropic` and ANTHROPIC_API_KEY).
"""

from __future__ import annotations

import argparse
import json
import sys

from acme_agent import fixtures
from acme_agent.agent import DEFAULT_MAX_STEPS, run_agent
from acme_agent.models import get_model
from acme_agent.trace import TraceWriter


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run the Acme Expense Agent.")
    parser.add_argument("--task", help="A single task to run.")
    parser.add_argument("--all", action="store_true", help="Run every manual task in fixtures/tasks.json.")
    parser.add_argument("--task-id", help="Run one task from fixtures/tasks.json by id.")
    parser.add_argument("--model", default="scripted", help="Model adapter: 'scripted' or an Anthropic model name.")
    parser.add_argument("--employee-id", default="emp-1001", help="Employee the agent is acting for.")
    parser.add_argument("--max-steps", type=int, default=DEFAULT_MAX_STEPS)
    parser.add_argument("--traces", default="traces/level-1.jsonl", help="JSONL file to append traces to.")
    parser.add_argument("--append", action="store_true", help="Append to the trace file instead of replacing it.")
    parser.add_argument("--quiet", action="store_true", help="Print one summary line per task instead of full JSON.")
    args = parser.parse_args(argv)

    if not (args.task or args.all or args.task_id):
        parser.error("pass --task, --task-id, or --all")

    if args.all or args.task_id:
        selected = [
            task
            for task in fixtures.tasks()
            if not args.task_id or task["task_id"] == args.task_id
        ]
        if not selected:
            print(f"No task with id {args.task_id!r}", file=sys.stderr)
            return 2
    else:
        selected = [{"task_id": "adhoc-001", "task": args.task, "employee_id": args.employee_id}]

    writer = TraceWriter(args.traces, append=args.append)
    failures = 0

    for entry in selected:
        model = get_model(args.model, employee_id=entry.get("employee_id", args.employee_id))
        result = run_agent(
            entry["task"],
            model=model,
            task_id=entry["task_id"],
            max_steps=args.max_steps,
            writer=writer,
        )
        if not result.ok:
            failures += 1
        if args.quiet:
            total = (result.final_answer or {}).get("total_reimbursable")
            print(f"{entry['task_id']:<12} {result.stop_reason:<20} total={total}")
        else:
            print(f"\n=== {entry['task_id']}: {entry['task']}")
            print(f"stop_reason: {result.stop_reason}")
            print(json.dumps(result.final_answer, indent=2) if result.final_answer else "(no final answer)")

    print(f"\n{len(selected) - failures}/{len(selected)} tasks reached a valid final answer.")
    print(f"Traces written to {args.traces}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
