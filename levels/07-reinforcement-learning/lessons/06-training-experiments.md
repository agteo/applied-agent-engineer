# Lesson 6: Training Experiments

## Core Idea

An RL experiment needs the same discipline as every previous module: versioning, measurement, diagnosis, and honest limitations.

## Experiment Record

Record:

- base model
- environment version
- reward version
- rollout source
- training method
- hyperparameters
- compute budget
- evaluation benchmark
- stopping criteria

## Common Failure Modes

- Skipping baseline eval before training.
- Changing task distribution between train and evaluation.
- Reporting learning curves without sampled rollout review.

## Exercise

List the minimum evidence for an RL training claim.

Check your answer:

```text
Baseline eval, training logs, reward curves, heldout simulator eval, Level 2 benchmark regression check, and sampled rollout review.
```

Use the Phase 7 experiment report to confirm the answer against the RL reliability workflow rather than relying on memory.

## Checkpoint

You are ready to move on when another engineer can reproduce or critique the experiment.
