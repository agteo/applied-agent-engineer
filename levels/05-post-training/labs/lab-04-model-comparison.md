# Lab 4: Model Comparison

## Objective

Compare candidates on evidence status, not on impressions, and produce a
recommendation someone can act on.

## Build

A comparison table needs three columns, and the middle one is what makes it more
than opinions:

| Candidate | **Evidence status** | Decision |

"Measured on 100 tasks", "supported by failure labels" and "not measured" are
three different epistemic positions. Flattening them into a single quality score
hides the difference between *we know this is good* and *we have not looked* —
and the second usually scores well on reputation.

Compare at least: your current baseline, a cheap intervention (prompt revision),
a training candidate, and a hosted or larger model.

**State the adoption gate as a conjunction, before you compare.** At minimum:

```text
Adopt only if held-out benchmark success improves AND the safety slice does not
regress.
```

A single-metric gate is one that something will eventually satisfy in a way you
did not intend — five ordinary tasks gained, two safety tasks lost, net positive,
policy violation shipped.

## Deliverable

Submit:

- the comparison table with an evidence column
- the adoption gate, written before any comparison
- a recommendation: adopt, reject, or keep testing
- for any candidate you did not measure, the words "not measured"

## Checks

This lab is judged against a rubric rather than a command, because the artifact
is an argument. Score each row **high / medium / low**:

| Criterion | High |
| --- | --- |
| Evidence column | every row states *what kind* of evidence exists, including "not measured" |
| Gate | a conjunction, written before the comparison, able to reject |
| Slices | safety-relevant slice reported separately, never netted into the aggregate |
| Denominators | every rate paired with its counts |
| Recommendation | one of adopt / reject / keep testing, with the condition that would change it |
| Honesty | at least one candidate marked unmeasured rather than guessed |

The lab passes at **high on Evidence, Gate and Recommendation**, and no lower
than medium elsewhere. Compare against the anchored examples in
[`examples/reference-artifacts/model-improvement-decision/`](../../../examples/reference-artifacts/model-improvement-decision/)
— read `weak.md` first, then `good.md`, then score yourself with `rubric.md`.

## Reference

Compare against
[`comparison-report.md`](../../../model_improvement/strongbench/comparison-report.md).

```bash
python3 -m model_improvement.strongbench && cat model_improvement/strongbench/comparison-report.md
```

Four candidates, four different evidence statuses, and the LoRA row reads
"Data prepared, no training run yet -> Defer adoption claim". That is what an
honest unmeasured row looks like.
