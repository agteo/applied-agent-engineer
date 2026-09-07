# Lesson 4: Hypotheses and Interventions

## Core Idea

A diagnosis should lead to a testable intervention.

## Pattern

```text
Failure -> Evidence -> Hypothesis -> Intervention -> Experiment -> Result
```

## Example

```text
Failure:
The agent misses manager approval for missing hotel receipts.

Evidence:
8 of 12 missing receipt failures retrieved the correct policy but omitted approvals.

Hypothesis:
The final answer contract does not force approval reasoning.

Intervention:
Add an approval_required field and a final-answer validation check.
```

## Common Failure Modes

- Choosing `use a better model` before identifying the failure mechanism.
- Writing hypotheses that cannot be falsified.
- Skipping the smallest intervention that would isolate the cause.

## Exercise

Write an intervention for a `TOOLS.arguments` receipt failure.

Check your answer:

```text
Add receipt-id/date/trip-id extraction checks, rerun the failing task, and promote the case to the regression pack if fixed.
```

Use the annotated failure bundle to confirm the answer against the diagnosis workflow rather than relying on memory.

## Checkpoint

You are ready to move on when each intervention maps to a specific failure category.
