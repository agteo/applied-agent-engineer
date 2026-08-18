# Level 1: Build

## Goal

Build a reliable agent that can interact with real or simulated systems using tools, state, and structured outputs.

The purpose of Level 1 is not to learn a trendy agent framework. The purpose is to understand what an agent actually is by building one from first principles and then improving the harness carefully.

## Learning Outcomes

By the end of this level, learners can:

1. Explain the difference between an LLM call and an agent loop.
2. Define tool schemas and validate tool arguments.
3. Maintain task state across multiple model calls.
4. Use retrieval or search to ground an answer.
5. Add human approval for risky actions.
6. Produce a structured final response.
7. Capture traces that later levels can evaluate and diagnose.

## Required Build

Learners build Acme Expense Agent v1.

The agent helps employees with expense reimbursement tasks. It must answer policy questions, inspect receipt records, calculate reimbursable amounts, and prepare a structured reimbursement recommendation.

## System Boundary

In Level 1, the agent does not need to send real emails, access real payroll systems, or submit real reimbursements. It should use local fixtures or safe mock tools.

```text
User
  |
  v
Agent Harness
  |
  +-- search_policy()
  +-- lookup_receipt()
  +-- calculate_reimbursement()
  +-- request_human_approval()
  |
  v
Structured Final Answer
```

## Concepts

### LLM vs Agent

An LLM call maps input messages to output text or structured data.

An agent is a system around one or more model calls that can inspect state, choose actions, use tools, observe results, and decide what to do next.

### Agent Harness

The harness is the code that owns the loop:

1. Prepare messages.
2. Call the model.
3. Detect tool calls.
4. Validate tool arguments.
5. Execute tools.
6. Add observations to context.
7. Stop when the agent returns a final answer or hits a limit.

### Tool Calling

Tools should be treated as typed interfaces, not loose strings. Each tool needs:

- name
- description
- input schema
- output schema or documented return shape
- error behavior
- permission level

### Structured Outputs

The final answer should be machine-readable. That lets Level 2 evaluate the agent without scraping prose.

### State

The agent needs state for:

- task id
- user request
- tool calls
- observations
- intermediate decisions
- approval status
- final answer

### Human-in-the-loop

Human approval is required when the agent would take an action with financial, legal, privacy, or external side effects.

For Level 1, approval can be simulated with a local function.

## Reference Agent Loop

```python
def run_agent(task, tools, model, max_steps=8):
    state = {
        "task": task,
        "messages": [{"role": "user", "content": task}],
        "tool_calls": [],
    }

    for step in range(max_steps):
        response = model(state["messages"], tools=tools)

        if response.final_answer:
            state["final_answer"] = response.final_answer
            return state

        if response.tool_call:
            tool = tools[response.tool_call.name]
            args = validate(tool.schema, response.tool_call.arguments)
            observation = tool.run(**args)
            state["tool_calls"].append(response.tool_call)
            state["messages"].append({
                "role": "tool",
                "name": response.tool_call.name,
                "content": observation,
            })
            continue

        state["messages"].append({
            "role": "system",
            "content": "Return a final answer or call an available tool.",
        })

    state["error"] = "max_steps_exceeded"
    return state
```

This is intentionally simple. Production systems add retries, timeouts, tracing, persistence, policy checks, sandboxing, and observability.

## Module Plan

Read the full lesson sequence in [lessons/README.md](lessons/README.md).

| Lesson | Topic | Artifact |
| --- | --- | --- |
| 1 | What is an agent? | Minimal single-tool loop |
| 2 | Tool schemas and validation | Typed calculator tool |
| 3 | Search and retrieval | Policy search tool |
| 4 | State and traces | Trace JSONL output |
| 5 | Human approval | Approval gate for risky actions |
| 6 | Final answer contracts | Structured reimbursement recommendation |
| 7 | Hardening the harness | Timeouts, max steps, errors, retries |

## Labs

| Lab | Description | Reference solution |
| --- | --- | --- |
| [Lab 1: Minimal Agent Loop](labs/lab-01-minimal-agent-loop.md) | Build the smallest useful agent loop. | [`lab_01_minimal_agent_loop.py`](../../examples/acme-expense-agent/solutions/lab_01_minimal_agent_loop.py) |
| [Lab 2: Tool Schemas](labs/lab-02-tool-schemas.md) | Add typed tools and argument validation. | [`lab_02_tool_schemas.py`](../../examples/acme-expense-agent/solutions/lab_02_tool_schemas.py) |
| [Lab 3: Policy Search](labs/lab-03-policy-search.md) | Ground answers using a local policy corpus. | [`lab_03_policy_search.py`](../../examples/acme-expense-agent/solutions/lab_03_policy_search.py) |
| [Lab 4: Trace Capture](labs/lab-04-trace-capture.md) | Save trajectories for later evaluation. | [`lab_04_trace_capture.py`](../../examples/acme-expense-agent/solutions/lab_04_trace_capture.py) |

Write your own version before reading a solution. [How to compare](../../examples/acme-expense-agent/solutions/README.md).

## Working Implementation

A complete Level 1 system ships in [examples/acme-expense-agent/](../../examples/acme-expense-agent/). It runs offline with no API key:

```bash
cd examples/acme-expense-agent
python run_agent.py --all --quiet
python -m acme_agent.check_traces traces/level-1.jsonl
```

Use it as a reference and an argument to have, not as a template to copy. Its [known limitations](../../examples/acme-expense-agent/README.md#known-limitations) are listed deliberately, and finding more of them is Level 3 work.

Fixtures you can build against without inventing your own: nine policy sections, twelve receipts across three employees, and the twenty-two manual tasks in `fixtures/tasks.json`.

## Project

The Level 1 project is [Acme Expense Agent v1](project/acme-expense-agent-v1.md).

## Exit Criteria

To complete Level 1, the learner must submit:

1. A runnable agent harness.
2. At least three tools.
3. Typed tool schemas.
4. Structured final answers.
5. Trace logs for at least 20 manual tasks.
6. A short implementation note explaining tradeoffs and known limitations.

Check your own trace bundle before submitting:

```bash
python -m acme_agent.check_traces path/to/your/traces.jsonl
```

It fails with the trace id and the field name, so "invalid trace" is never the whole message.

The agent should handle multi-step tasks such as:

```text
I flew to Denver for a customer meeting, paid $47 for airport parking,
spent $68 on dinner, and lost the hotel receipt. What can I reimburse,
and what needs manager approval?
```

The expected answer should include:

- reimbursable items
- non-reimbursable items
- missing information
- approvals required
- policy citations
- confidence
- next action
