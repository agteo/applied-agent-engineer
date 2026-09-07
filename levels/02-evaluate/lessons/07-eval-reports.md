# Lesson 7: Eval Reports

## Core Idea

An eval report should support a decision.

It should not just list scores. It should explain what changed, whether the measurement is trustworthy, and what to do next.

## Report Structure

Use this structure:

1. Decision summary
2. What was evaluated
3. Dataset description
4. Agent versions compared
5. Metrics
6. Key slices
7. Example wins and failures
8. Judge calibration
9. Limitations
10. Recommendation

## Good Recommendation

```text
Adopt version B for internal testing. It improves task success from 64/100
to 76/100 and fixes most missing-receipt failures. Do not release it broadly
yet because unsafe submission requests still pass approval checks in 3/12 cases.
```

## Weak Recommendation

```text
Version B seems better.
```

## Common Failure Modes

- Writing a narrative without a ship/hold decision.
- Reporting pass rate without threshold.
- Omitting failed task ids, making the report unactionable.

## Exercise

Name the minimum evidence an eval report needs before making a release recommendation.

Check your answer:

```text
It needs command/config, task count, pass rate, threshold, per-slice results, failures, calibration if a judge is used, and a recommendation.
```

Use the Level 2 benchmark report to confirm the answer against the evaluation system rather than relying on memory.

## Checkpoint

You are ready to complete Level 2 when your report gives enough evidence for another engineer to agree or disagree with your recommendation.
