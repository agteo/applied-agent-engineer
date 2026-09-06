# Project: Acme Expense Agent Failure Report v1

## Objective

Analyze Level 2 benchmark failures and produce a diagnostic report that explains what is failing, why it is failing, and what should be improved next.

## Required Inputs

- Level 2 benchmark tasks
- benchmark run results
- agent traces
- grader outputs
- human review notes if available

## Required Outputs

- annotated failed traces: [`evals/operations/acme/annotated-failures.jsonl`](../../../evals/operations/acme/annotated-failures.jsonl)
- taxonomy file: [`evals/operations/acme/taxonomy.md`](../../../evals/operations/acme/taxonomy.md)
- failure distribution: [`evals/operations/acme/failure-distribution.json`](../../../evals/operations/acme/failure-distribution.json)
- hypotheses: [`evals/operations/acme/failure-report.md`](../../../evals/operations/acme/failure-report.md)
- intervention experiment: [`evals/operations/acme/intervention-experiment.md`](../../../evals/operations/acme/intervention-experiment.md)
- report: [`evals/operations/acme/failure-report.md`](../../../evals/operations/acme/failure-report.md)

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
