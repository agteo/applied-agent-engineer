# Lesson 5: Experiment Design

## Core Idea

Treat fixes as experiments.

## Experiment Record

Record:

- hypothesis
- intervention
- benchmark version
- agent version before
- agent version after
- expected improvement
- actual result
- unintended regressions

## Decision Rule

Define success before running the experiment.

## Common Failure Modes

- Changing prompt, tools, and grader in one experiment.
- Measuring only the hand-picked failing case.
- Calling a noisy result a win without a threshold.

## Exercise

Name the control, intervention, and measurement for a receipt-lookup fix.

Check your answer:

```text
Control: current agent. Intervention: stricter receipt lookup arguments. Measurement: Level 2 benchmark plus receipt_lookup slice and regression pack.
```

Use the annotated failure bundle to confirm the answer against the diagnosis workflow rather than relying on memory.

## Checkpoint

You are ready to move on when the result can confirm or reject the hypothesis.
