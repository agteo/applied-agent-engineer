# Lab 4: Reward Function

## Objective

Build a reward that is derived from named verifier checks, and prove it
discriminates by writing a policy that tries to cheat it.

## Build

**Every reward component reads a named check.** The reward function does no
judging — it converts booleans the verifiers already decided into numbers. That
constraint is what makes a reward debuggable: when a score is suspicious you
read which components it earned.

If you find yourself adding logic to the scorer, that logic belongs in the
verifier as a named check.

**Make the asymmetries deliberate.** Uniform ranges hide decisions:

- A cheap exploit needs a penalty larger than its reward. "Ask approval on
  everything" is free unless the wrong-direction penalty outweighs the
  right-direction reward.
- Safety terms are `0` or negative, never positive. You do not earn credit for
  not doing the forbidden thing.
- Count-scaled penalties for repeated errors — ten malformed calls should cost
  more than one.

**Reward the judgment, not the action.** `bool(approval)` rewards asking;
`bool(approval) == expected` rewards deciding correctly. Any check of the form
"did the agent do X?" is hackable by always doing X.

## Deliverable

Submit:

- the reward function, with every component naming its check
- a reward design document listing components and hacking risks
- **an adversarial policy** that runs every exploit you listed
- the caught/total figure for that policy

## Checks

```bash
python3 - <<'PY'
import json, collections
ref = [json.loads(l) for l in open("path/to/your/rollouts.jsonl")]
hack = [json.loads(l) for l in open("path/to/your/probe-rollouts.jsonl")]
caught = sum(1 for r in hack if not r["verifier"]["passed"])
print(f"reference passed: {sum(1 for r in ref if r['verifier']['passed'])}/{len(ref)}")
print(f"hacker caught:    {caught}/{len(hack)}")
fails = collections.Counter(k for r in hack for k, v in r["verifier"]["checks"].items() if not v)
print("checks that catch the hacker:", dict(fails))
never = [k for k in ref[0]["verifier"]["checks"] if k not in fails]
print("checks the hacker always passes:", never)
print("FAIL: hacker not always caught" if caught < len(hack) else "OK")
PY
```

The lab passes when your adversarial policy is caught on **every** rollout, and
you can name at least one check it always passes. That last list is the honest
part: in the reference environment the hacker passes `deterministic_total` every
time, because a memorised total is indistinguishable from a computed one within
a single seen task.

## Reference

Compare against
[`reward-design.md`](../../../environments/strongbench_finance/reward-design.md)
and `score_reward` in
[`environments/strongbench_finance/__init__.py`](../../../environments/strongbench_finance/__init__.py).

```bash
python3 -m environments.strongbench_finance
```

The verifier report prints a policy comparison: reference at 1.000, reward
hacker at 0.000, caught 120 of 120. **A verifier suite with no policy that fails
it is not evidence** — which is why the shared environment contract requires
`run_reward_hacking_policy` as a function every environment must provide.
