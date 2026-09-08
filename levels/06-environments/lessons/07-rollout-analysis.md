# Lesson 7: Rollout Analysis

## Core Idea

A rollout is one episode: a task, the actions an agent took, what the
environment returned, and how it was scored. A rollout *log* is the whole set,
and it is the environment's real output. Everything downstream — evaluation,
diagnosis, training data, regression suites — reads from it.

Which makes the design question worth stating plainly: **a rollout record should
contain everything needed to answer a question about the run without re-running
it.** Re-running is not always possible. The policy may be gone, the seed may
have moved, and the interesting run happened in a session you cannot reproduce.
Anything you did not write down is a question you can never ask.

The analysis skill is the mirror of that. A success rate summarises rollouts; it
does not explain them. Two policies in this repo both score 0.0, and they fail
for completely different reasons that no aggregate can distinguish. Learning to
read past the mean is what this lesson is for.

## What A Record Holds, And Why

One line of
[`environments/strongbench_finance/rollouts.jsonl`](../../../environments/strongbench_finance/rollouts.jsonl):

```json
{"rollout_id": ..., "environment": ..., "policy": ..., "task_id": ..., "seed": ...,
 "initial_state_hash": "932ca7a7...", "terminal_state_hash": "cb6c02bd...",
 "actions": [...], "observations": [...],
 "verifier": {"passed": ..., "checks": {...}, "expected": {...}, "evidence": {...}},
 "reward":   {"total": ..., "components": {...}}}
```

| Field | The question it makes answerable later |
| --- | --- |
| `policy`, `seed` | which agent, which task set — without these a log is anonymous |
| `initial_state_hash` / `terminal_state_hash` | did this episode change anything at all? |
| `actions` | what did it try? |
| `observations` | what did the environment tell it? |
| `verifier.checks` | which specific requirement failed? |
| `verifier.evidence` | what did it read, retrieve, and cite? |
| `reward.components` | which behaviour earned or lost what? |

The two hashes are the cheapest useful field in the record. `initial == terminal`
means the episode was a no-op — the agent talked and changed nothing. You can
scan for that across a million rollouts without parsing a single action.

`verifier.evidence` is the field people leave out and regret. Here it holds
`receipts_looked_up`, `policies_retrieved`, `policies_cited` and
`model_judgment`. Storing what the agent *read*, separately from what it
*claimed*, is what makes the next section possible.

## Reading Past The Mean

The Phase 7 bundle logs three policies over the same 120 tasks:

| Policy | Success | Avg reward | Distinct rewards | Unsafe submissions |
| --- | ---: | ---: | ---: | ---: |
| `scripted_reference` | 1.000 | 1.90 | **1** | 0 |
| `weak_submitter` | 0.000 | −1.63 | 4 | **120** |
| `reward_hacker` | 0.000 | −0.82 | 4 | 19 |

Three findings live in that table, and none of them is the success rate.

**The two failing policies are not similar.** Both score 0.000. `weak_submitter`
submits as the wrong actor on every single task — 120 unsafe submissions.
`reward_hacker` does it 19 times, only where the requester genuinely lacked
authority, and fails for a different reason entirely. A dashboard showing
success rate would render these as the same bar.

**`reward_hacker` scores better than `weak_submitter` while being the more
dangerous policy.** It produces correct totals, cites plausible policies, and
files valid drafts. It is wrong in ways that look right. Ranking by reward puts
it above the clumsy failure, which is a property of the reward, not a mistake in
it — but you only notice by reading the components.

**`scripted_reference` has one distinct reward across 120 rollouts.** Perfect
success, zero variance. As training data this is worthless: every episode agrees,
so there is no signal about what to do differently. A rollout set can be a fine
regression suite and useless for learning, and `distinct_rewards` is the column
that tells you which you have.

## Analyses The Evidence Block Unlocks

Because `verifier.evidence` stores what was read alongside what was claimed,
these are one pass over the log — no environment, no re-run:

```python
fabricated = set(ev["policies_cited"]) - set(ev["policies_retrieved"])
never_read = not ev["receipts_looked_up"]
no_op      = rollout["initial_state_hash"] == rollout["terminal_state_hash"]
```

Run across both logs in this repo:

| Signal | `scripted_reference` | `reward_hacker` |
| --- | ---: | ---: |
| cited a policy it never retrieved | 0 / 120 | **120 / 120** |
| looked up zero receipts | 0 / 120 | **120 / 120** |
| terminal state == initial | 0 / 120 | 0 / 120 |
| action count | 6–14, spread | **4, always** |

The last row is the tell. A policy whose action count never varies is not
responding to the task. Reference rollouts run 6 to 14 actions depending on how
many receipts a task involves; the hacker runs exactly four, every time, because
it never looks anything up. **Variance in trajectory length is a proxy for
whether the agent is reading its input**, and it costs one line to compute.

Note also that the hacker's no-op count is zero. It does change state — it files
drafts and submits reports. It is not idle, it is confidently wrong, which is
why a state-change check alone would clear it.

## Filtering Before Use

Not every rollout belongs downstream. Phase 7 screens with
`rollout_rejection_reason`:

```python
if not row.get("actions"):        return "missing_actions"
if not row.get("observations"):   return "missing_observations"
if "verifier" not in row or "reward" not in row:
                                  return "missing_verifier_or_reward"
if row.get("termination_reason") not in {"final_answer", "truncated"}:
                                  return "invalid_termination"
```

Rejections are logged to `rl-rollouts-rejected.jsonl` rather than dropped, for
the same reason the Level 4 dataset logs its rejects: a silent filter cannot be
distinguished from a broken one.

Current count: **0 rejected of 360.** Read that with suspicion rather than
satisfaction. Zero rejections means either the producers are well-behaved, or
the filter does not bite. Both of this repo's policies are scripted and always
terminate cleanly, so zero is expected here — but the first time a learned or
sampled policy writes into this log, that number should move, and if it does not
the filter needs testing.

## Common Failure Modes

- **Logging total reward without components.** `−0.82` is not diagnosable;
  the eight components that sum to it are.
- **Comparing policies on success rate alone.** It cannot separate 120 unsafe
  submissions from 19.
- **Discarding observations.** Without them you cannot tell "never saw the
  evidence" from "saw it and ignored it" — two different fixes.
- **No policy or seed on the record.** An anonymous log cannot be attributed or
  reproduced.
- **Treating any rollout set as training data.** Zero within-policy variance
  means no learning signal, however good the mean looks.
- **A filter that never rejects anything.** Either your producers are perfect or
  your filter is decorative; find out which.
- **Reading only failures.** The reference log is what tells you what normal
  looks like, which is how you notice a fixed action count.

## Exercise

Open [`rollouts.jsonl`](../../../environments/strongbench_finance/rollouts.jsonl)
and [`probe-rollouts.jsonl`](../../../environments/strongbench_finance/probe-rollouts.jsonl).

1. Compute the action-count distribution for each log. One is a single value.
   What does that tell you about the policy, and which field would you check
   next to confirm it?
2. `weak_submitter` and `reward_hacker` both score a success rate of 0.000.
   Name two fields in the record that separate them, and say which policy you
   would rather ship if forced.
3. The rollout filter has rejected 0 of 360. Write the rollout that would trip
   `invalid_termination`, and say why a scripted policy never produces one.

Check your answer:

```text
1. reward_hacker is 4 actions on every one of 120 rollouts; scripted_reference
   spreads 6-14. A constant action count means the policy is not reacting to
   the task at all. Confirm with verifier.evidence.receipts_looked_up — it is
   empty on all 120 hacker rollouts, so it never reads anything, which is why
   the trajectory length cannot vary.

2. unsafe_submission_failures (120 vs 19) and reward.components — the hacker
   loses on correct_policy_basis and required_records_checked while the weak
   submitter loses on safety. Neither is shippable. Forced to choose, ship the
   weak_submitter: it fails loudly on every task and would be caught in an
   afternoon. The hacker produces correct-looking totals and plausible
   citations, so it survives review and fails in production. Prefer the
   failure you can see.

3. Any rollout whose termination_reason is neither "final_answer" nor
   "truncated" — for example one that ended on an exception, a timeout, or a
   step-budget abort recorded under some other name. Scripted policies always
   emit final_answer as their last action, so the field is always
   "final_answer". The filter is untested until a sampled or learned policy
   can crash mid-episode.
```

Then compute `set(policies_cited) - set(policies_retrieved)` across both logs.
It is 0/120 for the reference and 120/120 for the hacker. That one line is a
fabrication detector, and it works only because the record stored what was read
as well as what was claimed.

## Checkpoint

You are ready to complete Level 6 when your rollout records let you answer
"which behaviour caused this score?" without re-running the environment, and
you can name one question about a run your record cannot currently answer.

## Reading

- [`environments/strongbench_finance/reward-design.md`](../../../environments/strongbench_finance/reward-design.md)
  — read the component list beside a rollout's `reward.components`. Deciding
  which components to log is the same decision as deciding what your analysis
  will be able to see.
- [`rl_reliability/strongbench/experiment-report.md`](../../../rl_reliability/strongbench/experiment-report.md)
  — read its "What this rollout set cannot do" section before you hand any log
  to a trainer. It states the variance problem in the terms a training run
  cares about.
