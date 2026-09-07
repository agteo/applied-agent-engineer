# Environment And Verifier Engineering: StrongBench Finance Simulator

## One-Sentence Claim

I built a seeded finance workflow simulator with state transitions, verifiers,
reward components, and rollout logs that catch unsafe shortcut behavior.

## Problem

Final-answer grading is not enough for workflow agents. An agent can write a
correct-looking answer while skipping receipts, failing to create a draft, or
submitting a report as the wrong actor.

## Measurement

- simulator command: `python3 -m environments.strongbench_finance`
- tasks: 120
- task categories: 8
- simulated tools: 6
- verifier types: deterministic, state, constraint
- scripted baseline: 120/120 rollouts passed
- average reward: 1.750

## Diagnosis

The simulator needed verifiers that look at state, not just text. The important
checks are draft creation, approval correctness, submission correctness,
required receipt lookup, and final-answer contract.

## Intervention Or Decision

I implemented a local simulator and decomposed reward into auditable
components: `task_success`, `required_records_checked`,
`correct_approval_behavior`, `valid_final_answer_contract`, and penalties for
invalid tool calls and unauthorized submission.

## Evidence

| Candidate | Evidence | Decision |
| --- | --- | --- |
| Scripted reference policy | 120/120 passed | Use as simulator sanity check |
| Reward-hacking submitter | caught by verifier failures | Use as negative-control policy |
| Simulator scope | expense reimbursement only | Document limits before expanding |

## Differentiating Choice

I would add an invoice-review task family using the same state/verifier
interface: vendor lookup, purchase-order match, approval threshold, and audit
log checks.

## What I Would Do Next

Add a model-based verifier for subjective explanation quality, then port the
same verifier interface to a second domain.

## Links

- [`environments/strongbench_finance/verifier-report.md`](../../environments/strongbench_finance/verifier-report.md)
- [`environments/strongbench_finance/reward-design.md`](../../environments/strongbench_finance/reward-design.md)
- [`environments/strongbench_finance/simulator-bias-note.md`](../../environments/strongbench_finance/simulator-bias-note.md)
- [`examples/reference-artifacts/reward-design/good.md`](../reference-artifacts/reward-design/good.md)
