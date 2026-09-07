# Lesson 3: Simulated Tools

## Core Idea

Simulated tools should behave like real tools in the ways that matter for learning and evaluation.

## Tool Examples

- `search_policy`
- `lookup_receipt`
- `create_reimbursement_draft`
- `request_manager_approval`
- `submit_reimbursement`
- `get_employee_profile`

## Realistic Constraints

Simulated tools should include:

- permissions
- missing records
- ambiguous records
- validation errors
- latency metadata if useful
- action logs

## Common Failure Modes

- Tools returning success without changing state.
- Simulated errors that are easier than production errors.
- Tool schemas that omit required arguments.

## Exercise

Name two simulated tools that should write state in Phase 6.

Check your answer:

```text
`create_reimbursement_draft` writes a draft; `request_manager_approval` writes an approval request; `submit_reimbursement` writes a report when authorized.
```

Use the Acme Finance rollout to confirm the answer against the environment simulator rather than relying on memory.

## Checkpoint

You are ready to move on when the agent cannot succeed by exploiting unrealistic tool behavior.
