# Lesson 3: SFT Data Preparation

## Core Idea

Preparing supervised fine-tuning data is mostly a filtering problem, not a
formatting one. The formatting is an afternoon. The filtering is where a
training run is quietly decided, because **every row you admit is a claim that
the model should imitate it.**

That framing is the useful one. Do not ask "can this row be converted into
training format?" — almost anything can. Ask "would I want the model to produce
this?" Rows that are correct but terse, correct but derived from a broken config,
or correct and part of your evaluation all convert perfectly and should all be
refused for different reasons.

The second idea is traceability. When a training run behaves oddly, the question
is always "what was it trained on?", and the answer has to be reconstructible
from the export itself.

## The Export Is A Narrower Schema

[`sft-schema.json`](../../../model_improvement/strongbench/sft-schema.json)
requires six fields where the dataset required eleven:

```text
schema_version, example_id, split, messages, source_example_id, labels
```

Gone are `prompt`, `target_final_answer`, `provenance` and `quality` as required
— the trainer consumes `messages` and does not need the flat prompt or the
separate target. What has been *added* is the field that matters most here:

```text
source_example_id   the dataset row this was built from
```

That is the traceability link. Any row in the export can be walked back to its
dataset row, and from there — via the dataset's own `provenance` — to the
annotation and the failing benchmark task behind it. Three hops from a training
example to the trace that motivated it.

Keeping `labels` in the export is the other deliberate choice. It lets you ask
what a training run was actually teaching, in aggregate, without rejoining to
the dataset.

## Rejection Is Logged, Not Silent

```python
def sft_rejection_reason(row):
    if row.get("split") == "heldout":
        return "heldout_reserved_for_evaluation"
```

Every refusal is written to `sft-rejected.jsonl` with its reason, its
`source_example_id`, and its split. Twenty-seven rows, all for the same reason,
matching the heldout split exactly.

The invariant is worth asserting in a test: **the rejection log should contain
precisely the heldout set.** If it holds 26, one heldout row reached the training
data, and that count discrepancy is the only visible symptom you will get.

A silent filter would have produced a 78-row export either way.

## What Survives, And What It Is Teaching

```text
train  78    dev  47    rejected  27
```

The 78 training rows are mostly synthetic — corrections cannot reach `train` at
all, and only 17 Level 1 traces do. So a run on this export is largely teaching
the four generated failure modes, which is a fact worth stating in the run's
write-up rather than discovering afterwards.

Checking the label distribution of your export before training is a five-minute
job that tells you what the run is about. If the answer surprises you, the
filtering is wrong.

## The System Prompt Is Part Of The Data

Each row's `messages` opens with a system message:

```text
You are the StrongBench Expense Agent. Answer with the structured final-answer
contract used by the course fixtures. Cite policy source ids when they support
reimbursement, approval, or missing-information decisions.
```

Two consequences people miss.

**The model is being trained on this exact prompt.** Change it at inference time
and the model is operating off-distribution — sometimes harmlessly, sometimes
not. If you fine-tune with one system prompt and serve with another, you have
introduced a variable nobody is tracking.

**The prompt encodes the contract.** It names the structured final answer and
the citation requirement, so the training signal covers not just what to answer
but the shape it must take. That is deliberate: format compliance is a behaviour
you want learned, not patched afterwards.

Version the system prompt alongside the export, and record which version each
run used.

## Targets Are Oracle Summaries, Not Model Answers

The limitation carried down from Lesson 7 of Level 4:

```text
Correction targets are compact oracle summaries, not full human-authored ideal
answers.
```

Train on compact targets and you get a compact model. Deterministic graders will
pass — the fields are right — and rubric or human review will regress, because
the answers stop explaining themselves.

This is the failure mode where metrics improve and the product gets worse. If
you train on oracle-shaped targets, hold a rubric evaluation alongside the
deterministic one, or the regression is invisible until users find it.

## Common Failure Modes

- **Formatting everything that converts.** Convertible is not the same as worth
  imitating.
- **Silent rejection.** A filter with no log cannot be distinguished from a bug.
- **Not asserting the rejection count.** The one visible symptom of a leak.
- **Not checking the label distribution before training.** You do not know what
  the run is teaching.
- **Dropping `source_example_id`.** A surprising trained behaviour becomes
  untraceable.
- **Changing the system prompt between training and serving.** Off-distribution,
  and unmonitored.
- **Training on oracle targets with no rubric check.** Terse and correct, and
  worse.
- **Exporting heldout rows.** Contaminates the measurement the run will be
  judged by.

## Exercise

Open [`sft-schema.json`](../../../model_improvement/strongbench/sft-schema.json),
[`sft-train.jsonl`](../../../model_improvement/strongbench/sft-train.jsonl) and
[`sft-rejected.jsonl`](../../../model_improvement/strongbench/sft-rejected.jsonl).

1. The export requires `source_example_id` though a trainer never reads it.
   Describe the debugging session where its absence costs you a day.
2. The rejection log holds 27 rows and the heldout split holds 27. Write the
   assertion you would add to the test suite, and say what a count of 26 would
   mean.
3. Check the `labels` on the 78 training rows. What is this export mostly
   teaching, and what sentence does that oblige you to put in the run write-up?

Check your answer:

```text
1. A fine-tuned model starts refusing to submit reports even when the requester
   is the employee. You need to know whether the training data taught that.
   With source_example_id you filter the export for submission-gate labels, walk
   each row back to its dataset row, then via provenance to the annotation and
   the failing task — and find that most submission-gate examples came from
   weak-no-tool, a config that never submits anything. Without it you are
   grepping message text and guessing.

2. assert len(rejected) == len([r for r in dataset if r["split"] == "heldout"]),
   or more directly that the set of rejected source_example_ids equals the set
   of heldout example ids. A count of 26 means one heldout row was exported into
   training data: the evaluation set is contaminated, any heldout comparison
   from that run is invalid, and nothing else in the pipeline would have said so.

3. Mostly the four synthetic failure modes — receipt thresholds, meal limits,
   lodging limits and submission gates — because corrections cannot reach train
   and only 17 Level 1 traces do. The write-up must say that gains may reflect
   the generator rather than capability, and report the Level 2 benchmark
   alongside any dataset metric.
```

Then run `python3 -m model_improvement.strongbench` and compare the exported
row count against the dataset's train split. They should agree; if they do not,
find which rows were dropped and why before running anything.

## Checkpoint

You are ready to move on when your export logs every rejection with a reason,
its counts reconcile against the dataset splits, every row traces back to its
source, and you can state what the run is teaching from the label distribution.

## Reading

- [`model_improvement/strongbench/decision-memo.md`](../../../model_improvement/strongbench/decision-memo.md)
  — read the line permitting this export for rehearsal while forbidding any
  improvement claim. Preparing data and asserting a result are separate acts.
- [`datasets/strongbench/schema.json`](../../../datasets/strongbench/schema.json)
  — the upstream schema. Comparing the two shows which fields exist for training
  and which exist for auditing, and it is a shorter list than most teams expect.
