# Good Eval Report: Acme Expense Agent v1

## Decision

Hold the release gate at 0.72 and do not ship changes that reduce the scripted
baseline below the current 0.890 success rate.

## Evidence

- Benchmark: `evals/acme_benchmark/tasks.jsonl`
- Runner: `python3 -m evals.runner --model scripted`
- Result: 89/100 tasks passed
- Weakest tag: `receipt_lookup`, 3/10 passed
- Safety tag: `unsafe_submission`, 9/10 passed
- Judge calibration: 5 examples, 1.000 agreement

## Failure Analysis

The dominant production risk is not generic answer quality. It is evidence
selection before calculation. Receipt-heavy tasks fail when lookup arguments are
too broad or when the agent calculates over the wrong receipt set.

The second risk is item interpretation. The room-service task should count both
meal items against the daily meal limit, but the scripted parser classifies room
service as lodging and overstates the reimbursable total.

The third risk is approval boundary handling. Missing-receipt and client-event
tasks can produce a valid final-answer shape while omitting required manager
approval or missing-information fields.

## Recommendation

Approve the benchmark as a release gate. Do not treat the 89% baseline as
production-ready behavior. Use the Phase 3 regression pack to drive fixes in
this order:

1. Receipt lookup argument extraction.
2. Same-day meal and room-service parsing.
3. Missing-receipt and prepare-vs-submit approval examples.

## Why This Is Good

This report makes a release decision, names the benchmark command, reports
aggregate and per-tag evidence, identifies dominant failure modes, and turns
failures into a concrete intervention order.

