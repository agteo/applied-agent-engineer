# Lab 1: Minimal Agent Loop

## Objective

Build the smallest useful agent loop: a model call that can either answer directly or call one tool and use the observation in a follow-up answer.

## Build

Create a script that supports this flow:

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

The lab passes if:

- the loop stops correctly
- the tool call is executed only when needed
- the final answer uses the tool result when a tool was called
- the trace records the model response, tool call, observation, and final answer

