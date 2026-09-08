# Lesson 3: Rollouts and Filtering

## Core Idea

A rollout log is the raw material for everything in Level 7, and raw material
needs a gate. Not every episode belongs downstream: some are incomplete, some
ended in ways that make their return meaningless, and some are perfectly valid
and still useless for the purpose at hand.

Two questions, and keeping them apart is the lesson:

**Is this rollout well-formed?** A structural question with a yes/no answer,
answerable by a filter. Missing actions, missing observations, no reward, an
unrecognised termination reason.

**Is this rollout useful?** A judgment about the set as a whole — whether it has
the variance a trainer needs, whether it covers the behaviours you care about,
whether it is all from one policy.

A filter answers the first. Nothing answers the second except looking, which is
why the second is where teams get surprised.

## The Filter Is Four Checks

```python
def rollout_rejection_reason(row):
    if not row.get("actions"):        return "missing_actions"
    if not row.get("observations"):   return "missing_observations"
    if "verifier" not in row or "reward" not in row:
                                      return "missing_verifier_or_reward"
    if row.get("termination_reason") not in {"final_answer", "truncated"}:
                                      return "invalid_termination"
    return None
```

Each rejects a rollout that cannot support downstream use.

**No actions** — nothing happened, so there is nothing to learn from or grade.

**No observations** — the actions have no consequences recorded, so the
trajectory cannot be reconstructed.

**No verifier or reward** — unscored, so it cannot contribute to any comparison.

**Unrecognised termination** — an episode that ended for a reason the runner does
not know about. This one is subtler than the others: an episode that crashed
mid-step may have a plausible-looking prefix and a return that means nothing,
because the return is over a truncated trajectory. Including it silently biases
every average.

Rejections go to `rl-rollouts-rejected.jsonl` with a reason, the rollout id, the
task id and the policy. **Log the refusal, always** — the same rule as Level 4's
cleaner and Level 5's SFT export, for the same reason: a silent filter and a
broken filter are indistinguishable from the outside.

## Zero Rejections Is A Result, Not A Relief

```text
rollout_count: 360    rejected_count: 0
```

Read that with suspicion. Zero rejections means one of two things: the producers
are well-behaved, or the filter does not bite.

Here it is genuinely the first. All three policies are scripted — they always
emit `final_answer`, always populate actions and observations, always get scored
— so nothing *can* trip the filter. The four checks are untested by construction.

That is fine now and will not be later. **The first time a sampled or learned
policy writes into this log, that number should move**, because a stochastic
policy can loop to a step budget, crash mid-episode, or produce an empty
trajectory. If it does not move, test the filter directly rather than concluding
your policy is unusually tidy.

A filter you have never seen reject anything is a filter you have not tested.

## Label Every Rollout With Its Policy

`label_rollouts` attaches the policy name and derives a termination reason, and
it refuses to relabel:

```python
existing = labeled.get("policy")
if existing and existing != policy:
    raise ValueError(f"rollout {labeled.get('rollout_id')} is policy {existing}, not {policy}")
```

That guard is worth having. Merging logs from several policies is exactly when a
mislabel happens, and a mislabelled rollout is invisible afterwards — it just
makes one policy's average slightly wrong in a way nothing flags.

Failing loudly at merge time beats a quiet miscomparison later.

## The Composition Matters More Than The Count

360 rollouts, and the useful description is not the total:

| Policy | Rollouts | Success | Avg reward | Distinct rewards |
| --- | ---: | ---: | ---: | ---: |
| `scripted_reference` | 120 | 1.000 | 1.90 | **1** |
| `weak_submitter` | 120 | 0.000 | −1.63 | 4 |
| `reward_hacker` | 120 | 0.000 | −0.82 | 4 |

Three policies, evenly split, and **nine distinct reward values across the whole
set**. The reference policy has one.

For a regression suite this is ideal: every rollout is reproducible and any
change to a verifier moves a known number. For training it is unusable, because
advantage estimation compares returns *within* a group and identical returns
compare to nothing.

**A rollout set is not a general-purpose asset.** It is fit for a purpose, and
`distinct_rewards` is the column that tells you which. Report it.

## Filtering For Training Is A Different Job

Structural filtering is the floor. A trainer usually wants more:

- **Within-policy variance.** Zero here, so nothing to learn from.
- **A stochastic producer.** Scripted policies replay decisions; sampling
  explores them.
- **Balance across task families.** All eight are present, but a filter that
  kept only successes would silently drop the hardest ones.
- **No contamination with the evaluation set.** The same discipline as Level 4:
  rollouts on held-out tasks are measurement, not training data.

The third deserves care. "Keep only rollouts that passed" is an obvious-looking
filter and it removes exactly the episodes with the most signal about what not to
do. Filter for well-formedness; think much harder before filtering on outcome.

## Common Failure Modes

- **Silent rejection.** Indistinguishable from a broken filter.
- **Reading zero rejections as good news.** It usually means untested.
- **No policy label.** A merged log cannot be compared by policy.
- **Relabelling on merge.** One policy's average is quietly wrong.
- **Accepting unknown termination reasons.** Truncated returns bias every mean.
- **Reporting only the rollout count.** Composition and variance are the useful
  facts.
- **Filtering on success for training data.** Removes the failures that carry
  the signal.
- **Assuming a valid log is training data.** Well-formed and useful are separate
  properties.

## Exercise

Open [`rl-rollouts.jsonl`](../../../rl_reliability/strongbench/rl-rollouts.jsonl)
and `rollout_rejection_reason` in
[`rl_reliability/strongbench/__init__.py`](../../../rl_reliability/strongbench/__init__.py).

1. Construct a rollout that trips `invalid_termination`, and explain why
   including it would bias an average return rather than simply adding noise.
2. `rejected_count` is 0 of 360. Give the two possible explanations and say how
   you would tell them apart without waiting for a learned policy.
3. A colleague proposes filtering the log to keep only rollouts where
   `verifier.passed` is true, to "train on good examples". Give the strongest
   version of their argument and then the objection.

Check your answer:

```text
1. A rollout whose termination_reason is neither "final_answer" nor "truncated"
   — an episode that ended on an exception or a timeout recorded under another
   name. Its reward is computed over a trajectory that stopped early, so the
   penalties it never had a chance to incur are missing and its return is
   systematically higher than a completed episode's. Including such rollouts
   inflates the mean in one direction; that is bias, not noise, and averaging
   more of them does not cancel it.

2. Either the producers are well-behaved or the filter does not bite. Tell them
   apart by testing the filter directly: hand-construct four rollouts, one per
   rejection reason, and assert each is rejected with the right reason. That is
   a unit test, not an experiment, and it converts "we have never seen it fire"
   into "we know it fires".

3. For: supervised fine-tuning learns from demonstrations, and a failed rollout
   demonstrates the wrong behaviour, so filtering to successes gives a cleaner
   imitation target. Against: for RL specifically, the signal is the difference
   between outcomes — keeping only successes removes the contrast, and with
   this set it would leave 120 identical rollouts and zero variance. It also
   removes the failure modes you most want the policy to learn to avoid. For an
   SFT export the argument has more force; for a rollout log feeding advantage
   estimation it removes the thing being estimated.
```

Then write the four unit tests from question 2. The filter should reject each
constructed rollout with the expected reason, and accept a well-formed one.

## Checkpoint

You are ready to move on when your filter logs every rejection with a reason,
you have tested that each reason can fire, every rollout carries its policy, and
you report the composition and reward variance of a log rather than only its
size.

## Reading

- [`rl_reliability/strongbench/rollout-schema.json`](../../../rl_reliability/strongbench/rollout-schema.json)
  — the ten required fields. Every one exists because some downstream step
  breaks without it; the filter is that schema enforced at use time.
- [`rl_reliability/strongbench/experiment-report.md`](../../../rl_reliability/strongbench/experiment-report.md)
  — its "What this rollout set cannot do" section states the variance problem in
  the terms a trainer cares about.
