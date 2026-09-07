# Lesson 4: Synthetic Data

## Core Idea

Synthetic data is useful when it targets known gaps and passes quality filters.

## Good Uses

Use synthetic data to:

- create variations of rare failures
- increase difficulty coverage
- generate clarifying-question cases
- create negative examples
- test policy edge cases

## Risks

- unrealistic examples
- duplicated patterns
- hidden leakage from eval tasks
- model-generated errors
- overfitting to the generator's style

## Common Failure Modes

- Generating examples that do not target known gaps.
- Letting synthetic examples leak into heldout evaluation.
- Claiming synthetic data proves model improvement.

## Exercise

Name one valid use and one invalid use of synthetic StrongBench examples.

Check your answer:

```text
Valid: target known receipt or approval gaps for training rehearsal. Invalid: claiming production improvement without heldout benchmark evidence.
```

Use the StrongBench training dataset to confirm the answer against the data workflow rather than relying on memory.

## Checkpoint

You are ready to move on when synthetic examples are labeled, filtered, and separated from held-out evals.
