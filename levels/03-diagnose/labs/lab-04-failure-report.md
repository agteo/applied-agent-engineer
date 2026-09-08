# Lab 4: Failure Report

## Objective

Write the report that causes the next improvement cycle to happen.

## Build

A report earns its name when a reader who was not in the room can finish it and
know **what to fix first, why that and not something else, and how they will
know it worked.**

Order it for three audiences, conclusion first:

1. **Executive summary** — headline numbers and the recommendation. Most readers
   stop here, so it must be self-contained.
2. **Benchmark run analysed** — version fields, so the result can be reproduced.
3. **Failure distribution** — counts by label.
4. **Dominant hypotheses, ranked by coverage** — how many failures each explains.
   That count is the priority.
5. **Recommended interventions, ordered** — each naming a component, so it can be
   checked and can be found not to have worked.
6. **Data needs for Level 4** — which failures should become correction examples.

Two things to include that are easy to skip:

- **A weak baseline beside the real one.** 89/100 alone is compatible with a
  benchmark so lenient that anything passes. A deliberately broken config
  scoring 0/30 is what makes the 89 a measurement.
- **A regression recommendation.** Every fix should promote its cases into the
  benchmark, or the same failure returns unnoticed.

Keep the release decision as its own short document. It has a different reader
and a longer life than the analysis around it, and burying it as a final
paragraph is how gates get weakened by someone who skimmed.

## Deliverable

Submit:

- the failure report
- a separate release recommendation, under a page
- the regression pack: one case per diagnosed failure, each linking back to its
  annotation

## Checks

```bash
python3 - <<'PY'
import json
rows = [json.loads(l) for l in open("path/to/your/regression-pack.jsonl") if l.strip()]
missing = [r.get("id", "?") for r in rows if "source_annotation_id" not in r]
print(f"regression cases: {len(rows)}")
print("FAIL: cases with no link to their diagnosis:", missing) if missing \
    else print("OK: every case traces to an annotation")
PY

grep -qiE "^#+ .*(recommend|summary)" path/to/your/report.md \
  && echo "OK: report leads with a recommendation"
```

The lab passes when every regression case links to the annotation that produced
it, the report's first section states a recommendation, and your hypotheses are
ranked by how many failures each explains rather than by how interesting they
are.

## Reference

Compare against
[`failure-report.md`](../../../evals/operations/strongbench/failure-report.md),
[`release-recommendation.md`](../../../evals/operations/strongbench/release-recommendation.md)
and
[`regression-pack.jsonl`](../../../evals/operations/strongbench/regression-pack.jsonl).

```bash
python3 -c "
import json, collections
rows=[json.loads(l) for l in open('evals/operations/strongbench/regression-pack.jsonl')]
print('cases:', len(rows), '| all linked:', all('source_annotation_id' in r for r in rows))
print('tags:', dict(collections.Counter(t for r in rows for t in r['tags'])))
"
```

Note that the reference report's dominant hypothesis covers 19 of 30 failures
and its intervention is **not** listed first — those 19 come from a deliberately
broken control, not the shipping agent. Coverage ranks hypotheses; the `config`
field decides whether the fix is worth doing.
