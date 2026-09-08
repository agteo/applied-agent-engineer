# Lesson 7: Eval Reports

## Core Idea

An eval report is the artifact a decision gets made from. Not the run, not the
logs — the report. Which means its job is not to describe what happened but to
**put the reader in a position to act, and to make over-claiming difficult.**

Two properties follow, and they pull in different directions. The report must be
short enough that people read all of it, and complete enough that nobody has to
open the raw output to check the headline. Getting both is mostly a matter of
ordering: the number that decides things first, the number that qualifies it
second, and the detail that supports both underneath.

The third property is the one people leave out. A report should be
**regenerable**. If a human assembles it by hand, it is a snapshot of a moment
and it starts drifting immediately. If a builder emits it, the report and the
run cannot disagree.

## The Report This Repo Emits

`python3 -m evals.runner --model scripted --report evals/reports/sample-report.md`
produces [`sample-report.md`](../../../evals/reports/sample-report.md), and its
three sections are the argument:

```text
Header metrics     the aggregate and the operational numbers
Success By Tag     the same result, sliced
Failures           every failure, by task, with values
```

**The header is the decision surface.**

```text
- model: scripted
- tasks: 100
- passed: 89
- success_rate: 0.890
- cost_usd: 0.0000
- latency_ms_p50: 0
- latency_ms_p95: 0
- rubric_agreement_rate: 1.000
- rubric_agreement_sample_size: 5
```

Note the last line. Reporting the agreement rate *without* its sample size would
be misleading, and the report refuses to do it — the two are emitted together so
a reader cannot see 1.000 without also seeing that it rests on five examples.

**Pair every rate with its denominator.** That single convention prevents most of
the over-reading described in Lesson 5, and it costs one extra line.

Note also `model: scripted`. A result without the configuration that produced it
cannot be compared with anything, and six months later nobody will remember.

## The Slice Table Is Not Optional

```text
| Tag              | Passed | Total |  Rate |
| calculation      |     28 |    30 | 0.933 |
| edge_case        |     29 |    30 | 0.967 |
| policy_question  |     20 |    20 | 1.000 |
| receipt_lookup   |      3 |    10 | 0.300 |
| unsafe_submission|      9 |    10 | 0.900 |
```

The header says 89%. This table says the agent is fine at four things and
broken at one. Those are different conclusions and only one of them is
actionable.

Reporting `Passed` and `Total` beside `Rate`, rather than the rate alone, is the
same discipline as the sample size above: the reader can see that
`receipt_lookup` is three of ten and calibrate accordingly, without doing
arithmetic or trusting the author to have thought about it.

A report that emits only an aggregate is not a shorter report. It is a report
that has hidden its most important finding.

## Failures Are Listed In Full, With Values

```text
### bench-029
- bench-029: total_reimbursable: expected 75.00, got 108.00.

### bench-038
- bench-038: approval_types: missing expected approval types ['manager'].
- bench-038: missing_information: expected present=True, got present=False.
```

Two properties worth insisting on.

**Every failure appears.** Not a sample, not the first five. Eleven tasks failed
and eleven appear, because the section's job is to be the input to Level 3
diagnosis, and a truncated list silently decides what gets diagnosed.

**Each line carries both values.** `expected 75.00, got 108.00` lets a reader
form a hypothesis without opening a trace. `total_reimbursable: FAIL` would cost
a debugging session per line.

And a task can appear more than once. `bench-038` failed two independent checks,
so it gets two lines — the grader accumulates rather than short-circuiting, and
the report preserves that. One line per task would hide the fact that some
failures are multi-causal, which is precisely what makes them expensive.

## The Report Is Generated, So It Cannot Lie

[`report.py`](../../../evals/report.py) builds every line from the run's own
results. Nothing is typed by hand, which buys three things:

- the numbers cannot drift from the run
- the report is byte-reproducible, so CI can diff it
- a change to what is measured forces a change to what is reported

That last one is the underrated benefit. When someone adds a grader, they must
decide where it surfaces. A hand-written report lets new checks be added and
quietly never reported.

Byte-reproducibility is also what lets the report be committed. A regenerated
report that differs from the committed one means the *agent* changed — which is
the whole basis of the release gate in Lesson 6.

## Common Failure Modes

- **Aggregate only.** Hides the broken capability, which is the finding.
- **Rates without denominators.** 30% and 3-of-10 prompt different reactions.
- **An agreement rate without its sample size.** 1.000 on n=5 reads as certainty.
- **Truncated failure lists.** Silently decides what gets diagnosed.
- **Failure lines without values.** Costs a debugging session each.
- **One line per failing task.** Hides multi-causal failures.
- **No configuration recorded.** The result cannot be compared to anything.
- **Hand-assembled reports.** They drift, and new checks go unreported.

## Exercise

Open [`sample-report.md`](../../../evals/reports/sample-report.md) and
[`report.py`](../../../evals/report.py).

1. The header reports `rubric_agreement_rate` and
   `rubric_agreement_sample_size` as two separate lines. What would a reader
   conclude from the first alone, and why is emitting them together a design
   decision rather than a formatting one?
2. `bench-038` appears with two failure lines and `bench-029` with one. What
   does that tell you about the grader, and what would be lost if the report
   emitted one line per failing task?
3. The report is generated and committed. Describe what a diff on this file
   means after a change to the agent, and what it means after a change to a
   grader.

Check your answer:

```text
1. From 1.000 alone a reader concludes the judge is calibrated and can be
   trusted. The sample size line reveals it rests on five examples, whose 95%
   interval runs from about 0.57 to 1.00 — nearly uninformative. Emitting them
   together makes the misreading unavailable: you cannot quote the rate from
   this report without also seeing what it rests on. That is a design decision
   about what the report permits, not about layout.

2. The grader accumulates failures rather than stopping at the first, so a task
   failing three checks produces three lines. One line per task would hide
   multi-causal failures — bench-038 gets both its approval and its
   missing-information defects reported, and a diagnostician who saw only the
   first would fix half of it and consider the case closed.

3. After an agent change, a diff is the intended signal: behaviour moved, and
   the diff shows exactly which tasks and fields. After a grader change, a diff
   is expected too — but it means every number produced under the old grader is
   no longer comparable, so the report must be regenerated and the change
   flagged as a measurement change rather than an agent change. Same diff, two
   very different meanings, which is why the commit that changes a grader
   should never also change the agent.
```

Then regenerate the report and confirm it is byte-identical to the committed
copy. If it is not, either the agent changed or something in the report is not
deterministic — and both are worth knowing before you trust the next run.

## Checkpoint

You are ready to move on when your report is generated rather than written,
pairs every rate with its denominator, lists every failure with both values, and
records the configuration that produced it.

## Reading

- [`evals/report.py`](../../../evals/report.py) — read what it chooses to emit
  and in what order. Every section is answering a question someone asked once;
  yours should be able to explain itself the same way.
- [`evals/operations/strongbench/failure-report.md`](../../../evals/operations/strongbench/failure-report.md)
  — the Level 3 document downstream of this one. Seeing what diagnosis needs
  from your Failures section is the best argument for listing all of them.
