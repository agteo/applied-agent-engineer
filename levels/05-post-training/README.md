# Level 5: Post-training

## Goal

Evaluate whether changing the model improves the agent more than prompting, tooling, retrieval, or harness changes.

Level 4 asked: what data could help the system improve?

Level 5 asks: should we use that data to adapt a model?

## Learning Outcomes

By the end of this level, learners can:

1. Explain when fine-tuning is appropriate and when it is not.
2. Prepare chat-style supervised fine-tuning data.
3. Run a small LoRA or QLoRA experiment.
4. Understand learning rate, batch size, checkpoints, and overfitting.
5. Compare base, prompted, frontier, and adapted models on the same benchmark.
6. Interpret whether the model improvement is worth the operational tradeoff.

## Required Build

Learners run a small post-training experiment using Agent Training Dataset v1 and evaluate the result on the Level 2 benchmark.

## Comparison

```text
Base model
Prompted baseline
Frontier API baseline
Fine-tuned or adapted model
        |
        v
Same Level 2 benchmark
```

## Module Plan

Read the full lesson sequence in [lessons/README.md](lessons/README.md).

| Lesson | Topic | Artifact |
| --- | --- | --- |
| 1 | When to train | Decision memo |
| 2 | ML foundations | Training notes |
| 3 | SFT data preparation | Training JSONL |
| 4 | LoRA and QLoRA | Adapter run |
| 5 | Preference optimization | DPO concept plan |
| 6 | Evaluation after training | Comparison report |

## Labs

| Lab | Description |
| --- | --- |
| [Lab 1: Training Decision](labs/lab-01-training-decision.md) | Decide whether model adaptation is justified. |
| [Lab 2: Prepare SFT Data](labs/lab-02-prepare-sft-data.md) | Convert Level 4 data into chat training format. |
| [Lab 3: LoRA Experiment](labs/lab-03-lora-experiment.md) | Run or simulate a small adapter experiment. |
| [Lab 4: Model Comparison](labs/lab-04-model-comparison.md) | Compare systems on the Level 2 benchmark. |

## Project

The Level 5 project is [Base vs Prompted vs Fine-tuned](project/base-vs-prompted-vs-finetuned.md).

## Exit Criteria

To complete Level 5, the learner must submit:

1. A training decision memo.
2. Training data derived from Level 4.
3. Training configuration or experiment plan.
4. Evaluation results on the Level 2 benchmark.
5. A comparison report.
6. A recommendation explaining whether to adopt the adapted model.

