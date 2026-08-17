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

## Checkpoint

You are ready to move on when your report can distinguish a real improvement from noise.

