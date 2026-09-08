# Lesson 5: Preference and Correction Data

## Core Idea

Demonstration data teaches what to do. Correction data teaches what to do
**instead** — and the "instead" is the part that carries the signal.

A demonstration is a single trajectory: here is a good answer. A correction is a
pair: here is what the agent produced, here is what it should have produced, for
the same prompt. That pairing is worth more than either half, because the
difference between them is the lesson. It localises the error rather than
leaving a model to infer which of a hundred differences from a good answer
mattered.

It is also the only data shape that supports preference training. DPO and its
relatives need a chosen and a rejected response for the same input, and you
cannot manufacture the rejected half after the fact — it has to be what actually
happened. Corrections are the only source where it exists.

Which produces the practical rule: **capture the wrong answer at the moment you
diagnose it.** A failure you fixed without recording what it produced is a
preference pair you can never reconstruct.

## The Only Rows That Carry Both

Across the 152 cleaned rows:

```text
rejected_final_answer  present on 30 rows — all failure_correction
                       present on  0 level1_trace or synthetic_gap_target rows
```

`rejected_final_answer` is the one field the dataset schema marks optional, and
that optionality is a statement: demonstrations have nothing to reject because
nothing went wrong; synthetic rows have no failure to point at. Only corrections
carry both sides.

Thirty rows is therefore the entire preference-training ceiling of this dataset,
and it is worth knowing before choosing a method rather than after. A team that
plans a DPO run on "152 examples" has misread the schema by a factor of five.

## A Correction Is Four Things

Every correction row carries:

| Field | Holds |
| --- | --- |
| `prompt` | the task, unchanged from the failing run |
| `rejected_final_answer` | what the agent actually produced |
| `target_final_answer` | what it should have produced |
| `labels` | the taxonomy label, e.g. `["MODEL.reasoning", "correction"]` |
| `provenance` | `annotation_id`, `config`, and the annotated-failures path |

The prompt must be *identical* to the failing run's. A preference pair over
slightly different prompts is not a preference pair — the model learns from the
prompt difference instead of the answer difference, and you will not notice.

The label is what makes corrections analysable in aggregate. Twenty of the 30
carry `RETRIEVAL.citation`; nine carry `MODEL.reasoning`. That distribution
tells you what a preference run would mostly be teaching, which is a design
question you should answer deliberately rather than discover.

## Provenance Decides Whether A Correction Is Usable

The `config` field records which agent build produced the failure, and this
dataset draws from two:

```text
scripted-current   11 annotations   the shipping agent
weak-no-tool       19 annotations   a deliberately broken control
```

Nineteen of the thirty corrections are derived from a configuration **nobody
ships**. They teach the model to compensate for an agent that never calls its
tools — a defect that does not exist in the real build.

Training on them costs budget, may shift behaviour in ways nothing measures, and
improves nothing in production. The filter is one line, and it is only possible
because `config` was recorded at annotation time.

**Filter corrections by the config that produced them.** This is the most common
way a correction pipeline quietly poisons itself.

## Corrections Are Evaluation Data First

The uncomfortable property, from Lesson 6: a correction is derived from a
benchmark failure, so it is part of your measurement. `choose_split` gives them
no path to `train`:

```text
failure_correction   train 0   dev 15   heldout 15
```

Zero, structurally. The thirty most informative rows in the dataset — the ones
written from known weaknesses, with the right answers attached — are all reserved
for evaluation.

This is the tension at the centre of correction data and it does not resolve
cleanly. The examples with the most signal are the examples you must not train
on, because they are how you will measure whether training worked. The resolution
here is to generate *new* correction-shaped data — the 100 synthetic rows target
the same failure modes without being derived from benchmark tasks — and keep the
real corrections as the measurement.

## Correction Targets Are Not Ideal Answers

From the dataset card:

```text
Correction targets are compact oracle summaries, not full human-authored ideal
answers.
```

The target is what a correct answer must *contain*, not what a thoughtful human
would write. Train on these and you get a model that emits terse, schema-correct
answers — which passes every deterministic grader and reads worse to a person.

This is a real and easily-missed failure mode: metrics improve while the product
degrades, because the thing that changed was answer style and nothing was
measuring it. If you intend to train on correction targets, either write them as
answers you would be happy to ship, or hold a rubric evaluation to catch the
regression.

## Common Failure Modes

- **Discarding the wrong answer.** The pair is unreconstructible afterwards.
- **Prompts that drift between the pair halves.** The model learns the prompt
  difference.
- **Not recording which config failed.** Corrections from a broken control get
  trained on.
- **Assuming your whole dataset supports preference training.** Here it is 30 of
  152.
- **Training on benchmark-derived corrections.** Contaminates the measurement.
- **Treating oracle targets as ideal answers.** Terse and correct trains a terse
  model.
- **Correction sets with no label distribution.** You cannot say what a run
  would be teaching.

## Exercise

Open [`cleaned.jsonl`](../../../datasets/strongbench/cleaned.jsonl) and
[`annotated-failures.jsonl`](../../../evals/operations/strongbench/annotated-failures.jsonl).

1. Count rows with `rejected_final_answer` and check their `source_type`. What
   does that count set a ceiling on, and what would you tell a colleague
   planning a DPO run on "the 152-row dataset"?
2. Of the 30 corrections, 19 derive from `weak-no-tool`. Write the filter you
   would apply before any training use, and say what remains.
3. Corrections are structurally barred from `train`, yet the pipeline still
   produces them. Explain what they are for, and how the dataset compensates for
   not being able to train on its best signal.

Check your answer:

```text
1. Thirty rows, all failure_correction. It caps preference training at 30 pairs
   — the other 122 rows have no rejected answer and cannot form one. Tell the
   colleague the usable figure is 30, not 152, and that it drops to 11 after
   filtering by config; at that size a preference run is a rehearsal of the
   mechanics rather than a source of measurable improvement.

2. Filter on provenance.config == "scripted-current", the shipping agent, which
   leaves 11 corrections. The other 19 come from a control build with its tools
   removed, so their targets teach the model to compensate for an agent that
   never calls tools — a behaviour the real build does not have.

3. They are evaluation data. Being derived from benchmark failures makes them
   the sharpest available test of whether a known weakness was fixed, which is
   exactly why training on them would destroy their value. The pipeline
   compensates by generating 100 synthetic rows targeting the same four failure
   modes — receipt thresholds, meal limits, lodging limits, submission gates —
   so the training set covers the weaknesses without being derived from the
   measurement.
```

Then take one correction row and diff `rejected_final_answer` against
`target_final_answer`. The changed fields are the lesson that row teaches; if
more than two or three fields differ, the pair is teaching several things at
once and may be worth splitting.

## Checkpoint

You are ready to move on when your corrections capture both answers with an
identical prompt, record the config that produced the failure, carry the
taxonomy label, and you can state how many usable preference pairs you actually
have.

## Reading

- [`datasets/strongbench/schema.json`](../../../datasets/strongbench/schema.json)
  — `rejected_final_answer` is the one optional field. Optional-by-source-type
  is a schema decision; make yours the same way.
- [`model_improvement/strongbench/sft-schema.json`](../../../model_improvement/strongbench/sft-schema.json)
  — what survives into a training export. Note that it keeps
  `source_example_id`, so any trained-on row can be traced back to the
  correction and the annotation behind it.
