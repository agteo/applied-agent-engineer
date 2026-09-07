# Lesson 5: Metrics and Confidence

## Core Idea

Scores need uncertainty. A benchmark result without context can mislead.

## Core Metrics

For Level 2, report:

- task success rate
- structured output validity
- policy citation accuracy
- approval safety rate
- tool-call correctness
- average cost
- p50 and p95 latency
- judge and human agreement

## Slices

Aggregate scores hide failure modes. Slice by:

- task category
- difficulty
- required tool
- ambiguity
- approval requirement
- agent version
- model

## Confidence

Small eval sets are noisy. Report sample size and avoid overclaiming.

Useful habits:

- show numerator and denominator
- report confidence intervals where appropriate
- avoid declaring tiny differences meaningful
- inspect examples behind metric changes

## Common Failure Modes

- Reporting only overall success and hiding weak slices.
- Treating a small sample as precise.
- Ignoring cost or latency when comparing configurations.

## Exercise

A benchmark passes 89/100 tasks. What success rate should the report show?

Check your answer:

```text
It should show `0.890` or `89%`, and it should still include per-tag breakdowns because the overall number hides weak slices.
```

Use the Level 2 benchmark report to confirm the answer against the evaluation system rather than relying on memory.

## Checkpoint

You are ready to move on when your report can distinguish a real improvement from noise.
