# Lesson 1: Environment Thinking

## Core Idea

An environment is a world an agent can act in.

For agent engineering, environments let us test behavior safely, generate tasks, and collect trajectories without touching real systems.

## Environment Parts

- state
- actions
- observations
- transitions
- success checks
- rewards
- termination conditions

## Example

```text
State:
Employee has one Denver trip, three receipts, and no manager approval.

Action:
Agent drafts reimbursement request.

Observation:
Draft created, but hotel receipt is missing.

Reward:
Partial credit for correct items, penalty for missing approval.
```

## Checkpoint

You are ready to move on when you can describe the Acme expense domain as state, actions, and outcomes.

