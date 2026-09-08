# Lab 2: Cleaning Filters

## Objective

Remove rows that should not be trained on, and leave an audit trail proving what
was removed and why.

## Build

**A filter must log what it rejected.** A cleaner that silently drops rows is
indistinguishable from a cleaner with a bug — both produce a smaller dataset that
looks fine.

Write at least these rules, each emitting a distinct reason:

| Reason | Catches |
| --- | --- |
| `duplicate_prompt_target` | the same prompt and target twice — can split across train and heldout |
| `missing_provenance` | a row that cannot say where it came from |
| `invalid_target_contract` | a target that does not match the answer schema |

Two design decisions worth making deliberately:

- **Provenance is a rejection reason, not a warning.** A row that cannot be
  traced is a permanent unknown in every future audit. When a source turns out
  to be wrong, "what else came from there?" must be answerable.
- **Dedup on meaning, not bytes.** Key on prompt + target + source. Too narrow
  (the whole row) and near-identical rows survive; too broad (prompt alone) and
  you delete legitimate rows where the same question has different correct
  answers.

**Plant a fixture per rule.** A filter that has never been seen to fire is a
filter you have not tested.

## Deliverable

Submit:

- filtering rules with one reason string each
- `rejected.jsonl` with a reason on every row
- before and after counts
- one deliberately-bad fixture row per rule, proving each fires

## Checks

```bash
python3 - <<'PY'
import json, collections
raw = sum(1 for l in open("path/to/your/raw.jsonl") if l.strip())
clean = sum(1 for l in open("path/to/your/cleaned.jsonl") if l.strip())
rej = [json.loads(l) for l in open("path/to/your/rejected.jsonl") if l.strip()]
reasons = collections.Counter(r["reason"] for r in rej)
print(f"raw={raw} cleaned={clean} rejected={len(rej)}")
print("reasons:", dict(reasons))
print("OK: counts reconcile" if raw - len(rej) == clean else "FAIL: rows vanished outside the filter")
print("FAIL: some rule never fired") if len(reasons) < 3 else print("OK: every rule exercised")
PY
```

The lab passes when `raw - rejected == cleaned` exactly, every rejection carries
a reason, and every rule you wrote has fired at least once. If a rule has never
fired, you do not know whether it works.

## Reference

Compare against
[`datasets/strongbench/rejected.jsonl`](../../../datasets/strongbench/rejected.jsonl)
and the counts in
[`metrics.json`](../../../datasets/strongbench/metrics.json).

```bash
python3 -c "
import json
m=json.load(open('datasets/strongbench/metrics.json'))
print(m['raw_count'], '-', m['rejected_count'], '=', m['cleaned_count'],
      '->', m['raw_count']-m['rejected_count']==m['cleaned_count'])
print(m['rejection_reasons'])
"
```

Note that every rejected row there is named `cleaning-fixture-*`. The filters are
exercised on every build by planted fixtures, which is why zero rejections in
that pipeline would be a red flag rather than a clean bill of health.
