# Intervention Experiment

## Question

Does forcing evidence-producing tool use improve benchmark behavior over a model that answers directly?

## Setup

- Control: `weak-no-tool-baseline-v1` on the first 30 benchmark tasks.
- Intervention: `scripted-reference-v1`, which searches policy and calculates through tools.
- Measurement: the same deterministic Level 2 graders.

## Result

- Control: 0/30 tasks passed.
- Intervention: the full scripted baseline passes 89/100 tasks and clears the release gate.

## Interpretation

The intervention validates the course's core claim that tool-grounded traces are necessary for evaluation. It does not prove the scripted baseline is production-ready; the remaining failures still point to receipt lookup, item parsing, and approval-boundary work.
