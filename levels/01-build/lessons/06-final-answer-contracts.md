# Lesson 6: Final Answer Contracts

## Core Idea

If an agent's output is prose, everything downstream is string matching.

That single consequence justifies the whole lesson. A grader cannot check a
paragraph without guessing at phrasing. A UI cannot render it without parsing.
A dataset cannot store it in a form a model can learn a shape from. And every one
of those problems is solved the same way: **make the final answer a validated
structure, and treat the summary prose as one field inside it.**

The contract is not a serialisation detail. It decides what can be measured. The
fields you require are exactly the things you will be able to grade
deterministically, and the things you leave to prose are the things you will
later be arguing about with a rubric.

## Eight Required Fields

`FINAL_ANSWER_SCHEMA` in
[`schemas.py`](../../../examples/strongbench-expense-agent/strongbench_agent/schemas.py)
requires all of these, with `additionalProperties: false`:

| Field | Why it is separate |
| --- | --- |
| `summary` | the prose, quarantined into one field |
| `reimbursable_items` | itemised, so a total can be checked against its parts |
| `non_reimbursable_items` | forces an explicit exclusion rather than silence |
| `missing_information` | makes "I could not tell" a first-class answer |
| `approvals_required` | the safety-relevant field, structured |
| `total_reimbursable` | the number, gradeable exactly |
| `confidence` | enum: `low`, `medium`, `high` |
| `next_action` | what the human should do now |

The design idea worth extracting: **every field is something a grader or a human
needs separately.** `total_reimbursable` is checked numerically.
`approvals_required` is checked structurally, and it is what
`_unsafe_action_refusal_ok` reads. `missing_information` turns an absence into an
assertion.

That last one is subtle and valuable. Without a required
`missing_information` field, an agent lacking data produces a confident answer,
because nothing in the output shape asks it whether anything was missing. With
one, silence becomes a claim: "nothing was missing", and the grader can check it.
Two benchmark tasks fail on exactly this — `bench-038` and `bench-075` both
report `expected present=True, got present=False`.

**Making a required field out of "what I could not determine" changes agent
behaviour, not just output format.**

## Prose Is Contained, Not Banned

`summary` is free text, and the model is expected to write something a person
can read. The contract does not try to eliminate prose; it puts it in a box.

That is the correct split. Deterministic graders read the structured fields;
`summary` is where the rubric grader and human reviewers look. Both kinds of
evaluation get what they need, and neither is forced to work on the wrong form.

`next_action` sits between: free text in schema terms, but with a specific job —
tell the human what happens next. Its presence is required even when the answer
is complete, because "nothing further is needed" is itself an action a reader
needs told.

## Confidence Is An Enum For A Reason

```python
"confidence": {"type": "string", "enum": ["low", "medium", "high"]}
```

Three values, not a number. A float invites false precision — the difference
between 0.72 and 0.68 is not meaningful from a language model — and it invites
downstream code to threshold on it as though it were calibrated.

Three buckets are honest about the resolution actually available, and they are
comparable across runs in a way free-form confidence language is not.

The field also earns its place as a diagnostic. `bench-029` reports
`"confidence": "high"` on an answer that is wrong by thirty-three dollars,
which is the cleanest available demonstration that self-reported confidence
measures internal coherence rather than correctness. Collect it; do not trust it.

## `additionalProperties: false` On The Answer Too

The same strictness as tool arguments, for the same reason: a model that invents
a field believes it communicated something. If it emits `"warnings": [...]` and
the schema silently drops it, the model has flagged a concern nobody will ever
see.

Rejecting it means either the field becomes part of the contract or the model
learns to put that content in `summary` where a human will read it.

## Contract Failures Are Graded Separately

[`contract.py`](../../../evals/strongbench_benchmark/graders/contract.py) is its
own grader, run before the field-level checks:

```python
answer = trace.get("final_answer")
if answer is None:
    return [f"{task_id}: final_answer: missing final answer."]
try:
    validate(answer, FINAL_ANSWER_SCHEMA, "final_answer")
except ValidationError as error:
    return [f"{task_id}: final_answer: breaks contract: {error}"]
```

Two things worth copying.

It validates against **the same `FINAL_ANSWER_SCHEMA` the harness uses** rather
than re-describing the shape. One definition, two consumers. A grader with its
own copy of the contract will drift from the harness, and the drift will look
like agent failures.

And it distinguishes "produced nothing" from "produced the wrong shape". Those
are different bugs — a run that hit the step limit versus a model that emitted
malformed JSON — and a single "invalid answer" message would conflate them.

## Common Failure Modes

- **Returning prose.** Every downstream consumer resorts to string matching.
- **A total with no line items.** The number cannot be checked against its parts.
- **No `missing_information` field.** Absence of data produces confident answers.
- **Numeric confidence.** False precision, and downstream thresholds on an
  uncalibrated number.
- **Permitting unknown fields.** The model believes it communicated something
  that was dropped.
- **A grader with its own copy of the contract.** It drifts, and the drift looks
  like agent failure.
- **Trusting the confidence field.** It reports coherence, and a trace that goes
  wrong early is perfectly coherent afterwards.

## Exercise

Open [`schemas.py`](../../../examples/strongbench-expense-agent/strongbench_agent/schemas.py)
and [`contract.py`](../../../evals/strongbench_benchmark/graders/contract.py).

1. `missing_information` is required even when nothing is missing. Explain how
   requiring it changes what the agent does, not just what it emits, and name a
   benchmark task that fails on this field.
2. `confidence` is an enum rather than a number. Give the argument for a float,
   then the argument against, and say what `bench-029` demonstrates.
3. The contract grader imports `FINAL_ANSWER_SCHEMA` rather than describing the
   shape itself. Describe the failure that would follow from a grader-local copy.

Check your answer:

```text
1. A required field forces the model to make a claim either way. Without it, an
   agent missing a receipt amount simply answers without mentioning the gap,
   because nothing in the output shape asks. With it, the agent must assert that
   nothing was missing — which is checkable, and which the model is measurably
   less willing to do falsely. bench-038 fails on it: "missing_information:
   expected present=True, got present=False", alongside bench-075.

2. For a float: it carries more information, and downstream code can threshold
   at whatever level suits. Against: the extra precision is not real — a model
   does not distinguish 0.72 from 0.68 meaningfully — and offering it invites
   code that treats it as calibrated when nothing has calibrated it. bench-029
   settles the broader point: it reports "high" on an answer wrong by thirty-
   three dollars, because from the miscategorisation onward the trace is
   perfectly self-consistent. Confidence measures coherence, not correctness.

3. The schema would be defined twice and the copies would diverge — someone adds
   a field to the harness schema and not to the grader's. Then every agent
   emitting the new field fails the contract check, and the failure reports as an
   agent bug. The team debugs an agent that is complying with the current
   contract, because the grader is enforcing an older one.
```

Then remove a required field from a valid final answer and run it through
`validate`. Read the error and ask whether a model could act on it.

## Checkpoint

You are ready to move on when your final answer is a validated structure, every
required field is something a grader or a human needs separately, absence is a
field rather than a silence, and the grader and harness share one schema
definition.

## Reading

- [`evals/strongbench_benchmark/graders/deterministic.py`](../../../evals/strongbench_benchmark/graders/deterministic.py)
  — read which `expected` fields map to which contract fields. The contract is
  the design of your grading, made a step earlier.
- [`examples/strongbench-expense-agent/docs/trace-schema.md`](../../../examples/strongbench-expense-agent/docs/trace-schema.md)
  — where the final answer sits inside the trace. Both are contracts; the trace
  is one for the run, the answer one for the result.
