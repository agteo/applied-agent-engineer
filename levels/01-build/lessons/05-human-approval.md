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

## Common Failure Modes

- Treating approval as a polite UI confirmation instead of a permission boundary.
- Requesting approval after the risky action has already happened.
- Asking for approval on every task, which hides the true risk signal.

## Exercise

Decide whether the agent may submit a reimbursement report when the user asks, "Can you submit this for me?"

Check your answer:

```text
No. The course policy says only the employee may submit. The agent may prepare a draft or recommendation, but submission stays employee-controlled.
```

Use the Acme Expense Agent trace to confirm the answer against the agent harness rather than relying on memory.

## Checkpoint

You are ready to move on when risky actions cannot proceed without an approval record.
