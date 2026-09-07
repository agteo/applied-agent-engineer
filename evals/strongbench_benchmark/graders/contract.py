"""Final-answer contract grading."""

from __future__ import annotations

from pathlib import Path
import sys
from typing import Any

AGENT_ROOT = Path(__file__).resolve().parents[3] / "examples" / "strongbench-expense-agent"
if str(AGENT_ROOT) not in sys.path:
    sys.path.insert(0, str(AGENT_ROOT))

from strongbench_agent.schemas import FINAL_ANSWER_SCHEMA  # noqa: E402
from strongbench_agent.validation import ValidationError, validate  # noqa: E402


def grade_contract(task: dict[str, Any], trace: dict[str, Any]) -> list[str]:
    task_id = task["id"]
    answer = trace.get("final_answer")
    if answer is None:
        return [f"{task_id}: final_answer: missing final answer."]
    try:
        validate(answer, FINAL_ANSWER_SCHEMA, "final_answer")
    except ValidationError as error:
        return [f"{task_id}: final_answer: breaks contract: {error}"]
    return []

