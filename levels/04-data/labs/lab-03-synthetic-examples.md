# Lab 3: Synthetic Examples

## Objective

Generate examples that fill a gap you identified, and build the evaluation that
would tell you whether the model learned the capability or the template.

## Build

**Target named failure modes from Level 3, not general variety.** Generating
because you want more data produces rows shaped like the ones you already have,
which is the one thing you did not need.

Record on every generated row:

- `provenance.generator` — which generator, at what version
- `provenance.target_failure_mode` — the gap this row exists to close

That second field is what lets you trace a flawed generator to exactly the rows
it produced.

**Generated rows get no exemption from cleaning.** A generator producing subtly
wrong targets at scale is the fastest way to poison a dataset; the cleaner is
the only thing between a template bug and a hundred bad examples.

**Synthetic rows may enter any split.** Unlike corrections, they are not derived
from your benchmark, so they leak nothing. Contamination is about derivation,
not about whether data is real.

## Deliverable

Submit:

- the generator script
- at least 100 generated rows, each naming its target failure mode
- accepted and rejected samples
- the evaluation design that would distinguish capability from template
  learning

## Checks

```bash
python3 - <<'PY'
import json, collections
rows = [json.loads(l) for l in open("path/to/your/synthetic.jsonl") if l.strip()]
modes = collections.Counter(r["provenance"].get("target_failure_mode") for r in rows)
print("rows:", len(rows)); print("by target failure mode:", dict(modes))
print("FAIL: rows with no target mode") if None in modes else print("OK: every row targets a named gap")
print("FAIL: fewer than 3 modes covered") if len(modes) < 3 else None
PY
```

Then the part that matters more than the generation:

```bash
# Your model must be evaluated on data this generator did not produce.
python3 -m evals.runner --model scripted --report /tmp/nonsynthetic.md
```

The lab passes when every row names its target failure mode, those modes come
from your Level 3 findings rather than intuition, and you can state in one
sentence how you would tell template learning from capability. If your answer is
"more varied templates", read it again — varied templates are still templates,
and the fix is the evaluation set.

## Reference

Compare against
[`datasets/strongbench/synthetic-generation.md`](../../../datasets/strongbench/synthetic-generation.md).

```bash
python3 -c "
import json, collections
rows=[json.loads(l) for l in open('datasets/strongbench/cleaned.jsonl')]
syn=[r for r in rows if r['source_type']=='synthetic_gap_target']
print('synthetic rows:', len(syn), 'of', len(rows))
print(dict(collections.Counter(r['provenance']['target_failure_mode'] for r in syn)))
"
```

Four modes, 25 rows each, all four drawn from Level 3 diagnosis. Note that 100
of 152 rows are synthetic — a ratio the dataset card discloses in its
Limitations section, because it is the fact most likely to change a reader's
mind about the data.
