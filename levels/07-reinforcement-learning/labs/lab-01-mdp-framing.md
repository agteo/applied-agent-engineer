# Lab 1: MDP Framing

## Objective

Frame your environment as an MDP, concretely enough that someone else could
implement a runner from your description — and find out whether your problem has
that shape at all.

## Build

Write all five parts. The one you cannot fill in is the finding.

| Part | Must be |
| --- | --- |
| **State** | inspectable by something outside the model |
| **Actions** | a closed, enumerated set with typed arguments |
| **Observations** | including failures, with a success flag |
| **Reward** | derived from named verifier checks |
| **Termination** | at least one reason, recorded per rollout |

Two of these carry most of the weight.

**Observations must include failures.** A channel reporting only successes makes
recovery unlearnable and unmeasurable — a refused action becomes
indistinguishable from one that never happened.

**Reward comes from verifiers, not a separate judgment.** This is why Level 6
precedes Level 7: the reward *is* the verifiers. A team reaching for RL before
it can verify anything picks its reward from whatever is computable, which is
how reward hacking gets designed in from the start.

Then add the section people skip: **what this framing does not claim.** Writing
an MDP down makes a project feel like an RL project, and a framing document is
where overclaiming starts.

## Deliverable

Submit an MDP framing document with the five parts, plus:

- a "does not claim" section
- the reward variance of your rollout set

## Checks

```bash
python3 - <<'PY'
import json, collections
rows = [json.loads(l) for l in open("path/to/your/rollouts.jsonl") if l.strip()]
by_policy = collections.defaultdict(list)
for r in rows:
    by_policy[r["policy"]].append(r["reward"]["total"])
for p, rewards in by_policy.items():
    d = len(set(rewards))
    print(f"  {p}: {len(rewards)} rollouts, {d} distinct rewards"
          + ("   <-- no within-policy variance" if d == 1 else ""))
print("\nUsable for training?" ,
      "no - advantage estimation has nothing to compare"
      if any(len(set(v)) == 1 for v in by_policy.values()) else "possibly")
PY
```

The lab passes when all five parts are filled in, your document states what it
does not claim, and you have reported the variance. **A correct framing does not
mean a trainable dataset** — those are independent facts, and reporting both is
the point.

## Reference

Compare against
[`mdp-framing.md`](../../../rl_reliability/strongbench/mdp-framing.md).

```bash
cat rl_reliability/strongbench/mdp-framing.md
```

Its last section reads: "This Phase 7 bundle compares a scripted reference policy
to a deliberately weak submitter policy; it does not claim trained-policy
improvement." Write that sentence for your own framing.

Then note that its reference policy has **one** distinct reward across 120
rollouts. The framing is entirely correct and the data is unusable for learning.
