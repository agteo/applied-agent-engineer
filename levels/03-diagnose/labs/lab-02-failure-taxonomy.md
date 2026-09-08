# Lab 2: Failure Taxonomy

## Objective

Build a taxonomy that turns a pile of failures into a short list of things to
fix.

## Build

The test for every label: **it earns its place when it changes what you would do
next.** If two failures carry different labels but need the same fix, the
distinction is decorative. If two share a label and need different fixes, the
label is too coarse.

Three structural rules:

- **Namespace by where the fix lives.** `TOOLS.*` is fixed in the harness or the
  schemas, `RETRIEVAL.*` in the search layer, `MODEL.*` in the prompt, data or
  model. The prefix answers "whose bug is this?" before anyone reads the
  description — and it lets you sum by prefix later to decide whether training
  is even the right intervention.
- **Split what needs different repairs.** `TOOLS.selection`, `TOOLS.arguments`
  and `TOOLS.interpretation` are three labels because they are three fixes: the
  tool was not called, was called wrongly, or was read wrongly.
- **Include an escape hatch for "the task is wrong."** A taxonomy with no
  `EVALUATION.expected_answer_wrong` forces benchmark bugs into model-blaming
  categories, and someone debugs an agent that is behaving correctly.

**Labels are not exclusive.** A failure usually has more than one thing wrong
with it; forcing one label per failure discards what the reviewer noticed.

## Deliverable

Submit:

- a taxonomy file with one line per label: id, and what it means
- worked examples for each label you actually used
- a note on any label pair you found hard to distinguish

## Checks

```bash
python3 - <<'PY'
import json, collections
rows = [json.loads(l) for l in open("path/to/your/annotations.jsonl") if l.strip()]
by_combo = collections.defaultdict(set)
for r in rows:
    by_combo[tuple(sorted(r["taxonomy_labels"]))].add(r["recommended_intervention"])
ambiguous = {k: len(v) for k, v in by_combo.items() if len(v) > 1}
labels = collections.Counter(l for r in rows for l in r["taxonomy_labels"])
print("label counts:", dict(labels))
print("labels per row:", sum(labels.values()) / len(rows))
print("FAIL - combos mapping to >1 intervention:", ambiguous) if ambiguous \
    else print("OK: every label combination implies one intervention")
PY
```

The lab passes when **every label combination maps to exactly one
intervention**. If one combination implies two different fixes, your labels are
not yet carrying enough information — split them.

Also check that your average labels-per-row is above 1.0. Exactly 1.0 means
reviewers were forced to choose.

## Reference

Compare against
[`evals/operations/strongbench/taxonomy.md`](../../../evals/operations/strongbench/taxonomy.md)
and the label distribution it produces.

```bash
python3 -c "
import json, collections
rows=[json.loads(l) for l in open('evals/operations/strongbench/annotated-failures.jsonl')]
c=collections.Counter(l for r in rows for l in r['taxonomy_labels'])
print(dict(c)); print('total labels', sum(c.values()), 'over', len(rows), 'rows')
"
```

Sixty-two labels over thirty rows, seven combinations, each implying one
intervention. Note that `EVALUATION.expected_answer_wrong` is defined and used
by zero rows — zero is the healthy state for that label, and its absence from
the taxonomy would be the problem.
