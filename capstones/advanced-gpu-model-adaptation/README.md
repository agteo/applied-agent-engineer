# Advanced Capstone: GPU Model Adaptation

## Status

This is an optional advanced capstone for learners completing the model-training track.

It requires GPU compute.

## Objective

Use curated proprietary-style data to adapt a local or open model, then evaluate whether the adapted model should be adopted.

## Core Question

```text
Does adapting a smaller local model improve the Acme Expense Agent enough
to justify the cost, complexity, and operational tradeoffs?
```

## Required Work

1. Select a suitable open model.
2. Prepare Level 4 training data in chat or instruction format.
3. Run a small SFT or LoRA experiment on a GPU.
4. Save training logs.
5. Produce an adapter or checkpoint artifact.
6. Evaluate the adapted model using the Level 2 benchmark.
7. Compare against the prompted baseline and a frontier/API baseline if available.
8. Write an adoption recommendation.

## Required Artifacts

- dataset version and dataset card
- train/validation split manifest
- training config
- hardware and cost notes
- training logs
- adapter or checkpoint
- benchmark results
- regression analysis
- adoption recommendation

## Minimum Completion Standard

This capstone is not complete without:

- a real training run
- training logs
- an adapter or checkpoint artifact
- benchmark comparison against the same eval set used by the baseline

A design-only memo can be valuable preparation, but it does not complete this capstone.

## GPU Guidance

Learners may use any suitable GPU environment, including:

- local workstation
- university or company GPU cluster
- cloud GPU VM
- managed notebook
- managed training platform

See [../../resources/gpu.md](../../resources/gpu.md).

## Grading Shape

| Area | Weight |
| --- | --- |
| Dataset preparation and leakage control | 20% |
| Training run and reproducibility | 25% |
| Benchmark comparison | 25% |
| Regression and failure analysis | 15% |
| Adoption recommendation | 15% |

## Cost And Safety Notes

Learners must document:

- GPU provider or hardware
- GPU type if known
- approximate runtime
- estimated cost
- model license
- data privacy assumptions

Do not train on real proprietary, private, or regulated data unless the learner has explicit authorization and an approved environment.

