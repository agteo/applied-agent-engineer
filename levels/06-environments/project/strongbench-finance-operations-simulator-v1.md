# Project: StrongBench Finance Operations Simulator v1

## Objective

Build a simulated company environment where the StrongBench agent can complete policy-governed finance operations tasks safely and reproducibly.

The first implementation may focus on expense reimbursement because that is the current executable seed. Design the state model so it can expand into invoices, purchase orders, approval routing, reconciliation, audit logs, and exception handling.

## Required Components

- environment state schema: [`environments/strongbench_finance/state-schema.json`](../../../environments/strongbench_finance/state-schema.json)
- simulated tools: [`environments/strongbench_finance/tool-schemas.json`](../../../environments/strongbench_finance/tool-schemas.json)
- task generator: [`environments/strongbench_finance/__init__.py`](../../../environments/strongbench_finance/__init__.py)
- generated tasks: [`environments/strongbench_finance/tasks.jsonl`](../../../environments/strongbench_finance/tasks.jsonl)
- deterministic, state, and constraint verifiers: [`environments/strongbench_finance/__init__.py`](../../../environments/strongbench_finance/__init__.py)
- reward function derived from verifier components: [`environments/strongbench_finance/reward-design.md`](../../../environments/strongbench_finance/reward-design.md)
- rollout logger: [`environments/strongbench_finance/rollouts.jsonl`](../../../environments/strongbench_finance/rollouts.jsonl)
- environment manifest: [`environments/strongbench_finance/manifest.json`](../../../environments/strongbench_finance/manifest.json)

Build the reference bundle:

```bash
python3 -m environments.strongbench_finance
```

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
