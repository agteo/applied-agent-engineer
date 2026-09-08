# Lab 3: Intervention Experiment

## Objective

Test one targeted fix as an experiment that could return "no".

## Build

Pick the hypothesis with the highest coverage — the one explaining the most
failures — and design a single intervention against it.

Your experiment needs four parts, and the fourth is the one people omit:

- **Control.** A runnable configuration, not "before the fix". If nobody can
  re-run it, it is not a control.
- **Intervention.** One change. A prompt tweak plus a tool fix plus a model swap
  produces a result you cannot attribute.
- **Measurement.** Chosen before the run, and the *same* for both arms. A new
  grader written for the intervention makes the comparison meaningless.
- **Decision rule.** Written before you look, and able to say revert.

Candidate interventions:

- tighten a tool schema
- add final-answer validation
- change a retrieval query strategy
- add a prompt instruction
- add an approval gate

## Deliverable

Submit:

- hypothesis, and the observation that would disprove it
- the intervention as a diff or a precise description
- control and intervention results on the same measurement
- an interpretation that states what the result does **not** establish
- a regression case added to your pack

## Checks

```bash
# Both arms, same graders, same task set.
python3 -m evals.runner --model scripted --report /tmp/control.md
# ... apply your intervention, then:
python3 -m evals.runner --model scripted --report /tmp/intervention.md

diff <(grep -E '^- (passed|success_rate)' /tmp/control.md) \
     <(grep -E '^- (passed|success_rate)' /tmp/intervention.md)
```

The lab passes when:

- both arms ran against the **same benchmark version** — record it
- your decision rule was written before the numbers existed
- your write-up contains a sentence beginning "this does not prove"
- a regression case exists for the failure you fixed

If your intervention made things worse, the lab still passes. An experiment that
can only succeed was a demonstration.

## Reference

Compare against
[`evals/operations/strongbench/intervention-experiment.md`](../../../evals/operations/strongbench/intervention-experiment.md).

```bash
cat evals/operations/strongbench/intervention-experiment.md
```

Its control is `weak-no-tool-baseline-v1` at 0/30 against the scripted baseline
at 89/100 — and note the interpretation says the result establishes tool
grounding is *necessary*, not *sufficient*, because the intervention arm still
fails 11 tasks. Write that sentence for your own result.

Note also that the two numbers use different denominators (30 vs 100), so they
are not a like-for-like effect size. Do better than the reference here: run both
arms on the same task set.
