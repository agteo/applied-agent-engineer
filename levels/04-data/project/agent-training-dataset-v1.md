# Project: Agent Training Dataset v1

## Objective

Create a curated dataset for improving StrongBench Expense Agent behavior.

## Required Sources

- Level 1 traces
- Level 2 benchmark failures
- Level 3 failure labels
- human corrections
- synthetic examples targeting known gaps

## Required Outputs

- raw data manifest: [`datasets/strongbench/raw.jsonl`](../../../datasets/strongbench/raw.jsonl)
- cleaned dataset: [`datasets/strongbench/cleaned.jsonl`](../../../datasets/strongbench/cleaned.jsonl)
- rejected rows: [`datasets/strongbench/rejected.jsonl`](../../../datasets/strongbench/rejected.jsonl)
- train split: [`datasets/strongbench/train.jsonl`](../../../datasets/strongbench/train.jsonl)
- development split: [`datasets/strongbench/dev.jsonl`](../../../datasets/strongbench/dev.jsonl)
- held-out split: [`datasets/strongbench/heldout.jsonl`](../../../datasets/strongbench/heldout.jsonl)
- quality metrics: [`datasets/strongbench/metrics.json`](../../../datasets/strongbench/metrics.json)
- schema: [`datasets/strongbench/schema.json`](../../../datasets/strongbench/schema.json)
- dataset card: [`datasets/strongbench/dataset-card.md`](../../../datasets/strongbench/dataset-card.md)
- synthetic generation note: [`datasets/strongbench/synthetic-generation.md`](../../../datasets/strongbench/synthetic-generation.md)

Build the reference dataset:

```bash
python3 -m datasets.strongbench
```

## Assessment Anchor

Compare your dataset card against the examples and rubric in
[`examples/reference-artifacts/dataset-card/`](../../../examples/reference-artifacts/dataset-card/).

## Submission Checklist

- [ ] Schema documented.
- [ ] Provenance included for every example.
- [ ] Low-quality rows filtered.
- [ ] Duplicates removed or labeled.
- [ ] Held-out benchmark protected.
- [ ] Dataset card complete.
- [ ] Level 5 training use case documented.
