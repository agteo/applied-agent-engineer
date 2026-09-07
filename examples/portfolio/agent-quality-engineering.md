# Agent Quality Engineering: Release Gate And Failure Diagnosis

## One-Sentence Claim

I built a deterministic benchmark and eval-ops loop for the Acme Expense Agent,
then used it to hold quality steady while diagnosing concrete receipt, policy,
and approval failures.

## Problem

The agent answers employee expense questions and can prepare reimbursement
recommendations. A wrong answer can overstate reimbursement, skip a required
approval, or imply that the agent may submit a report the employee must submit
personally.

## Measurement

- benchmark command: `python3 -m evals.runner --model scripted`
- diagnostic command: `python3 -m evals.operations`
- benchmark size: 100 tasks
- release threshold: 0.720 success rate
- current baseline: 0.890 success rate
- safety slice: `unsafe_submission`, 9/10 passed

## Diagnosis

The overall score hid weak behavior in `receipt_lookup`, where only 3/10 tasks
passed. The Phase 3 failure bundle annotated 30 failures and showed recurring
`TOOLS.selection`, `TOOLS.arguments`, and `RETRIEVAL.citation` labels.

## Intervention Or Decision

The release gate should stay in CI, and new changes should not ship if they
reduce total success or increase submission-gate failures. The next
intervention should target receipt lookup arguments before model training.

## Evidence

| Candidate | Evidence | Decision |
| --- | --- | --- |
| Scripted baseline | 89/100 benchmark tasks passed | Keep as release gate baseline |
| Weak no-tool baseline | 0/30 calibration-slice tasks passed | Reject |
| Receipt lookup slice | 3/10 passed | Diagnose before shipping broader changes |

## Differentiating Choice

I would extend the benchmark with a new ambiguous-receipt task family covering
same merchant, same amount, different trip dates. That tests whether the agent
uses receipt ids and trip context instead of broad keyword lookup.

## What I Would Do Next

Add regression cases for the receipt lookup failures, improve argument
extraction, and rerun the Level 2 benchmark plus the Phase 3 regression pack.

## Links

- [`evals/reports/sample-report.md`](../../evals/reports/sample-report.md)
- [`evals/operations/acme/failure-report.md`](../../evals/operations/acme/failure-report.md)
- [`examples/reference-artifacts/eval-report/good.md`](../reference-artifacts/eval-report/good.md)
- [`examples/reference-artifacts/failure-analysis/good.md`](../reference-artifacts/failure-analysis/good.md)
