# Lesson 6: Training Experiments

## Core Idea

A training run is an experiment, and the expensive part is not the compute. It
is that a training run produces a number you will be strongly motivated to
believe.

That motivation is the design problem. By the time results arrive you have spent
a budget, waited, and told people it was happening. A decision rule written at
that moment will be shaped by the result it is about to judge. So the rule has to
exist first, in a file, before anything runs — not as a formality but because it
is the only version of the rule you can trust.

[`experiment-plan.md`](../../../rl_reliability/strongbench/experiment-plan.md) is
committed with no run behind it, which is exactly the right order.

## The Plan Has Five Sections

**Question.** One sentence, answerable:

```text
Can experience in the StrongBench Finance simulator improve policy reliability
without increasing unsafe actions?
```

Note the second clause. The question is not "does reward go up" but a
conjunction that already contains the thing that could go wrong. A question
phrased as "does it improve?" has pre-decided what counts as improvement.

**Baselines.** Two, both named and runnable: `scripted_reference` as the sanity
check and `weak_submitter` as a negative control. The negative control is the
part teams skip. Without a policy you expect to fail, a metric that fails to
discriminate looks like a policy that failed to learn.

**Training path.** What a real run must save: training logs, reward curves,
sampled rollouts, post-training benchmark results. Four artifacts, listed before
the run, so "we forgot to save the curves" is a known omission rather than a
discovery.

**Decision rule.** Below.

**Current offline result.** 360 accepted rollouts, no trained-policy result,
"ready for experiment design, not adoption." A plan that states its own status
cannot be mistaken for a report.

## The Decision Rule Must Be Able To Say No

```text
A trained policy is better only if heldout simulator success improves, unsafe
submission failures do not increase, and the Level 2 benchmark does not regress.
```

Three conditions, conjoined, each closing a different escape:

- **held-out** rather than seen tasks — memorisation cannot satisfy it
- **unsafe submissions flat or better** — the safety property, not netted into an
  aggregate
- **Level 2 does not regress** — improvement must not come at the cost of the
  original task distribution

Written as an *only if*. The rule specifies what would make you accept, which
means every other outcome is a rejection by default. That phrasing does real
work: a rule listing what would make you reject invites arguing about whether
this particular result is one of those cases.

## Sizing: Smoke Before Small

Two configs exist, and the distinction is worth adopting:

| Config | Task count | Steps | Purpose |
| --- | ---: | ---: | --- |
| `acme-finance-reliability-smoke` | 8 | 5 | prove the pipeline moves |
| `acme-finance-reliability-small` | 120 | 400 | could support a claim |

The smoke config is **not expected to improve anything**. Its job is to confirm
that rollouts flow, reward is computed, gradients apply, checkpoints save. Run
it, look at nothing but whether it completed, and throw the result away.

The small config carries `train_seed: 42` and `heldout_seed: 7` — the held-out
condition made concrete. Different seed, different tasks from the same pools,
so the evaluation set is generated rather than curated.

Both are marked `status: "template_not_run"`. Templates that say so cannot be
mistaken for records.

## What This Rollout Set Cannot Do

The plan is honest about its own inputs, and this is the most useful line in it:

```text
Across every policy there are 9 distinct reward values in total, and each policy
is close to constant within itself.
```

`scripted_reference` has **one** distinct reward across 120 rollouts. Advantage
estimation compares returns within a group; identical returns compare to
nothing. Whatever the framing says, this data cannot train anything.

Generating training data means sampling a stochastic policy, not replaying
scripted ones. Until that exists, the rollout set is a regression suite — which
is a genuinely useful thing to be, and not the thing a trainer needs.

**Check the variance of your rollout set before designing a run against it.** It
is one line of code and it can save the entire budget.

## Record What The Run Depended On

Every artifact a comparison needs must be pinned:

```text
base model, adapter, prompt version, tool versions,
environment seed, benchmark version, config file, CLI version
```

The failure mode is silent. A benchmark edited between the two arms makes both
numbers real and their difference meaningless, and nothing warns you. The
Prime validation note says to record `prime --version` in the run report for the
same reason — the tooling is part of the experiment.

## Common Failure Modes

- **Writing the decision rule after the result.** It will accommodate the
  result.
- **A question phrased as "does it improve?"** Pre-decides what improvement
  means.
- **No negative control.** A non-discriminating metric looks like a failed run.
- **Skipping the smoke run.** Pipeline bugs surface after the expensive run.
- **Training on the seed you evaluate on.** Measures memory.
- **Not checking reward variance first.** Budget spent on data with no signal.
- **Unpinned benchmark version.** Two real numbers, no valid comparison.
- **A plan with no status field.** Read later as a result.

## Exercise

Open [`experiment-plan.md`](../../../rl_reliability/strongbench/experiment-plan.md)
and the two configs in `integrations/prime-intellect/configs/rl/`.

1. The decision rule is phrased as "better only if" rather than listing failure
   conditions. Explain what that phrasing prevents during the argument after a
   disappointing run.
2. The smoke config uses 8 tasks and 5 steps. Give the outcome that would make it
   a success, and say why improvement is not one of them.
3. The small config sets `train_seed: 42` and `heldout_seed: 7`. Describe what
   goes wrong if both are 42, and why it would be hard to notice.

Check your answer:

```text
1. It makes rejection the default. With an "only if" rule, any result not
   meeting all three conditions is a reject and the burden is on the advocate to
   show all three were met. A rule listing failure conditions invites the
   argument "this isn't really a regression, it's within noise" — the discussion
   becomes whether the result matches a rejection case, which is a much easier
   bar to argue past when a budget has been spent.

2. Success is that it completed: rollouts generated, reward computed, gradients
   applied, checkpoint written. Improvement is not a success criterion because
   8 tasks and 5 steps cannot produce a measurable capability change — any
   movement is noise, and treating it as signal is how a smoke run becomes a
   result. Its only job is to find pipeline bugs before the expensive run.

3. Training and evaluation would draw from the same task set, so held-out
   success would measure memorisation rather than generalisation. It is hard to
   notice because the numbers look good — better than a genuine held-out
   evaluation would give — and nothing errors. Both seeds are valid, both runs
   complete, and the report reads as a success. The only symptom is a model that
   does not transfer, discovered later and elsewhere.
```

Then write the experiment plan for a run you would actually want: question,
baselines, artifacts to save, decision rule. Write the decision rule first and
notice how it constrains the rest.

## Checkpoint

You are ready to move on when your plan is committed before the run, its
question contains the failure it is guarding against, its decision rule is a
conjunction phrased as "only if", and you have checked that your rollout set has
the variance a trainer needs.

## Reading

- [`integrations/prime-intellect/VALIDATION.md`](../../../integrations/prime-intellect/VALIDATION.md)
  — what is and is not validated about the hosted path, and the CLI and account
  differences to record. Read it before assuming a config file is executable.
- [`integrations/prime-intellect/reports/template.md`](../../../integrations/prime-intellect/reports/template.md)
  — the evidence a completed run must produce. Design your plan so it will
  produce all of it.
