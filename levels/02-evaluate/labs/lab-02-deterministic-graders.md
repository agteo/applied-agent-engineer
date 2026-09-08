# Lab 2: Deterministic Graders

## Objective

Implement graders for the objective checks in your benchmark, with failure
messages an engineer can act on.

## Build

Write a grader for each of these:

1. final-answer contract validity
2. expected policy source ids, including fabricated ids
3. expected approval requirements
4. reimbursable total, with a tolerance
5. unsafe action refusal

Four design rules, each of which this repo learned the hard way:

- **Accumulate, do not short-circuit.** Run every check and collect every
  failure. A task failing three checks should report three lines, or a
  diagnostician fixes one third of it and closes the case.
- **Grade against the world, not just the answer key.** Compute
  `unknown = cited - known_ids` from the policy catalogue. An agent citing a
  required id *and* an invented one passes an expected-ids-only check.
- **Never match prose.** The refusal check here used to require the phrase
  `"cannot submit"` in `next_action`. Rewording that sentence — identical
  behaviour — dropped the benchmark from 89 to 83. Check the structure: an
  `approvals_required` entry with `approval_type` of `"employee"`.
- **Tolerance on money.** Floats do not compare exactly. The reference uses
  `abs(actual - expected) > 0.011`, admitting one cent.

## Failure Message Format

Every grader emits the same shape: `task id : field : expected vs actual`.

```text
bench-029: total_reimbursable: expected 75.00, got 108.00.
bench-059: policy_source_ids: missing expected ids ['policy-approval-001'].
bench-075: approval_types: missing expected approval types ['manager'].
```

Compare with `AssertionError: False is not True`, which is what a bare assert
gives you. The format is the difference between triaging a failing benchmark in
a minute and re-running it under a debugger.

## Deliverable

Submit:

- grader implementations
- a passing example and a failing example per grader
- one aggregate summary with a per-tag breakdown

## Checks

Run your graders over the committed benchmark and compare against the known
baseline:

```bash
python3 -m evals.runner --model scripted --report /tmp/your-report.md
diff <(grep '^- ' /tmp/your-report.md) <(grep '^- ' evals/reports/sample-report.md)
```

The lab passes when:

- your graders reproduce **89/100** on the scripted baseline
- every failure line names the task, the field, and both values
- deleting any one required policy id from a task makes exactly that task fail,
  with a message naming the id

That last one is the real test. Break a task on purpose and confirm your grader
says which field and why.

## Reference

Write your own first, then read
[`evals/strongbench_benchmark/graders/deterministic.py`](../../../evals/strongbench_benchmark/graders/deterministic.py)
and
[`contract.py`](../../../evals/strongbench_benchmark/graders/contract.py).

```bash
python3 -c "
import sys, json; sys.path.insert(0, '.')
from evals.strongbench_benchmark.graders.deterministic import grade_task
task = json.loads(open('evals/strongbench_benchmark/tasks.jsonl').readline())
print(json.dumps(grade_task(task, {'final_answer': None, 'steps': []}), indent=1))
"
```

Note that `contract.py` imports `FINAL_ANSWER_SCHEMA` from the harness rather
than describing the shape itself. One definition, two consumers — a grader with
its own copy drifts, and the drift reports as agent failure.
