# Trace Schema v1.0.0

One JSON object per task, one object per line, in a `.jsonl` file. Every later level reads this format: Level 2 grades it, Level 3 annotates it, Level 4 converts it into training data. Adding a field is a safe change. Changing what a field means is not — bump `trace_schema_version` when you do.

Written by [`acme_agent/trace.py`](../acme_agent/trace.py). Checked by `python -m acme_agent.check_traces`.

## Top level

| Field | Type | Notes |
| --- | --- | --- |
| `task_id` | string | Unique within a bundle. Level 2 joins benchmark tasks on this. |
| `task` | string | The user request, verbatim. |
| `agent_version` | string | e.g. `acme-expense-agent-v1`. |
| `model` | string | The adapter's model name, e.g. `scripted-reference-v1`. |
| `prompt_version` | string | Which system prompt produced this run. Without it, an eval result cannot be reproduced. |
| `trace_schema_version` | string | Semantic version of this document. |
| `run_id` | string | Distinguishes two runs of the same task. |
| `started_at` | number | Unix timestamp. |
| `steps` | array | One entry per loop iteration. See below. |
| `final_answer` | object or null | Must match the final-answer contract in [`acme_agent/schemas.py`](../acme_agent/schemas.py). Null when the run stopped early. |
| `error` | string or null | Set on `model_error` and `max_steps_exceeded`. |
| `metadata` | object | Derived summary; see below. |

## Step

| Field | Type | Notes |
| --- | --- | --- |
| `step` | integer | 1-indexed. |
| `started_at` | number | Unix timestamp. |
| `model_text` | string | Any prose the model returned this turn. |
| `tool_name` | string or null | Null when the model answered or stalled. |
| `tool_arguments` | object or null | What the model asked for, **before** validation. Keep it even when validation fails: this is the raw material for Level 3's failure taxonomy. |
| `validated_arguments` | object or null | Null when validation rejected the call. |
| `observation` | any | What the tool returned. Null on error. |
| `error` | string or null | Prefixed by kind: `invalid_arguments`, `unknown_tool`, `tool_error`, `model_error`, `final_answer_invalid`, `no_action`. |
| `latency_ms` | integer | Model call duration. |
| `usage` | object | `input_tokens` / `output_tokens` when the provider reports them. |

## Metadata

| Field | Type | Notes |
| --- | --- | --- |
| `stop_reason` | string | `final_answer`, `max_steps_exceeded`, or `model_error`. |
| `step_count` | integer | |
| `tool_calls` | array of string | Tool names in call order — the trajectory shape Level 3 reads first. |
| `total_tokens` | integer | Summed across steps. |
| `latency_ms` | integer | Summed across steps. |
| `max_steps` | integer | The budget this run was given. |

## Why the error prefixes matter

Level 3 classifies failures by cause, not by symptom. The prefix is the join key between a raw trace and a taxonomy entry, so keep the vocabulary closed:

- `invalid_arguments` — the model asked for something the schema forbids.
- `unknown_tool` — the model hallucinated a capability.
- `tool_error` — the tool itself failed. Not the model's fault.
- `final_answer_invalid` — the answer did not match the contract.
- `no_action` — the model neither answered nor acted.
- `model_error` — the provider call failed.

An agent that scores 60% is not interesting. An agent that scores 60% with 30% `invalid_arguments` and 10% `final_answer_invalid` tells you exactly what to fix first, and neither fix is "improve the prompt".
