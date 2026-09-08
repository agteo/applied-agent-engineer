# Lab 1: Trace To Dataset

## Objective

Convert agent traces and annotated failures into structured dataset rows that
something downstream can actually consume.

## Build

Three source types, and they are not interchangeable:

| `source_type` | Made from | Carries |
| --- | --- | --- |
| `level1_trace` | successful runs | a target answer |
| `failure_correction` | annotated failures | a target **and** a rejected answer |
| `synthetic_gap_target` | a generator | a target, plus the gap it targets |

**`source_type` is structural, not descriptive.** It decides which split a row
may enter, what shape its provenance takes, and whether it can form a preference
pair. Record it on every row.

Required fields on every row: `schema_version`, `example_id`, `source_type`,
`task_id`, `prompt`, `messages`, `target_final_answer`, `labels`, `provenance`,
`quality`, `split`.

Two that are easy to get wrong:

- **Carry both `prompt` and `messages`.** The flat string is what you dedup on,
  grep, and show in review; the structured form is what a trainer consumes.
  Deduping on `messages` means a system-prompt revision makes duplicates look
  distinct.
- **Only corrections get `rejected_final_answer`.** It is optional by source
  type, and counting rows that have it gives your preference-training ceiling
  directly.

## Deliverable

Submit:

- the conversion script
- a committed JSON Schema for your rows
- at least 100 rows, every one validating
- provenance on every row, shaped for its source type

## Checks

```bash
python3 - <<'PY'
import json, collections, sys
sys.path.insert(0, "examples/strongbench-expense-agent")
from strongbench_agent.validation import validate, ValidationError

schema = json.load(open("path/to/your/schema.json"))
rows = [json.loads(l) for l in open("path/to/your/dataset.jsonl") if l.strip()]
bad = 0
for r in rows:
    try:
        validate(r, schema, r.get("example_id", "?"))
    except ValidationError as e:
        print("SCHEMA", e); bad += 1
    if not r.get("provenance"):
        print(f"{r.get('example_id')}: no provenance"); bad += 1
print("rows:", len(rows), "| by source:", dict(collections.Counter(r["source_type"] for r in rows)))
print("with rejected answer:", sum(1 for r in rows if r.get("rejected_final_answer")))
print("FAIL" if bad else "OK: every row valid and attributable")
PY
```

The lab passes when every row validates, every row has provenance, and you can
say from the output how many preference pairs you have.

## Reference

Compare against [`datasets/strongbench/`](../../../datasets/strongbench/) and
its [`schema.json`](../../../datasets/strongbench/schema.json).

```bash
python3 -m datasets.strongbench
python3 -c "
import json, collections
rows=[json.loads(l) for l in open('datasets/strongbench/cleaned.jsonl')]
print(dict(collections.Counter(r['source_type'] for r in rows)))
print('with rejected_final_answer:', sum(1 for r in rows if r.get('rejected_final_answer')))
"
```

152 rows: 22 traces, 30 corrections, 100 synthetic — and exactly 30 carry a
rejected answer, all corrections. That number, not the row count, is what a
preference method can use.
