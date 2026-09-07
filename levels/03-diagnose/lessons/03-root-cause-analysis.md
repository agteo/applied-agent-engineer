# Lesson 3: Root Cause Analysis

## Core Idea

Do not stop at the symptom. Ask what caused the failure and what evidence supports that explanation.

## Example

Symptom:

```text
The final reimbursable total is wrong.
```

Possible causes:

- receipt lookup returned the wrong record
- meal limit policy was not retrieved
- calculator arguments omitted one item
- final answer ignored the calculator result
- expected answer in the eval task is wrong

## Common Failure Modes

- Treating symptoms as causes.
- Changing multiple variables before testing a hypothesis.
- Ignoring fixture or oracle mistakes as possible causes.

## Exercise

Turn "wrong total" into a testable root-cause hypothesis.

Check your answer:

```text
Example: `Receipt lookup is too broad and returns receipts from the wrong trip; constrain lookup by receipt id or trip id and rerun affected tasks.`
```

Use the annotated failure bundle to confirm the answer against the diagnosis workflow rather than relying on memory.

## Checkpoint

You are ready to move on when every labeled failure includes evidence from the trace.
