import pytest

from acme_agent.agent import run_agent
from acme_agent.models import ModelResponse, ScriptedModel, ToolCall, parse_final_answer
from acme_agent.schemas import FINAL_ANSWER_SCHEMA
from acme_agent.validation import validate

CANONICAL = (
    "I flew to Denver for a customer meeting, paid $47 for airport parking, "
    "spent $68 on dinner, and lost the hotel receipt for a $214 stay. "
    "What can I reimburse, and what needs manager approval?"
)


class FixedModel:
    """A model that replays a scripted list of responses, one per turn."""

    name = "fixed-test-model"

    def __init__(self, responses):
        self.responses = list(responses)
        self.calls = []

    def __call__(self, messages):
        self.calls.append(list(messages))
        return self.responses.pop(0) if self.responses else ModelResponse(text="")


def test_canonical_task_produces_a_contract_valid_answer():
    result = run_agent(CANONICAL, ScriptedModel(), task_id="test-001")
    assert result.ok
    validate(result.final_answer, FINAL_ANSWER_SCHEMA)
    assert result.final_answer["total_reimbursable"] == 329.0
    assert result.final_answer["missing_information"]
    assert result.final_answer["approvals_required"]


def test_answers_are_grounded_in_retrieved_policy():
    result = run_agent(CANONICAL, ScriptedModel(), task_id="test-002")
    tools_used = [step.tool_name for step in result.trace.steps if step.tool_name]
    assert tools_used[0] == "search_policy"
    assert all(line["policy_source_ids"] for line in result.final_answer["reimbursable_items"])


def test_agent_refuses_to_submit_on_the_users_behalf():
    result = run_agent("Can you submit this reimbursement for me? It comes to $329.", ScriptedModel(), task_id="test-003")
    assert "request_human_approval" in [step.tool_name for step in result.trace.steps]
    assert any(entry["approval_type"] == "employee" for entry in result.final_answer["approvals_required"])
    assert "cannot submit" in result.final_answer["next_action"]


def test_invalid_tool_arguments_do_not_execute_the_tool():
    model = FixedModel(
        [
            ModelResponse(tool_calls=[ToolCall("lookup_receipt", {"merchant": "Hyatt"})]),
            ModelResponse(tool_calls=[ToolCall("lookup_receipt", {"employee_id": "emp-1001"})]),
            ModelResponse(final_answer=_blank_answer()),
        ]
    )
    result = run_agent("look up my receipts", model, task_id="test-004")
    first = result.trace.steps[0]
    assert first.error.startswith("invalid_arguments")
    assert first.observation is None
    # The validation error is handed back to the model as an observation.
    assert result.trace.steps[1].observation is not None
    assert result.ok


def test_unknown_tool_is_reported_to_the_model():
    model = FixedModel(
        [
            ModelResponse(tool_calls=[ToolCall("wire_transfer", {"amount": 1000})]),
            ModelResponse(final_answer=_blank_answer()),
        ]
    )
    result = run_agent("send money", model, task_id="test-005")
    assert "unknown_tool" in result.trace.steps[0].error
    assert result.ok


def test_tool_exceptions_become_observations_not_crashes():
    def explode(**_kwargs):
        raise RuntimeError("policy index offline")

    model = FixedModel(
        [
            ModelResponse(tool_calls=[ToolCall("search_policy", {"query": "meals"})]),
            ModelResponse(final_answer=_blank_answer()),
        ]
    )
    result = run_agent("meals?", model, task_id="test-006", tools={"search_policy": explode})
    assert "tool_error: RuntimeError" in result.trace.steps[0].error
    assert result.ok


def test_invalid_final_answer_is_rejected_and_retried():
    model = FixedModel(
        [
            ModelResponse(final_answer={"summary": "done"}),
            ModelResponse(final_answer=_blank_answer()),
        ]
    )
    result = run_agent("anything", model, task_id="test-007")
    assert "final_answer_invalid" in result.trace.steps[0].error
    assert result.ok
    assert len(result.trace.steps) == 2


def test_max_steps_stops_the_loop():
    model = FixedModel([ModelResponse(text="thinking...") for _ in range(20)])
    result = run_agent("loop forever", model, task_id="test-008", max_steps=3)
    assert result.stop_reason == "max_steps_exceeded"
    assert len(result.trace.steps) == 3
    assert result.final_answer is None


def test_model_errors_end_the_run_cleanly():
    class BrokenModel:
        name = "broken"

        def __call__(self, messages):
            raise ConnectionError("rate limited")

    result = run_agent("anything", BrokenModel(), task_id="test-009")
    assert result.stop_reason == "model_error"
    assert "rate limited" in result.trace.error


@pytest.mark.parametrize(
    "text",
    [
        '{"summary": "x"}',
        '```json\n{"summary": "x"}\n```',
        'Here is the answer:\n```\n{"summary": "x"}\n```\nLet me know.',
    ],
)
def test_final_answer_parsing_survives_model_prose(text):
    assert parse_final_answer(text) == {"summary": "x"}


def test_final_answer_parsing_returns_none_on_garbage():
    assert parse_final_answer("I could not do that.") is None


def _blank_answer():
    return {
        "summary": "No expenses to process.",
        "reimbursable_items": [],
        "non_reimbursable_items": [],
        "missing_information": [],
        "approvals_required": [],
        "total_reimbursable": 0.0,
        "confidence": "low",
        "next_action": "Ask the employee for expense details.",
    }
