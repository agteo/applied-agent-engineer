# Lesson 6: Splits and Contamination

## Core Idea

Training data must not leak into trusted evaluation data.

## Splits

Use:

- train
- development
- held-out evaluation

Keep the Level 2 reporting benchmark protected.

## Contamination Risks

- generating training examples from held-out tasks
- copying expected answers into prompts
- tuning repeatedly against the final eval set
- mixing duplicate examples across splits

## Checkpoint

You are ready to move on when every example has a split and no held-out eval task appears in training data.

