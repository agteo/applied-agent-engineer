# Local Comparison Path: TRL

The hosted path is optional. If you want a training comparison without a Prime
account, TRL runs against the same local environment on a single GPU.

## Why this exists

Phase 7's claim is about *reliability*, not about a vendor. If the verifier and
reward contracts are real, they should drive a local trainer as well as a hosted
one. If they only work hosted, the contract was the vendor's, not yours.

## Shape of the run

```python
from strongbench_finance_reliability import load_environment

env = load_environment(seed=42, task_count=120)

# 1. Baseline: score the untrained policy with the local verifiers.
baseline = env.evaluate(my_policy)

# 2. Train. The reward function is env.reward(task_id, observations, terminal_state).
#    Use trl.GRPOTrainer with that as the reward, or SFT on the Phase 4 export
#    at model_improvement/strongbench/sft-train.jsonl.

# 3. Held-out eval: rebuild with a different seed so tasks are not the ones
#    trained on, then evaluate again.
heldout = load_environment(seed=7, task_count=120).evaluate(my_policy)
```

## What the trainer must not do

- Read `task["expected"]` — that is the grading key, not an observation.
- Train on the same seed it evaluates on. `load_environment(seed=...)` changes
  the task set; use a different one for held-out.
- Report reward improvement without the Level 2 benchmark regression check
  (`python3 -m evals.runner --model scripted`).

## Honest status

No TRL run has been performed in this repo. This file is a recipe, not a
result. The same evidence bar in [`VALIDATION.md`](VALIDATION.md) applies.
