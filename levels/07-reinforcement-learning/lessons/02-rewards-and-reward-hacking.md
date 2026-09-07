# Lesson 2: Rewards and Reward Hacking

## Core Idea

The agent may optimize the reward instead of the real goal.

## Reward Hacking Examples

- requesting approval for every task to avoid unsafe submission penalties
- refusing too often because refusal is safer than action
- creating drafts with minimal content if draft creation is rewarded
- stopping early to avoid invalid-action penalties

## Review Questions

- What behavior does this reward encourage?
- What useful behavior does it ignore?
- How could the agent get high reward while failing the user?
- Which metrics should catch the exploit?

## Common Failure Modes

- Assuming a reward component cannot be exploited.
- Failing to create a negative-control policy.
- Using reward improvement as the only adoption gate.

## Exercise

What does the weak_submitter policy prove?

Check your answer:

```text
It proves the verifier/reward setup catches unsafe submission shortcuts rather than giving credit for fast terminal actions.
```

Use the Phase 7 experiment report to confirm the answer against the RL reliability workflow rather than relying on memory.

## Checkpoint

You are ready to move on when every reward component has a known exploit risk.
