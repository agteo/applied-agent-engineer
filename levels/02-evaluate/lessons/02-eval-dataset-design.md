# Lesson 2: Eval Dataset Design

## Core Idea

An eval dataset is not a collection of hard questions. It is an instrument, and
like any instrument it is designed backwards — from the decisions it has to
support.

The question that produces a good benchmark is: **what will I need to say, and
what would make me wrong?** If you will need to say "receipt handling works",
there must be enough receipt tasks to support the claim. If you will need to say
"the agent respects the submission gate", there must be tasks where submitting
is forbidden and refusing is the correct behaviour.

Everything else — the schema, the tags, the difficulty split — is machinery for
making those claims checkable. A dataset assembled by collecting interesting
failures instead will be a fine bug list and a poor instrument, because nothing
constrains what it covers.

## The Task Contract

Every one of the 100 tasks in
[`tasks.jsonl`](../../../evals/strongbench_benchmark/tasks.jsonl) validates
against [`schema.json`](../../../evals/strongbench_benchmark/schema.json), which
requires eleven fields:

```json
{"id": "bench-001",
 "domain": "strongbench_expense",
 "prompt": "Explain whether dinner during business travel is reimbursable.",
 "employee_id": "emp-1001",
 "category": "policy_question",
 "difficulty": "easy",
 "tags": ["policy_question"],
 "required_tools": ["search_policy"],
 "forbidden_tools": [],
 "expected": {"total_reimbursable": 0.0,
              "policy_source_ids": ["policy-meals-001"],
              "approval_types": [],
              "requires_missing_information": false,
              "unsafe_action_refused": false},
 "grading_notes": "Static Phase 2 benchmark task with deterministic oracle fields."}
```

The schema sets `additionalProperties: false` at both levels. That is a strong
choice and the right one: a task carrying a field no grader reads is a task
whose author believed something was being checked that was not. Rejecting
unknown fields makes the contract honest in both directions.

**`expected` is five fields, not one.** A task does not have "an answer"; it has
a total, a required citation set, required approval types, a
missing-information flag, and a refusal expectation. Grading only the total
would pass an agent that got the number right by ignoring the approval rule —
which is exactly what `bench-038` does.

**`required_tools` and `forbidden_tools` grade the process.** Getting the right
answer without calling `search_policy` is not success; it is an answer from
memory that will not survive a policy change. Encoding that in the task is what
makes it gradeable.

**`grading_notes` is prose for humans.** When a task turns out to be wrong,
whoever fixes it needs to know what the author intended. That field is where the
intent lives.

## The Coverage Is A Design Statement

100 tasks distributed as:

| Tag | Tasks | Why this many |
| --- | ---: | --- |
| calculation | 30 | the core capability; needs precision |
| edge_case | 30 | where policies interact; where agents break |
| policy_question | 20 | retrieval without arithmetic |
| receipt_lookup | 10 | a distinct capability, thinly covered |
| unsafe_submission | 10 | a safety property, thinly covered |

And by difficulty: 20 easy, 40 medium, 40 hard.

The shape is deliberate and it is also where the design's weakness is. From
Lesson 5, a 10-task slice puts one task at ten points, which is exactly the
precision you would *not* choose for a safety property. `unsafe_submission` at
10 tasks is a rate you cannot read confidently, guarding behaviour where being
wrong is expensive.

Sizing slices by how much precision the decision needs — rather than by how many
tasks were easy to write — is the main lever in dataset design. The 30/30 split
on calculation and edge_case is well judged; the 10/10 on the other two is a
known limitation, and the honest move is to say so rather than to report the
rate as though it were as solid as the others.

## Easy Tasks Are Not Filler

20 of 100 are easy, and dropping them would be a mistake. Easy tasks are the
ones that catch catastrophic regressions: when a change breaks something
fundamental, the easy slice goes first and loudly. A benchmark made only of hard
tasks is noisy at exactly the moment you most need a clear signal.

They also make the weak-baseline comparison legible. `weak-no-tool` scores 0/30
partly because it cannot even do the easy tasks, which is what makes "removing
tools is catastrophic" obvious rather than statistical.

## Every Task Needs An Oracle

The five `expected` fields are all computed or verified in advance, which is what
lets deterministic graders exist at all. This is the constraint that shapes what
can be in the dataset: **if you cannot state the correct answer before the run,
the task cannot go in the deterministic set.**

That is a real limit, not a failure. Tasks whose quality is genuinely subjective
belong in the rubric-graded path from Lesson 4, with a calibration sample and an
agreement rate. Mixing them into the deterministic set produces graders that
argue with themselves.

## Common Failure Modes

- **Collecting failures instead of designing coverage.** You get a bug list,
  and nothing tells you what is missing.
- **Slices too small for the decisions they support.** A 10-task safety slice
  cannot support a safety claim.
- **One expected value per task.** Grades the number and misses the behaviour.
- **Not grading process.** An answer from memory looks identical to a correct
  retrieval until the policy changes.
- **Allowing unknown fields.** Authors believe things are checked that are not.
- **Dropping easy tasks as unchallenging.** They are the regression alarm.
- **Putting subjective tasks in the deterministic set.** Produces graders that
  cannot be right.
- **No note of intent.** When a task is wrong, nobody can tell what it meant.

## Exercise

Open [`schema.json`](../../../evals/strongbench_benchmark/schema.json) and
[`tasks.jsonl`](../../../evals/strongbench_benchmark/tasks.jsonl).

1. The schema sets `additionalProperties: false` on both the task and its
   `expected` block. Name a concrete bug this prevents that a permissive schema
   would let through silently.
2. `unsafe_submission` has 10 tasks and guards a safety property. Argue for
   resizing it, and say what you would take the tasks from.
3. `bench-001` expects `total_reimbursable: 0.0` for a policy question with no
   amounts. Why is zero the right expected value rather than omitting the field,
   and what would break if the field were optional?

Check your answer:

```text
1. An author adds "expected_latency_ms" or "notes" to a task believing it will
   be graded. No grader reads it, nothing fails, and the field sits there for a
   year looking like coverage that does not exist. With additionalProperties
   false the task is rejected at validation, and the author finds out
   immediately that the check they wanted does not exist yet.

2. Ten tasks put one case at ten points, so the slice cannot distinguish 0.90
   from 0.80 with any confidence — and this is the slice that guards "the agent
   must not submit on an employee's behalf", where a false pass is a policy
   violation rather than a wrong number. Take tasks from edge_case or
   calculation at 30 each: both are comfortably precise and would still be the
   two tightest slices at 25.

3. Every task must supply all five expected fields, so graders can run
   uniformly without branching on presence. Zero is the correct answer to "how
   much is reimbursable" for a question that asks about policy rather than an
   amount — it is a real expectation, not a placeholder. If the field were
   optional, _total_ok would need a "no expectation" branch, and the day someone
   forgot the field on a task that did have an amount, that task would silently
   stop being graded on its total.
```

Then pick a capability the benchmark does not cover at all and write one task
for it, schema-valid, with all five expected fields. Notice how much of the work
is deciding the oracle rather than writing the prompt.

## Checkpoint

You are ready to move on when your task schema rejects unknown fields, every
task carries a full expected block and its tool constraints, and you can justify
each slice's size by the decision it supports.

## Reading

- [`evals/strongbench_benchmark/graders/deterministic.py`](../../../evals/strongbench_benchmark/graders/deterministic.py)
  — read it next to the schema. Every `expected` field exists because a grader
  reads it; the two files are one design, and they should be edited together.
- [`evals/strongbench_benchmark/build_tasks.py`](../../../evals/strongbench_benchmark/build_tasks.py)
  — how the 100 tasks are produced. Read it when deciding whether your own set
  should be authored, generated, or both.
