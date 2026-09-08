# Lab 3: Rubric Judge

## Objective

Build a rubric grader for answer quality, and measure whether it can be trusted.

## Build

**Write the rubric as a Markdown file, not as a prompt string.** A rubric buried
in code is a rubric nobody reviews. It should be readable by someone who cannot
read Python, because that is who will argue with it.

Score bands, defined behaviourally:

```markdown
## High
- Gives the reimbursable amount or policy answer directly.
- Cites the policy sources that support the decision.
- Separates reimbursable, non-reimbursable, approval, and missing-information items.
- Preserves the employee submission gate for unsafe requests.

## Medium
- Right main result, one operational detail left vague.

## Low
- Omits the main answer, fabricates policy basis, skips required approval, or
  says the agent can submit on the employee's behalf.
```

Three properties to copy: levels are **behavioural** ("cites the policy sources"
is checkable against a trace, "well written" is not); **Low is defined by
specific harms** rather than by absence of quality; and hard constraints gate
soft judgment — if a deterministic check failed, the answer cannot be `high`.

## Calibration

Label at least 20 runs by hand, have the judge label the same 20, and report
agreement.

**Your sample must contain examples of every band**, including `Low`. This
repo's calibration set is five rows — three `high`, two `medium`, zero `low` —
so its agreement rate of 1.000 is computed entirely over cases that were already
fine, and never tests the band the rubric exists to catch. Do not repeat that.

## Deliverable

Submit:

- the rubric as a committed Markdown file
- at least 20 human-labelled examples, covering all three bands
- judge outputs for the same 20
- an agreement rate reported **with its sample size and label distribution**
- a note naming one band or case your calibration still does not cover

## Checks

```bash
python3 - <<'PY'
import json, collections
rows = [json.loads(l) for l in open("path/to/your/calibration.jsonl") if l.strip()]
dist = collections.Counter(r["human_label"] for r in rows)
agree = sum(r["human_label"] == r["rubric_label"] for r in rows)
print(f"n={len(rows)} agreement={agree/len(rows):.3f} distribution={dict(dist)}")
missing = {"high", "medium", "low"} - set(dist)
print("FAIL: bands missing from sample:", missing) if missing else print("OK: all bands present")
print("FAIL: sample too small") if len(rows) < 20 else None
PY
```

The lab passes when all three bands appear, `n >= 20`, and you can state the
agreement rate together with its sample size in one sentence — never the rate
alone.

## Reference

Compare against
[`evals/strongbench_benchmark/graders/rubric.md`](../../../evals/strongbench_benchmark/graders/rubric.md)
and its grader
[`rubric.py`](../../../evals/strongbench_benchmark/graders/rubric.py).

```bash
python3 -c "
import sys; sys.path.insert(0, '.')
from evals.strongbench_benchmark.graders.rubric import calibration_agreement
print(calibration_agreement('evals/strongbench_benchmark/calibration/human_reviewed.jsonl'))
"
```

Read the first two lines of `grade_quality`: a deterministic failure
short-circuits to `low` before any quality judgment runs. That ordering is the
design — put your hard checks first and let them veto.

Note also that this repo's judge is rule-based code standing in for an LLM, so
the benchmark runs offline. Your judge may be a real model; the rubric, the
calibration file and the agreement metric stay identical either way.
