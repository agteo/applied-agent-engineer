# Lesson 4: RLHF and RLVR

## Core Idea

Modern LLM reinforcement learning often uses human preferences, verifiable rewards, or both.

## RLHF

Reinforcement Learning from Human Feedback uses human judgments or preference data to shape behavior.

## RLVR

Reinforcement Learning from Verifiable Rewards uses automatically checkable outcomes, such as correct math, passing tests, or successful environment tasks.

## Acme Fit

Acme Finance Operations Simulator is closer to RLVR when success checks are deterministic. Human review can supplement it when answer quality, clarity, or judgment is subjective.

## Common Failure Modes

- Using human preference when deterministic verification is available.
- Using verifier reward for subjective quality without calibration.
- Combining reward sources without logging components.

## Exercise

For Acme totals and approvals, should you prefer RLHF or RLVR-style rewards?

Check your answer:

```text
Prefer verifier-derived rewards for objective totals, state changes, and approval constraints; reserve human review for subjective answer quality.
```

Use the Phase 7 experiment report to confirm the answer against the RL reliability workflow rather than relying on memory.

## Checkpoint

You are ready to move on when you can decide which Acme outcomes are verifiable and which need human or rubric judgment.
