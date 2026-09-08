# Lab 3: Task Generator

## Objective

Generate many *distinct* tasks, and be able to prove they are distinct.

## Build

The failure this lab exists to prevent: cycling eight templates fifteen times
gives you 120 task ids, 120 rows, and a metrics block reporting
`task_count: 120`. You have eight tasks.

Three requirements:

- **Define a signature and dedup on it.** Here it is
  `(actor, employee_id, receipt_ids)` — everything else about the task is
  derived from those three. Two tasks with the same signature are the same task
  wearing different ids.
- **Families are predicates over the fixtures, not templates.** A predicate
  yields as many distinct tasks as the fixture set supports, so adding a receipt
  grows every family that matches it. A template yields one task forever.
- **No randomness.** Enumerate candidates in a fixed order and draw round-robin.
  Let the seed rotate the starting family rather than sample, so the same seed
  gives the same set byte for byte and a different seed gives a genuine held-out
  set.

**Derive the expected answer from the same rules the verifier uses.** Change a
policy limit and every expected total updates on the next build. Hand-authored
oracles need N edits and the ones nobody remembers become silent task bugs.

## Deliverable

Submit:

- the generator
- at least 100 tasks, with `task_count` **and** `distinct_task_count` reported
- expected answers computed from your policy functions, not typed
- two task sets from different seeds, with their overlap measured

## Checks

```bash
python3 - <<'PY'
import json, collections
tasks = [json.loads(l) for l in open("path/to/your/tasks.jsonl") if l.strip()]
sig = lambda t: (t["actor"], t["employee_id"], tuple(t["receipt_ids"]))
distinct = {sig(t) for t in tasks}
print(f"task_count={len(tasks)} distinct_task_count={len(distinct)}")
print("FAIL: duplicate tasks under different ids" if len(distinct) < len(tasks)
      else "OK: every task is distinct")
print("by family:", dict(collections.Counter(t["category"] for t in tasks)))
PY
```

Determinism, and a usable held-out set:

```bash
python3 -c "
from your_module import generate_tasks
a, b = generate_tasks(seed=42, count=120), generate_tasks(seed=42, count=120)
print('deterministic:', a == b)
c = generate_tasks(seed=7, count=120)
sig = lambda t: (t['actor'], t['employee_id'], tuple(t['receipt_ids']))
overlap = len({sig(t) for t in a} & {sig(t) for t in c})
print(f'overlap with seed 7: {overlap}/120')
"
```

The lab passes when `distinct_task_count == task_count`, the same seed
reproduces byte-identically, and a different seed gives low enough overlap to
serve as a held-out set.

## Reference

Compare against `generate_tasks` and `FAMILY_BUILDERS` in
[`environments/strongbench_finance/__init__.py`](../../../environments/strongbench_finance/__init__.py).

```bash
python3 -c "
import json, collections
t=[json.loads(l) for l in open('environments/strongbench_finance/tasks.jsonl')]
sig=lambda x:(x['actor'],x['employee_id'],tuple(x['receipt_ids']))
print('tasks', len(t), 'distinct', len({sig(x) for x in t}))
print(dict(collections.Counter(x['category'] for x in t)))
"
```

Family sizes there are uneven — 22 down to 9 — because pools exhaust at
different points and round-robin fills from whichever families still have
candidates. Do not force them equal: padding an exhausted family means repeating
its tasks, which is the original bug in a new place.
