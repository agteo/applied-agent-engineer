# Lab 1: Training Decision

## Objective

Decide whether training is justified, from counts rather than intuition.

## Build

The question is not "is the agent good enough?" It is **"where do the failures
live?"** Training only moves the model; pointing it at a tool bug produces a
model that has memorised compensations for a defect that stays in the codebase.

Because your Level 3 taxonomy namespaces labels by where the fix lives, this is
arithmetic:

```text
TOOLS.* + RETRIEVAL.*  ->  fix the harness, the schemas, the search layer
MODEL.*                ->  prompt, data, or training
```

Sum both. If tools and retrieval dominate, training is the wrong intervention
however cheap it looks.

Then write an intervention matrix — every candidate with three fields:

| Intervention | Status | Success measure |

**Write the success measure before running anything.** A measure chosen
afterwards will be the one the result happens to satisfy. If you cannot write
it, you are not ready to run the intervention.

Use `defer_until_X` rather than `no` for anything you are postponing. A matrix
that only says no is a matrix nobody revisits.

## Deliverable

Submit:

- a decision record with both label counts and a stated decision
- an intervention matrix, every row carrying evidence and a success measure
- a memo naming the next experiment and what would make you abandon it

## Checks

```bash
python3 - <<'PY'
import json, collections
rows = [json.loads(l) for l in open("path/to/your/annotations.jsonl") if l.strip()]
labels = collections.Counter(l for r in rows for l in r["taxonomy_labels"])
tools = sum(v for k, v in labels.items() if k.startswith(("TOOLS.", "RETRIEVAL.")))
model = sum(v for k, v in labels.items() if k.startswith("MODEL."))
print(f"tools/retrieval: {tools}   model: {model}")
print("-> decision implied:",
      "fix tools and retrieval first" if tools > model else "model work is justified")

matrix = json.load(open("path/to/your/intervention-matrix.json"))
missing = [m.get("intervention") for m in matrix if not m.get("success_measure")]
if missing:
    print("FAIL rows with no success measure:", missing)
else:
    print("OK: every intervention states how it would be measured")
PY
```

The lab passes when your decision follows from the counts, every intervention
carries a success measure written in advance, and anything deferred names the
condition that would revive it.

## Reference

Compare against
[`decision.json`](../../../model_improvement/strongbench/decision.json) and
[`intervention-matrix.json`](../../../model_improvement/strongbench/intervention-matrix.json).

```bash
python3 -m model_improvement.strongbench
python3 -c "
import json; d=json.load(open('model_improvement/strongbench/decision.json'))
print(d['tool_or_retrieval_failure_labels'], 'vs', d['model_failure_labels'], '->', d['decision'])
"
```

49 against 13, decision `fix_tools_and_retrieval_before_training`. Nearly four
times as many failures live outside the model as inside it — and the decision
required no judgment, only a taxonomy applied consistently and then summed.
