# Lesson 2: State and Transitions

## Core Idea

State defines what is true in the environment. Transitions define how actions change what is true.

## State Should Include

- employees
- managers
- policies
- trips
- receipts
- reimbursement drafts
- approvals
- action history

## Transition Design

Every action should specify:

- preconditions
- inputs
- state changes
- observation returned
- possible errors
- whether the episode terminates

## Common Failure Modes

- Mutating state without an audit log.
- Allowing impossible transitions such as approval without an employee.
- Hashing volatile fields and losing reproducibility.

## Exercise

What state changes when `create_reimbursement_draft` succeeds?

Check your answer:

```text
A draft record is written with task id, employee id, receipt ids, total, and status; an audit event records the action and observation.
```

Use the Acme Finance rollout to confirm the answer against the environment simulator rather than relying on memory.

## Checkpoint

You are ready to move on when every simulated action changes state in a predictable and inspectable way.
