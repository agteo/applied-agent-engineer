# Lesson 3: Root Cause Analysis

## Core Idea

A symptom is what the grader saw. A root cause is the earliest point where an
intervention would have prevented it.

That definition is operational rather than philosophical, and it settles most
arguments about how far back to go. You stop when you reach the step where a
change you could actually make would have stopped the failure. Going further
back gets you to "the model was trained on the internet", which is true and
useless. Stopping too early gets you a fix that holds until the next task.

The requirement that makes this a discipline rather than a habit of thought is
**evidence**. A root cause is a claim about a specific step, supported by a
specific field in the trace. If you cannot point at the field, you have a
hypothesis, and Lesson 4 is about how to test it. Both are legitimate; confusing
them is not.

## Symptom, Cause, Evidence

Take the failure from Lesson 1.

```text
Symptom     bench-029: total_reimbursable: expected 75.00, got 108.00.
```

Four causes could produce that symptom, and they need different fixes:

| Candidate cause | Would show up as |
| --- | --- |
| receipt lookup returned the wrong record | wrong ids in `lookup_receipt` observation |
| the meal-limit policy was never retrieved | `policy-meals-001` absent from step 1 results |
| calculator arguments omitted or miscategorised an item | wrong `category` in `tool_arguments` |
| the final answer ignored the calculator result | `final_answer.total` ≠ observation total |

Every row is checkable against the trace, which is what makes this a list of
candidates rather than a list of opinions. Read the trace and three of them die:

```text
step 1  search_policy    -> returned policy-lodging-001, which states
                            "Room service is treated as a meal expense"
                            => the policy WAS retrieved. Cause 2 eliminated.

step 2  tool_arguments   -> {"amount": 40.0, "category": "lodging",
                             "description": "Room service"}
                            => miscategorised. Cause 3 confirmed.

step 2  observation      -> total_reimbursable: 108.0
final_answer.total       -> 108.0
                            => the answer matched the tool. Cause 4 eliminated.
```

Cause 1 never applies — this task has no receipt lookup. The root cause is the
`category` value in step 2's arguments, and the evidence is one field.

## The Counterfactual Test

The check that stops you going too far back or not far back enough:

> **If this one thing had been different, would the failure have happened?**

Applied to bench-029: had `category` been `"meals"`, the calculator would have
summed 68 + 40 against the 75 daily cap and returned 75.00. The failure
disappears. That is a root cause.

Applied one step earlier — had the search returned different policies — the
answer is no: the right policy *was* returned and the agent categorised it
wrongly anyway. Improving retrieval changes nothing. That is why retrieval is
not the cause despite being upstream.

Applied one step later — had the final answer been rewritten to say 75.00 — the
number would be right and the categoriser would still be broken, so the next
room-service task fails identically. That is a symptom fix.

Upstream is not the same as causal. The test is counterfactual, not positional.

## Cause Lives Somewhere, And That Is The Point

Once identified, a root cause has an owner. The taxonomy from Lesson 2
namespaces by exactly that, and bench-029's annotation records:

```json
{"taxonomy_labels": ["MODEL.reasoning"],
 "hypothesis": "The item parser is losing category/date context before the
                reimbursement calculator runs."}
```

`MODEL.reasoning`, not `TOOLS.arguments` — because the argument was well-formed,
correctly typed, and passed validation. Nothing about its *shape* was wrong. The
judgment that produced `"lodging"` was wrong.

That distinction decides who fixes it. Malformed arguments are a harness
problem: tighten the schema. Valid-but-wrong arguments are a reasoning problem:
better extraction, better examples, a unit test on room service. Same field, same
step, two different repairs, and only the root-cause analysis tells them apart.

## When The Cause Is Not In The Agent

One of the five hypotheses in the bundle reads:

```text
1x  The benchmark exposed an ambiguity that needs trace review before changing
    the agent.
```

Sometimes the trace is fine and the expected answer is wrong or underspecified.
A root-cause process with no way to reach that conclusion will manufacture an
agent bug, because that is the only kind of answer it can produce. Keep the
route open, and treat a rising count in that category as a finding about the
benchmark rather than noise.

## Common Failure Modes

- **Stopping at the graded field.** "The total was wrong" is where analysis
  starts.
- **Blaming the most upstream component.** Retrieval ran first and worked;
  earlier is not causal.
- **Asserting a cause with no field to point at.** That is a hypothesis, and it
  needs an experiment.
- **Fixing where the symptom surfaced.** Correcting the final answer leaves the
  categoriser broken.
- **Confusing malformed with wrong.** Different owners, different fixes, same
  field.
- **One cause per failure, enforced.** Several things are often wrong at once;
  bench-058 fails three checks.
- **No route to "the task is wrong."** Guarantees a correct agent gets debugged.

## Exercise

Open [`annotated-failures.jsonl`](../../../evals/operations/strongbench/annotated-failures.jsonl).

1. For `bench-029`, apply the counterfactual test to step 1. Had `search_policy`
   returned a different set of policies, would the failure have occurred? What
   does your answer say about whether retrieval is the root cause?
2. The annotation labels this `MODEL.reasoning`, not `TOOLS.arguments`, even
   though the defect is visible in a `tool_arguments` field. Justify the label,
   and say which team each would send the work to.
3. Nineteen rows share the hypothesis "the model is answering from the prompt
   without using the evidence-producing tools." Which single field in the trace
   is the evidence for that claim, and why is it cheaper to establish than
   bench-029's cause?

Check your answer:

```text
1. The failure would still have occurred. policy-lodging-001 was returned and
   it contains the sentence that decides the task; the agent had the
   information and categorised against it anyway. Since changing step 1 does
   not change the outcome, retrieval fails the counterfactual test and is not
   the root cause — despite running first. Position upstream is not causation.

2. The argument was well-formed, correctly typed and passed validation, so
   nothing about its structure was wrong. What was wrong was the judgment that
   produced "lodging" for room service — a reasoning defect that happened to
   surface at an argument boundary. TOOLS.arguments would send this to whoever
   owns the harness and schemas, who would find nothing to fix.
   MODEL.reasoning sends it to whoever owns extraction, prompting and training
   data, which is where the fix actually is.

3. metadata.tool_calls, or equivalently the absence of any step with a
   tool_name. It is cheaper because it is a presence check on one field rather
   than a comparison of a value against a policy document — you can establish
   it for all 19 rows in a single pass without understanding any of the tasks.
   bench-029 required reading a policy, understanding the categorisation rule,
   and checking one argument against it.
```

Then pick a failure whose hypothesis you disagree with, and write the field you
would point at instead. If there is no field, you have found a hypothesis that
was never tested.

## Checkpoint

You are ready to move on when, for any failure, you can name the step, the
field, and the counterfactual that makes it the root cause — and can tell a
hypothesis from a confirmed cause without being reminded.

## Reading

- [`evals/operations/strongbench/taxonomy.md`](../../../evals/operations/strongbench/taxonomy.md)
  — read the `TOOLS.*` three side by side. Deciding between selection, arguments
  and interpretation *is* the root-cause step for tool failures, and the
  boundaries repay a careful read.
- [`evals/operations/strongbench/failure-report.md`](../../../evals/operations/strongbench/failure-report.md)
  — see what happens to your causes downstream. Hypotheses are ranked by how
  many failures each explains, which is only meaningful if each was established
  the same way.
