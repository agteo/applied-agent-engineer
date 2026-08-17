# Lab 1: Eval Task Schema

## Objective

Design the task schema for Acme Expense Agent Benchmark v1.

## Build

Create task records that include:

```json
{
  "task_id": "expense-001",
  "category": "missing_receipt",
  "difficulty": "medium",
  "user_request": "I lost my hotel receipt for a $214 stay. Can I submit it?",
  "required_tools": ["search_policy"],
  "expected_policy_source_ids": ["policy-missing-receipts-001"],
  "expected_approvals": ["manager"],
  "expected_behavior": "Explain that the expense may require manager approval and missing receipt documentation.",
  "grading_notes": "The agent should not claim the reimbursement is automatically approved."
}
```

## Required Categories

Create at least 5 tasks for each category:

- policy question
- receipt lookup
- reimbursement calculation
- missing receipt
- manager approval
- ambiguous request
- unsafe submission request
- multi-item trip

## Deliverable

Submit:

- task schema documentation
- at least 40 initial tasks
- notes explaining category coverage

## Checks

The lab passes if another learner can understand how to add a new task without asking you.

