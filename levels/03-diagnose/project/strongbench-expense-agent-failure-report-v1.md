# Project: StrongBench Expense Agent Failure Report v1

## Objective

Analyze Level 2 benchmark failures and produce a diagnostic report that explains what is failing, why it is failing, and what should be improved next.

## Required Inputs

- Level 2 benchmark tasks
- benchmark run results
- agent traces
- grader outputs
- human review notes if available

## Required Outputs

- annotated failed traces: [`evals/operations/strongbench/annotated-failures.jsonl`](../../../evals/operations/strongbench/annotated-failures.jsonl)
- taxonomy file: [`evals/operations/strongbench/taxonomy.md`](../../../evals/operations/strongbench/taxonomy.md)
- failure distribution: [`evals/operations/strongbench/failure-distribution.json`](../../../evals/operations/strongbench/failure-distribution.json)
- hypotheses: [`evals/operations/strongbench/failure-report.md`](../../../evals/operations/strongbench/failure-report.md)
- intervention experiment: [`evals/operations/strongbench/intervention-experiment.md`](../../../evals/operations/strongbench/intervention-experiment.md)
- report: [`evals/operations/strongbench/failure-report.md`](../../../evals/operations/strongbench/failure-report.md)

## Assessment Anchor

Compare your report against the failure-analysis examples and rubric in
[`examples/reference-artifacts/failure-analysis/`](../../../examples/reference-artifacts/failure-analysis/).

## Submission Checklist

- [ ] 30+ failed traces annotated.
- [ ] Failure taxonomy documented.
- [ ] Dominant failure modes identified.
- [ ] At least three hypotheses documented.
- [ ] At least one intervention tested.
- [ ] Report recommends data work for Level 4.
