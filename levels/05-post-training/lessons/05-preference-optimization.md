# Lesson 5: Preference Optimization

## Core Idea

Supervised fine-tuning teaches a model to reproduce good answers. Preference
optimization teaches it to prefer one answer **over another** — and the second is
a different kind of signal, not just a stronger one.

The difference matters when "good" is easier to recognise than to specify. SFT
needs a target you are willing to have the model imitate exactly, which is a high
bar: any sloppiness in your targets becomes a habit. A preference pair needs only
that you can say which of two responses is better, which is a much lower bar and
often the only honest one available.

DPO and its relatives consume pairs: a prompt, a **chosen** response, a
**rejected** response. That shape is the constraint the whole lesson turns on,
because it is not something you can manufacture after the fact. The rejected
half has to be what actually happened.

## Count Your Pairs Before Choosing A Method

In this dataset, exactly one source type carries a rejected answer:

```text
rejected_final_answer   present on 30 rows — all failure_correction
                        present on  0 demonstration or synthetic rows
```

Thirty pairs. Not 152.

And the usable figure is smaller. Nineteen of those thirty corrections derive
from `weak-no-tool`, a deliberately broken control build. Filtering on
`provenance.config == "scripted-current"` leaves **eleven pairs** from the agent
you actually ship.

Eleven is not a preference-training dataset. It is enough to rehearse the
mechanics — formatting, a training loop, an evaluation harness — and not enough
to move a benchmark. Knowing that before you pick a method is the point of this
lesson.

**Count the pairs first.** It is one line, and it decides whether the method is
available to you at all.

## The Rejected Half Cannot Be Reconstructed

This is the operational consequence, and it is worth acting on immediately.

When a failure is diagnosed and fixed, the wrong answer is usually discarded —
it was a bug, the bug is gone, why keep it? But the moment it is gone, that
prompt can never form a preference pair. You can write a new chosen answer any
time; you cannot re-derive what a previous build produced.

This repo keeps it. Every annotated failure records the agent's actual output in
`evidence`, and the dataset builder carries it through as
`rejected_final_answer`. The preference data exists because Level 3 captured it
at diagnosis time, not because anyone planned a DPO run.

**Capture the wrong answer when you diagnose it**, whether or not you intend to
train. It costs a field and it is unrecoverable later.

## The Prompt Must Be Identical

Both halves of a pair must sit under exactly the same prompt. Not equivalent —
identical.

If the chosen response was produced under a revised system prompt, or the task
text was cleaned up between the failure and the correction, the model learns
from the *prompt* difference as readily as from the answer difference. Nothing
warns you; the loss goes down and the model has learned something you did not
intend.

Corrections here inherit `prompt` verbatim from the failing run, which is why
the dataset schema carries the flat string alongside `messages`.

## What A Pair Is Actually Teaching

Diff the two halves before trusting a pair. For a correction labelled
`MODEL.reasoning`, the difference might be one field — a total, recalculated. For
one labelled `RETRIEVAL.citation`, a missing policy id.

Two heuristics:

**If more than two or three fields differ, the pair teaches several things at
once.** The model cannot tell which difference you cared about, and neither can
you afterwards. Consider splitting it.

**If nothing structural differs — only prose — you are training on style.** That
may be what you want. It is rarely what people think they are doing when they
say they are fixing a reasoning failure.

The label distribution across the thirty tells you what a run would emphasise:
twenty carry `RETRIEVAL.citation`, nine `MODEL.reasoning`. A preference run on
this set would mostly be teaching citation behaviour. Decide that deliberately.

## Preference Data Is Evaluation Data Here

The same tension as everywhere in Level 4: corrections are derived from
benchmark failures, so `choose_split` gives them **no path to `train`** —
fifteen to dev, fifteen to heldout, zero to train.

So the thirty pairs cannot be trained on without contaminating the measurement
they came from. To run preference optimization properly you would need
correction pairs generated from tasks outside the benchmark — the same move the
synthetic generator makes for SFT, applied to pairs.

That is a real gap in this dataset, and it is better to name it than to work
around it by quietly relaxing the split rule.

## When Preference Optimization Is The Right Tool

| Situation | Method |
| --- | --- |
| you can write the ideal answer | SFT |
| you can only say which of two is better | preference optimization |
| the failure is a tool or retrieval bug | neither — fix the tool |
| you have fewer than a few hundred pairs | rehearsal only |

The third row is the one that applies here. With 49 of 62 failure labels in
`TOOLS.*` and `RETRIEVAL.*`, the dominant failures are not preference problems at
all. Preference optimization would teach the model to prefer correct-looking
answers while the retrieval layer that caused the failures stays broken.

## Common Failure Modes

- **Assuming your dataset supports pairs.** Here it is 30 of 152, and 11 after
  filtering.
- **Discarding the wrong answer at fix time.** The pair becomes unrecoverable.
- **Prompts that differ between halves.** The model learns the prompt
  difference.
- **Not diffing the pair.** You cannot say what it teaches.
- **Training on benchmark-derived pairs.** Contaminates the measurement.
- **Ignoring the label distribution.** The run emphasises whatever dominates.
- **Reaching for preference methods on tool bugs.** Wrong layer entirely.

## Exercise

Open [`cleaned.jsonl`](../../../datasets/strongbench/cleaned.jsonl) and
[`annotated-failures.jsonl`](../../../evals/operations/strongbench/annotated-failures.jsonl).

1. Count rows with `rejected_final_answer`, then count those whose
   `provenance.config` is `scripted-current`. Explain the gap and what the
   second number means for method selection.
2. The rejected half of a pair cannot be reconstructed after a fix ships.
   Describe the process change that guarantees you have it, and where in this
   repo that change already lives.
3. Corrections are barred from the `train` split. Propose a way to obtain usable
   preference pairs without weakening that rule.

Check your answer:

```text
1. Thirty rows carry rejected_final_answer, all failure_correction; eleven have
   config "scripted-current". The gap is the nineteen corrections derived from
   weak-no-tool, a deliberately broken control whose failures the shipping agent
   does not have. Eleven usable pairs is far below what preference optimization
   needs to move a benchmark, so the honest conclusion is that DPO here is a
   mechanics rehearsal, not a candidate intervention.

2. Record the agent's actual output at diagnosis time, before any fix is
   written — the failing answer, verbatim, in the annotation. It already lives
   in the Level 3 bundle: each annotated failure carries an evidence block with
   the agent's real final answer, and the Level 4 builder carries it through as
   rejected_final_answer. The preference data exists as a side effect of
   diagnosing carefully, not because a training run was planned.

3. Generate correction pairs from tasks outside the benchmark — the same move
   the synthetic generator already makes for SFT. Take the four target failure
   modes, generate prompts that are not benchmark tasks, produce a deliberately
   wrong answer with a weak configuration and a correct one with the reference,
   and pair them. Those pairs are not derived from the measurement, so they can
   enter train without contaminating anything.
```

Then diff `rejected_final_answer` against `target_final_answer` on three pairs
with different labels. Say in one sentence what each pair teaches; if you cannot,
the pair is teaching too much at once.

## Checkpoint

You are ready to move on when you know how many usable preference pairs you
have, capture rejected answers at diagnosis time, keep prompts identical across
both halves, and can state what a run on your pairs would emphasise.

## Reading

- [`datasets/strongbench/schema.json`](../../../datasets/strongbench/schema.json)
  — `rejected_final_answer` is the only optional field, present by source type.
  That asymmetry is the schema documenting where preference data can come from.
- [`model_improvement/strongbench/intervention-matrix.json`](../../../model_improvement/strongbench/intervention-matrix.json)
  — where preference and SFT approaches sit against tool fixes. Read the
  statuses before assuming a training method is the next move.
