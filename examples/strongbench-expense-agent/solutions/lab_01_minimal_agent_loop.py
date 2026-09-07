#!/usr/bin/env python3
"""Reference solution: Lab 1, Minimal Agent Loop.

    python solutions/lab_01_minimal_agent_loop.py

Deliberately standalone. Nothing here imports the full harness, because the
point of Lab 1 is that an agent loop is about forty lines of code and no
framework. Everything the later labs add — schemas, retrieval, tracing — is an
answer to a problem you should feel here first.

The loop stops for exactly three reasons: the model answered, the model asked
for a tool that does not exist, or the step budget ran out.
"""

from __future__ import annotations

import ast
import json
import operator
import re
from pathlib import Path
from typing import Any

TRACE_PATH = Path(__file__).resolve().parent.parent / "traces" / "lab-01.jsonl"

# --- The tool ---------------------------------------------------------------

_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.USub: operator.neg,
}


def calculator(expression: str) -> dict[str, Any]:
    """Evaluate an arithmetic expression.

    `eval` would be shorter and would also let a model run arbitrary code. The
    Level 1 constraint "do not let the model execute arbitrary code" is not
    decoration: this is what honouring it costs.
    """

    def evaluate(node: ast.AST) -> float:
        if isinstance(node, ast.Expression):
            return evaluate(node.body)
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return float(node.value)
        if isinstance(node, ast.BinOp) and type(node.op) in _OPERATORS:
            return _OPERATORS[type(node.op)](evaluate(node.left), evaluate(node.right))
        if isinstance(node, ast.UnaryOp) and type(node.op) in _OPERATORS:
            return _OPERATORS[type(node.op)](evaluate(node.operand))
        raise ValueError(f"unsupported expression: {ast.dump(node)}")

    try:
        tree = ast.parse(expression, mode="eval")
    except SyntaxError as error:
        return {"error": f"could not parse {expression!r}: {error.msg}"}
    try:
        return {"result": round(evaluate(tree), 2)}
    except ValueError as error:
        return {"error": str(error)}


# --- The "model" ------------------------------------------------------------

_AMOUNTS = re.compile(r"\$?\s?(\d+(?:\.\d{1,2})?)")
_NEEDS_MATH = ["total", "plus", "add", "sum", "how much", "altogether", "combined"]


def model(messages: list[dict[str, Any]]) -> dict[str, Any]:
    """A stand-in for an LLM: same interface, deterministic decisions.

    A real model call goes here. What matters for the lab is the shape of the
    return value: either a tool call or a final answer, never both.
    """
    task = messages[0]["content"]
    observation = next((message for message in messages if message["role"] == "tool"), None)

    if observation is not None:
        result = observation["content"].get("result")
        if result is None:
            return {"final_answer": f"I could not compute that: {observation['content'].get('error')}"}
        return {"final_answer": f"The total is ${result:.2f}."}

    lowered = task.lower()
    amounts = _AMOUNTS.findall(task)
    if len(amounts) >= 2 and any(word in lowered for word in _NEEDS_MATH):
        return {"tool_call": {"name": "calculator", "arguments": {"expression": " + ".join(amounts)}}}

    return {
        "final_answer": (
            "Dinner during business travel is reimbursable up to the daily meal limit. "
            "No calculation was needed to answer that."
        )
    }


# --- The loop ---------------------------------------------------------------

TOOLS = {"calculator": calculator}


def run(task: str, max_steps: int = 4) -> dict[str, Any]:
    messages: list[dict[str, Any]] = [{"role": "user", "content": task}]
    trace: dict[str, Any] = {"task": task, "steps": [], "final_answer": None}

    for step in range(1, max_steps + 1):
        response = model(messages)
        record: dict[str, Any] = {"step": step, "model_response": response}

        if "final_answer" in response:
            trace["steps"].append(record)
            trace["final_answer"] = response["final_answer"]
            trace["stop_reason"] = "final_answer"
            return trace

        call = response["tool_call"]
        if call["name"] not in TOOLS:
            record["error"] = f"unknown tool {call['name']!r}"
            trace["steps"].append(record)
            trace["stop_reason"] = "unknown_tool"
            return trace

        observation = TOOLS[call["name"]](**call["arguments"])
        record["tool_call"] = call
        record["observation"] = observation
        trace["steps"].append(record)
        messages.append({"role": "tool", "name": call["name"], "content": observation})

    trace["stop_reason"] = "max_steps_exceeded"
    return trace


TASKS = [
    "What is 47 plus 68?",
    "I spent $47 on parking and $68 on dinner. What is the total?",
    "Explain whether dinner is reimbursable.",
]


def main() -> int:
    TRACE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(TRACE_PATH, "w", encoding="utf-8") as handle:
        for task in TASKS:
            trace = run(task)
            handle.write(json.dumps(trace) + "\n")
            used = [step.get("tool_call", {}).get("name") for step in trace["steps"]]
            print(f"task: {task}")
            print(f"  tools used : {[name for name in used if name] or 'none'}")
            print(f"  answer     : {trace['final_answer']}\n")

    print(f"Three traces written to {TRACE_PATH}")
    print(
        "\nWhen does the agent call the tool? Only when the task contains two or more\n"
        "numbers AND asks for a combined figure. Task 3 has neither, so it is answered\n"
        "in one model call. That decision belongs to the model, but the *budget* for it\n"
        "belongs to the loop: max_steps is what stops a confused model from spending\n"
        "your money forever."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
