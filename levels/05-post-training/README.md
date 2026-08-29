# Level 5: Model Improvement, Post-training, and Local Inference

## Goal

Evaluate whether changing the model is justified, then optionally run a real post-training experiment or operate a local inference stack.

Level 4 asked: what data could help the system improve?

Level 5 asks: should we use that data to adapt a model, and if yes, can the adapted model beat the alternatives on the same benchmark? If the system uses local or open models, can it serve them reliably enough for an agent to depend on them?

## Track Split

Level 5 has three tracks:

| Track | Required For | Outcome |
| --- | --- | --- |
| 5A Model Improvement Decisions | All learners continuing past Level 4 | Decide whether to use prompting, retrieval, tooling, frontier APIs, or local model adaptation. |
| 5B Post-training Implementation | Optional ML training track | Run SFT/LoRA with real compute and evaluate the adapted model. |
| 5C Local Inference Operations | Optional serving and platform track | Deploy a local or open model behind a gateway with routing, fallback, and observability. |

Completing Track 5A does not mean the learner has trained a model. Completing Track 5B requires an actual training run, a produced artifact, and benchmark comparison.

Completing Track 5C does not require training a model. It requires a working serving stack and a resilience report showing how the agent behaves when local inference is unavailable.

## Learning Outcomes

By the end of this level, learners can:

1. Explain when fine-tuning is appropriate and when it is not.
2. Prepare chat-style supervised fine-tuning data.
3. Estimate compute, cost, serving, and governance tradeoffs.
4. Run a small LoRA or QLoRA experiment if completing Track 5B.
5. Understand learning rate, batch size, checkpoints, and overfitting.
6. Compare base, prompted, frontier, and adapted models on the same benchmark.
7. Interpret whether the model improvement is worth the operational tradeoff.
8. Route agent traffic through a local inference gateway with health checks and fallback behavior.
9. Measure local inference latency, throughput, error rate, and resource saturation.

## Required Build

Track 5A learners produce a model improvement decision memo.

Track 5B learners run a small post-training experiment using Agent Training Dataset v1 and evaluate the result on the Level 2 benchmark.

Track 5C learners run the Acme Expense Agent through a local inference gateway and demonstrate reliable fallback when the local worker fails.

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
| 7 | Local inference operations | Resilient serving plan |

## Labs

| Lab | Description |
| --- | --- |
| [Lab 1: Training Decision](labs/lab-01-training-decision.md) | Decide whether model adaptation is justified. |
| [Lab 2: Prepare SFT Data](labs/lab-02-prepare-sft-data.md) | Convert Level 4 data into chat training format. |
| [Lab 3: LoRA Experiment](labs/lab-03-lora-experiment.md) | Run a small adapter experiment for Track 5B. |
| [Lab 4: Model Comparison](labs/lab-04-model-comparison.md) | Compare systems on the Level 2 benchmark. |
| [Lab 5: Gateway Failover Drill](labs/lab-05-gateway-failover-drill.md) | Route the agent through a gateway and verify fallback behavior. |

## Projects

The Track 5B project is [Base vs Prompted vs Fine-tuned](project/base-vs-prompted-vs-finetuned.md).

The Track 5C project is [Resilient Local Inference Stack](project/resilient-local-inference-stack.md).

## Exit Criteria

To complete Track 5A, the learner must submit:

1. A training decision memo.
2. Evidence from Level 2-4.
3. Data sufficiency assessment.
4. Cost, latency, privacy, and deployment tradeoffs.
5. A recommendation explaining whether to train, use a frontier API, improve retrieval, improve tools, or keep a hybrid stack.

To complete Track 5B, the learner must additionally submit:

1. Training data derived from Level 4.
2. Training configuration.
3. Completed training run logs.
4. Adapter or checkpoint artifact.
5. Evaluation results on the Level 2 benchmark.
6. A comparison report.

To complete Track 5C, the learner must additionally submit:

1. Gateway configuration.
2. Local serving command or container configuration.
3. Health check and fallback behavior notes.
4. Resilience test evidence.
5. Latency, throughput, error, and resource observations.
6. A recommendation explaining whether local, hosted, or hybrid inference should be adopted.
