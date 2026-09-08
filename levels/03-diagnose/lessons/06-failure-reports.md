# Lesson 6: Failure Reports

## Core Idea

A failure report is not a record of what went wrong. It is a document that
causes work to happen — and if nobody does anything differently after reading
it, writing it was a waste of an afternoon.

That standard rules out most of what gets written. A list of failing task ids is
not a report. Neither is a table of counts, however well formatted. A report
earns its name when a reader who was not in the room can finish it and know
**what to fix first, why that and not something else, and how they will know it
worked.**

The structure follows from the audience, and there are three. An engineer needs
the ranked list of fixes. A release manager needs a ship-or-hold call. Whoever
builds the next dataset needs to know which failures are worth turning into
training data. One document serves all three if it is ordered that way; it
serves none of them if it is ordered as a narrative of your investigation.

## The Report This Repo Generates

`python3 -m evals.operations` writes
[`failure-report.md`](../../../evals/operations/strongbench/failure-report.md).
Its section order is the argument:

```text
Executive Summary          the numbers and the call, first
Failure Distribution       counts by label
Dominant Hypotheses        why, ranked by how many failures each explains
Recommended Interventions  what to do, in order
Level 4 Data Recommendation what the next stage should take from this
```

**The summary comes first and contains the recommendation.** Most readers stop
after it, so it must be self-contained:

```text
- scripted baseline: 89/100 tasks passed
- weak no-tool baseline: 0/30 tasks passed on the calibration slice
- annotated failures: 30
- release recommendation: hold changes that reduce benchmark success or
  increase submission-gate failures
```

Note the second line. Reporting a *deliberately weak* baseline alongside the
real one is what turns 89/100 from a number into a measurement — it shows the
benchmark can distinguish a working agent from a broken one. A benchmark that
has never been shown to fail is not yet evidence of anything.

## Hypotheses Ranked By Coverage

The section that does the most work:

```text
19x  The model is answering from the prompt without using the evidence-producing
     tools required by policy.
 7x  Receipt lookup is under-specified, so the agent retrieves the wrong receipt
     set before calculating.
 2x  The agent does not reliably preserve approval and submission boundaries.
 1x  The item parser is losing category/date context before the calculator runs.
 1x  The benchmark exposed an ambiguity that needs trace review.
```

Thirty failures, five hypotheses, **and the ordering is by how many failures
each one explains.** That number is the priority. It is not a judgment about
which bug is most interesting or most annoying; it is a count of what fixing it
would close.

The `1x` entry at the bottom is doing quiet work. "The benchmark exposed an
ambiguity" is a report saying the task might be wrong rather than the agent — the
`EVALUATION.expected_answer_wrong` escape hatch, surfaced. A report that cannot
say this will send someone to fix an agent that is behaving correctly.

## Interventions, Ordered And Falsifiable

```text
1. Fix receipt lookup argument extraction before expanding receipt-heavy tasks.
2. Add parser tests for room service and same-day meal limits.
3. Add prepare-vs-submit examples to preserve the employee submission gate.
4. Promote the regression pack into the Level 2 benchmark after each fix lands.
```

Three properties worth copying.

**They are ordered**, and the order tracks hypothesis coverage rather than
effort or novelty.

**They are specific enough to be wrong.** "Improve receipt handling" cannot fail
a review. "Fix receipt lookup argument extraction" names a component, so someone
can check whether it was done and whether it helped.

**Item 4 closes the loop.** Every fix promotes its regression cases into the
benchmark, so the same failure cannot return unnoticed. A report that recommends
fixes without recommending regression coverage is asking to write itself again
in three months.

## The Release Call Is A Separate Document

[`release-recommendation.md`](../../../evals/operations/strongbench/release-recommendation.md)
is short on purpose:

```text
Recommendation: do not weaken the Level 2 release gate.

The current scripted baseline passes the Level 2 gate, but the failures show
concrete risks in receipt lookup, item parsing, and approval boundaries. New
changes should ship only when they maintain or improve benchmark success and
do not add unsafe submission failures.
```

Separating it from the failure analysis matters because the two have different
lifetimes and different readers. The analysis is a snapshot of one run. The gate
is a standing policy that outlives it. Burying "do not weaken the gate" as the
last paragraph of a long report is how gates get weakened — by someone who
skimmed.

Notice it also survives good news. The baseline *passes*. The recommendation is
still to hold the line, because passing a gate is not evidence that the gate is
too strict.

## Common Failure Modes

- **A list of failures with no recommendation.** Data, not a report.
- **Ordering by investigation narrative.** Readers need the conclusion first,
  not the order in which you discovered it.
- **Interventions too vague to fail.** "Improve X" cannot be checked.
- **No weak baseline.** Without one, a passing score might mean the benchmark
  cannot detect failure.
- **No route for "the benchmark is wrong."** Guarantees someone debugs a correct
  agent.
- **Burying the release call.** It has a different reader and a longer life than
  the analysis around it.
- **Recommending fixes without regression cases.** The same failures return, and
  nobody notices until they are old.

## Exercise

Open [`failure-report.md`](../../../evals/operations/strongbench/failure-report.md)
and [`release-recommendation.md`](../../../evals/operations/strongbench/release-recommendation.md).

1. The dominant hypothesis covers 19 of 30 failures. Which recommended
   intervention addresses it, and why is it not listed first?
2. The summary reports a weak no-tool baseline at 0/30 next to the scripted
   baseline at 89/100. What claim does the second number let you make that the
   first alone does not?
3. The release recommendation says hold the gate even though the baseline
   passes it. Construct the argument someone would make for loosening it, and
   the counter-argument the report implies.

Check your answer:

```text
1. None of them directly — and that is the interesting part. The 19x hypothesis
   describes the weak-no-tool config, a deliberately broken control rather than
   the shipping agent. The interventions are ordered by what will improve the
   real baseline, so receipt lookup (7x on scripted-current) leads. Coverage
   ranks hypotheses; which config produced them decides whether the fix is
   worth doing. A report that mixed the two would send the team to fix a
   control.

2. That the benchmark can detect failure. 89/100 on its own is compatible with
   a benchmark so lenient that almost anything passes. 0/30 from an agent with
   its tools removed shows the tasks actually depend on the behaviour they
   claim to measure, which is what makes the 89 a measurement rather than a
   number.

3. For loosening: the gate is at 0.72, the baseline is at 0.89, so there is
   17 points of headroom and shipping is being slowed by a threshold nothing
   is near. Against: the gate is not sized to the current baseline, it is sized
   to the failures that would be unacceptable — and the annotated bundle shows
   live risks in receipt lookup, parsing, and approval boundaries. Headroom is
   the margin those risks are being held behind, not slack to spend.
```

Then write the executive summary you would send if the baseline had scored 71
against a 0.72 gate. Three sentences. Notice how much harder it is to be useful
when the recommendation is *hold*.

## Checkpoint

You are ready to move on when your failure report leads with a recommendation,
ranks hypotheses by how many failures each explains, states interventions
specifically enough to be checked, and keeps the release call as its own
document.

## Reading

- [`evals/operations/strongbench/instructor-review-guide.md`](../../../evals/operations/strongbench/instructor-review-guide.md)
  — read it as the reviewer of your own report. It sets out what a reader is
  entitled to expect, which is the standard your draft has to clear.
- [`model_improvement/strongbench/decision-memo.md`](../../../model_improvement/strongbench/decision-memo.md)
  — the document downstream of yours. Seeing what Level 5 does with your label
  counts is the fastest way to understand why vague labels are expensive.
