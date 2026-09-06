# Model Improvement

This folder contains the executable Level 5A model-improvement decision
workflow and Track 5B/5C preparation artifacts.

Build the Acme bundle with no API key:

```bash
python3 -m model_improvement.acme
```

The command consumes:

- the Level 2 benchmark
- the Level 3 failure distribution
- the Level 4 cleaned dataset

It writes:

```text
model_improvement/
  acme/
    decision-memo.md
    decision.json
    comparison-report.md
    intervention-matrix.json
    sft-train.jsonl
    sft-dev.jsonl
    sft-rejected.jsonl
    sft-schema.json
    metrics.json
    lora-config.template.json
    gateway-plan.json
```

Validate the optional LoRA config without running training:

```bash
python3 -m model_improvement.acme.train_lora --dry-run
```

Core Phase 5 does not claim that a model was trained. Track 5B completion still
requires real training logs, an adapter or checkpoint artifact, and a Level 2
benchmark comparison.
