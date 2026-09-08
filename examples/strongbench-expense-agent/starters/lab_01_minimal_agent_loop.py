#!/usr/bin/env python3
"""Starter for Lab 1: Minimal Agent Loop.

Module contract used by ``checks/lab_01.py``:

* ``TASKS`` contains the three lab tasks.
* ``calculator(expression)`` returns ``{"result": float}`` or
  ``{"error": str}``.
* ``run(task, max_steps=4)`` returns a trace with ``task``, ``steps``,
  ``final_answer``, and ``stop_reason``. Each step records ``model_response``;
  tool steps also record ``tool_call`` and ``observation``.

Complete the TODOs below. The starter is intentionally runnable before it is
finished so the checks can show useful failures.
"""

from __future__ import annotations

import ast
import operator
import re
from typing import Any

TASKS = [
    "What is 47 plus 68?",
    "I spent $47 on parking and $68 on dinner. What is the total?",
    "Explain whether dinner is reimbursable.",
]

_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.USub: operator.neg,
}


def calculator(expression: str) -> dict[str, Any]:
    """Return a safe arithmetic result or an error."""
    # TODO: parse and evaluate only numeric arithmetic AST nodes.
    return {"error": "calculator is not implemented yet"}


_AMOUNTS = re.compile(r"\$?\s?(\d+(?:\.\d{1,2})?)")
_NEEDS_MATH = ["total", "plus", "add", "sum", "how much", "altogether", "combined"]


def model(messages: list[dict[str, Any]]) -> dict[str, Any]:
    """Deterministic stand-in for a model call."""
    task = messages[0]["content"]
    observation = next((message for message in messages if message["role"] == "tool"), None)
    if observation is not None:
        # TODO: use the observation to produce the final answer.
        return {"final_answer": "I received the tool result."}

    lowered = task.lower()
    amounts = _AMOUNTS.findall(task)
    if len(amounts) >= 2 and any(word in lowered for word in _NEEDS_MATH):
        # TODO: return a calculator tool call with the requested expression.
        return {"final_answer": "I need to calculate this, but the tool call is TODO."}

    return {"final_answer": "Dinner during business travel may be reimbursable."}


TOOLS = {"calculator": calculator}


def run(task: str, max_steps: int = 4) -> dict[str, Any]:
    """Run the model/tool loop and return a trace."""
    messages: list[dict[str, Any]] = [{"role": "user", "content": task}]
    trace: dict[str, Any] = {"task": task, "steps": [], "final_answer": None}

    for step in range(1, max_steps + 1):
        # TODO: call model, execute a known tool, and append the observation.
        response = model(messages)
        record = {"step": step, "model_response": response}
        trace["steps"].append(record)
        if "final_answer" in response:
            trace["final_answer"] = response["final_answer"]
            trace["stop_reason"] = "final_answer"
            return trace

    trace["stop_reason"] = "max_steps_exceeded"
    return trace
