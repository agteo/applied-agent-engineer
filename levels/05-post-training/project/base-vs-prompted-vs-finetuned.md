# Project: Base vs Prompted vs Fine-tuned

## Objective

Compare whether post-training improves StrongBench Expense Agent behavior enough to justify adoption.

This project completes Track 5B. Learners who only complete a model strategy memo have completed Track 5A, not post-training implementation.

## Required Systems

Compare at least three:

- base model
- prompted baseline
- frontier API model
- fine-tuned or LoRA-adapted model

Reference Phase 5A artifacts:

- decision memo: [`model_improvement/strongbench/decision-memo.md`](../../../model_improvement/strongbench/decision-memo.md)
- comparison report: [`model_improvement/strongbench/comparison-report.md`](../../../model_improvement/strongbench/comparison-report.md)
- SFT train data: [`model_improvement/strongbench/sft-train.jsonl`](../../../model_improvement/strongbench/sft-train.jsonl)
- SFT dev data: [`model_improvement/strongbench/sft-dev.jsonl`](../../../model_improvement/strongbench/sft-dev.jsonl)
- optional LoRA config: [`model_improvement/strongbench/lora-config.template.json`](../../../model_improvement/strongbench/lora-config.template.json)
- dry-run validator: `python3 -m model_improvement.strongbench.train_lora --dry-run`

## Required Metrics

Use the Level 2 benchmark and report:

- task success
- success by category
- structured output validity
- policy citation accuracy
- approval safety
- cost if available
- latency if available
- failure distribution

## Assessment Anchor

Compare your adoption decision against the model-improvement examples and
rubric in
[`examples/reference-artifacts/model-improvement-decision/`](../../../examples/reference-artifacts/model-improvement-decision/).

## Submission Checklist

- [ ] Training decision memo complete.
- [ ] Training data documented.
- [ ] Training config documented.
- [ ] Optional LoRA config dry-run passes.
- [ ] Adapter or checkpoint artifact produced.
- [ ] Training logs included.
- [ ] Model comparison run on same benchmark.
- [ ] Regressions inspected.
- [ ] Recommendation explains adoption decision.
