# Lesson 4: Synthetic Data

## Core Idea

Synthetic data is generated to fill a gap you have identified. That clause does
the work: **"a gap you have identified"** is what separates useful synthetic data
from volume.

Generating examples because you want more data produces rows that look like the
rows you already have, which is the one thing you did not need. Generating them
because Level 3 told you the agent fails at receipt thresholds produces coverage
you could not otherwise get, aimed at a weakness you can name.

The risk is equally specific. A generator is a program, so its output carries its
structure. Train on template-generated rows and a model can learn the template —
scoring well on anything the generator produces and no better on the real task.
The defence is never "make the templates more varied". It is to **evaluate on
data the generator did not produce.**

## Generate Against Named Failure Modes

[`synthetic-generation.md`](../../../datasets/strongbench/synthetic-generation.md)
states the targeting up front:

```text
The generator targets four Level 3 failure modes:

- receipt threshold handling
- daily meal limits
- lodging limits
- employee-only submission gates
```

Every one is a failure the diagnosis stage actually found. The generator is not
inventing situations it imagines might be hard; it is manufacturing practice for
weaknesses with evidence behind them.

The result is 100 rows, and their labels record what each was aimed at:

```text
receipt_threshold  25    meal_limit  25
lodging_limit      25    submission_gate  25
```

Twenty-five each — a deliberate split, and visible in the metrics rather than
implied. When someone later asks what the synthetic portion is teaching, the
answer is a table, not a guess.

`provenance.target_failure_mode` carries the same information per row, so a
generator that turns out to be flawed can be traced to exactly the rows it
produced.

## Synthetic Rows Are Held To The Same Standard

They pass through the same cleaning gate as everything else:

```text
Accepted rows must have provenance, a contract-shaped target final answer, and
a non-empty prompt. Rejected rows are written to rejected.jsonl.
```

No exemption. A generated row with a malformed target is rejected exactly like a
hand-written one — which matters, because a generator producing subtly wrong
targets at scale is the fastest way to poison a dataset. The cleaner is the only
thing standing between a bug in a template and a hundred wrong examples.

They are also split like everything else, by content hash: 61 train, 27 dev, 12
heldout. Note they *can* reach heldout, unlike corrections, because they were not
derived from the benchmark and leak nothing. Being synthetic is not a
contamination risk; being derived from your measurement is.

## Two Thirds Of This Dataset Is Synthetic

```text
synthetic_gap_target  100
failure_correction     30
level1_trace           22
```

That ratio is the most decision-relevant fact about the dataset and it is
disclosed in the card's Limitations section:

```text
Synthetic examples are template-generated and should not be used to claim real
model improvement without held-out benchmark evaluation.
```

Two thirds is not automatically wrong. It reflects a real constraint: only 30
corrections exist, all reserved for evaluation, and only 22 traces. If you want
training data at all, most of it has to be generated.

But it does mean **every result measured on this dataset needs a non-synthetic
check beside it.** The Level 2 benchmark is that check, and it is why the
adoption gate in Level 5 names held-out benchmark success rather than dataset
metrics.

## Detecting Template Learning

The test is a comparison, not an inspection:

| Evaluation set | Model improves? | Reading |
| --- | --- | --- |
| synthetic held-out | yes | consistent with either |
| Level 2 benchmark | yes | capability |
| synthetic held-out | yes | |
| Level 2 benchmark | no | **template learning** |

A model that gains on generated data and not on the real benchmark has learned
the generator. The gap between the two numbers is the measurement; either alone
is uninterpretable, which is why you keep both and always report them together.

This is also the argument for having a non-synthetic held-out set at all. If
everything you hold out came from the same generator as everything you trained
on, no amount of splitting will reveal the problem.

## What Synthetic Data Cannot Give You

- **Surprise.** A generator produces situations its author thought of. The
  failures that hurt in production are the ones nobody enumerated.
- **Realistic distribution.** Twenty-five each is a design choice, not a
  reflection of how often these cases occur.
- **Ground truth beyond its rules.** Targets are computed by the same logic the
  graders use, so an error in that logic appears identically in both and cancels.
- **Evidence of real improvement.** Only the non-synthetic benchmark supplies
  that, which is what the card says.

## Common Failure Modes

- **Generating for volume.** More rows shaped like the ones you had.
- **Not naming the failure mode.** Nobody can say later what the rows were for.
- **Exempting generated rows from cleaning.** One template bug becomes a hundred
  wrong examples.
- **No non-synthetic held-out set.** Template learning becomes undetectable.
- **Reporting the synthetic fraction nowhere.** The reader assumes the data is
  real.
- **Reading the generator's split as the real distribution.** Twenty-five each
  is a choice.
- **Believing more templates fixes it.** Varied templates are still templates;
  the fix is the evaluation set, not the generator.

## Exercise

Open [`synthetic-generation.md`](../../../datasets/strongbench/synthetic-generation.md),
[`metrics.json`](../../../datasets/strongbench/metrics.json) and the card.

1. The generator targets four failure modes and produces 25 rows each. Where did
   those four come from, and what would be wrong with picking them by asking
   which cases seem hard?
2. Synthetic rows can be assigned to `heldout`, while corrections cannot. Explain
   the asymmetry in terms of what each was derived from.
3. A model trained on this dataset improves from 0.84 to 0.91 on a synthetic
   held-out split, and stays at 0.89 on the Level 2 benchmark. State your
   conclusion and the single sentence you would put in the write-up.

Check your answer:

```text
1. From Level 3 diagnosis — they are failure modes observed in annotated
   benchmark failures, so there is evidence the agent is weak at each. Picking
   by intuition would generate practice for weaknesses the agent may not have,
   while leaving the real ones uncovered; and it would produce no way to check
   afterwards whether the generated rows addressed anything, because nothing
   would connect them to observed failures.

2. Corrections are derived from the benchmark: each one is written from a task
   the agent failed, so training on them contaminates the measurement they came
   from. Synthetic rows are generated from the policy rules, not from benchmark
   tasks, so nothing about them leaks the evaluation — they can sit in any
   split. Contamination is about derivation, not about whether data is real.

3. The model learned the template. It improved on data the generator produced
   and not on the independent benchmark, which is the signature. Write-up
   sentence: "Gains are confined to synthetic held-out data (0.84 -> 0.91) with
   no movement on the Level 2 benchmark (0.89), so we cannot claim a capability
   improvement." Report both numbers; either alone would mislead.
```

Then check `provenance.target_failure_mode` across the 100 synthetic rows and
confirm the 25/25/25/25 split. If a generator bug were found tomorrow, that
field is how you would find its output.

## Checkpoint

You are ready to move on when every synthetic row records the failure mode it
targets, generated rows pass the same cleaning as authored ones, and you have a
non-synthetic held-out set that could reveal template learning.

## Reading

- [`datasets/strongbench/dataset-card.md`](../../../datasets/strongbench/dataset-card.md)
  — the Limitations section states the synthetic fraction and the check it
  requires. That disclosure is voluntary, which is what makes it worth copying.
- [`evals/operations/strongbench/failure-report.md`](../../../evals/operations/strongbench/failure-report.md)
  — its Level 4 data recommendation is where the four target failure modes came
  from. Read it to see generation being specified by diagnosis rather than
  guessed.
