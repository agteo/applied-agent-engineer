# Lesson 2: Tool Schemas and Validation

## Core Idea

A tool schema is two documents in one, aimed at two different readers.

For the **model**, it is a description: the name, what the tool does, what
arguments it takes. This is prompt material, and it is how the model decides
whether to call the tool at all.

For the **harness**, it is a contract: a set of rules an argument object must
satisfy before anything executes. This is code, and it is what stands between a
plausible-looking model output and your systems.

The mistake is treating it as only the first. A schema used to describe but not
to enforce means the model's intentions reach your tools unchecked — and models
produce confident, well-formed, wrong arguments routinely. Validation is where
you decide that a malformed call is a *fact about this step* rather than an
exception that ends the run.

## Four Tools, And The Field That Matters Most

`TOOL_SCHEMAS` in
[`schemas.py`](../../../examples/strongbench-expense-agent/strongbench_agent/schemas.py):

| Tool | Permission | Required |
| --- | --- | --- |
| `search_policy` | `read` | `query` |
| `lookup_receipt` | `read` | `employee_id` |
| `calculate_reimbursement` | `read` | `items` |
| `request_human_approval` | **`write`** | `action`, `reason` |

`permission` is the field to notice. It is not part of any JSON Schema standard
— it was added because the harness needs to know which calls can change
something outside itself.

Three tools are `read`: they answer questions and touch nothing. One is `write`,
and it is the only tool that can have an effect a person would care about. That
distinction is what makes "the agent must not act without approval" a property
you can check by reading a schema rather than by reading the agent's reasoning.

**Classify your tools by effect before you write a line of the loop.** The split
determines where every safety check goes.

## The Validator Is Deliberately Small

[`validation.py`](../../../examples/strongbench-expense-agent/strongbench_agent/validation.py)
is a hand-written subset of JSON Schema, and the docstring says why:

```text
The course deliberately does not depend on `jsonschema` here. Learners should
see exactly what "validating a tool call" means: a handful of type checks, a
required-field check, and an error message the model can actually act on.

Supported keywords: type, properties, required, enum, items, minimum, maximum,
minItems, additionalProperties, format ("date" only).
```

Ten keywords. That is genuinely most of what tool validation needs, and seeing
the whole implementation removes the impression that validation is a library
feature rather than a design decision.

One detail in it is worth stealing outright:

```python
# bool is a subclass of int in Python; never let it pass as a number.
if isinstance(value, bool) and expected in {"number", "integer"}:
    errors.append(f"{path}: expected {expected}, got boolean")
```

`isinstance(True, int)` is `True` in Python, so a naive numeric check accepts
`{"amount": true}` and passes it to a calculator. Every hand-rolled validator in
this language has this bug until someone hits it. Yours will too.

## Error Messages Are Model-Facing

Validation errors here name the path, the expectation, and what arrived:

```text
items[0].category: 'dinner' is not one of ['meals', 'travel', 'lodging', ...]
date: expected an ISO date (YYYY-MM-DD), got '3rd March'
amount: expected number, got boolean
```

These are not for your logs. They go back to the model as the observation for
that step, and the model is expected to fix the call and retry. That reframes
what a good message is: **not "what went wrong" but "what to do differently".**

An error reading `ValidationError` teaches a model nothing. One naming the field
and listing the allowed values often gets a correct call on the next step, which
is the recovery behaviour Level 2 measures.

## Invalid Calls Are Observations, Not Exceptions

From the harness docstring:

```text
A model failure should never become a harness crash — invalid tool arguments
come back to the model as an observation, because recovery is the behaviour
Level 2 measures.
```

This is the load-bearing decision. If a bad argument raised, the run would end
and the trace would record a crash. Instead the loop catches it, writes the
error into the step, and continues — so the trace shows the bad call, the error,
and whatever the model did next.

That distinction shows up directly in the benchmark: `required_tools` and
`forbidden_tools` grade which tools were used, and `_tool_use_ok` reads the tool
names from the trace. A run that died on step two has no such record.

**Crash on harness bugs. Observe on model mistakes.** Confusing the two either
hides your bugs or throws away the data you are trying to collect.

## `additionalProperties: false`, Everywhere

Every tool schema and the final-answer schema set it. An unexpected key is
rejected rather than ignored.

This catches a specific and common model behaviour: inventing a plausible
parameter. A model that sends `{"query": "meals", "top_k": 5, "filter":
"recent"}` to a tool with no `filter` gets an error naming the unknown field,
rather than silently having its intent dropped. Silently ignoring it would leave
the model believing a filter was applied.

Strictness here is kindness to the model.

## Common Failure Modes

- **Schemas that describe but do not enforce.** The model's intentions reach
  your tools unchecked.
- **Raising on invalid arguments.** Ends the run and destroys the recovery
  behaviour you wanted to measure.
- **Opaque error messages.** The model cannot act on `ValidationError`.
- **No permission classification.** Safety checks have nowhere to hang.
- **Accepting booleans as numbers.** A Python-specific bug every hand-rolled
  validator has once.
- **Permitting unknown fields.** The model thinks a parameter applied when it
  was dropped.
- **Validating only tool inputs.** The final answer is a contract too, and
  Lesson 6 is about that.

## Exercise

Open [`schemas.py`](../../../examples/strongbench-expense-agent/strongbench_agent/schemas.py)
and [`validation.py`](../../../examples/strongbench-expense-agent/strongbench_agent/validation.py).

1. Exactly one of the four tools has `permission: "write"`. Name it, and say
   what a harness can enforce because the field exists that it could not enforce
   from the tool's name alone.
2. The validator special-cases `bool` before its numeric check. Write the call
   that would pass without it, and describe what the calculator would do with it.
3. Every schema sets `additionalProperties: false`. Give the model behaviour
   this catches, and say what the model would wrongly believe if unknown fields
   were ignored.

Check your answer:

```text
1. request_human_approval. With the field, the harness can enforce a rule like
   "no write-permission tool may run before an approval step" mechanically,
   across all present and future tools, without knowing what any of them do. From
   the name alone the harness would need a hardcoded list of dangerous tool
   names — which silently fails to cover the next tool someone adds.

2. {"items": [{"amount": true, "category": "meals"}]}. isinstance(True, int) is
   True in Python, so a plain numeric type check accepts it. The calculator then
   treats True as 1 and returns a reimbursable total of 1.00, which is a
   perfectly well-formed wrong answer: no crash, no error, and a number that
   looks like arithmetic.

3. A model inventing plausible parameters — top_k, filter, limit — on a tool
   that does not accept them. With additionalProperties false it gets an error
   naming the unknown field and can retry correctly. If they were ignored, the
   model would believe a filter had been applied and reason about the result as
   if it were filtered, which produces a confidently wrong answer with no error
   anywhere in the trace.
```

Then send a deliberately invalid tool call through `validate` and read the error
as though you were the model. If it does not tell you what to send instead, it
is not finished.

## Checkpoint

You are ready to move on when every tool has a schema the harness enforces, each
carries a permission classification, invalid arguments return to the model as
observations, and your error messages name the fix rather than the fault.

## Reading

- [`examples/strongbench-expense-agent/strongbench_agent/agent.py`](../../../examples/strongbench-expense-agent/strongbench_agent/agent.py)
  — read how validation errors are attached to the step and returned. The
  ordering there is the design: validate, observe, continue.
- [`evals/strongbench_benchmark/graders/deterministic.py`](../../../evals/strongbench_benchmark/graders/deterministic.py)
  — `_tool_use_ok` grades which tools were called. It only works because invalid
  calls stay in the trace instead of ending the run.
