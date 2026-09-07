# Lesson 7: Dataset Cards

## Core Idea

A dataset card explains what the dataset is, where it came from, and how it should and should not be used.

## Required Sections

1. Summary
2. Intended use
3. Sources
4. Schema
5. Collection process
6. Cleaning and filtering
7. Quality metrics
8. Splits
9. Limitations
10. Licensing and privacy notes

## Common Failure Modes

- Claiming the dataset is useful without source counts.
- Omitting cleaning rules and rejected-row evidence.
- Leaving synthetic-data limitations unstated.

## Exercise

Name three facts the StrongBench dataset card must include.

Check your answer:

```text
It should include intended use, source counts, cleaning/rejection summary, split policy, contamination controls, and limitations.
```

Use the StrongBench training dataset to confirm the answer against the data workflow rather than relying on memory.

## Checkpoint

You are ready to complete Level 4 when another engineer can decide whether the dataset is safe and useful.
