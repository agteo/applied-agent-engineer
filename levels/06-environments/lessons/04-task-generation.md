# Lesson 4: Task Generation

## Core Idea

Generated tasks let agents practice many variations of the same workflow.

## Task Generator Inputs

- employee profile
- trip record
- receipt records
- policy constraints
- difficulty
- target failure mode

## Task Metadata

Each task should include:

- task id
- user request
- initial state seed
- expected actions
- success condition
- difficulty
- known edge cases

## Common Failure Modes

- Generating many tasks that are surface variants of one easy case.
- Using random seeds but not recording them.
- Creating tasks without expected outcomes.

## Exercise

What does each generated simulator task need for reproducibility?

Check your answer:

```text
It needs task id, seed, category/tags, initial state reference, prompt/action context, and expected outcome.
```

Use the StrongBench Finance rollout to confirm the answer against the environment simulator rather than relying on memory.

## Checkpoint

You are ready to move on when generated tasks have known outcomes and reproducible initial states.
