# Lesson 6: Final Answer Contracts

## Core Idea

A structured final answer makes the agent easier to evaluate, debug, and integrate.

The final answer should be useful to a person and predictable for a program.

## Contract Design

A good final answer contract includes:

- human-readable summary
- key decisions
- supporting evidence
- uncertainty
- required approvals
- next action

## Expense Agent Contract

Use the project contract in [../project/acme-expense-agent-v1.md](../project/acme-expense-agent-v1.md).

## Validation

The harness should validate the final answer before returning it.

If the answer is invalid, the harness can ask the model to repair it once or twice. After that, it should fail clearly.

## Common Failure Modes

- Returning persuasive prose that cannot be graded.
- Putting policy citations in free text instead of structured fields.
- Omitting missing-information or approval fields when they are empty.

## Exercise

Name three fields that must exist for the grader to evaluate an expense answer.

Check your answer:

```text
`total_reimbursable`, `approvals_required`, and `missing_information` are required; policy citation fields are strongly recommended for grounding checks.
```

Use the Acme Expense Agent trace to confirm the answer against the agent harness rather than relying on memory.

## Checkpoint

You are ready to move on when final answers can be parsed and validated without reading prose.
