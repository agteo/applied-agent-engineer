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

## Common Failure Modes

- Using an uncalibrated judge as if it were ground truth.
- Hiding the rubric inside a prompt nobody reviews.
- Asking the judge to score facts that deterministic code can check.

## Exercise

Name one field deterministic code should grade and one field a rubric judge may grade.

Check your answer:

```text
Code should grade `total_reimbursable`; a rubric judge may grade clarity or helpfulness after hard constraints pass.
```

Use the Level 2 benchmark report to confirm the answer against the evaluation system rather than relying on memory.

## Checkpoint

You are ready to move on when your judge has been tested against a human-reviewed sample and its limitations are documented.

## Reading

- [Inspect's scorer documentation](https://inspect.aisi.org.uk/scorers.html) — including its model-graded scorers. Pay attention to how it separates the rubric from the grading model, so the rubric can be reviewed by a human who does not read code.
