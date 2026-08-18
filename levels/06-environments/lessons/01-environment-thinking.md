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

## Reading

- [tau2-bench](https://github.com/sierra-research/tau2-bench) — the closest published relative of what Level 6 asks you to build: a domain with a written policy, simulated tools, generated tasks, and per-task success criteria. Read its domain definitions before designing Acme Corp Simulator, then note where you are deliberately building something smaller.
- [WebArena](https://github.com/web-arena-x/webarena) — a self-hostable environment for the harder case, where the environment is a real application rather than a state machine you wrote.
