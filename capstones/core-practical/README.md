# Core Capstone: Applied AI Systems Practical

## Status

This capstone is the required final assessment for Levels 1-4.

It should be executable without a GPU.

## Objective

Improve a flawed Acme Expense Agent using the core loop:

```text
Build -> Evaluate -> Diagnose -> Data Recommendation
```

## Scenario

You are given:

- a flawed Acme Expense Agent implementation
- policy, receipt, employee, and trip fixtures
- a benchmark subset
- traces from failed runs
- grader outputs

Your job is to identify one meaningful failure mode, make a targeted improvement, rerun the benchmark, and explain what changed.

## Required Work

1. Run the provided benchmark.
2. Inspect failed traces.
3. Identify a dominant failure mode.
4. Implement one targeted fix.
5. Rerun the benchmark.
6. Compare before and after results.
7. Write a diagnosis and recommendation memo.

## Required Artifacts

- code changes
- benchmark before and after
- trace samples
- failure diagnosis
- intervention explanation
- data recommendation for the next improvement cycle

## Grading Shape

| Area | Weight |
| --- | --- |
| Agent runs and produces valid outputs | 20% |
| Eval run and metrics are correct | 20% |
| Failure diagnosis is evidence-backed | 25% |
| Intervention targets the diagnosis | 20% |
| Recommendation is practical and honest | 15% |

## Not Required

- GPU access
- model fine-tuning
- RL training
- production deployment

