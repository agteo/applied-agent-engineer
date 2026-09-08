# Lab 2: Prepare SFT Data

## Objective

Export training data where every admitted row is one you would want the model to
imitate, and every refusal is logged.

## Build

Filtering, not formatting, is where a training run is decided. Do not ask "can
this row be converted?" — almost anything can. Ask **"would I want the model to
produce this?"**

Refuse, with a logged reason:

- **anything in your held-out split** — it is your measurement
- **corrections derived from a build you do not ship** — they teach compensations
  for a defect the real agent does not have
- rows failing your target contract

Keep `source_example_id` on every exported row even though a trainer never reads
it. When a trained model behaves oddly, that field is how you walk a behaviour
back to the dataset row, the annotation, and the failing task behind it.

**The system prompt is part of the data.** Version it with the export, and serve
with the same one you trained with — otherwise the model is off-distribution and
nobody is tracking it.

## Deliverable

Submit:

- the export script
- train and dev exports
- a rejection log with a reason per row
- the label distribution of your training rows

## Checks

```bash
python3 - <<'PY'
import json, collections
data = [json.loads(l) for l in open("path/to/your/dataset.jsonl") if l.strip()]
train = [json.loads(l) for l in open("path/to/your/sft-train.jsonl") if l.strip()]
rej = [json.loads(l) for l in open("path/to/your/sft-rejected.jsonl") if l.strip()]

heldout = {r["example_id"] for r in data if r["split"] == "heldout"}
rejected_ids = {r["source_example_id"] for r in rej}
leaked = heldout - rejected_ids
print(f"heldout rows: {len(heldout)}   rejected: {len(rej)}")
print("FAIL: heldout rows reached the export:", sorted(leaked)[:5]) if leaked \
    else print("OK: the rejection log is exactly the heldout set")
print("no source_example_id:", [r.get("example_id") for r in train if "source_example_id" not in r][:5])
print("training labels:", dict(collections.Counter(l for r in train for l in r["labels"])))
PY
```

The lab passes when the rejection log contains **exactly** your held-out set,
every exported row traces to a source, and you can say from the label
distribution what the run would be teaching. If that surprises you, the
filtering is wrong.

## Reference

Compare against
[`sft-schema.json`](../../../model_improvement/strongbench/sft-schema.json) and
the exports beside it.

```bash
python3 -m model_improvement.strongbench
wc -l model_improvement/strongbench/sft-*.jsonl
```

78 train, 47 dev, 27 rejected — and those 27 are exactly the heldout split. That
equality is an invariant worth asserting in a test: a count of 26 means one
held-out row reached training data, and the discrepancy is the only symptom you
would get.
