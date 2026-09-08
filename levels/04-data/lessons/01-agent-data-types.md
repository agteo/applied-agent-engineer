# Lesson 1: Agent Data Types

## Core Idea

"Training data" is not one thing. An agent dataset is assembled from sources
that differ in how they were produced, what they can teach, and how much you
should trust them — and treating them as interchangeable rows is how a dataset
becomes unfixable.

The practical consequence is that **`source_type` is not metadata, it is the
most load-bearing field in the schema.** It decides which split a row may enter,
whether the row can carry a preference pair, and what a result measured on it is
allowed to claim. Every serious decision downstream keys on it.

The three types in this repo are worth learning as a set, because most agent
datasets are some mixture of the same three: recordings of success, corrections
of failure, and examples you manufactured because you had neither.

## The Three Types

`python3 -m datasets.strongbench` produces 152 cleaned rows:

| `source_type` | Rows | Made from | Teaches |
| --- | ---: | --- | --- |
| `level1_trace` | 22 | successful agent runs | what good looks like |
| `failure_correction` | 30 | annotated benchmark failures | what to do instead |
| `synthetic_gap_target` | 100 | a template generator | coverage you lacked |

Read the proportions before anything else. Two thirds of this dataset is
synthetic, which is the single most decision-relevant fact about it and the
reason the dataset card leads its Limitations section with that admission.

**Demonstrations** are cheap and safe. They come from runs that already passed,
so they cannot teach a behaviour the agent does not already have — their value is
in stabilising it, not extending it.

**Corrections** are expensive and the only type that targets a known weakness.
Each one exists because a specific task failed, which is exactly why Lesson 6
forbids them from the training split.

**Synthetic rows** buy coverage of situations that neither source produced. They
are also the type most likely to teach a template rather than a capability, and
the only defence is held-out evaluation on non-synthetic tasks.

## Only Corrections Carry What Went Wrong

The types do not share a schema, and the difference is instructive. Every row has
`prompt`, `messages`, `target_final_answer`, `labels`, `provenance`, `quality`,
`split`. Corrections have one field the others do not:

```text
rejected_final_answer   present on all 30 failure_correction rows
                        present on 0 demonstration or synthetic rows
```

A correction knows both the answer that was produced and the answer that should
have been, which makes it the only type that can become a **preference pair** —
the chosen/rejected format that DPO and similar methods require. Demonstrations
have nothing to reject; synthetic rows have no failure to point at.

If you are planning preference training, that single field determines how much
usable data you have, and the answer here is thirty rows. Worth knowing before
choosing a method rather than after.

## Provenance Is Shaped By Type

Each type records where it came from in the form that makes it auditable:

```json
level1_trace         {"path": ..., "model": ..., "trace_schema_version": ...}
failure_correction   {"path": ..., "annotation_id": "scripted-current:bench-029",
                      "config": "scripted-current"}
synthetic_gap_target {"generator": ..., "target_failure_mode": ...}
```

Different fields, same purpose: answer "what else came from here?" when
something turns out to be wrong.

The correction's `config` field is the one that repays attention. It records
*which agent build* produced the failure being corrected. Without it you cannot
tell a correction derived from the shipping agent from one derived from a
deliberately broken control — and this repo has both, in a ratio of 11 to 19.
Training on the second teaches the model to fix a config nobody ships.

`target_failure_mode` on synthetic rows does the equivalent job forwards: it
records what gap the row was generated to close, so a generator that turns out
to be skewed can be traced to the rows it produced.

## Type Decides Split

The rule from Lesson 6 is a function of this field alone:

```python
if row["source_type"] == "failure_correction":
    return "dev" if index % 2 else "heldout"      # train unreachable
if row["source_type"] == "level1_trace":
    return "dev" if index % 5 == 0 else "train"
# synthetic: content-hash bucket across all three
```

Corrections cannot reach `train`, because they were derived from the measurement.
Demonstrations mostly can, because they came from runs the agent already passed
and leak nothing. Synthetic rows are split by content hash because there is
nothing to protect — they were not derived from any evaluation.

Three types, three policies, one field deciding all of them. That is what makes
`source_type` structural rather than descriptive.

## Common Failure Modes

- **Mixing types without recording which is which.** Every downstream rule needs
  the field, and it cannot be recovered later.
- **Treating synthetic rows as evidence.** Improvement on template-generated data
  may be template-learning; only non-synthetic held-out tasks separate them.
- **Not recording which config produced a correction.** Corrections from a broken
  control teach fixes for a build nobody ships.
- **Assuming demonstrations extend capability.** They come from runs that already
  passed; they stabilise, they do not teach new behaviour.
- **Planning preference training without counting rejected answers.** Only
  corrections have one, and there may be fewer than you assumed.
- **One provenance schema for all types.** Different origins need different
  fields to be auditable.

## Exercise

Open [`cleaned.jsonl`](../../../datasets/strongbench/cleaned.jsonl) and
[`metrics.json`](../../../datasets/strongbench/metrics.json).

1. Count rows carrying `rejected_final_answer`. Which `source_type` has it, and
   what training method does that field enable that the others cannot support?
2. `failure_correction` provenance records a `config`. This repo's annotations
   come from two configs in an 11 / 19 split. What goes wrong if you train on
   corrections without checking that field?
3. 100 of 152 rows are `synthetic_gap_target`. Design the evaluation that would
   tell you whether a model trained on this set learned a capability or a
   template.

Check your answer:

```text
1. Thirty rows, all failure_correction. It enables preference training — DPO
   and similar methods need a chosen and a rejected response for the same
   prompt. Demonstrations have no rejected answer because nothing went wrong;
   synthetic rows have none because no failure produced them. Thirty pairs is
   the real ceiling on preference training here, and it is worth knowing before
   picking a method.

2. Nineteen of the thirty annotations come from weak-no-tool, a deliberately
   broken control that answers without calling tools. Corrections derived from
   it teach the model to compensate for a configuration nobody ships. Training
   on them consumes budget, may degrade behaviour on the real agent, and
   improves nothing in production. Filter on config before using corrections.

3. Evaluate on non-synthetic held-out tasks — the Level 2 benchmark and the
   heldout split's failure_correction rows, which are real. Compare the lift
   there against the lift on synthetic held-out rows. A model that improves on
   synthetic and not on real tasks learned the template. The gap between the
   two numbers is the measurement; either alone is uninterpretable.
```

Then group the cleaned rows by `source_type` and `split` and check that no
`failure_correction` row appears in `train`. That invariant is the contamination
guard, and it is one line to assert in a test.

## Checkpoint

You are ready to move on when every row in your dataset records its type and a
provenance shaped for that type, you can state your synthetic fraction, and you
know how many rows could support preference training.

## Reading

- [`datasets/strongbench/schema.json`](../../../datasets/strongbench/schema.json)
  — note which fields are required for all rows and which appear only on
  corrections. Optional-by-type is a schema decision worth making deliberately.
- [`datasets/strongbench/synthetic-generation.md`](../../../datasets/strongbench/synthetic-generation.md)
  — read what the generator was asked to cover before trusting the 100 rows it
  produced. A generator's target list is the shape of the bias it introduces.
