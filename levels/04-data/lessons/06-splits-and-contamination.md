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

## Common Failure Modes

- Training on heldout benchmark answers.
- Choosing splits randomly after seeing evaluation results.
- Letting duplicate prompts appear across train and heldout.

## Exercise

Why does Phase 5 reject heldout rows from SFT export?

Check your answer:

```text
Heldout rows are reserved for evaluation. Training on them would contaminate the measurement used to decide whether the model improved.
```

Use the Acme training dataset to confirm the answer against the data workflow rather than relying on memory.

## Checkpoint

You are ready to move on when every example has a split and no held-out eval task appears in training data.
