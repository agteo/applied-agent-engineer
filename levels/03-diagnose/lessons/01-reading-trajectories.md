# Lesson 1: Reading Trajectories

## Core Idea

The final answer is not enough. To diagnose an agent, inspect the path it took.

## What To Inspect

- user task
- system and prompt version
- retrieved context
- tool selected
- tool arguments
- tool observation
- model interpretation
- final answer
- grader result

## Failure Timeline

Mark the first point where the trajectory went wrong. Later mistakes often cascade from the first error.

## Common Failure Modes

- Starting from the final answer instead of the first wrong transition.
- Ignoring observations and blaming the model generically.
- Assuming a tool was correct because it returned successfully.

## Exercise

In a wrong-total trace, what do you inspect before editing the prompt?

Check your answer:

```text
Inspect tool calls, arguments, observations, intermediate calculations, and the first step where expected and actual behavior diverge.
```

Use the annotated failure bundle to confirm the answer against the diagnosis workflow rather than relying on memory.

## Checkpoint

You are ready to move on when you can identify the earliest visible failure in a trace.
