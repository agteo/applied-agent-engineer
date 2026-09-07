"""The agent harness.

The loop owns everything the model does not: validation, tool execution, error
handling, step limits, and trace capture. A model failure should never become a
harness crash — invalid tool arguments come back to the model as an
observation, because recovery is the behaviour Level 2 measures.
"""

from __future__ import annotations

import time
from typing import Any, Callable

from . import AGENT_VERSION
from .models import Model, ModelResponse, SYSTEM_PROMPT_VERSION
from .schemas import FINAL_ANSWER_SCHEMA, TOOL_SCHEMAS
from .tools import TOOL_FUNCTIONS
from .trace import Step, Trace, TraceWriter
from .validation import ValidationError, validate

DEFAULT_MAX_STEPS = 8


class AgentResult:
    """The outcome of one run: the final answer, the trace, and why it stopped."""

    def __init__(self, trace: Trace, final_answer: dict[str, Any] | None, stop_reason: str) -> None:
        self.trace = trace
        self.final_answer = final_answer
        self.stop_reason = stop_reason

    @property
    def ok(self) -> bool:
        return self.stop_reason == "final_answer"

    def __repr__(self) -> str:  # pragma: no cover - debugging aid
        return f"AgentResult(stop_reason={self.stop_reason!r}, task_id={self.trace.task_id!r})"


def run_agent(
    task: str,
    model: Model,
    task_id: str = "manual-001",
    tools: dict[str, Callable[..., Any]] | None = None,
    max_steps: int = DEFAULT_MAX_STEPS,
    writer: TraceWriter | None = None,
) -> AgentResult:
    """Run one task to a final answer, a step limit, or a hard error."""
    tools = tools or TOOL_FUNCTIONS
    trace = Trace(
        task_id=task_id,
        task=task,
        agent_version=AGENT_VERSION,
        model=getattr(model, "name", "unknown"),
        prompt_version=SYSTEM_PROMPT_VERSION,
        metadata={"max_steps": max_steps},
    )
    messages: list[dict[str, Any]] = [{"role": "user", "content": task}]
    stop_reason = "max_steps_exceeded"
    final_answer: dict[str, Any] | None = None

    for step_number in range(1, max_steps + 1):
        started = time.time()
        step = Step(step=step_number, started_at=started)
        trace.steps.append(step)

        try:
            response: ModelResponse = model(messages)
        except Exception as error:  # noqa: BLE001 - a model outage ends the run, cleanly
            step.error = f"model_error: {error}"
            step.latency_ms = _elapsed_ms(started)
            trace.error = step.error
            stop_reason = "model_error"
            break

        step.latency_ms = _elapsed_ms(started)
        step.model_text = response.text
        step.usage = response.usage

        if response.final_answer is not None:
            try:
                validate(response.final_answer, FINAL_ANSWER_SCHEMA, "final_answer")
            except ValidationError as error:
                step.error = f"final_answer_invalid: {error}"
                messages.append(
                    {
                        "role": "system",
                        "content": (
                            "The final answer did not match the contract: "
                            f"{error}. Fix the listed fields and return the JSON object again."
                        ),
                    }
                )
                continue
            final_answer = response.final_answer
            trace.final_answer = final_answer
            stop_reason = "final_answer"
            break

        if not response.tool_calls:
            messages.append(
                {
                    "role": "system",
                    "content": "Return a final answer as JSON, or call one of the available tools.",
                }
            )
            step.error = "no_action"
            continue

        for call in response.tool_calls:
            step.tool_name = call.name
            step.tool_arguments = call.arguments
            observation, error = execute_tool(call.name, call.arguments, tools)
            if error:
                step.error = error
                messages.append(
                    {
                        "role": "tool",
                        "name": call.name,
                        "call_id": call.call_id,
                        "content": {"error": error},
                        "error": True,
                    }
                )
                continue
            step.validated_arguments = call.arguments
            step.observation = observation
            messages.append(
                {
                    "role": "tool",
                    "name": call.name,
                    "call_id": call.call_id,
                    "content": observation,
                }
            )

    trace.metadata["stop_reason"] = stop_reason
    if stop_reason == "max_steps_exceeded":
        trace.error = "max_steps_exceeded"
    if writer:
        writer.write(trace)
    return AgentResult(trace, final_answer, stop_reason)


def execute_tool(
    name: str, arguments: dict[str, Any], tools: dict[str, Callable[..., Any]]
) -> tuple[Any, str | None]:
    """Validate then run one tool. Returns `(observation, error_message)`."""
    if name not in tools:
        known = ", ".join(sorted(tools))
        return None, f"unknown_tool: {name!r} is not available. Available tools: {known}."

    schema = TOOL_SCHEMAS.get(name)
    if schema:
        try:
            validate(arguments, schema["input_schema"], f"{name}.arguments")
        except ValidationError as error:
            return None, f"invalid_arguments: {error}"

    try:
        return tools[name](**arguments), None
    except TypeError as error:
        return None, f"invalid_arguments: {error}"
    except Exception as error:  # noqa: BLE001 - tool failures are observations, not crashes
        return None, f"tool_error: {type(error).__name__}: {error}"


def _elapsed_ms(started: float) -> int:
    return int((time.time() - started) * 1000)
