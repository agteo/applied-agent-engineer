# Feedback and Assessment Plan

The curriculum should not rely on self-assessment alone.

Learners need feedback from automated checks, reference solutions, worked examples, and human review rubrics. Without those, the course can create confidence without skill.

## Feedback Layers

## 1. Automated Checks

Automated checks should verify objective requirements:

- code runs
- tool schemas validate
- final answers match the expected contract
- traces load as valid JSONL
- benchmark tasks execute
- deterministic graders pass or fail with clear messages
- unsafe actions are blocked

These checks should be added first for Levels 1-2.

## 2. Reference Solutions

Each executable lab should include:

- reference implementation
- explanation of design choices
- common mistakes
- extension ideas
- tests that the reference solution passes

Reference solutions should model good engineering taste, not just produce passing output.

## 3. Bad Submission Examples

For each major project, include examples of weak submissions:

- brittle string matching
- missing trace data
- vague failure labels
- contaminated datasets
- uncalibrated LLM judges
- training claims without benchmark evidence

Bad examples help learners see the difference between "done" and "good."

## 4. Worked Reviews

Each project should eventually include at least one reviewed example:

- what the learner submitted
- what passed
- what failed
- what an instructor would ask them to revise
- what a stronger version would look like

## 5. Human Review Rubrics

Human review is required for subjective work:

- failure taxonomy quality
- eval report credibility
- dataset card completeness
- model improvement decision memo
- reward hacking review

Rubrics should include examples of high, medium, and low quality answers.

## Priority Order

1. Automated checks for Level 1 labs.
2. Reference solutions for Level 1 labs.
3. 100-task benchmark and graders for Level 2.
4. Reference eval report.
5. Bad eval report example.
6. Annotated failure report examples for Level 3.
7. Dataset card examples for Level 4.

