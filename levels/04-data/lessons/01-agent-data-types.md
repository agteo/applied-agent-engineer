# Lesson 1: Agent Data Types

## Core Idea

Agent systems produce many kinds of useful data, not just prompt-response pairs.

## Data Types

- traces
- tool calls
- tool observations
- failed final answers
- corrected answers
- human demonstrations
- preference pairs
- rubric grades
- failure labels
- environment rollouts

## Common Failure Modes

- Mixing traces, demonstrations, corrections, and preferences in one undocumented file.
- Using final answers as training data without provenance.
- Treating production logs as safe training rows by default.

## Exercise

Classify a row with a bad answer and a corrected answer.

Check your answer:

```text
It is correction or preference data, not a plain demonstration, because it contains both rejected and target behavior.
```

Use the Acme training dataset to confirm the answer against the data workflow rather than relying on memory.

## Checkpoint

You are ready to move on when you can map each failure category to a useful data type.
