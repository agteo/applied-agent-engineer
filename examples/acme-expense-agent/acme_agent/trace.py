"""Trace capture.

One JSON object per task, one line per object, appended to a JSONL file. This
is the contract every later level reads: Level 2 grades traces, Level 3
annotates them, Level 4 converts them into training data. Adding a field is
safe. Changing the meaning of a field is not — bump `trace_schema_version`.

Schema documented in docs/trace-schema.md.
"""

from __future__ import annotations

import json
import time
import uuid
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

TRACE_SCHEMA_VERSION = "1.0.0"


@dataclass
class Step:
    step: int
    started_at: float
    model_text: str = ""
    tool_name: str | None = None
    tool_arguments: dict[str, Any] | None = None
    validated_arguments: dict[str, Any] | None = None
    observation: Any = None
    error: str | None = None
    latency_ms: int = 0
    usage: dict[str, int] = field(default_factory=dict)


@dataclass
class Trace:
    task_id: str
    task: str
    agent_version: str
    model: str
    prompt_version: str
    trace_schema_version: str = TRACE_SCHEMA_VERSION
    run_id: str = field(default_factory=lambda: uuid.uuid4().hex[:12])
    started_at: float = field(default_factory=time.time)
    steps: list[Step] = field(default_factory=list)
    final_answer: dict[str, Any] | None = None
    error: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["metadata"] = {
            **self.metadata,
            "step_count": len(self.steps),
            "tool_calls": [step.tool_name for step in self.steps if step.tool_name],
            "total_tokens": sum(
                usage.get("input_tokens", 0) + usage.get("output_tokens", 0)
                for usage in (step.usage for step in self.steps)
            ),
            "latency_ms": sum(step.latency_ms for step in self.steps),
        }
        return payload


class TraceWriter:
    """Write traces to a JSONL file. Every row must load with plain json.loads.

    Truncates on first write by default. Appending is opt-in because a bundle
    with the same task run twice fails the Level 1 uniqueness check, and that
    failure is confusing when the cause is just a second run.
    """

    def __init__(self, path: str | Path, append: bool = False) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._opened = append

    def write(self, trace: Trace) -> None:
        mode = "a" if self._opened else "w"
        self._opened = True
        with open(self.path, mode, encoding="utf-8") as handle:
            handle.write(json.dumps(trace.to_dict(), default=str) + "\n")


def load_traces(path: str | Path) -> list[dict[str, Any]]:
    """Load every trace from a JSONL file, skipping blank lines only."""
    traces = []
    with open(path, encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                traces.append(json.loads(line))
            except json.JSONDecodeError as error:
                raise ValueError(f"{path}:{line_number} is not valid JSON: {error}") from error
    return traces
