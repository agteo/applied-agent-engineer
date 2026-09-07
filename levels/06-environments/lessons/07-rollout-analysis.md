# Lesson 7: Rollout Analysis

## Core Idea

Rollouts are trajectories collected from agent-environment interaction.

They are useful for evaluation, diagnosis, data generation, and reinforcement learning.

## Rollout Record

Each rollout should include:

- task
- initial state
- actions
- observations
- rewards
- final state
- termination reason
- success label
- trace metadata

## Analysis

Analyze rollouts by:

- success rate
- average reward
- termination reason
- invalid actions
- approval errors
- common state transitions
- failure category

## Common Failure Modes

- Looking only at total reward and ignoring component failures.
- Keeping rollouts without actions or observations.
- Failing to compare strong and weak policies.

## Exercise

What fields should a rollout contain before Level 7 uses it?

Check your answer:

```text
Actions, observations, verifier outputs, reward components, terminal state or hash, policy id, seed, and termination reason.
```

Use the StrongBench Finance rollout to confirm the answer against the environment simulator rather than relying on memory.

## Checkpoint

You are ready to complete Level 6 when your rollouts can feed Level 7 training experiments.
