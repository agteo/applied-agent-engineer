# Project: Acme Finance Operations Simulator v1

## Objective

Build a simulated company environment where the Acme agent can complete policy-governed finance operations tasks safely and reproducibly.

The first implementation may focus on expense reimbursement because that is the current executable seed. Design the state model so it can expand into invoices, purchase orders, approval routing, reconciliation, audit logs, and exception handling.

## Required Components

- environment state schema
- simulated tools
- task generator
- deterministic, state, and constraint verifiers
- reward function derived from verifier components
- rollout logger
- environment manifest

## Assessment Anchor

Compare your verifier-derived reward design against the reward-design examples
and rubric in
[`examples/reference-artifacts/reward-design/`](../../../examples/reference-artifacts/reward-design/).

## Required Tasks

Create at least 100 tasks. The first slice should cover:

- straightforward reimbursement
- missing receipts
- meal limits
- ambiguous receipt lookup
- manager approval
- unsafe submission attempts
- multi-step trip reimbursement
- edge cases

The expanded finance operations slice should add:

- invoice review
- purchase order matching
- approval routing
- vendor lookup
- account code validation
- reconciliation exceptions
- audit trail checks

## Submission Checklist

- [ ] Environment state documented.
- [ ] Five or more simulated tools implemented or specified.
- [ ] 100+ tasks generated.
- [ ] Deterministic, state, and constraint verifiers implemented or specified.
- [ ] Reward function documented as a composition of verifier outputs.
- [ ] Rollout format documented.
- [ ] Simulator bias note included.
