# Lesson 4: Hypotheses and Interventions

## Core Idea

A diagnosis that does not end in something you can do is a description.

The chain that turns observation into work is short and each link is a different
kind of claim:

```text
Failure  ->  Evidence  ->  Hypothesis  ->  Intervention  ->  Experiment  ->  Result
```

**Failure** is what the grader reported. **Evidence** is fields in the trace.
**Hypothesis** is a claim about cause that goes beyond the evidence — which is
what makes it a hypothesis rather than a finding. **Intervention** is the change
you would make if the hypothesis is right. **Experiment** is how you would find
out. **Result** is what happened.

The two most common ways to break this chain: jumping from failure straight to
intervention with no hypothesis in between — a fix with no theory, which works
or does not for reasons you never learn — and writing a hypothesis so vague that
no intervention follows from it.

The test for a good hypothesis is therefore not whether it sounds right. It is
**whether a specific intervention falls out of it, and whether you would know if
it were wrong.**

## One Hypothesis Explains Nineteen Failures

The value of writing hypotheses down is that they group. From the annotated
bundle:

```text
19x  The model is answering from the prompt without using the evidence-producing
     tools required by policy.
 7x  Receipt lookup is under-specified, so the agent retrieves the wrong receipt
     set before calculating.
 2x  The agent does not reliably preserve approval and submission boundaries.
 1x  The item parser is losing category/date context before the calculator runs.
 1x  The benchmark exposed an ambiguity that needs trace review.
```

Thirty failures, five hypotheses. The count in front of each is its **coverage**,
and coverage is the closest thing diagnosis has to a priority: it says how many
failures this one change would close.

Coverage is not the whole priority — the 19x hypothesis describes a deliberately
broken control config, not the shipping agent, so it does not lead the
intervention list. But it is the first number to look at, and it is only
available because hypotheses were written as reusable claims rather than as
per-failure notes.

## Hypotheses Are Written To Be Wrong

Compare two ways of saying the same thing:

```text
Weak     The agent is bad at receipts.
Strong   Receipt lookup is under-specified, so the agent retrieves the wrong
         receipt set before calculating.
```

The strong version names a component, a mechanism, and an ordering. That is what
makes it disprovable: instrument `lookup_receipt`, and if the retrieved set is
correct on the failing tasks, the hypothesis is dead and you have learned
something. The weak version survives any observation, which is why it feels safe
and buys nothing.

Ask of your own: **what would I expect to see if this were false?** If nothing
comes to mind, the hypothesis is not yet written.

## Each Hypothesis Carries Its Intervention

In the bundle every annotation holds both fields, and each of the seven label
combinations maps to exactly one intervention:

| Hypothesis (abbrev.) | Intervention |
| --- | --- |
| answering without tools | tighten prompt/tool policy; fail CI when required evidence tools are skipped |
| receipt lookup under-specified | add receipt-id, merchant, date, trip-id extraction checks, then regression cases |
| approval boundaries not preserved | add prepare-vs-submit examples and deterministic tests |
| item parser losing category context | improve item extraction; unit tests for room service and multi-item meal limits |

Two properties to copy.

**The intervention names a component.** "Improve receipt handling" cannot be
reviewed. "Add receipt-id, merchant, date and trip-id extraction checks" can be
checked off, and can be found to have not worked.

**Every one ends in a test.** Extraction checks, deterministic tests, regression
cases, CI failure. An intervention that changes behaviour without adding a check
fixes today's failure and permits its return.

## Interventions Are Ranked By Cost, Not Just Coverage

Level 5 makes this explicit in
[`intervention-matrix.json`](../../../model_improvement/strongbench/intervention-matrix.json),
where each option carries a status and a success measure:

| Intervention | Status | Success measured by |
| --- | --- | --- |
| `tool_and_retrieval_fix` | recommended_next | receipt_lookup and citation slices improve |
| `prompt_revision` | use_as_low_cost_control | no regression below threshold, fewer approval failures |
| `small_lora_sft` | defer_until_tool_plateau | heldout improvement, unsafe-submission rate unchanged |
| `frontier_api_or_hybrid` | compare_if_quality_gap_remains | quality lift justifies cost and tradeoffs |

The success measure is written **before** the intervention runs. That ordering is
the whole discipline: a measure chosen afterwards will be the one the result
happens to satisfy. Writing it first is what makes the experiment in the next
lesson capable of returning "no".

Note also that `prompt_revision` is kept as a *control* rather than a fix. A
cheap intervention that you expect to do little is worth running precisely
because it calibrates how much of any improvement was the expensive change.

## Common Failure Modes

- **Failure straight to intervention.** A fix with no theory teaches nothing
  when it works.
- **Hypotheses that cannot be false.** "The agent is bad at X" survives every
  observation.
- **Interventions too vague to review.** No component named, nothing to check.
- **Interventions with no test.** The failure is permitted to return.
- **Ranking by coverage alone.** The largest group here belongs to a broken
  control config.
- **Success measures chosen after the result.** Any outcome then reads as
  progress.
- **One hypothesis per failure.** Hypotheses are meant to be reused across
  failures; that is where coverage comes from.

## Exercise

Open [`annotated-failures.jsonl`](../../../evals/operations/strongbench/annotated-failures.jsonl)
and [`intervention-matrix.json`](../../../model_improvement/strongbench/intervention-matrix.json).

1. Take the 7x hypothesis about receipt lookup. Write the observation that would
   disprove it, and say which field of the trace you would check.
2. The 19x hypothesis has the highest coverage but its intervention is not first
   in the report's ranked list. Explain why, and what that says about using
   coverage as a priority.
3. `prompt_revision` is listed as `use_as_low_cost_control` rather than as a
   fix. What does running it buy you that going straight to
   `tool_and_retrieval_fix` would not?

Check your answer:

```text
1. Instrument lookup_receipt on the seven failing tasks and inspect the
   observation. If the retrieved receipt set is correct and the failure happens
   later, the hypothesis is disproved — the problem is downstream of retrieval,
   in the calculation or the answer. The field is the lookup_receipt step's
   observation, compared against the receipt ids the task actually concerns.

2. The 19 failures come from config "weak-no-tool", a deliberately broken
   control, not the shipping agent. Fixing it would improve nothing anyone
   ships. Coverage ranks hypotheses by explanatory power, which is the right
   first cut, but priority also needs to know which build produced the
   failures. Coverage without the config field is a ranking of the wrong thing.

3. It calibrates. If a cheap prompt change captures most of the improvement,
   the expensive tool work was not the binding constraint and you have learned
   that for the price of an afternoon. If it captures none, any later gain from
   tool_and_retrieval_fix is more credibly attributable to the tools rather
   than to incidental prompt drift that shipped alongside it.
```

Then take a hypothesis from the bundle and write the experiment that would test
it: control, intervention, measurement, and the result that would make you
abandon it. That is Lesson 5.

## Checkpoint

You are ready to move on when each of your hypotheses names a mechanism, has an
observation that would disprove it, carries an intervention that names a
component, and states its success measure before the intervention runs.

## Reading

- [`evals/operations/strongbench/intervention-experiment.md`](../../../evals/operations/strongbench/intervention-experiment.md)
  — one hypothesis carried through to a result. Read it after writing an
  intervention of your own, and compare how much of your version is testable.
- [`model_improvement/strongbench/decision-memo.md`](../../../model_improvement/strongbench/decision-memo.md)
  — where interventions get chosen between. It shows what a hypothesis has to
  look like to survive contact with a budget.
