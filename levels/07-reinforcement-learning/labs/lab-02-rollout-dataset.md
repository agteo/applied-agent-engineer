# Lab 2: Rollout Dataset

## Objective

Produce a rollout log that answers questions about a run without re-running it,
and a filter that has been seen to reject something.

## Build

**A rollout record should contain everything needed to answer a question about
the run later.** Re-running is not always possible: the policy may be gone, the
seed may have moved. Anything you did not write down is a question you can never
ask.

Required per rollout:

```text
rollout_id, environment, policy, task_id, seed,
initial_state_hash, terminal_state_hash,
actions[], observations[], verifier{checks, evidence}, reward{total, components}
```

Three fields people omit and regret:

- **The two state hashes.** `initial == terminal` means the episode was a no-op —
  scannable across a million rollouts without parsing an action.
- **`verifier.evidence`.** Store what the agent *read* separately from what it
  *claimed*. That is what makes `cited - retrieved` a one-line fabrication
  detector.
- **`policy`.** An anonymous log cannot be compared by policy, and merging logs
  is exactly when a mislabel happens. Refuse to relabel on merge.

**Write a filter, and log its rejections.** Structural checks only: missing
actions, missing observations, no verifier or reward, unrecognised termination.
Rejections go to their own file with a reason.

## Deliverable

Submit:

- the rollout log, at least two policies
- the filter, with a rejection log
- unit tests proving each rejection reason can fire
- reward variance per policy

## Checks

```bash
python3 - <<'PY'
import json, collections
rows = [json.loads(l) for l in open("path/to/your/rollouts.jsonl") if l.strip()]
required = {"rollout_id","policy","task_id","seed","initial_state_hash",
            "terminal_state_hash","actions","observations","verifier","reward"}
bad = [r.get("rollout_id","?") for r in rows if not required <= set(r)]
print("FAIL incomplete rows:", bad[:5]) if bad else print("OK: all rows complete")
noop = sum(1 for r in rows if r["initial_state_hash"] == r["terminal_state_hash"])
print(f"rollouts: {len(rows)} | no-ops: {noop}")
for p, g in collections.groupby(sorted(rows, key=lambda r: r["policy"]), key=lambda r: r["policy"]):
    g = list(g); acts = {len(r["actions"]) for r in g}
    print(f"  {p}: {len(g)} rollouts, action counts {min(acts)}-{max(acts)}"
          + ("   <-- constant, policy is not reading its input" if len(acts) == 1 else ""))
PY
```

The lab passes when every rollout has all ten fields, your filter's four
rejection reasons each have a test that fires them, and you have reported action-
count spread per policy.

**Zero rejections is not a relief.** It means either your producers are
well-behaved or your filter does not bite — test it directly rather than waiting
to find out.

## Reference

Compare against
[`rl-rollouts.jsonl`](../../../rl_reliability/strongbench/rl-rollouts.jsonl) and
[`rollout-schema.json`](../../../rl_reliability/strongbench/rollout-schema.json).

```bash
python3 -m rl_reliability.strongbench
python3 -c "
import json, collections
ref=[json.loads(l) for l in open('environments/strongbench_finance/rollouts.jsonl')]
hack=[json.loads(l) for l in open('environments/strongbench_finance/probe-rollouts.jsonl')]
for n,rows in (('reference',ref),('hacker',hack)):
    acts={len(r['actions']) for r in rows}
    fab=sum(1 for r in rows if set(r['verifier']['evidence']['policies_cited'])
                              - set(r['verifier']['evidence']['policies_retrieved']))
    print(f'{n}: actions {min(acts)}-{max(acts)}, fabricated citations {fab}/{len(rows)}')
"
```

The reference spreads 6-14 actions; the hacker runs exactly 4 every time.
**Constant trajectory length is a proxy for a policy not reading its input**, and
it costs one line to compute.
