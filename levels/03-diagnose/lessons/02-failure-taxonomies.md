# Lesson 2: Failure Taxonomies

## Core Idea

A taxonomy turns scattered anecdotes into analyzable data.

## Good Labels

Good failure labels are:

- specific
- mutually understandable
- evidence-based
- useful for deciding an intervention

## Bad Labels

Avoid labels like:

- bad answer
- model dumb
- hallucinated somehow
- failed

They do not tell an engineer what to fix.

## Common Failure Modes

- Using vague labels such as `bad answer`.
- Mixing root cause labels with severity labels.
- Creating labels that cannot guide an intervention.

## Exercise

Classify a failure where the agent never calls required receipt lookup.

Check your answer:

```text
Use a tool-selection label such as `TOOLS.selection`, not a generic model-quality label.
```

Use the annotated failure bundle to confirm the answer against the diagnosis workflow rather than relying on memory.

## Checkpoint

You are ready to move on when two people can label the same failure and mostly agree.

## Reading

- [tau2-bench](https://github.com/sierra-research/tau2-bench) — its per-task failure analysis is a worked example of classifying agent failures by cause rather than by symptom. Compare its categories against the taxonomy you build in Lab 2.
