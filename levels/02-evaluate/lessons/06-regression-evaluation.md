# Lesson 6: Regression Evaluation

## Core Idea

A benchmark tells you how good the agent is. A regression eval tells you whether
you just broke something — and those are different jobs that people routinely
try to do with one number.

The distinction matters because agent changes are rarely uniformly good. A
prompt revision that lifts the aggregate by three points while destroying one
capability is the normal shape of a bad change, not an unusual one. The aggregate
cannot see it. Something has to be watching the specific behaviours you have
already paid to fix.

That is the second idea, and it is the one that makes regression evaluation a
practice rather than a rerun: **every bug you fix should leave a test behind.**
A failure that was diagnosed, fixed, and not encoded is a failure you have
agreed to find again. The regression pack is where that discipline lives.

## The Pack Is Built From Diagnosis

`python3 -m evals.operations` writes
[`regression-pack.jsonl`](../../../evals/operations/strongbench/regression-pack.jsonl):
30 cases, one per annotated failure, each carrying its origin.

```json
{"id": "bench-029",
 "source_annotation_id": "scripted-current:bench-029",
 "prompt": "I spent $68 on dinner and $40 on room service. How much is reimbursable?",
 "expected": {"total_reimbursable": 75.0,
              "policy_source_ids": ["policy-meals-001"],
              "approval_types": [], "requires_missing_information": false,
              "unsafe_action_refused": false},
 "tags": ["MODEL.reasoning", "calculation", "regression"]}
```

Three fields make this more than a copy of the benchmark.

**`source_annotation_id`** points back to the diagnosis. A year from now, when
this case starts failing after an unrelated refactor, nobody has to re-derive why
75.00 is correct — the annotation holds the trace, the root cause, and the
hypothesis, one hop away.

**`tags` carry the taxonomy labels**, not just topic tags. Every row has
`regression` plus the labels from Level 3: `RETRIEVAL.citation` on 20 rows,
`TOOLS.selection` on 19, `MODEL.reasoning` on 9. That means you can ask "did this
change break anything in the class of failures we fixed last quarter?" rather
than only "did anything break?"

**`expected` is the full contract**, not just the total. A change that gets the
number right while dropping the policy citation is caught, because the case
checks every field the original failure touched.

## Two Gates, Two Questions

The Level 2 threshold in
[`thresholds.json`](../../../evals/strongbench_benchmark/thresholds.json) is a
floor:

```json
{"min_success_rate": 0.72}
```

The baseline sits at 0.89, so there is 17 points of headroom. That headroom is
deliberate and it is *not* slack: it is the margin the known risks are held
behind. The release recommendation says as much — do not weaken the gate merely
because nothing is near it.

But a floor answers only "is the agent still acceptable?" It cannot answer "did
this specific change break a specific thing?", because a change can take a
capability from 100% to 0% while the aggregate stays comfortably above 0.72.
That is what the pack is for, and why the failure report's fourth recommendation
is to promote it into the benchmark after each fix lands.

| Instrument | Question | Fails when |
| --- | --- | --- |
| `min_success_rate` | is the agent shippable at all? | aggregate drops below the floor |
| per-tag table | is any capability broken? | a slice collapses while the mean holds |
| regression pack | did a fixed bug come back? | a previously-fixed case fails again |

Three instruments, three questions. Running only the first is the most common
mistake in this lesson.

## Version Metadata Or The Comparison Is Meaningless

A regression eval is a comparison, and comparisons need both sides pinned:

- agent version
- prompt version
- model
- tool versions
- retrieval corpus version
- **eval dataset version**
- timestamp

The fifth and sixth are the ones people omit and regret. If the benchmark itself
changed between the two runs, the delta mixes agent change with benchmark change
and cannot be attributed to either. Both numbers are real; they answer different
questions; nothing warns you.

This is the argument for promoting regression cases in a deliberate, recorded
step rather than continuously. Every promotion changes the benchmark, so it must
be a version bump you can point at, not a drift.

## The Cases That Currently Fail Are Also A Pack

Eleven benchmark tasks fail today. They are not a backlog to be embarrassed
about — they are the pack that proves the graders still work. If a change makes
`bench-029` start passing, you want to know that too, and to check it passed for
the right reason rather than because someone loosened a grader.

Which is the other half of regression discipline: **a case going green is also a
result that needs explaining.** Unexpected improvement is the classic signature
of a weakened check.

## Common Failure Modes

- **Only running the aggregate gate.** A capability can go to zero without
  moving it.
- **Fixing without adding a case.** You have agreed to rediscover the bug.
- **Cases with no link to their diagnosis.** A future failure becomes a fresh
  investigation.
- **Comparing runs across benchmark versions.** Two real numbers, different
  questions, no warning.
- **Promoting cases continuously.** The benchmark drifts and no comparison is
  stable.
- **Treating headroom above the floor as slack.** It is the margin the known
  risks sit behind.
- **Ignoring unexpected passes.** Cases going green without explanation is what
  a loosened grader looks like.

## Exercise

Open [`regression-pack.jsonl`](../../../evals/operations/strongbench/regression-pack.jsonl),
[`thresholds.json`](../../../evals/strongbench_benchmark/thresholds.json) and
[`sample-report.md`](../../../evals/reports/sample-report.md).

1. The threshold is 0.72 and the baseline is 0.890. Construct a change that
   passes the gate while breaking a capability entirely, using the per-tag table
   to make it concrete.
2. Every regression row carries `tags` including its Level 3 taxonomy labels.
   What question does that let you ask after a change that a pass/fail count
   cannot?
3. A refactor makes three currently-failing benchmark tasks start passing, and
   no code touched the agent's reasoning. What is your first hypothesis, and
   which file would you check?

Check your answer:

```text
1. receipt_lookup is 10 tasks, currently 3 passing. A change that breaks it
   entirely loses 3 tasks: 89 -> 86, or 0.860, comfortably above 0.72. The gate
   passes, the release proceeds, and an entire capability is dead. The per-tag
   table shows receipt_lookup at 0.000 — but only if someone reads it, which is
   the argument for gating on slices and not only on the aggregate.

2. Whether a change re-broke a class of failure you previously fixed. With
   labels you can ask "did anything tagged TOOLS.selection regress?" and get an
   answer scoped to the 19 cases that came from that diagnosis. A pass/fail
   count tells you the number moved; the labels tell you which kind of bug came
   back, which is what decides whether to revert.

3. Suspect a grader, not the agent. If nothing touched reasoning, an
   improvement in reasoning-dependent tasks is more likely a check that stopped
   discriminating. Check the graders — evals/strongbench_benchmark/graders/ —
   and diff them against the previous version. An unexplained pass is the same
   evidence as an unexplained failure; it is just more welcome, which is why it
   gets investigated less.
```

Then take one currently-failing task and write the regression case you would add
once it is fixed. Include the field that links it back to its diagnosis.

## Checkpoint

You are ready to move on when every fixed bug has a regression case linked to
its diagnosis, your runs record the eval dataset version alongside the agent
version, and you gate on slices as well as on the aggregate.

## Reading

- [`evals/operations/strongbench/failure-report.md`](../../../evals/operations/strongbench/failure-report.md)
  — its fourth recommendation is to promote the pack into the benchmark after
  each fix. Read it as the policy that turns a one-off fix into a permanent
  guard.
- [`evals/operations/strongbench/release-recommendation.md`](../../../evals/operations/strongbench/release-recommendation.md)
  — the standing rule your regression results feed. Note that it holds the gate
  even when the baseline passes comfortably.
