# Datasets

This folder contains the Level 4 Acme Agent Training Dataset v1 builder and
generated artifacts.

Build the dataset with no API key:

```bash
python3 -m datasets.acme
```

The command reads Level 1 traces and Level 3 failure annotations, adds
synthetic gap-targeted examples, filters low-quality rows, and writes:

```text
datasets/
  acme/
    raw.jsonl
    cleaned.jsonl
    rejected.jsonl
    train.jsonl
    dev.jsonl
    heldout.jsonl
    metrics.json
    schema.json
    dataset-card.md
    synthetic-generation.md
```

Current output: 155 raw rows, 152 cleaned rows, 3 rejected rows, and separate
train/dev/heldout splits. Benchmark-derived failure corrections are kept out of
the train split to reduce contamination risk.

Start with [../levels/04-data/README.md](../levels/04-data/README.md). The
dataset-card assessment anchor is in
[`examples/reference-artifacts/dataset-card/`](../examples/reference-artifacts/dataset-card/).
