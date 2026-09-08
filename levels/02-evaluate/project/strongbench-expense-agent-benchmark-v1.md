# Project: StrongBench Expense Agent Benchmark v1

## Objective

Build a reproducible benchmark for StrongBench Expense Agent v1.

The benchmark should measure whether the agent completes realistic expense tasks
correctly, safely, and efficiently — and it should be able to tell you when it
does not.

## Required Dataset

At least 100 tasks, every one validating against a committed schema.

Required per task: `id`, `domain`, `prompt`, `employee_id`, `category`,
`difficulty`, `tags`, `required_tools`, `forbidden_tools`, `expected`, and
`grading_notes`.

Three properties that decide what your benchmark can measure:

- **`expected` is five fields, not one** — total, policy source ids, approval
  types, a missing-information flag, and a refusal expectation. Grading only the
  total passes an agent that got the number right by ignoring the approval rule.
- **`required_tools` and `forbidden_tools` grade the process.** The right answer
  reached without calling `search_policy` is an answer from memory that will not
  survive a policy change.
- **`additionalProperties: false`**, so a task carrying a field no grader reads
  is rejected at validation rather than sitting there looking like coverage.

Reference:
[`evals/strongbench_benchmark/schema.json`](../../../evals/strongbench_benchmark/schema.json)
and the 100 committed tasks in
[`tasks.jsonl`](../../../evals/strongbench_benchmark/tasks.jsonl).

## Required Categories

Include tasks for: policy questions, receipt lookup, reimbursement calculation,
missing receipts, manager approval, multi-item trips, ambiguous requests, unsafe
submission requests, and edge cases.

**Size each slice by the decision it supports, not by how easy the tasks are to
write.** On a ten-task slice one task moves the rate by ten points, which is too
coarse to read confidently — and the reference benchmark puts exactly ten tasks
on `unsafe_submission`, a safety property. Decide whether you accept that, and
say so.

## Required Graders

At least five deterministic graders: structured output validity, policy citation
accuracy, approval safety, reimbursable total accuracy, unsafe action refusal.
Plus one rubric grader for answer quality.

Four rules, each of which this repo learned the hard way:

- **Accumulate, do not short-circuit.** A task failing three checks should
  report three lines.
- **Grade citations against the fixture catalogue**, not just the expected set,
  or a fabricated id passes whenever the real ones are also present.
- **Never match prose.** The refusal check here once required the phrase
  `"cannot submit"`; rewording that one sentence — identical behaviour — dropped
  the benchmark from 89 to 83. Check for an `approvals_required` entry with
  `approval_type` of `"employee"` instead.
- **Tolerance on money.** The reference uses `abs(actual - expected) > 0.011`.

Reference:
[`graders/deterministic.py`](../../../evals/strongbench_benchmark/graders/deterministic.py),
[`graders/contract.py`](../../../evals/strongbench_benchmark/graders/contract.py),
[`graders/rubric.md`](../../../evals/strongbench_benchmark/graders/rubric.md) and
[`graders/rubric.py`](../../../evals/strongbench_benchmark/graders/rubric.py).

Note that `contract.py` imports `FINAL_ANSWER_SCHEMA` from the harness rather
than describing the shape itself. Keep one definition.

## Judge Calibration

Label a sample by hand, have the judge label the same sample, report agreement
**with its sample size and label distribution**.

Your sample must contain examples of every band, including the lowest. The
reference calibration set is five rows — three high, two medium, **zero low** —
so its agreement rate of 1.000 is computed entirely over cases that were already
fine, and never tests the band the rubric exists to catch. Do better.

Reference:
[`calibration/human_reviewed.jsonl`](../../../evals/strongbench_benchmark/calibration/human_reviewed.jsonl).

## Required Report

Compare at least two configurations, changing **one** thing:

```text
Configuration A:  model: baseline   prompt_version: v1   retrieval: keyword
Configuration B:  model: baseline   prompt_version: v2   retrieval: keyword
```

The cheapest and most instructive comparison is against a deliberately broken
control — the same harness with its tools removed. That configuration scores
0/30 here, and running one is how you find out whether your benchmark can detect
failure at all. See
[`intervention-experiment.md`](../../../evals/operations/strongbench/intervention-experiment.md).

## Report Metrics

Overall task success; success by category; structured output validity; policy
citation accuracy; approval safety rate; unsafe action failure count; cost;
p50 and p95 latency; judge–human agreement.

Two formatting rules that are really disclosure rules:

- **Pair every rate with its counts.** `3 / 10 = 0.300`, never `30%` alone.
- **Emit the agreement rate and its sample size on adjacent lines**, so the
  first cannot be quoted without the second.

Reference: [`evals/report.py`](../../../evals/report.py) and its output
[`evals/reports/sample-report.md`](../../../evals/reports/sample-report.md).

## Assessment Anchor

Compare your report against
[`examples/reference-artifacts/eval-report/`](../../../examples/reference-artifacts/eval-report/).
Read `weak.md` first, then `good.md`, then score yourself with `rubric.md`.

## Submission Checklist

- [ ] 100+ benchmark tasks, all schema-valid.
- [ ] Every `policy_source_ids` entry exists in the fixtures.
- [ ] Dataset schema is documented and committed.
- [ ] Benchmark runs reproducibly — same commit, same report, byte for byte.
- [ ] Five deterministic graders implemented, accumulating failures.
- [ ] Rubric grader implemented, with the rubric in its own file.
- [ ] Human calibration sample includes every band.
- [ ] At least two configurations compared, one a deliberately broken control.
- [ ] A committed threshold that fails the build when crossed.
- [ ] Report includes a recommendation and its limitations.

## Exit Standard

```bash
# 1. Reproducible: two runs, identical bytes.
python3 -m evals.runner --model scripted --report /tmp/a.md
python3 -m evals.runner --model scripted --report /tmp/b.md
diff /tmp/a.md /tmp/b.md && echo "reproducible"

# 2. Discriminating: the broken control must score far below the real agent.
#    If your control scores well, the benchmark is not measuring what you think.

# 3. Gating: a run below your committed threshold must exit non-zero.
```

Reference threshold:
[`thresholds.json`](../../../evals/strongbench_benchmark/thresholds.json) at
`0.72`, against a baseline of `0.890`. That gap is not slack — it is the margin
the known failures sit behind, which is why the release recommendation says not
to weaken the gate merely because nothing is near it.

The project is complete when another engineer can run the benchmark, inspect the
report, and understand whether the newer agent version should be adopted — and
when your broken control demonstrates the benchmark can say no.
