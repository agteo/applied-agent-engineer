# Lesson 5: Metrics and Confidence

## Core Idea

Every number a benchmark reports is an estimate from a sample, and an estimate
without a sense of its precision is an invitation to over-read it.

This is not a statistics lesson dressed up as an engineering one. It has a
concrete operational consequence: **the slice you most want to act on is usually
the slice with the fewest tasks in it**, because you added the capability
recently and gave it ten cases. Its number moves the most and means the least,
and that is exactly the number a team will spend a sprint chasing.

The skill is to read every rate alongside its denominator, and to know roughly
how much one task is worth on that denominator before deciding anything.

## One Task Is Not One Percent

The Level 2 report gives an aggregate and five slices:

```text
- tasks: 100
- passed: 89
- success_rate: 0.890
```

| Tag | Passed | Total | Rate | One task is worth |
| --- | ---: | ---: | ---: | ---: |
| calculation | 28 | 30 | 0.933 | 3.3 points |
| edge_case | 29 | 30 | 0.967 | 3.3 points |
| policy_question | 20 | 20 | 1.000 | 5.0 points |
| receipt_lookup | 3 | 10 | 0.300 | **10.0 points** |
| unsafe_submission | 9 | 10 | 0.900 | **10.0 points** |

On the full benchmark, one task moves the score by a point. On a ten-task slice
it moves it by ten. So `unsafe_submission` dropping from 0.900 to 0.800 is *one
task*, and a team that treats it as a ten-point regression will go looking for a
systemic cause that does not exist.

Before reacting to a slice, compute what one task is worth on it. That single
division prevents most over-reading.

## What The Intervals Actually Are

Wilson 95% intervals on the same numbers:

| Measure | Rate | 95% interval | Width |
| --- | ---: | --- | ---: |
| overall | 0.890 | [0.81, 0.94] | 0.12 |
| calculation | 0.933 | [0.79, 0.98] | 0.19 |
| policy_question | 1.000 | [0.84, 1.00] | 0.16 |
| unsafe_submission | 0.900 | [0.60, 0.98] | 0.39 |
| **receipt_lookup** | **0.300** | **[0.11, 0.60]** | **0.50** |
| rubric agreement | 1.000 | [0.57, 1.00] | 0.43 |

Three readings worth taking away.

**The aggregate is reasonably tight.** ±6 points at n=100. A change of two or
three points on the overall number is not clearly a change at all.

**`receipt_lookup` is genuinely broken and genuinely imprecise, at once.** The
interval [0.11, 0.60] does not come close to the other slices, so the finding is
real — but "30%" is not the finding. "Somewhere between a tenth and six tenths,
and far below everything else" is the finding, and it is enough to act on
because the *ranking* is unambiguous even though the point estimate is not.

**`policy_question` at 20/20 is not 100%.** Twenty successes gives a lower bound
around 0.84. Perfect scores on small samples are the most over-read numbers in
evaluation: they invite the conclusion that a capability is solved when the data
supports only "no failures seen in twenty tries".

**Rubric agreement at 5/5 is nearly uninformative.** The interval runs from 0.57
to 1.00. Lesson 4 makes the qualitative version of this argument — the sample
contains no `low` labels — and the interval makes the quantitative one.

## Rates Are Not The Only Metric

The report also carries operational numbers:

```text
- cost_usd: 0.0000
- latency_ms_p50: 0
- latency_ms_p95: 0
```

Zero here because the scripted adapter is offline and instant. On a real model
they matter, and the reason p50 *and* p95 are reported rather than a mean is
that agent latency distributions have long tails — a handful of runs that loop
to the step budget will drag a mean somewhere no individual run ever was.

Report a median for the typical case and a high percentile for the bad case.
Never a mean alone.

## When A Number Is Allowed To Move A Decision

Combining this with Lesson 6, a practical rule:

| Change | Read as | Because |
| --- | --- | --- |
| aggregate ±1–2 points | noise | inside the interval at n=100 |
| aggregate crosses the 0.72 gate | act | the gate is a decision, not an estimate |
| a 10-task slice ±1 task | noise | one task is 10 points |
| a 10-task slice collapses to 0 | act | ranking change, not a point estimate |
| a regression case flips | act | n=1 by design, and it is a named case |

The last row is the important asymmetry. A regression case is not a sample of
anything — it is a specific behaviour you decided must keep working. One case
flipping is a definite event, not an estimate, which is why regression packs are
read differently from slices.

## Common Failure Modes

- **Quoting a rate without its denominator.** "30%" and "3 of 10" prompt
  different reactions, correctly.
- **Chasing one task on a small slice.** Ten-point moves that are one test case.
- **Reading a perfect score as solved.** 20/20 has a lower bound near 0.84.
- **Comparing slices of different sizes as if equally precise.** The 30-task
  slices are twice as tight as the 10-task ones.
- **Reporting a mean latency.** The tail is the part users notice.
- **Treating a regression case as a sample.** It is a named requirement, not an
  estimate.
- **Adding tasks only to slices that already look good.** Precision goes where
  you spend cases, and the broken slice is where you need it.

## Exercise

Open [`sample-report.md`](../../../evals/reports/sample-report.md).

1. `unsafe_submission` is 9/10 and `calculation` is 28/30. Which is measured
   more precisely, and by roughly how much? Answer using the denominators before
   looking at any interval.
2. A change takes the aggregate from 0.890 to 0.870 and takes `receipt_lookup`
   from 3/10 to 0/10. Which movement should drive your response, and what would
   you say to someone who wanted to revert on the aggregate alone?
3. You have budget to add 40 tasks. Distribute them across the five tags and
   justify the split in terms of what each addition buys.

Check your answer:

```text
1. calculation, by roughly double. Its 30 tasks put one case at 3.3 points
   against 10 points on unsafe_submission's 10 tasks, and the intervals follow:
   0.19 wide versus 0.39. Both look like "about 90%" and one of them is three
   times less certain than the other.

2. receipt_lookup. Two points on a 100-task aggregate sits inside the interval
   and is not distinguishable from noise; a slice going 3/10 to 0/10 is a
   capability that stopped working entirely, and it is what caused the
   aggregate move. Reverting "because the aggregate dropped" would be the right
   action for the wrong reason — and would teach the team to watch a number
   that cannot see the failure that mattered.

3. Most of them to receipt_lookup: it is the broken slice, the least precise,
   and the one where a decision is pending, so precision there is worth the
   most. A smaller share to unsafe_submission, since it is the other 10-task
   slice and it covers a safety property where a wrong reading is expensive.
   Nothing to policy_question at 20/20 — more tasks there buy a tighter
   interval around a number nobody is going to act on. Spend cases where a
   decision depends on them.
```

Then recompute the aggregate assuming `receipt_lookup` were fixed to 10/10. The
benchmark moves from 0.890 to 0.960 — seven points from one capability, which is
the clearest possible argument for reading slices before priorities.

## Checkpoint

You are ready to move on when every rate you report carries its denominator, you
know what one task is worth on each slice, and you can say which movements in
your benchmark are large enough to act on.

## Reading

- [`evals/report.py`](../../../evals/report.py) — read what the report chooses to
  emit. Every metric here was a decision about what a reader would need; ask of
  each whether you could act on it.
- [`evals/strongbench_benchmark/thresholds.json`](../../../evals/strongbench_benchmark/thresholds.json)
  — a gate is a decision boundary, not an estimate. Notice that it is a single
  committed number, which is what makes crossing it unambiguous.
