# Lab 3: LoRA Experiment

## Objective

Configure a LoRA run, validate its inputs, and — if you have the hardware — run
it and report it honestly.

**This lab has two completion paths.** The dry-run path requires no GPU and is a
complete deliverable. The training path requires hardware and is optional. Do not
attempt the second without the prerequisites in Lesson 2.

## Build

Write a config that is a specification, not a settings file:

```json
{"method": "LoRA", "base_model": "<your choice>",
 "hyperparameters": {"lora_rank": 8, "lora_alpha": 16, "epochs": 1,
                     "learning_rate": 2e-4, "max_sequence_length": 2048},
 "dataset": {"train": "...", "train_rows": 78, "dev": "...", "dev_rows": 47},
 "compute_estimate": {"reference_gpu": "...", "expected_runtime": "..."},
 "status": "template_not_run",
 "required_evidence_before_claiming_completion": [...]}
```

Four fields that are not hyperparameters and matter more than most of them:

- **`status`** — so a committed config cannot be mistaken for a record.
- **`compute_estimate`** — cost as a decision input, not a mid-run surprise.
- **`dataset` row counts** — so a dry run can detect a config describing a
  dataset that no longer exists.
- **`required_evidence_before_claiming_completion`** — written before the run.

**Size the adapter to the data.** Rank 8 against 78 rows is the honest pairing;
rank 64 memorises them, and training loss will look excellent while the benchmark
does not move. If raising rank improves a metric, the constraint you are hitting
is data.

**Measure your longest row against `max_sequence_length`.** Silent truncation
removes the end of the target, which is where the answer lives.

## Deliverable

**Dry-run path (no GPU):** the config, a dry-run validator, and a written
prediction of what the run would show and what would make you reject it.

**Training path (optional):** additionally training logs, an adapter artifact,
a Level 2 benchmark comparison, and the `unsafe_submission` slice.

## Checks

```bash
# 1. The config declares what it needs to.
python3 - <<'PY'
import json
c = json.load(open("path/to/your/lora-config.json"))
for k in ("status", "compute_estimate", "dataset",
          "required_evidence_before_claiming_completion"):
    print(f"  {'OK ' if k in c else 'MISSING'} {k}")
PY

# 2. The dry run catches a config that disagrees with its data.
python3 path/to/your_train_lora.py --dry-run          # expect: ready
# now edit train_rows to a wrong number, then:
python3 path/to/your_train_lora.py --dry-run          # expect: blocked, naming the mismatch
```

The dry-run path passes when your validator reports ready on a correct config
and **refuses on a wrong row count, naming which number disagreed**. A dry run
is a contract check between config and data; it cannot tell you the run will
learn anything and should not pretend to.

The training path passes only with all four evidence artifacts. Reward or loss
improvement alone is not a result.

## Reference

Compare against
[`lora-config.template.json`](../../../model_improvement/strongbench/lora-config.template.json)
and
[`train_lora.py`](../../../model_improvement/strongbench/train_lora.py).

```bash
python3 -m model_improvement.strongbench.train_lora --dry-run
```

Note `"status": "template_not_run"` and the four required evidence items. The
fourth — the `unsafe_submission` slice, checked separately from the aggregate —
is the one teams omit, and it exists because the adoption gate is a conjunction.
