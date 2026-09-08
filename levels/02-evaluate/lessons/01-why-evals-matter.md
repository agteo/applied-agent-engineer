# Lesson 1: Why Evals Matter

## Core Idea

Without evaluation you have opinions about your agent. With evaluation you have
a number you can be wrong about — and being wrong in a way you can detect is the
whole point.

The reason this matters more for agents than for ordinary software is that
agents fail *plausibly*. A broken function throws. A broken agent returns a
confident, well-formatted, entirely wrong answer, and nothing in the output
distinguishes it from a correct one. In this repo, `bench-029` produces a clean
summary, cites a real policy, reports `"confidence": "high"`, and is wrong by
thirty-three dollars. No exception was raised. No log line was unusual.

That is the gap evaluation closes. Not "is the agent good?" — a question that
resists answering — but the two questions you can actually act on: **did this
change make things worse, and is it safe to ship?**

## Demos Prove Nothing

Every agent has a demo where it works. It was built against those cases.

The failure of demo-driven development is not that the demo is faked; it is that
the demo is a sample of size one, chosen by the person with the strongest reason
to choose favourably. It cannot detect a regression, cannot compare two
configurations, and cannot tell you which of an agent's capabilities is broken —
because it exercises one.

Compare with the artifact this level produces:

```text
- tasks: 100
- passed: 89
- success_rate: 0.890

| receipt_lookup | 3 | 10 | 0.300 |
```

The second line is a claim about the whole system. The fourth is the finding: a
capability that fails seven times in ten, invisible to anyone running a demo of
the other four.

## A Benchmark Has To Be Shown To Fail

Here is the trap that makes many benchmarks worthless: **a test that everything
passes is not a test.** A benchmark whose tasks can be satisfied without doing
the work will report a high number for an agent that does not work, and the
number will feel like reassurance.

This repo checks for that explicitly by running a deliberately broken
configuration alongside the real one:

```text
scripted baseline:      89/100 passed
weak no-tool baseline:   0/30  passed
```

`weak-no-tool` is the same agent with its evidence-producing tools removed — it
answers from the prompt. It scores zero. That is what makes the 89 a
measurement: the tasks genuinely require the behaviour they claim to require,
and an agent that skips it is caught on every single one.

Run a deliberately broken configuration against your own benchmark before
trusting it. If it does well, your benchmark is measuring something other than
what you think.

## The Number Becomes A Gate

An eval that informs is useful. An eval that *blocks* changes behaviour.

```json
{"min_success_rate": 0.72}
```

That threshold is committed to the repo and enforced in CI. A change that drops
the benchmark below it fails the build, which converts "we should check the
benchmark" from a discipline someone has to remember into a property of the
pipeline.

The gap between 0.890 and 0.72 is not slack. It is the margin the known failures
sit behind — receipt lookup, item parsing, approval boundaries — and the release
recommendation says explicitly not to weaken the gate merely because nothing is
near it.

## What Evaluation Cannot Do

Worth stating early, so the rest of the level is read accurately.

**It cannot tell you the agent is good.** It tells you the agent scores 0.890 on
one hundred tasks that someone chose. Coverage is a design decision, and the
benchmark cannot see what it does not contain.

**It cannot replace diagnosis.** A score says something is wrong, never why.
That is Level 3, and it needs traces the benchmark does not read.

**It cannot outrun contamination.** If tasks leak into training data, the
number rises and means less. That is Level 4.

**A passing gate is not evidence of correctness.** It is evidence that a
specific set of checks did not fire.

An evaluation you understand the limits of is worth more than one you trust.

## Common Failure Modes

- **Shipping on a demo.** A sample of one, chosen by an interested party.
- **Trusting a benchmark nothing has failed.** Run a broken config first.
- **Reading the aggregate only.** 89% conceals a capability at 30%.
- **Treating the score as a verdict on quality.** It is a score on the tasks you
  wrote.
- **An eval that informs but does not gate.** Discipline decays; CI does not.
- **Weakening the gate because there is headroom.** The headroom is the margin.
- **Expecting the score to explain itself.** Scores locate; traces explain.

## Exercise

Open [`sample-report.md`](../../../evals/reports/sample-report.md) and
[`intervention-experiment.md`](../../../evals/operations/strongbench/intervention-experiment.md).

1. `weak-no-tool` scores 0/30 and the scripted baseline scores 89/100. What
   claim does having both numbers support that either alone would not?
2. A colleague proposes lowering `min_success_rate` from 0.72 to 0.65 because
   "no build has ever come close to failing it." Give the strongest version of
   their argument, then the counter-argument.
3. `bench-029` returns a fluent, well-cited answer with `"confidence": "high"`
   and is wrong. Name two things in the report that catch it, and one thing that
   would not have.

Check your answer:

```text
1. That the benchmark can detect failure. 89/100 alone is compatible with a
   lenient benchmark almost anything passes; 0/30 alone says only that a broken
   agent is broken. Together they show the tasks depend on the behaviour they
   claim to measure — removing the tools collapses the score to zero — which is
   what upgrades 89 from a number to a measurement.

2. For: a gate nothing approaches is not gating anything, it is ceremony, and
   the real quality bar is enforced by review. Against: the gate is not sized to
   the current baseline, it is sized to what would be unacceptable to ship. The
   annotated failures show live risks in receipt lookup, parsing and approval
   boundaries; the headroom is the margin those are held behind. Lowering the
   floor because you are far from it is spending a safety margin to buy nothing.

3. Caught by: the deterministic total check, which compares 108.00 against the
   expected 75.00 and reports both values; and the per-tag table, where the
   failure contributes to a slice that can be seen collapsing. Not caught by:
   the agent's own confidence field, which reports "high" — self-reported
   confidence measures internal coherence, and this trace is perfectly coherent
   from the miscategorisation onward.
```

Then run `python3 -m evals.runner --model scripted` and read the header before
the slice table. Notice how different a picture you have after ten more seconds
of reading.

## Checkpoint

You are ready to move on when you can state what your benchmark can and cannot
establish, have run a deliberately broken configuration against it, and know
what your gate is protecting rather than only what it is set to.

## Reading

- [`evals/operations/strongbench/release-recommendation.md`](../../../evals/operations/strongbench/release-recommendation.md)
  — one page on why a passing baseline is not a reason to relax a gate. Read it
  before the first time someone proposes lowering yours.
- [SWE-bench](https://github.com/princeton-nlp/SWE-bench) — a benchmark whose
  tasks cannot be passed without doing the work, because the success criterion
  is an executable test suite. Read it when deciding how much of your own
  grading can be made that unambiguous.
