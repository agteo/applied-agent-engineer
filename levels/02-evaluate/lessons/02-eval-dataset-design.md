# Lesson 2: Eval Dataset Design

## Core Idea

The dataset defines what "good" means.

If the eval tasks are narrow, contaminated, unrealistic, or too easy, the benchmark will give false confidence.

## Task Record

Each task should include:

- task id
- user request
- category
- difficulty
- required tools
- expected policy source ids
- expected approvals
- expected reimbursable items
- expected non-reimbursable items
- grading notes

## Coverage

The Acme Expense Agent benchmark should cover:

- simple policy questions
- multi-item reimbursement tasks
- missing receipts
- meal limits
- travel and lodging
- receipt lookup
- ambiguous requests
- unsafe submission requests
- edge cases
- tasks where the correct answer is to ask a clarifying question

## Splits

Use splits even before model training:

- development tasks for prompt and harness iteration
- evaluation tasks for trusted reporting
- hidden or held-out tasks for later regression checks

Do not tune directly against the final reporting set.

## Checkpoint

You are ready to move on when your task set can fail the agent in meaningful, diverse ways.

