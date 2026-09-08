# Lab 1: Minimal Agent Loop

## Objective

Build the smallest useful agent loop: a model call that can either answer directly or call one tool and use the observation in a follow-up answer.

## Run this in the browser

Open the [Lab 1 browser workspace](#/levels/01-build/labs/lab-01/workspace) to edit and run your starter code without a local Python setup. The local command below remains available for comparison.

## Build

Start from the learner file:

```bash
cd examples/strongbench-expense-agent
python3 checks/lab_01.py starters/lab_01_minimal_agent_loop.py
```

Complete the TODOs until the same command passes. Your script should support this flow:

```text
User task
  |
  v
Model decides whether to call a tool
  |
  +-- no tool -> final answer
  |
  +-- tool call -> execute tool -> send observation back to model -> final answer
```

## Required Tool

Implement a calculator tool.

Input:

```json
{
  "expression": "47 + 68"
}
```

Output:

```json
{
  "result": 115
}
```

## Test Tasks

Use at least these tasks:

1. "What is 47 plus 68?"
2. "I spent $47 on parking and $68 on dinner. What is the total?"
3. "Explain whether dinner is reimbursable." 

The third task should not call the calculator unless calculation is needed.

## Deliverable

Submit:

- agent loop code
- calculator tool code
- three example traces
- a short note describing when the agent calls the tool

## Checks

Run the deterministic grader:

```bash
cd examples/strongbench-expense-agent
python3 checks/lab_01.py starters/lab_01_minimal_agent_loop.py
```

The grader checks that:

- the loop stops correctly
- the tool call is executed only when needed
- the final answer uses the tool result when a tool was called
- the trace records the model response, tool call, observation, and final answer
- the calculator rejects unsafe expressions instead of evaluating arbitrary code

## Reference Solution

Write your own version first, then compare: [`solutions/lab_01_minimal_agent_loop.py`](../../../examples/strongbench-expense-agent/solutions/lab_01_minimal_agent_loop.py).

```bash
cd examples/strongbench-expense-agent
python3 checks/lab_01.py solutions/lab_01_minimal_agent_loop.py
python3 solutions/lab_01_minimal_agent_loop.py
```

It is standalone by design: no imports from the harness, because Lab 1's point is that an agent loop is about forty lines and no framework. [How to compare](../../../examples/strongbench-expense-agent/solutions/README.md).
