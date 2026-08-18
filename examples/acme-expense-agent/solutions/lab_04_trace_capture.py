#!/usr/bin/env python3
"""Reference solution: Lab 4, Trace Capture.

    python solutions/lab_04_trace_capture.py

Produces the Level 1 trace bundle: one JSONL row per manual task, plus one
hand-annotated example. Everything Levels 2-4 do reads this file, so the check
that matters is not "did it write" but "can another script load every row
without special-casing a malformed one".

Trace schema: docs/trace-schema.md. Writer: acme_agent/trace.py.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from acme_agent import fixtures
from acme_agent.agent import run_agent
from acme_agent.check_traces import check
from acme_agent.models import ScriptedModel
from acme_agent.trace import TraceWriter, load_traces

ROOT = Path(__file__).resolve().parent.parent
TRACE_PATH = ROOT / "traces" / "level-1.jsonl"
ANNOTATED_PATH = ROOT / "traces" / "annotated-example.json"

ANNOTATIONS = {
    "why_this_trace": (
        "manual-004 is the canonical Level 1 task: three expenses, one of them "
        "missing a receipt, and a question about approvals. It exercises every "
        "tool except the approval gate."
    ),
    "step_1": (
        "search_policy runs first and unconditionally. That is a harness "
        "decision, not a model decision: an agent that answers a policy "
        "question without retrieving policy has no defensible citation, even "
        "when the answer happens to be right."
    ),
    "step_2": (
        "lookup_receipt fires because the task says 'lost the hotel receipt'. "
        "Note it returns several receipts and sets ambiguous=true. The agent "
        "does not use them here — the amounts came from the task text — which "
        "is a real weakness worth flagging in Level 3: the agent never "
        "reconciles what the user claims against what is on file."
    ),
    "step_3": (
        "calculate_reimbursement does all arithmetic and all threshold logic. "
        "The model never adds numbers. This is what makes the total auditable: "
        "329.00 is reproducible from the tool arguments alone."
    ),
    "step_4": (
        "The final answer carries policy_source_ids on every line. Level 2's "
        "citation grader reads exactly this field."
    ),
    "known_failure_modes_visible_here": [
        "The hotel is counted as reimbursable while also flagged as needing a "
        "missing-receipt approval. That is a defensible reading of the policy, "
        "but it means total_reimbursable is 'pending approval', not 'payable'. "
        "Level 2 has to decide which one it is grading.",
        "Item descriptions come from shallow text extraction ('Stay'), so they "
        "read worse than a human would write them.",
        "Nothing checks the 60-day submission window against the expense date.",
    ],
}


def main() -> int:
    writer = TraceWriter(TRACE_PATH)

    for task in fixtures.tasks():
        result = run_agent(
            task["task"],
            ScriptedModel(employee_id=task["employee_id"]),
            task_id=task["task_id"],
            writer=writer,
        )
        print(f"  {task['task_id']:<12} {result.stop_reason}")

    traces = load_traces(TRACE_PATH)
    print(f"\n{len(traces)} traces written to {TRACE_PATH}")

    annotated = next(trace for trace in traces if trace["task_id"] == "manual-004")
    ANNOTATED_PATH.write_text(
        json.dumps({"annotations": ANNOTATIONS, "trace": annotated}, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Hand-annotated example written to {ANNOTATED_PATH}")

    problems = check(TRACE_PATH)
    if problems:
        print("\nFAIL:")
        for problem in problems:
            print(f"  - {problem}")
        return 1

    print("\nPASS: every row loads, every final answer matches the contract, every")
    print("cited policy id exists, and every total equals the sum of its line items.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
