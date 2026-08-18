# Lesson 4: Rubrics and LLM Judges

## Core Idea

Some qualities are hard to grade with code. Rubrics make subjective judgment more consistent.

LLM judges can help, but they are graders, not truth machines.

## When To Use A Rubric

Use rubrics for:

- helpfulness
- completeness
- clarity
- appropriate uncertainty
- quality of explanation
- whether the next action is sensible

## Rubric Shape

A good rubric defines:

- score levels
- evidence requirements
- disallowed behavior
- examples of good and bad answers

## Judge Calibration

Always compare judge output against human review.

Track:

- agreement rate
- false positives
- false negatives
- common disagreement patterns
- cases the judge should not grade

## Checkpoint

You are ready to move on when your judge has been tested against a human-reviewed sample and its limitations are documented.

## Reading

- [Inspect's scorer documentation](https://inspect.aisi.org.uk/scorers.html) — including its model-graded scorers. Pay attention to how it separates the rubric from the grading model, so the rubric can be reviewed by a human who does not read code.
