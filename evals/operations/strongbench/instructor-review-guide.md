# Instructor Review Guide

Use this guide to review Level 3 submissions without relying on vibes.

## Required Evidence

- At least 30 annotated failed traces.
- A regression pack derived from those annotations.
- Failure counts by taxonomy label and task category.
- Three or more hypotheses tied to trace evidence.
- One intervention plan that can be tested against the Level 2 benchmark.
- A release recommendation that references the committed threshold.

## Revision Triggers

- Labels are generic, such as `bad answer`, without naming model, tool, retrieval, harness, or evaluation causes.
- The report discusses benchmark scores but does not quote failed task ids.
- The regression pack contains hand-picked easy cases rather than failures.
- The intervention is `use a better model` without a targeted experiment.
- The recommendation ignores unsafe submission or approval failures.
