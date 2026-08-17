# Lab 2: Deterministic Graders

## Objective

Implement graders for objective benchmark checks.

## Build

Create graders for:

1. final answer schema validity
2. expected policy source ids
3. expected approval requirements
4. reimbursable total when the expected amount is known
5. unsafe action refusal

## Input

Each grader should receive:

- task record
- agent trace
- final answer

## Output

Each grader should return:

```json
{
  "grader": "approval_required",
  "passed": true,
  "score": 1.0,
  "comment": "Manager approval was correctly identified."
}
```

## Deliverable

Submit:

- grader implementations
- passing examples
- failing examples
- one aggregate score summary

## Checks

The lab passes if the graders produce useful failure comments, not just true or false values.

