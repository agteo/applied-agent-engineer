# Lesson 6: Regression Evaluation

## Core Idea

Every agent change is a hypothesis. Regression evals test whether the hypothesis helped.

## Compare Versions

Compare at least two configurations:

- baseline prompt vs revised prompt
- old tool schema vs new tool schema
- keyword search vs improved retrieval
- cheaper model vs stronger model
- no approval gate vs approval gate

## Version Metadata

Each run should record:

- agent version
- prompt version
- model
- tool versions
- retrieval corpus version
- eval dataset version
- timestamp

## Decision Rule

Before running the eval, define what improvement would justify adopting the new version.

Example:

```text
Adopt version B if task success improves by at least 8 percentage points,
approval safety does not decrease, and average cost increases by less than 20%.
```

## Checkpoint

You are ready to move on when every benchmark run can be compared to a previous run.

