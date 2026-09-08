# Lesson 6: Evaluation After Training

## Core Idea

Training produces a number that means almost nothing. Loss went down. That is
what training does; it is the objective, and a run that failed to reduce it is
broken rather than uninformative.

The question you actually need answered is different: **is this model better at
the job, and is it worse at anything?** Both halves. Teams reliably measure the
first and discover the second from users.

Evaluation after training is therefore not "run the benchmark again". It is a
comparison with a pre-registered decision rule, against a set the model has not
seen, checked on the slices that could regress. Everything in this lesson is
machinery for making that comparison honest.

## Loss Is Not Capability

A loss curve tells you the model fits the training distribution better than it
did. It cannot distinguish:

- learning the capability
- memorising the 78 training rows
- learning the *format* of the targets rather than their content
- learning the template a generator produced

All four lower the loss. Only the first is what you wanted, and the other three
are more likely with 78 rows, two-thirds of which are synthetic.

This is why the adoption gate names the benchmark rather than any training
metric. Loss is a diagnostic for whether the run worked mechanically. Capability
is measured somewhere the model has never been.

## The Comparison Table Is The Artifact

[`comparison-report.md`](../../../model_improvement/strongbench/comparison-report.md)
lays candidates side by side with their evidence status:

| Candidate | Evidence status | Decision |
| --- | --- | --- |
| Current scripted/tool baseline | measured on 100 tasks | keep as baseline gate |
| Tool and retrieval fixes | supported by Phase 3 failure labels | build next |
| Small LoRA/SFT adapter | data prepared, no training run yet | **defer adoption claim** |
| Frontier or hybrid API | not measured in offline course path | optional comparison |

The middle column is the one to copy. Every row states **what kind of evidence
exists**, not just a verdict. "Measured on 100 tasks" and "supported by failure
labels" and "no training run yet" are three different epistemic positions, and
flattening them into good/bad/unknown loses exactly the information a reader
needs to disagree with you.

A comparison table without an evidence column is a table of opinions.

## The Gate Is A Conjunction

```text
Adopt a trained or local model only if heldout benchmark success improves
without increasing unsafe submission failures.
```

Two conditions joined by *and*, and the structure matters more than either
clause.

A single-metric gate is one that optimisation will eventually satisfy in a way
you did not intend. Aggregate benchmark success can rise while a ten-task safety
slice collapses — five tasks gained elsewhere, two lost here, net +3 and a
policy violation shipped.

Pre-registering the conjunction means the awkward case is decided before you are
looking at a result you want to accept. That is the entire function of writing
gates in advance.

## What To Measure, In Order

**1. Held-out benchmark.** Tasks the model has never seen. The Level 2 benchmark
serves, provided no correction derived from it reached training — the
contamination guard from Level 4 is what makes this number mean anything.

**2. Per-slice, not just aggregate.** `receipt_lookup` at 3/10 and
`unsafe_submission` at 9/10 are the slices where movement matters. A ten-task
slice moves ten points per task, so read the counts rather than the rates.

**3. The safety slice explicitly.** Named in the gate, so it is not optional and
not netted into the aggregate.

**4. Regression cases.** The 30-row pack of previously-diagnosed failures. A case
flipping is a definite event rather than an estimate — and a case going *green*
unexpectedly needs explaining too, since that is what a loosened grader looks
like.

**5. Rubric or human review on a sample.** The one most often skipped, and the
one that catches the failure below.

## The Regression Everything Else Misses

From the dataset card:

```text
Correction targets are compact oracle summaries, not full human-authored ideal
answers.
```

Train on those and you get a model that emits terse, schema-correct answers.
Every deterministic grader passes — the fields are right, the total is right, the
citations are present. The aggregate improves.

And the answers stop explaining themselves. A user reading the output gets a
correct number with no reasoning attached, which is a worse product than the one
you replaced.

**Deterministic graders cannot see this**, because format compliance is exactly
what they check. Only a rubric evaluation or a human reading a sample catches
it. If you train on oracle-shaped targets, budget for that check or accept that
your metrics and your product have been decoupled.

## Attribution Requires Holding Things Still

A trained model usually arrives alongside a prompt tweak and a tool fix, because
they were all in flight. Then the benchmark moves and nobody can say which change
moved it.

Version everything the run depended on — base model, adapter, prompt version,
tool versions, benchmark version — and change one at a time where you can. The
`prompt_version` field exists in the trace schema for precisely this reason: a
model fine-tuned on one system prompt and served with another is operating
off-distribution, and that is a variable, not a detail.

## Common Failure Modes

- **Reporting loss as a result.** It is the objective, not the outcome.
- **Evaluating on data the model trained on.** Measures memory.
- **A single-metric gate.** Something will satisfy it the wrong way.
- **Aggregate only.** A ten-task safety slice can collapse invisibly.
- **No rubric check after training on oracle targets.** Metrics improve, product
  degrades.
- **Changing prompt and model together.** No attribution.
- **A comparison table with no evidence column.** Opinions in a grid.
- **Ignoring unexpected improvements.** The signature of a weakened grader.

## Exercise

Open [`comparison-report.md`](../../../model_improvement/strongbench/comparison-report.md)
and [`decision.json`](../../../model_improvement/strongbench/decision.json).

1. A LoRA run improves the Level 2 aggregate from 0.890 to 0.940 and takes
   `unsafe_submission` from 9/10 to 7/10. Apply the adoption gate and justify
   your answer in tasks, not rates.
2. The comparison table gives each candidate an evidence status rather than a
   score. Name the two rows whose statuses are least comparable, and say what a
   single "quality" column would have hidden.
3. Your fine-tuned model passes every deterministic grader with a higher
   aggregate, and a colleague says the outputs "feel worse". What is your first
   hypothesis, and which evaluation would settle it?

Check your answer:

```text
1. Reject. The aggregate gained five tasks; the safety slice lost two of ten.
   The gate requires improvement AND no increase in unsafe submission failures,
   so the second clause fails on its own. In task terms the trade is five
   ordinary tasks for two safety-relevant ones, which is a bad trade at any
   ratio — the slice guards a policy violation, not a score.

2. "Measured on 100 tasks" and "not measured in offline course path". One is a
   number from a real run; the other is an absence of evidence entirely. A
   single quality column would render both as a score — probably a high one for
   the frontier API on reputation — and hide that nothing has been measured. The
   evidence column keeps "we do not know" distinguishable from "we know it is
   good".

3. That the model learned the target format rather than the capability:
   correction targets are compact oracle summaries, so training on them produces
   terse, schema-correct answers that pass field checks and read badly.
   Deterministic graders cannot detect it because format compliance is what they
   check. A rubric evaluation against the committed rubric, or a human reading
   twenty sampled outputs beside the pre-training ones, would settle it.
```

Then write the evaluation plan you would run before adopting a trained model:
which sets, which slices, which decision rule. Write the decision rule first.

## Checkpoint

You are ready to move on when your post-training evaluation runs on unseen data,
your gate is a conjunction registered before the run, you check slices and
regression cases separately, and you have a review path that can catch a quality
regression the graders cannot.

## Reading

- [`model_improvement/strongbench/decision-memo.md`](../../../model_improvement/strongbench/decision-memo.md)
  — the adoption gate in its original context. Note it was written before any
  training run existed, which is what makes it binding.
- [`evals/reports/sample-report.md`](../../../evals/reports/sample-report.md)
  — the per-tag table you will be comparing against. Read it now so you know
  which slices are small enough to move on one task.
