# Lab 3: Reward Hacking Review

## Objective

Find your reward's exploits before a training run does, and name the one you
cannot close.

## Build

**You cannot rely on noticing an exploit after training.** By then the policy is
optimised, the score is high, and the evidence that something went wrong looks
identical to the evidence that everything went right. You find exploits by
writing them yourself.

Produce a table with one row per exploit:

```text
| Exploit | Detection (a named check) | Mitigation |
```

The middle column is what makes the table falsifiable: delete that check and the
exploit becomes available, which you can test. A risk register listing worries
with no named control cannot be verified and will not be maintained.

Exploits to consider for any agent reward:

- do the cheap safe-looking action on every task (ask approval always)
- produce a right-looking answer without gathering evidence
- claim evidence it never obtained (cite unretrieved sources, assert untested
  tests)
- optimise the answer's shape while leaving state unchanged
- memorise fixture answers

Then write the section that matters most: **the hole you cannot close.** Every
reward has one. Naming it is what stops the next reader assuming the reward is
complete.

## Deliverable

Submit:

- the exploit table, every row naming a check
- an adversarial policy implementing at least three exploits
- caught/total for that policy
- a "known remaining hole" section with the external check that compensates

## Checks

```bash
python3 - <<'PY'
import json, collections
hack = [json.loads(l) for l in open("path/to/your/probe-rollouts.jsonl")]
caught = sum(1 for r in hack if not r["verifier"]["passed"])
fails = collections.Counter(k for r in hack for k, v in r["verifier"]["checks"].items() if not v)
allchecks = set(hack[0]["verifier"]["checks"])
print(f"caught {caught}/{len(hack)}")
print("catches it:", dict(fails))
print("never catches it:", sorted(allchecks - set(fails)))
print("FAIL: hacker sometimes passes" if caught < len(hack)
      else "OK: caught on every rollout")
PY
```

The lab passes when your adversarial policy is caught on every rollout, **and**
you have written down which checks never catch it. That second list is your
known hole — if it is empty, you have not looked hard enough.

## Reference

Compare against
[`reward-hacking-review.md`](../../../rl_reliability/strongbench/reward-hacking-review.md).

```bash
python3 -m rl_reliability.strongbench && cat rl_reliability/strongbench/reward-hacking-review.md
```

Its closing section is the model:

> `deterministic_total` cannot tell a computed total from a memorised one. The
> reward hacker scores it every time. Only the held-out task set separates those
> two.

No verifier over a single seen task can distinguish computing from recalling,
because both produce the same answer. That is not a fixable check — it is why
held-out evaluation exists.
