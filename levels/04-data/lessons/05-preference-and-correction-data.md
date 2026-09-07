# Lesson 5: Preference and Correction Data

## Core Idea

Failures can become demonstrations, corrections, or preference pairs.

## Data Shapes

Demonstration:

```text
task -> ideal answer
```

Correction:

```text
bad answer -> corrected answer
```

Preference:

```text
task + answer A + answer B -> preferred answer
```

## Common Failure Modes

- Saving only the preferred answer and losing the rejected answer.
- Treating all corrections as equally reliable.
- Training on benchmark corrections without split controls.

## Exercise

What extra field does a correction example need beyond the target answer?

Check your answer:

```text
It needs the rejected or original bad answer, plus provenance linking the correction to the failure annotation.
```

Use the Acme training dataset to confirm the answer against the data workflow rather than relying on memory.

## Checkpoint

You are ready to move on when each example type has a clear use in Level 5.
