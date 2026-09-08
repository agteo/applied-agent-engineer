# Lesson 4: LoRA and QLoRA

## Core Idea

LoRA is a way of fine-tuning a model without updating most of it. Instead of
changing the base weights, you train small low-rank matrices alongside them and
add their output at inference time. QLoRA goes further: quantise the frozen base
to 4-bit so it fits in less memory, and train the adapter on top of that.

The practical consequence is what matters for an agent engineer. A full
fine-tune of a small instruct model needs multiple high-memory GPUs. A LoRA run
on the same model needs one 16–24GB card. That difference is what turns "we
would need to justify a training budget" into "someone can try it this
afternoon", which changes how you plan Level 5 entirely.

The second consequence is reversibility. An adapter is a separate artifact you
load or do not load. You can ship the base model, keep the adapter behind a
flag, compare them on the same benchmark, and roll back by not loading a file.
Full fine-tuning gives you a new model and a much worse rollback story.

## The Config Is The Experiment Design

[`lora-config.template.json`](../../../model_improvement/strongbench/lora-config.template.json)
is committed and unrun. Read it as a specification rather than a settings file:

```json
{"method": "LoRA",
 "base_model": "choose-small-instruct-model-locally",
 "hyperparameters": {"lora_rank": 8, "lora_alpha": 16, "epochs": 1,
                     "learning_rate": 0.0002, "max_sequence_length": 2048},
 "dataset": {"train": "...sft-train.jsonl", "train_rows": 78,
             "dev": "...sft-dev.jsonl",     "dev_rows": 47},
 "compute_estimate": {"reference_gpu": "single 16-24GB VRAM GPU for a small instruct model",
                      "expected_runtime": "minutes to low hours",
                      "ci_mode": "dry-run only"},
 "status": "template_not_run"}
```

Three fields do work that a hyperparameter file normally does not.

**`status: "template_not_run"`.** The artifact says of itself that it has never
been executed. Anyone finding this file cannot mistake it for a record of
something that happened — which is the standard failure mode of committed
configs.

**`compute_estimate`.** The hardware and runtime are stated before the run, so
the cost is a decision input rather than a surprise. A config that does not say
what it will cost invites someone to start it and find out.

**`required_evidence_before_claiming_completion`.** Four items, listed below.

## The Hyperparameters, Briefly

You do not need to be an RL researcher to read these, but you should know what
each one trades.

| Parameter | Value | What it controls |
| --- | ---: | --- |
| `lora_rank` | 8 | adapter capacity — higher fits more, overfits sooner |
| `lora_alpha` | 16 | scaling on the adapter's contribution, conventionally 2× rank |
| `epochs` | 1 | passes over the data |
| `learning_rate` | 2e-4 | far higher than full fine-tuning, because only the adapter moves |
| `max_sequence_length` | 2048 | truncation point; agent traces are long |

Rank 8 with 78 training rows is the honest pairing. **Small data wants a small
adapter.** Rank 64 on 78 examples memorises them, and the run will look
excellent on training loss and teach you nothing.

That ratio is worth internalising: adapter capacity should be sized to your data,
not to your ambition. If you find yourself raising rank to improve a metric, the
constraint you are hitting is data.

`max_sequence_length: 2048` deserves a check rather than trust. Agent training
rows contain a system prompt, a task, and a structured answer — measure your
longest row before assuming it fits, because silent truncation removes the end
of the target, which is where the answer usually is.

## The Dry Run Validates Inputs, Not Learning

```bash
python3 -m model_improvement.strongbench.train_lora --dry-run
```

`build_training_plan` runs a set of checks and returns
`"dry_run_ready"` or `"blocked_missing_inputs"`. It verifies the config has its
required keys, the dataset files exist, and the row counts match what the config
claims.

That last check is the useful one. If `train_rows: 78` and the file holds 74,
the config is describing a dataset that no longer exists — probably because
someone rebuilt it after a split change. Catching that before a GPU spins up is
the whole point, and it is a five-line check.

**A dry run is a contract check between your config and your data.** It cannot
tell you the run will learn anything, and it should not pretend to.

## Four Pieces Of Evidence Before Claiming Anything

```json
"required_evidence_before_claiming_completion": [
  "training logs",
  "adapter or checkpoint artifact",
  "Level 2 benchmark comparison",
  "unsafe_submission slice check"]
```

Written into the config, before the run, which is the point. Each closes a
specific way of overclaiming:

- **Training logs** — otherwise "we trained it" is unverifiable.
- **An adapter artifact** — a result with no reproducible weights is a story.
- **Level 2 comparison** — training loss is not capability; the benchmark is.
- **The `unsafe_submission` slice** — a model can improve overall and get worse
  at the safety-relevant behaviour, and the aggregate will not show it.

The fourth is the one teams omit. It exists because the adoption gate is a
conjunction: heldout success must improve **and** unsafe submissions must not
increase.

## LoRA Does Not Fix A Tool Bug

The decision memo defers this run — `defer_until_tool_plateau` — because 49 of
62 failure labels are tools or retrieval.

Worth restating in this lesson, because LoRA's low cost is exactly what makes it
tempting to run anyway. Cheap is not free, and a cheap run pointed at the wrong
cause still produces a model that has memorised compensations for a defect that
stays in the codebase. The rank you chose and the GPU you rented are not the
mistake; the diagnosis was.

## Common Failure Modes

- **Rank sized to ambition rather than data.** 78 rows and rank 64 memorises.
- **Trusting `max_sequence_length`.** Silent truncation eats the target.
- **A config with no `status`.** Someone reads a template as a result.
- **No compute estimate.** Cost becomes a surprise mid-run.
- **Treating a dry run as validation of learning.** It checks inputs.
- **Claiming completion without an artifact.** Unreproducible by construction.
- **Skipping the safety slice.** Overall improvement can hide a safety
  regression.
- **Running LoRA at a tool bug.** Cheap, easy, and the wrong intervention.

## Exercise

Open [`lora-config.template.json`](../../../model_improvement/strongbench/lora-config.template.json)
and [`train_lora.py`](../../../model_improvement/strongbench/train_lora.py).

1. `lora_rank` is 8 against 78 training rows. Argue why raising it to 64 would
   probably improve training loss and probably not improve the benchmark.
2. The dry run checks that `train_rows` matches the actual file length. Describe
   the change that makes those disagree, and what the run would do without the
   check.
3. `required_evidence_before_claiming_completion` lists the `unsafe_submission`
   slice separately from the Level 2 comparison. Explain why the aggregate is
   not sufficient.

Check your answer:

```text
1. Higher rank means more adapter capacity, and with only 78 examples the extra
   capacity is spent memorising them — training loss drops because the model is
   fitting the training set more exactly. The benchmark is 100 held-out tasks
   the adapter has never seen, so memorisation does not transfer; you would
   expect flat or worse benchmark results alongside a much better loss curve.
   That divergence is the signature of overfitting, and it is what the dev split
   exists to reveal before the benchmark does.

2. Anyone rebuilding the dataset — a split rule change, a new cleaning filter,
   more synthetic rows — changes the row counts while the config keeps the old
   numbers. Without the check the run proceeds on whatever the file now holds,
   so the config no longer describes the experiment. Every later comparison
   references a config that is wrong about its own inputs, and nothing surfaces
   it.

3. Because the adoption gate is a conjunction and the two can move in opposite
   directions. unsafe_submission is 10 tasks of 100, so a model could gain five
   tasks elsewhere and lose two here — the aggregate improves by three while a
   safety-relevant behaviour got worse. Reporting them separately makes that
   trade visible rather than netted out.
```

Then run the dry run, then edit `train_rows` to a wrong value and run it again.
The second should refuse, and its message should tell you which number
disagreed.

## Checkpoint

You are ready to move on when your training config states its status, its
compute estimate and the evidence required before any claim, your dry run checks
config against data, and your adapter rank is justified by your row count.

## Reading

- [`model_improvement/strongbench/decision-memo.md`](../../../model_improvement/strongbench/decision-memo.md)
  — why this run is deferred. Read it before running one; the cheapness of LoRA
  is precisely what makes the diagnosis step easy to skip.
- [`model_improvement/strongbench/sft-schema.json`](../../../model_improvement/strongbench/sft-schema.json)
  — what the run would consume. Check your longest row against
  `max_sequence_length` before trusting the default.
