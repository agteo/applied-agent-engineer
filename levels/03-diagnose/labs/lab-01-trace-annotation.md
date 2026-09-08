# Lab 1: Trace Annotation

## Objective

Annotate failed traces from the Level 2 benchmark so that someone else can act
on them without re-reading the traces.

## Build

Select at least 20 failed runs and annotate each with:

- **first wrong transition** — the step and the *field* where it diverged
- **evidence** — the value in that field, quoted
- **taxonomy label** — from your Level 3 taxonomy
- **hypothesis** — a claim about cause that goes beyond the evidence
- **recommended intervention** — what you would change

Keep the last three as separate fields. They have different lifetimes: a label
is applied in a minute, a hypothesis survives until disproved, an intervention
is a commitment of engineering time. Collapsing them into one "notes" field
loses the ability to re-derive the second two when the taxonomy changes.

**Read forward, not backward.** The final answer is the most visible part of a
trace and the least informative, because by then every error has compounded.
Start at step one and stop at the first step whose output you would not have
produced.

**A successful tool call is not a correct one.** In `bench-029` the calculator
returns 108.00 flawlessly — it was asked the wrong question. Check
`tool_arguments` before blaming the tool or the model's arithmetic.

## Deliverable

Annotated traces as JSONL, one object per annotation, each carrying at minimum:

```json
{"annotation_id": "<config>:<task_id>", "task_id": "...", "config": "...",
 "failures": ["..."], "taxonomy_labels": ["..."], "hypothesis": "...",
 "recommended_intervention": "...", "evidence": {...}}
```

`config` is not optional. It records which agent build produced the failure, and
without it a correction derived from a broken control looks identical to one
from the shipping agent.

## Checks

```bash
python3 - <<'PY'
import json, collections
rows = [json.loads(l) for l in open("path/to/your/annotations.jsonl") if l.strip()]
required = {"annotation_id", "task_id", "config", "taxonomy_labels",
            "hypothesis", "recommended_intervention", "evidence"}
bad = [r.get("task_id", "?") for r in rows if not required <= set(r)]
print(f"rows={len(rows)}")
print("FAIL missing fields:", bad) if bad else print("OK: all rows complete")
print("FAIL: fewer than 20") if len(rows) < 20 else None
print("hypotheses:", len({r["hypothesis"] for r in rows}),
      "interventions:", len({r["recommended_intervention"] for r in rows}))
PY
```

The lab passes when every row has all seven fields, you have at least 20, and
**your distinct hypothesis count is well below your row count**. Twenty
annotations with twenty different hypotheses means you have described failures
rather than grouped them.

## Reference

Compare against
[`evals/operations/strongbench/annotated-failures.jsonl`](../../../evals/operations/strongbench/annotated-failures.jsonl),
30 annotations produced by `python3 -m evals.operations`.

```bash
python3 -c "
import json, collections
rows=[json.loads(l) for l in open('evals/operations/strongbench/annotated-failures.jsonl')]
print('rows:', len(rows))
print('distinct hypotheses:', len({r['hypothesis'] for r in rows}))
print('distinct interventions:', len({r['recommended_intervention'] for r in rows}))
"
```

Thirty annotations, five hypotheses, four interventions. That compression is the
output of the lab, not the annotation count.
