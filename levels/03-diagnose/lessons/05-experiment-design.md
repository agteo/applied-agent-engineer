# Lesson 5: Experiment Design

## Core Idea

Treat every fix as an experiment, because that is what it is: a change made on a
theory, whose effect you do not yet know.

Most teams skip the framing and go straight to shipping, then read the resulting
number as confirmation. That works until two things are true at once — the
number moved and the theory was wrong — which is common and undetectable without
a design. You end up with a codebase full of changes that are kept because the
metric went up, and no idea which of them are load-bearing.

An experiment needs four things: a **control** to compare against, an
**intervention** that changes one thing, a **measurement** decided in advance,
and a **decision rule** that can return no. The fourth is the one people leave
out, and it is what separates an experiment from a demonstration.

The version of that discipline you will use most is the smallest: write down
what result would make you revert, *before* you look.

## The Experiment This Repo Ran

[`intervention-experiment.md`](../../../evals/operations/strongbench/intervention-experiment.md)
is short enough to read whole, and every section is load-bearing:

```text
Question
  Does forcing evidence-producing tool use improve benchmark behavior over a
  model that answers directly?

Setup
  Control:       weak-no-tool-baseline-v1 on the first 30 benchmark tasks
  Intervention:  scripted-reference-v1, which searches policy and calculates
                 through tools
  Measurement:   the same deterministic Level 2 graders

Result
  Control:       0/30 tasks passed
  Intervention:  89/100, clears the release gate
```

**The question is answerable.** Not "is the agent good?" but a comparison
between two named configurations on a fixed task set.

**The control is a real configuration, not an absence.** `weak-no-tool-baseline-v1`
is a build you can run. "Before the fix" is not a control if nobody can
reproduce it.

**The measurement is the existing graders**, chosen before the run and shared
between both arms. Using the same deterministic graders is what makes 0 and 89
comparable at all — a new grader written for the intervention would have made
the comparison meaningless.

**One thing changes.** Tool use. Not tool use plus a prompt revision plus a
model swap, which is the shape most real experiments drift into and the reason
most of them cannot be interpreted.

## The Interpretation Is The Skilled Part

```text
The intervention validates the course's core claim that tool-grounded traces are
necessary for evaluation. It does not prove the scripted baseline is
production-ready; the remaining failures still point to receipt lookup, item
parsing, and approval-boundary work.
```

Two sentences, and the second is the one worth copying. A result establishes
something narrow, and the pressure after a good number is always to let it
establish something broader.

Here the honest reading is: tool grounding is *necessary*. The experiment shows
that removing tools destroys performance — 0 out of 30. It does not show tools
are *sufficient*, because the intervention arm still fails 11 tasks. Necessity
and sufficiency are different claims and this design can only speak to one.

Write the "does not prove" sentence for every experiment. If you cannot think of
one, you have not understood what you measured.

## A Result Needs Somewhere To Live

Record enough that someone can tell later whether a result still applies:

| Field | Why it matters later |
| --- | --- |
| hypothesis | what you were testing, in the words you used at the time |
| intervention | what changed |
| benchmark version | results are not comparable across benchmark edits |
| agent version before / after | what "before" meant |
| expected improvement | stated in advance, so the result can disappoint |
| actual result | what happened |
| unintended regressions | what got worse while the headline improved |

The last row is the one that catches real problems. A change that improves the
aggregate while degrading one slice is the normal shape of a bad fix, and it is
invisible unless you look for it. The Level 2 report's per-tag table exists for
exactly this: 89% overall while `receipt_lookup` sits at 30%.

The benchmark version matters more than it looks. Comparing a result measured
against one benchmark with a result measured against a later one is not a
comparison, and the failure mode is silent — the numbers are both real, they
just answer different questions.

## Close The Loop With Regression Cases

An experiment that succeeds should leave something behind that stops the failure
returning. The bundle's
[`regression-pack.jsonl`](../../../evals/operations/strongbench/regression-pack.jsonl)
holds 30 rows built from the annotated failures, each carrying its origin:

```json
{"id": "bench-029",
 "source_annotation_id": "scripted-current:bench-029",
 "prompt": "I spent $68 on dinner and $40 on room service. How much is reimbursable?",
 "expected": {"total_reimbursable": 75.0, "policy_source_ids": ["policy-meals-001"]},
 "tags": ["MODEL.reasoning", "calculation", "regression"]}
```

`source_annotation_id` links the case back to the diagnosis that produced it, so
a future failure of this case is not a new mystery. The failure report's fourth
recommendation is to promote the pack into the Level 2 benchmark after each fix
lands — which converts a one-off experiment into a permanent guard.

Fix, prove, then make the proof automatic. An intervention without a regression
case is a temporary result.

## Common Failure Modes

- **No control.** Every change looks like an improvement against nothing.
- **A control nobody can run.** "Before the fix" is not reproducible.
- **Changing several things at once.** The result cannot be attributed.
- **Choosing the measurement afterwards.** Guarantees a positive finding.
- **No decision rule.** An experiment that cannot fail is a demonstration.
- **Overreading the result.** Necessary is not sufficient; a slice is not the
  whole.
- **Not recording the benchmark version.** Two real numbers, silently answering
  different questions.
- **No regression case.** The failure is free to come back.

## Exercise

Open [`intervention-experiment.md`](../../../evals/operations/strongbench/intervention-experiment.md)
and [`regression-pack.jsonl`](../../../evals/operations/strongbench/regression-pack.jsonl).

1. The control scored 0/30 and the intervention 89/100. Why are those two
   numbers not directly comparable, and what would you run to make them so?
2. The interpretation says the result does not prove production readiness.
   State precisely what it *does* establish, using the words necessary and
   sufficient.
3. Every regression row carries `source_annotation_id`. Give the concrete
   scenario, a year from now, where that field saves an afternoon.

Check your answer:

```text
1. Different denominators: 30 tasks versus 100, so the control ran on a subset.
   0/30 and 89/100 are both real but they are not a like-for-like comparison —
   the control's slice may be easier or harder than the full set. To compare,
   run the control on all 100 tasks, or the intervention on the same first 30.
   Either fixes it; the current pairing supports "removing tools is
   catastrophic" but not a precise effect size.

2. It establishes that tool grounding is necessary: with tools removed, the
   agent scores zero, so no part of the benchmark is passable without them. It
   does not establish sufficiency — the intervention arm still fails 11 of 100
   tasks, so tools alone do not produce a correct agent. The design can only
   speak to necessity because it removed a capability rather than adding one.

3. A regression case starts failing after an unrelated refactor. Without the
   field, someone re-derives from scratch what the case was testing and why
   75.00 is correct. With it, they open the annotation, find the room-service
   categorisation analysis, the trace, and the original hypothesis in one hop —
   and immediately know whether the refactor reintroduced a known bug or the
   expected value was always wrong.
```

Then design an experiment for the receipt-lookup hypothesis: name the control,
the intervention, the measurement, and the result that would make you revert.
Write the decision rule before you would run it.

## Checkpoint

You are ready to move on when your experiments name a runnable control, change
one thing, use a measurement chosen in advance, state a decision rule that can
return no, and leave a regression case behind.

## Reading

- [`evals/reports/sample-report.md`](../../../evals/reports/sample-report.md)
  — read the per-tag table as an instrument for unintended regressions. It is
  where a fix that improves the aggregate and breaks a slice becomes visible.
- [`evals/operations/strongbench/release-recommendation.md`](../../../evals/operations/strongbench/release-recommendation.md)
  — the decision rule your experiment feeds. Notice it is a standing rule rather
  than a per-experiment judgment, which is what stops results being reinterpreted
  to fit.
