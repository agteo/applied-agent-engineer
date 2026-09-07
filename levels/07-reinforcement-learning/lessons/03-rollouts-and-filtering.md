# Lesson 3: Rollouts and Filtering

## Core Idea

Training data from experience is only useful if the rollouts are valid, diverse, and correctly scored.

## Filter Rollouts

Filter or label:

- environment errors
- malformed actions
- reward function bugs
- duplicate trajectories
- trivial tasks
- unsafe behavior
- unclear termination

## Useful Rollout Sets

- successful demonstrations
- failed attempts with corrections
- preference pairs
- high-reward and low-reward contrast sets
- hard negative examples

## Common Failure Modes

- Training on rollouts with missing observations.
- Filtering only failures and keeping a biased dataset.
- Dropping termination reasons.

## Exercise

Why should incomplete rollouts be rejected?

Check your answer:

```text
Without actions, observations, verifier output, reward, and termination reason, the rollout cannot support learning or audit.
```

Use the Phase 7 experiment report to confirm the answer against the RL reliability workflow rather than relying on memory.

## Checkpoint

You are ready to move on when rollout data is clean enough to train or analyze.
