# Lesson 5: Preference Optimization

## Core Idea

Preference optimization uses comparisons, not just ideal answers.

## Concepts

- preferred vs rejected answers
- DPO
- reward models
- pair quality
- annotator consistency
- failure modes from bad preferences

## Level 5 Scope

This lesson is conceptual unless the learner has enough preference data from Level 4.

## Common Failure Modes

- Creating preference pairs where both answers are bad.
- Rewarding style over task success.
- Using preferences before hard verifiers catch safety failures.

## Exercise

What makes a StrongBench preference pair useful?

Check your answer:

```text
The chosen answer must be better for a named reason such as correct approval handling, grounded policy citation, or correct total.
```

Use the Phase 5 decision memo to confirm the answer against the model-improvement workflow rather than relying on memory.

## Checkpoint

You are ready to move on when you can decide whether your dataset supports preference optimization.
