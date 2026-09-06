# Project: Agent Training Dataset v1

## Objective

Create a curated dataset for improving Acme Expense Agent behavior.

## Required Sources

- Level 1 traces
- Level 2 benchmark failures
- Level 3 failure labels
- human corrections
- synthetic examples targeting known gaps

## Required Outputs

- raw data manifest: [`datasets/acme/raw.jsonl`](../../../datasets/acme/raw.jsonl)
- cleaned dataset: [`datasets/acme/cleaned.jsonl`](../../../datasets/acme/cleaned.jsonl)
- rejected rows: [`datasets/acme/rejected.jsonl`](../../../datasets/acme/rejected.jsonl)
- train split: [`datasets/acme/train.jsonl`](../../../datasets/acme/train.jsonl)
- development split: [`datasets/acme/dev.jsonl`](../../../datasets/acme/dev.jsonl)
- held-out split: [`datasets/acme/heldout.jsonl`](../../../datasets/acme/heldout.jsonl)
- quality metrics: [`datasets/acme/metrics.json`](../../../datasets/acme/metrics.json)
- schema: [`datasets/acme/schema.json`](../../../datasets/acme/schema.json)
- dataset card: [`datasets/acme/dataset-card.md`](../../../datasets/acme/dataset-card.md)
- synthetic generation note: [`datasets/acme/synthetic-generation.md`](../../../datasets/acme/synthetic-generation.md)

Build the reference dataset:

```bash
python3 -m datasets.acme
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
