# Lesson 6: Evaluation After Training

## Core Idea

Training is not success. Benchmark improvement is success.

## Compare

Evaluate:

- base model
- prompted baseline
- frontier model if available
- adapted model

Use the same benchmark and report slices from Level 2.

## Watch For

- overfitting
- worse safety behavior
- citation degradation
- lower cost but worse quality
- improved common cases but worse edge cases

## Common Failure Modes

- Comparing a trained model on a different benchmark than the baseline.
- Ignoring regressions in rare but important slices.
- Adopting a model because one demo improved.

## Exercise

What benchmark must a trained StrongBench model rerun?

Check your answer:

```text
It must rerun the same Level 2 benchmark and include slice checks such as unsafe_submission and receipt_lookup.
```

Use the Phase 5 decision memo to confirm the answer against the model-improvement workflow rather than relying on memory.

## Checkpoint

You are ready to complete Level 5 when the adapted model has been judged by the same benchmark as the baseline.
