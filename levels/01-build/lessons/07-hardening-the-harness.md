# Lesson 7: Hardening the Harness

## Core Idea

Agent reliability is mostly harness design.

Before adding advanced planning or more tools, make the basic loop safer and more observable.

## Required Hardening

Add:

- maximum step count
- timeout handling
- tool validation
- final answer validation
- structured errors
- trace logging
- prompt versioning
- model configuration

## Useful Error Types

```text
max_steps_exceeded
tool_not_found
tool_validation_failed
tool_execution_failed
approval_required
final_answer_invalid
model_response_invalid
```

## Recovery

Recover when the model can reasonably fix the issue:

- malformed tool arguments
- missing final answer field
- ambiguous task that needs clarification

Fail clearly when the system cannot safely continue:

- unknown tool
- repeated invalid output
- permission denied
- tool timeout

## Common Failure Modes

- Letting the loop run without a step budget.
- Allowing unknown tool names to execute dynamically.
- Swallowing tool errors and producing a confident final answer anyway.

## Exercise

Name two harness checks that should fail before a tool executes.

Check your answer:

```text
Unknown tool name and invalid argument schema should fail before execution; both should be visible in the trace.
```

Use the Acme Expense Agent trace to confirm the answer against the agent harness rather than relying on memory.

## Checkpoint

You are ready to complete Level 1 when the agent fails visibly, safely, and with enough trace detail for Level 2 and Level 3.
