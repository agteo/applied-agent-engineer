# Lab 4: Trace Capture

## Objective

Capture trajectories that later levels can evaluate and diagnose.

## Build

Add trace logging to the agent harness.

Each trace should include:

- task id
- user task
- model name
- prompt or prompt version
- step number
- model response
- tool call
- validated arguments
- tool observation
- errors
- final answer
- timestamps
- token usage if available
- latency if available

## Recommended Format

Use JSONL: one JSON object per task.

```json
{
  "task_id": "manual-001",
  "agent_version": "acme-expense-agent-v1",
  "model": "example-model",
  "steps": [],
  "final_answer": {},
  "metadata": {
    "latency_ms": 1234,
    "total_tokens": 900
  }
}
```

## Deliverable

Submit:

- trace writer
- 20 manual traces
- trace schema documentation
- one example trace marked up by hand

## Checks

The lab passes if another script can load every trace without special casing malformed rows.

