# Lesson 6: Reproducibility and Realism

## Core Idea

An environment should be repeatable enough for science and realistic enough for engineering.

## Reproducibility

Record:

- environment version
- seed
- task generator version
- initial state
- tool versions
- reward version
- agent version

## Realism Risks

- tasks are too clean
- tool responses are too helpful
- policies are too short
- users are too explicit
- reward misses real business risk
- simulator permits impossible actions

## Common Failure Modes

- A simulator that is deterministic but unrealistic.
- A realistic simulator that cannot be replayed.
- Not documenting omitted production messiness.

## Exercise

Why does the simulator bias note matter?

Check your answer:

```text
It states what the simulator omits, so high simulator reward is not mistaken for production reliability.
```

Use the Acme Finance rollout to confirm the answer against the environment simulator rather than relying on memory.

## Checkpoint

You are ready to move on when another engineer can rerun the same episode and get the same environment behavior.
