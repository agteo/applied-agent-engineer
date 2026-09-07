# Good Failure Analysis: StrongBench Expense Agent v1

## Claim

The scripted agent's remaining benchmark failures are concentrated in evidence
selection and policy-boundary interpretation, not final-answer formatting.

## Evidence

- Benchmark: `python3 -m evals.runner --model scripted`
- Result: 89/100 tasks passed
- Diagnostic bundle: `python3 -m evals.operations`
- Annotated failures: 30 rows in `evals/operations/strongbench/annotated-failures.jsonl`
- Regression pack: 30 cases in `evals/operations/strongbench/regression-pack.jsonl`

## Failure Modes

1. `TOOLS.receipt_lookup`: receipt-heavy tasks use broad lookup arguments and
   calculate over the wrong receipt set.
2. `MODEL.policy_boundary`: room service and threshold cases are classified
   under the wrong policy branch.
3. `MODEL.instruction_following`: prepare-vs-submit and approval-gated tasks
   can produce a valid answer shape while missing required approval behavior.

## Intervention Order

Fix receipt lookup argument extraction first because it accounts for the
largest recurring error family. Then add correction examples for meal/lodging
boundaries. Finally, lock unsafe submission behavior with regression tests.

## Why This Is Good

This analysis names commands, counts, artifacts, and trace-backed labels. It
separates root causes from symptoms and turns diagnosis into a build order.
