"""Model adapters.

The harness talks to models through one narrow interface so that swapping a
frontier API for a local model (Level 5) changes one line, not the agent.

Two adapters ship with Level 1:

- `ScriptedModel` is not an LLM. It is a deterministic planner that produces
  the same tool calls an LLM should produce. It exists so the harness, the
  tools, the traces, and the tests can run offline, in CI, with no API key and
  no cost. Treat it as the reference trajectory, not as the agent's brain.
- `AnthropicModel` is the real thing, used when ANTHROPIC_API_KEY is set.

Level 2 compares them on the same benchmark, which is the point: you cannot
tell how much the model contributes until the harness is measurable without it.
"""

from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass, field
from typing import Any, Protocol

from .schemas import FINAL_ANSWER_SCHEMA, anthropic_tool_definitions

SYSTEM_PROMPT_VERSION = "acme-expense-system-prompt-v1"

SYSTEM_PROMPT = """You are the Acme Expense Agent. You help employees understand what \
they can reimburse under Acme's expense policy.

Rules you must follow:
1. Never state a policy rule you have not retrieved with search_policy. Cite the \
source_id of every policy section you rely on.
2. Use calculate_reimbursement for all arithmetic and all limit decisions. Do not do \
the maths yourself.
3. Use lookup_receipt when the user refers to a receipt or a past expense.
4. Call request_human_approval before preparing or submitting anything. You must never \
submit a report on the employee's behalf.
5. When you are done, return a final answer as a JSON object matching the contract \
below and nothing else.

Final answer contract:
{contract}
""".format(contract=json.dumps(FINAL_ANSWER_SCHEMA["properties"], indent=2))


@dataclass
class ToolCall:
    name: str
    arguments: dict[str, Any]
    call_id: str = ""


@dataclass
class ModelResponse:
    """What one model turn produced: a tool call, a final answer, or text."""

    tool_calls: list[ToolCall] = field(default_factory=list)
    final_answer: dict[str, Any] | None = None
    text: str = ""
    usage: dict[str, int] = field(default_factory=dict)
    raw: Any = None


class Model(Protocol):
    name: str

    def __call__(self, messages: list[dict[str, Any]]) -> ModelResponse: ...


# --------------------------------------------------------------------------
# Deterministic offline adapter
# --------------------------------------------------------------------------

_CATEGORY_KEYWORDS = {
    "meals": ["dinner", "lunch", "breakfast", "meal", "food", "coffee", "restaurant", "steakhouse"],
    "lodging": ["hotel", "lodging", "room", "motel", "stay"],
    "travel": ["parking", "taxi", "uber", "lyft", "rideshare", "flight", "airfare", "train", "rail", "mileage", "cab"],
    "alcohol": ["drinks", "bar", "alcohol", "wine", "beer", "cocktail"],
    "entertainment": ["entertainment", "golf", "event", "outing", "client event"],
}

_MISSING_RECEIPT = ["lost", "missing", "no receipt", "without a receipt", "misplaced", "can't find", "cannot find"]
_SUBMIT_WORDS = ["submit", "file it", "send it", "expense it for me", "put it through"]
_PREPARE_WORDS = ["prepare", "draft", "recommendation", "put together", "build a report"]
_TOTAL_WORDS = ["how much", "total", "claim", "reimburse", "reimbursable", "get back", "comes back", "recommendation"]
_AMOUNT = re.compile(r"\$\s?([0-9][0-9,]*(?:\.[0-9]{1,2})?)")


_CLAUSE_BREAK = re.compile(r",|\.|;|\?|\band\b|\bbut\b|\bwhat\b|\bcan\b|\bis\b")


def _first_clause(text: str) -> str:
    """Everything up to the first clause boundary, so items stop at 'and'."""
    match = _CLAUSE_BREAK.search(text)
    return text[: match.start()] if match else text


def _last_clause(text: str) -> str:
    """Everything after the last clause boundary."""
    matches = list(_CLAUSE_BREAK.finditer(text))
    return text[matches[-1].end() :] if matches else text


def _wants_a_total(lowered: str) -> bool:
    """True when the user asked for a number, not just for the rule."""
    return any(phrase in lowered for phrase in _TOTAL_WORDS)


def _category_for(text: str) -> str:
    lowered = text.lower()
    for category, words in _CATEGORY_KEYWORDS.items():
        if any(word in lowered for word in words):
            return category
    return "other"


def _describe(fragment: str) -> str:
    words = [word for word in re.split(r"[^A-Za-z]+", fragment) if word]
    stop = {"on", "for", "a", "an", "the", "my", "i", "spent", "paid", "and", "of", "in", "at", "was", "is", "it"}
    kept = [word for word in words if word.lower() not in stop][:3]
    return " ".join(kept).strip().capitalize() or "Expense"


def extract_items(task: str) -> list[dict[str, Any]]:
    """Pull `{description, amount, category, has_receipt}` items out of a task.

    This stands in for the model's reading comprehension. Each amount owns the
    clause it sits in: text runs from the previous amount to the next one, so
    "$47 for parking, $68 on dinner" produces two items and not two guesses. It
    is still intentionally shallow, and Level 3 uses its mistakes as a source of
    real failure traces.
    """
    matches = list(_AMOUNT.finditer(task))
    items: list[dict[str, Any]] = []
    for index, match in enumerate(matches):
        amount = float(match.group(1).replace(",", ""))
        clause_start = matches[index - 1].end() if index else 0
        clause_end = matches[index + 1].start() if index + 1 < len(matches) else len(task)
        after = _first_clause(task[match.end() : clause_end])
        before = _last_clause(task[clause_start : match.start()])
        # The noun usually follows the amount ("$47 for airport parking"); fall
        # back to the words before it ("a hotel room at $214").
        category = _category_for(after)
        fragment = after
        if category == "other":
            category = _category_for(before)
            fragment = before if category != "other" else after
        clause = before + after
        has_receipt = not any(phrase in clause.lower() for phrase in _MISSING_RECEIPT)
        items.append(
            {
                "description": _describe(fragment),
                "amount": amount,
                "category": category,
                "has_receipt": has_receipt,
            }
        )
    return items


class ScriptedModel:
    """A deterministic reference planner. See the module docstring."""

    name = "scripted-reference-v1"

    def __init__(self, employee_id: str = "emp-1001") -> None:
        self.employee_id = employee_id

    def __call__(self, messages: list[dict[str, Any]]) -> ModelResponse:
        task = next(message["content"] for message in messages if message["role"] == "user")
        observed = {
            message["name"]: message["content"]
            for message in messages
            if message["role"] == "tool" and not message.get("error")
        }
        lowered = task.lower()

        if "search_policy" not in observed:
            return ModelResponse(tool_calls=[ToolCall("search_policy", {"query": task, "top_k": 4})])

        wants_lookup = any(word in lowered for word in ["receipt", "find the", "look up", "last thursday", "my trip"])
        if wants_lookup and "lookup_receipt" not in observed:
            arguments: dict[str, Any] = {"employee_id": self.employee_id}
            category = _category_for(task)
            if category != "other":
                arguments["category"] = category
            return ModelResponse(tool_calls=[ToolCall("lookup_receipt", arguments)])

        if "calculate_reimbursement" not in observed:
            items = extract_items(task)
            if not items and _wants_a_total(lowered):
                # Only total up looked-up receipts when the user actually asked
                # for a number. "What happens if I lose a receipt?" is a policy
                # question, and answering it with a dollar figure is a failure.
                items = self._items_from_receipts(observed.get("lookup_receipt"))
            if items:
                return ModelResponse(tool_calls=[ToolCall("calculate_reimbursement", {"items": items})])

        needs_approval = any(word in lowered for word in _SUBMIT_WORDS + _PREPARE_WORDS)
        if needs_approval and "request_human_approval" not in observed:
            action = "submit_report" if any(word in lowered for word in _SUBMIT_WORDS) else "prepare_report"
            calculation = observed.get("calculate_reimbursement") or {}
            return ModelResponse(
                tool_calls=[
                    ToolCall(
                        "request_human_approval",
                        {
                            "action": action,
                            "reason": f"User asked the agent to {action.replace('_', ' ')}.",
                            "amount": calculation.get("total_reimbursable", 0.0),
                        },
                    )
                ]
            )

        return ModelResponse(final_answer=self._compose(task, observed))

    def _items_from_receipts(self, lookup: dict[str, Any] | None) -> list[dict[str, Any]]:
        if not lookup:
            return []
        return [
            {
                "description": receipt["merchant"],
                "amount": receipt["amount"],
                "category": receipt["category"],
                "date": receipt["date"],
                "has_receipt": receipt["has_image"],
                "receipt_id": receipt["receipt_id"],
            }
            for receipt in lookup.get("matches", [])
        ]

    def _compose(self, task: str, observed: dict[str, Any]) -> dict[str, Any]:
        calculation = observed.get("calculate_reimbursement")
        approval = observed.get("request_human_approval")
        cited = [result["source_id"] for result in observed.get("search_policy", {}).get("results", [])]

        if not calculation:
            snippets = observed.get("search_policy", {}).get("results", [])
            summary = snippets[0]["text"] if snippets else "No relevant policy section was found."
            matches = (observed.get("lookup_receipt") or {}).get("matches", [])
            if matches:
                found = "; ".join(
                    f"{receipt['merchant']} on {receipt['date']} for USD {receipt['amount']:.2f}"
                    + ("" if receipt["has_image"] else " (no receipt image on file)")
                    for receipt in matches
                )
                summary = f"Found {len(matches)} matching receipt(s): {found}. {summary}"
            return {
                "summary": summary,
                "reimbursable_items": [],
                "non_reimbursable_items": [],
                "missing_information": (
                    []
                    if matches
                    else ["No expense amounts were provided, so nothing was calculated."]
                ),
                "approvals_required": [],
                "total_reimbursable": 0.0,
                "cited_policy_source_ids": cited,
                "confidence": "medium" if snippets else "low",
                "next_action": (
                    "Confirm which of these receipts to include, then ask for a reimbursement total."
                    if matches
                    else "Share the expense amounts and dates so a reimbursement total can be calculated."
                ),
            }

        total = calculation["total_reimbursable"]
        missing = list(calculation["missing_information"])
        approvals = list(calculation["approvals_required"])
        next_action = "Submit the report in the expense system."

        if approval and not approval["approved"]:
            approvals.append(
                {
                    "approval_type": "employee",
                    "reason": approval["note"],
                    "policy_source_ids": ["policy-submission-001"],
                }
            )
            next_action = "Review the prepared draft and submit it yourself; the agent cannot submit on your behalf."
        elif missing:
            next_action = "Resolve the missing information above, then ask your manager to approve the exception."

        confidence = "high" if not missing and not approvals else "medium"
        return {
            "summary": (
                f"USD {total:.2f} of USD {calculation['total_submitted']:.2f} is reimbursable under "
                f"the current policy. {len(approvals)} approval(s) and {len(missing)} open item(s) remain."
            ),
            "reimbursable_items": [
                {
                    "description": line["description"],
                    "amount": line["amount"],
                    "policy_source_ids": line["policy_source_ids"],
                    "reason": line["reason"],
                }
                for line in calculation["reimbursable_items"]
            ],
            "non_reimbursable_items": [
                {
                    "description": line["description"],
                    "amount": line["amount"],
                    "policy_source_ids": line["policy_source_ids"],
                    "reason": line["reason"],
                }
                for line in calculation["non_reimbursable_items"]
            ],
            "missing_information": missing,
            "approvals_required": [
                {
                    "approval_type": entry["approval_type"],
                    "reason": entry["reason"],
                    "policy_source_ids": entry.get("policy_source_ids", cited[:1]),
                }
                for entry in approvals
            ],
            "total_reimbursable": total,
            "cited_policy_source_ids": cited,
            "confidence": confidence,
            "next_action": next_action,
        }


# --------------------------------------------------------------------------
# Anthropic adapter
# --------------------------------------------------------------------------


class AnthropicModel:
    """Claude via the Messages API. Requires `anthropic` and ANTHROPIC_API_KEY."""

    def __init__(self, model: str = "claude-sonnet-5", max_tokens: int = 2048) -> None:
        try:
            import anthropic
        except ImportError as error:  # pragma: no cover - depends on optional extra
            raise ImportError(
                "The Anthropic adapter needs the `anthropic` package: pip install -r requirements.txt"
            ) from error
        if not os.environ.get("ANTHROPIC_API_KEY"):
            raise RuntimeError("ANTHROPIC_API_KEY is not set. Use --model scripted to run offline.")
        self.name = model
        self.max_tokens = max_tokens
        self._client = anthropic.Anthropic()
        self._tools = anthropic_tool_definitions()

    def __call__(self, messages: list[dict[str, Any]]) -> ModelResponse:
        response = self._client.messages.create(
            model=self.name,
            max_tokens=self.max_tokens,
            system=SYSTEM_PROMPT,
            tools=self._tools,
            messages=to_anthropic_messages(messages),
        )
        tool_calls = [
            ToolCall(name=block.name, arguments=dict(block.input), call_id=block.id)
            for block in response.content
            if block.type == "tool_use"
        ]
        text = "".join(block.text for block in response.content if block.type == "text")
        usage = {
            "input_tokens": response.usage.input_tokens,
            "output_tokens": response.usage.output_tokens,
        }
        if tool_calls:
            return ModelResponse(tool_calls=tool_calls, text=text, usage=usage, raw=response)
        return ModelResponse(final_answer=parse_final_answer(text), text=text, usage=usage, raw=response)


def to_anthropic_messages(messages: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Convert the harness's flat message list into Anthropic content blocks."""
    converted: list[dict[str, Any]] = []
    for message in messages:
        if message["role"] == "user":
            converted.append({"role": "user", "content": message["content"]})
        elif message["role"] == "assistant":
            converted.append({"role": "assistant", "content": message["content"]})
        elif message["role"] == "tool":
            converted.append(
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "tool_result",
                            "tool_use_id": message.get("call_id") or message["name"],
                            "content": json.dumps(message["content"], default=str),
                            "is_error": bool(message.get("error")),
                        }
                    ],
                }
            )
        elif message["role"] == "system":
            converted.append({"role": "user", "content": message["content"]})
    return converted


def parse_final_answer(text: str) -> dict[str, Any] | None:
    """Best-effort JSON extraction from model prose.

    Models wrap JSON in fences and commentary. Level 3 counts how often this
    fails: `output_format` failures are a real and separately fixable category.
    """
    if not text:
        return None
    fenced = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
    candidate = fenced.group(1) if fenced else None
    if candidate is None:
        start = text.find("{")
        end = text.rfind("}")
        candidate = text[start : end + 1] if start != -1 and end > start else None
    if candidate is None:
        return None
    try:
        parsed = json.loads(candidate)
    except json.JSONDecodeError:
        return None
    return parsed if isinstance(parsed, dict) else None


def get_model(name: str, employee_id: str = "emp-1001") -> Model:
    """Resolve a `--model` flag to an adapter."""
    if name in {"scripted", "offline", "reference"}:
        return ScriptedModel(employee_id=employee_id)
    return AnthropicModel(model=name)
