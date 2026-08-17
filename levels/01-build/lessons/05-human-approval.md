# Lesson 5: Human Approval

## Core Idea

Some actions require permission. A reliable agent needs explicit approval gates for risky operations.

In Level 1, approval can be simulated. The design habit matters more than the integration.

## Approval Triggers

Require approval for actions involving:

- money
- external messages
- account changes
- private data
- irreversible operations
- compliance exceptions

## Expense Agent Examples

The agent may answer:

```text
"This hotel expense may be reimbursable with manager approval."
```

The agent must ask before:

```text
"Submit this reimbursement request."
```

## Approval Record

The trace should record:

- requested action
- risk reason
- approver
- decision
- timestamp

## Checkpoint

You are ready to move on when risky actions cannot proceed without an approval record.

