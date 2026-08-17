# Lab 3: Rubric Judge

## Objective

Build a rubric grader for answer quality and calibrate it against human review.

## Rubric Dimensions

Score each answer on:

- completeness
- groundedness
- clarity
- uncertainty handling
- usefulness of next action

Use a 1-5 score for each dimension.

## Calibration Sample

Select at least 20 benchmark runs. Grade them manually first, then compare the LLM judge against the human labels.

## Deliverable

Submit:

- judge prompt or rubric instructions
- 20 human-reviewed examples
- judge outputs for the same examples
- agreement summary
- known judge limitations

## Checks

The lab passes if the judge is treated as an imperfect measurement tool and its disagreement patterns are documented.

