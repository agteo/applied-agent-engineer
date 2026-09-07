# Lesson 1: What Is an Agent?

## Core Idea

An agent is not a model. An agent is a system that uses a model to decide what to do next.

A plain LLM call produces a response. An agent can inspect state, call tools, observe results, and continue until it reaches a stopping condition.

## Minimal Definition

For this curriculum, an agent has five parts:

1. A task from a user or system.
2. A model that decides what to do.
3. Tools the model can request.
4. State that records what has happened.
5. A stopping condition.

## Agent Loop

```text
Task
  |
  v
Model
  |
  +-- Final answer -> Stop
  |
  +-- Tool call -> Validate -> Execute -> Observe -> Model
```

## Common Failure Modes

- The model answers when it should use a tool.
- The model calls the right tool with wrong arguments.
- The tool works, but the model misreads the result.
- The loop continues after the task is complete.
- The harness hides the trace, so no one can diagnose what happened.

## Exercise

Take three tasks and label whether each requires:

- direct answer
- tool call
- retrieval
- human approval

Example:

```text
"Can I reimburse dinner during business travel?"
```

Likely requires retrieval because the answer depends on policy.

Check your answer:

```text
"Can I reimburse dinner during business travel?"  -> retrieval
    The answer lives in policy text, not in the model.

"What is 48.50 plus 91.00 against a USD 75 daily cap?"  -> tool call
    Arithmetic against a policy limit is a calculator job, not a guess.

"Submit Noah's expense report for him."  -> human approval
    policy-submission-001 reserves submission for the employee. The agent
    prepares the draft and stops.
```

A task can need more than one. The useful question is which capability the
task *starts* with, because that decides the agent's first action.

## Checkpoint

You are ready to move on when you can explain why an agent harness is responsible for reliability, not just the model.

