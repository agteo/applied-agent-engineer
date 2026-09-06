# Failure Analysis Rubric

## High

A high-quality failure analysis is evidence-backed and actionable.

Required anchors:

- Names the benchmark run and diagnostic command.
- Reports how many failures were reviewed.
- Uses concrete taxonomy labels.
- Connects labels to trace behavior, not only final-answer text.
- Prioritizes interventions by frequency, severity, or unblock value.

Example: [`good.md`](good.md) earns high because it cites the 89/100 benchmark
result, the 30 annotated failures, concrete failure labels, and an intervention
order.

## Medium

A medium analysis identifies plausible failure themes but does not fully prove
them from traces or turn them into a specific intervention plan.

## Low

A low analysis explains failures with vibes.

Example: [`weak.md`](weak.md) is low because it guesses about edge cases and
training data without naming evidence or a concrete next test.
