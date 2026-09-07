# Lesson 6: Failure Reports

## Core Idea

A failure report should help the next engineer improve the system.

## Report Structure

1. Summary
2. Benchmark run analyzed
3. Failure taxonomy
4. Failure distribution
5. Representative traces
6. Hypotheses
7. Interventions tested
8. Results
9. Remaining risks
10. Data recommendations for Level 4

## Common Failure Modes

- Listing failures without prioritizing them.
- Making recommendations that do not follow from counts or severity.
- Omitting uncertainty about ambiguous tasks.

## Exercise

What should a failure report recommend after finding receipt lookup is the dominant failure?

Check your answer:

```text
Fix receipt lookup first, add regression cases for those failures, and rerun the full benchmark before claiming broader improvement.
```

Use the annotated failure bundle to confirm the answer against the diagnosis workflow rather than relying on memory.

## Checkpoint

You are ready to complete Level 3 when your report explains what to fix next and why.
