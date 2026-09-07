# Lesson 1: RL Framing

## Core Idea

Reinforcement learning frames behavior as interaction between an agent and an environment.

## Concepts

- state
- action
- observation
- reward
- policy
- episode
- return
- termination

## StrongBench Example

```text
State:
Employee trip, receipts, policy, draft status.

Action:
Request manager approval.

Reward:
Positive if approval was required and requested, negative if unnecessary or missing.
```

## Common Failure Modes

- Calling every optimization problem RL without defining state/action/reward.
- Optimizing reward without a termination rule.
- Ignoring that the policy acts through tools, not just tokens.

## Exercise

Frame one StrongBench simulator task as state, action, reward, and termination.

Check your answer:

```text
State is finance records; actions are simulator tools; reward is verifier-derived; termination is final_answer or truncation.
```

Use the Phase 7 experiment report to confirm the answer against the RL reliability workflow rather than relying on memory.

## Checkpoint

You are ready to move on when you can map a StrongBench task to state, action, reward, and termination.
