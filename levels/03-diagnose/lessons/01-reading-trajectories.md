# Lesson 1: Reading Trajectories

## Core Idea

The final answer tells you an agent was wrong. The trajectory tells you where it
became wrong, and those are rarely the same place.

Diagnosis is the discipline of finding the **first wrong transition** — the
earliest step where the agent's state diverged from what it should have been.
Everything after that point is downstream, and usually looks like a separate bug
while being the same one. An agent that misreads a receipt will then compute the
wrong total, cite the wrong policy, and give the wrong final answer. Fixing the
total is fixing a symptom three steps from the cause.

The habit to break is starting at the end. The final answer is the most visible
part of a trace and the least informative, because by then every error has had a
chance to compound. Read forward from step one, and stop at the first step whose
output you would not have produced yourself.

The second habit to break is trusting success. A tool call that returns without
an error is not a tool call that did the right thing. Most of the interesting
failures in this repo are calls that succeeded perfectly and were asked the
wrong question.

## What A Trajectory Contains

Every run writes a trace with this shape — see
[`docs/trace-schema.md`](../../../examples/strongbench-expense-agent/docs/trace-schema.md):

```text
task_id, task, agent_version, model, prompt_version, trace_schema_version
steps[]
    step, tool_name, tool_arguments, validated_arguments, observation, error
final_answer
metadata: stop_reason, step_count, tool_calls
```

The fields to read in order, and what each rules out:

| Read | Rules out |
| --- | --- |
| `task` | you are diagnosing the task you think you are |
| `agent_version`, `prompt_version`, `model` | you are diagnosing the build you think you are |
| `tool_name` per step | wrong tool, or no tool |
| `tool_arguments` | right tool, wrong question |
| `observation` | the tool itself is broken |
| the gap between observation and next step | the agent read the result and drew the wrong conclusion |
| `final_answer` | everything above was fine and the write-up is wrong |

Most people read the first and last rows of that table. The middle four are
where diagnosis actually happens.

## A Worked Trajectory: bench-029

This is a real failure from the benchmark, preserved in
[`annotated-failures.jsonl`](../../../evals/operations/strongbench/annotated-failures.jsonl).

**The task:** *"I spent $68 on dinner and $40 on room service. How much is
reimbursable?"*
**Expected:** 75.00. **Got:** 108.00.

Read it forward.

**Step 1 — `search_policy`.** The agent passes the user's question verbatim as
the query. It gets back four policies, including `policy-lodging-001`, whose
text reads:

```text
Hotel lodging is reimbursable up to USD 250 per night before taxes and
mandatory fees. Stays above the nightly limit require manager approval.
Room service is treated as a meal expense and counts against the daily meal limit.
```

**The agent retrieved the exact sentence that decides this task.** Retrieval is
not the bug. Note that carefully, because a shallow read of "wrong total" would
send you to improve the search layer, and the search layer already worked.

**Step 2 — `calculate_reimbursement`.** Here are the arguments:

```json
{"items": [
  {"amount": 68.0, "category": "meals",   "description": "Dinner",      "has_receipt": true},
  {"amount": 40.0, "category": "lodging", "description": "Room service", "has_receipt": true}
]}
```

**This is the first wrong transition.** Room service is categorised as
`lodging`, one step after retrieving the sentence that says it is a meal. The
$68 dinner sits under the $75 daily meal cap; the $40 is booked against the $250
lodging cap; nothing exceeds a limit, so nothing is reduced.

**Step 2's observation.** The tool did its job flawlessly:

```json
{"reimbursable_items": [
   {"amount": 68.0, "description": "Dinner",       "reason": "Within policy."},
   {"amount": 40.0, "description": "Room service", "reason": "Within policy."}],
 "total_reimbursable": 108.0}
```

`108.0` is the *correct* answer to the question that was asked. The calculator
is not broken. If you had started your diagnosis by testing the calculator you
would have found it working and moved on, still not knowing why the total was
wrong.

**Final answer.** 108.00, citing `policy-lodging-001` for the room-service line
— the agent cites the policy that contradicts its own categorisation — with
`"confidence": "high"`.

That confidence field is worth dwelling on. The agent had no internal signal
that anything was wrong, because from step 2 onward everything was consistent.
Self-reported confidence measures coherence, not correctness.

## Where The Trace Says The Fix Goes

The annotation records the conclusion:

```json
{"taxonomy_labels": ["MODEL.reasoning"],
 "hypothesis": "The item parser is losing category/date context before the
                reimbursement calculator runs.",
 "recommended_intervention": "Improve item extraction and add unit tests for
                room service, missing receipts, and multi-item meal limits."}
```

The label is `MODEL.reasoning`, not `TOOLS.arguments`, and the distinction is
the whole lesson. The arguments were well-formed, correctly typed, and passed
validation. Nothing about their *shape* was wrong. What was wrong was the
judgment that produced `"category": "lodging"` — a reasoning failure that
happened to surface at an argument boundary.

Ask "was the argument malformed, or was it valid and wrong?" Malformed is a
harness problem. Valid and wrong is a reasoning problem. They have different
fixes and the trace shows you which you have.

## Common Failure Modes

- **Starting from the final answer.** By then every error has compounded and
  they all look equally plausible as the cause.
- **Trusting a successful tool call.** `ok: true` means the tool ran, not that
  it was asked the right question. bench-029's calculator was perfect.
- **Blaming retrieval when the document was retrieved.** Check what came back
  before you tune the search.
- **Reading `confidence` as evidence.** It measures internal coherence. A trace
  that goes wrong early and stays consistent afterwards reports high confidence.
- **Fixing the last wrong thing.** Correcting the total here would leave the
  categoriser broken and the next room-service task failing.
- **Diagnosing without the version fields.** A trace from a build you no longer
  ship is an interesting story about the past.

## Exercise

Open [`annotated-failures.jsonl`](../../../evals/operations/strongbench/annotated-failures.jsonl)
and find `bench-029`. Read its `trace.steps` before reading its
`taxonomy_labels`.

1. The agent retrieved `policy-lodging-001`, which states that room service
   counts against the meal limit. Name the step and field where the trajectory
   first diverges, and explain why it is not step 1.
2. Step 2's observation reports `total_reimbursable: 108.0` and the grader
   expects `75.0`. Is the calculator wrong? Justify from the observation.
3. Nineteen other rows in this bundle have `config: "weak-no-tool"` and never
   call a tool at all. For those, which row of the table above does diagnosis
   stop at, and why is that failure cheaper to diagnose than bench-029's?

Check your answer:

```text
1. Step 2, the tool_arguments field: {"amount": 40.0, "category": "lodging",
   "description": "Room service"}. Step 1 succeeded — it retrieved the exact
   policy that governs the case, so retrieval is not the defect. The divergence
   is the categorisation the agent chose when constructing the call, one step
   after it had the sentence in hand.

2. No. Given items categorised as 68.00 meals and 40.00 lodging, 108.00 is
   correct: the meal sits under the 75.00 daily cap and the lodging under the
   250.00 nightly cap, so neither is reduced. The observation shows both lines
   marked "Within policy." The calculator answered the question it was asked
   accurately; the question was wrong.

3. Diagnosis stops at the first row, tool_name — there are no tool calls, so
   there is nothing downstream to inspect. That is cheaper because the first
   wrong transition is the first step: the agent answered from the prompt
   instead of gathering evidence. One look at metadata.tool_calls resolves it,
   which is why all nineteen collapse to a single intervention.
```

Then pick a different failing row and write down the first wrong transition
before reading its `hypothesis`. Where you disagree with the annotation, one of
you has missed a step — find out which.

## Checkpoint

You are ready to move on when, given a failing trace, you can name the step and
the field where it first diverged, and say what you would have expected there
instead — without referring to the final answer.

## Reading

- [`examples/strongbench-expense-agent/docs/trace-schema.md`](../../../examples/strongbench-expense-agent/docs/trace-schema.md)
  — read this before designing your own trace format. Every field exists so that
  some diagnosis is possible without a re-run; decide which of yours earns its
  place by the same test.
- [`evals/operations/strongbench/instructor-review-guide.md`](../../../evals/operations/strongbench/instructor-review-guide.md)
  — read the review order it prescribes when you are about to skip straight to
  the final answer, which you will.
