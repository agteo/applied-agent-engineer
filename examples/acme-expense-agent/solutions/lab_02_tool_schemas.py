#!/usr/bin/env python3
"""Reference solution: Lab 2, Tool Schemas.

    python solutions/lab_02_tool_schemas.py

Lab 1 called a tool with whatever the model produced. This lab puts a validator
in front of every call, so a malformed argument becomes an observation the
model can recover from instead of a traceback or, worse, a silent wrong answer.

The schemas live in acme_agent/schemas.py and the validator in
acme_agent/validation.py — read those two files alongside this script.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from acme_agent.agent import execute_tool, run_agent
from acme_agent.models import ModelResponse, ToolCall
from acme_agent.schemas import TOOL_SCHEMAS
from acme_agent.tools import TOOL_FUNCTIONS

PASSING: list[tuple[str, dict[str, Any]]] = [
    ("lookup_receipt", {"employee_id": "emp-1001"}),
    ("lookup_receipt", {"employee_id": "emp-1001", "merchant": "Hotel", "date": "2026-03-12"}),
    ("search_policy", {"query": "missing receipt", "top_k": 2}),
    ("calculate_reimbursement", {"items": [{"description": "Dinner", "amount": 68.0, "category": "meals"}]}),
    ("request_human_approval", {"action": "prepare_report", "reason": "user asked for a draft"}),
]

FAILING: list[tuple[str, dict[str, Any], str]] = [
    ("lookup_receipt", {"merchant": "Hyatt"}, "missing required field"),
    ("lookup_receipt", {"employee_id": "emp-1001", "amount": "forty seven"}, "wrong type"),
    ("lookup_receipt", {"employee_id": "emp-1001", "category": "yacht"}, "unknown enum value"),
    ("lookup_receipt", {"employee_id": "emp-1001", "date": "March 12"}, "bad date format"),
    ("lookup_receipt", {"employee_id": "emp-1001", "sql": "DROP TABLE receipts"}, "unknown field"),
    ("search_policy", {"query": "meals", "top_k": 99}, "out of range"),
    ("calculate_reimbursement", {"items": []}, "empty array"),
    ("calculate_reimbursement", {"items": [{"description": "Dinner"}]}, "incomplete item"),
    ("request_human_approval", {"action": "wire_funds", "reason": "why not"}, "action outside the allowed set"),
    ("wire_transfer", {"amount": 10000}, "tool that does not exist"),
]

# An ambiguous lookup is not a validation failure. The arguments are legal, the
# answer is genuinely uncertain, and the tool says so rather than guessing.
AMBIGUOUS = ("lookup_receipt", {"employee_id": "emp-1001"})


class RecoveringModel:
    """Calls a tool with a missing required field, then corrects itself."""

    name = "recovering-test-model"

    def __init__(self) -> None:
        self.turn = 0

    def __call__(self, messages: list[dict[str, Any]]) -> ModelResponse:
        self.turn += 1
        if self.turn == 1:
            return ModelResponse(tool_calls=[ToolCall("lookup_receipt", {"merchant": "Hotel Teatro"})])
        if self.turn == 2:
            return ModelResponse(
                tool_calls=[ToolCall("lookup_receipt", {"employee_id": "emp-1001", "merchant": "Hotel Teatro"})]
            )
        matches = next(
            message["content"]["matches"]
            for message in messages
            if message["role"] == "tool" and not message.get("error")
        )
        return ModelResponse(
            final_answer={
                "summary": f"Found {len(matches)} matching receipt after correcting the tool call.",
                "reimbursable_items": [],
                "non_reimbursable_items": [],
                "missing_information": ["Receipt image for the Hotel Teatro stay."],
                "approvals_required": [],
                "total_reimbursable": 0.0,
                "confidence": "medium",
                "next_action": "Submit a missing receipt declaration.",
            }
        )


def main() -> int:
    print("Schemas under test:", ", ".join(sorted(TOOL_SCHEMAS)), "\n")

    print("--- Arguments that should pass ---")
    for name, arguments in PASSING:
        observation, error = execute_tool(name, arguments, TOOL_FUNCTIONS)
        status = "FAIL (unexpected error)" if error else "ok"
        print(f"  {status:<24} {name}({json.dumps(arguments)[:70]})")
        assert error is None, error

    print("\n--- Arguments that should be rejected ---")
    for name, arguments, label in FAILING:
        observation, error = execute_tool(name, arguments, TOOL_FUNCTIONS)
        assert error is not None, f"{label} was accepted, which is the bug this lab exists to catch"
        assert observation is None, "a rejected call must not reach the tool"
        print(f"  {label:<32} -> {error[:110]}")

    print("\n--- Legal arguments, uncertain answer ---")
    observation, _ = execute_tool(*AMBIGUOUS, TOOL_FUNCTIONS)
    print(
        f"  lookup_receipt(employee_id='emp-1001') matched {observation['match_count']} receipts, "
        f"ambiguous={observation['ambiguous']}."
    )
    print("  The tool reports ambiguity instead of picking one. The agent must ask.")

    print("\n--- Recovery trace: a rejected call is an observation, not a crash ---")
    result = run_agent("Find my Hotel Teatro receipt.", RecoveringModel(), task_id="lab-02-recovery")
    for step in result.trace.steps:
        print(f"  step {step.step}: tool={step.tool_name} error={step.error or 'none'}")
    print(f"  stop_reason: {result.stop_reason}")

    print(
        "\nThe rule this lab encodes: validate before you execute, and return the\n"
        "validation error verbatim. A model cannot fix an argument it was never told\n"
        "was wrong, and 'the tool crashed' is not a fixable error message."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
