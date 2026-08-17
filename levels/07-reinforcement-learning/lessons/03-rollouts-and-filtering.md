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

## Checkpoint

You are ready to move on when rollout data is clean enough to train or analyze.

