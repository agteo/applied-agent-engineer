# Lab 1: State Model

## Objective

Design the smallest state your verifiers can actually read.

## Build

State is not a model of the world. It is the minimum record that makes agent
behaviour verifiable, and every key you add is a consistency obligation forever.

Split your keys in two:

| Fixtures — the world as given | Records — what the agent did |
| --- | --- |
| employees, policies, receipts, trips | drafts, approvals, submissions, audit log |
| populated at start | **start empty** |

That second column starting empty is the property to aim for: anything in those
keys at the end of an episode was put there by the agent, so verification is a
direct question about its footprint rather than a diff against a starting
population.

Three requirements:

- **Every key must be read by some check.** Add state when a verifier needs it,
  not before.
- **Include `schema_version` and `seed` in the state itself**, so a rollout
  carries the world it ran in.
- **Deep-copy per episode.** Without it, episode two starts inside episode one's
  drafts and your failures make no sense.

## Deliverable

Submit:

- a state schema with required keys
- an initial state where every record key is empty
- a note naming, for each key, the check that reads it

## Checks

```bash
python3 - <<'PY'
import json
schema = json.load(open("path/to/your/state-schema.json"))
initial = json.load(open("path/to/your/initial-state.json"))
missing = set(schema["required"]) - set(initial)
print("FAIL missing required keys:", missing) if missing else print("OK: initial state complete")
records = ["drafts", "approvals", "submissions", "audit_log"]  # your record keys
nonempty = [k for k in records if k in initial and initial[k]]
print("FAIL: record keys not empty at start:", nonempty) if nonempty \
    else print("OK: records start empty - agent footprint is distinguishable")
for k in ("schema_version", "seed"):
    print(f"  {'OK ' if k in initial else 'MISSING'} {k}")
PY
```

The lab passes when every record key starts empty, `schema_version` and `seed`
are in state, and your note names a check for every key. **A key with no check
is a key to delete.**

## Reference

Compare against
[`state-schema.json`](../../../environments/strongbench_finance/state-schema.json)
and
[`initial-state.json`](../../../environments/strongbench_finance/initial-state.json).

```bash
python3 -c "
import json
s=json.load(open('environments/strongbench_finance/initial-state.json'))
for k,v in s.items(): print(f'  {k}: {len(v) if isinstance(v,(dict,list)) else v}')
"
```

Twelve required keys; four of them empty. Six employees, six policies,
thirty-two receipts and eight trips is exactly enough world to generate 120
distinct tasks — and no more.
