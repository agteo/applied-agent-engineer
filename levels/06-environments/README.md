# Level 6: Environments

## Goal

Build simulated environments and verifiers where agents can practice safely, produce measurable outcomes, and generate trajectories for evaluation or training.

Level 5 asked: should we adapt the model?

Level 6 asks: can we create a world where the agent can act, fail, recover, and be scored?

## Learning Outcomes

By the end of this level, learners can:

1. Model a domain as state, actions, observations, and transitions.
2. Build simulated tools with realistic constraints and errors.
3. Generate tasks with known success conditions.
4. Define deterministic, state, constraint, and model-based verifiers.
5. Make environment runs reproducible.
6. Detect simulator bias and unrealistic shortcuts.
7. Convert verifier outputs into reward components.
8. Produce rollouts that can feed Level 7 reinforcement learning.

## Required Build

Learners build the first version of StrongBench Finance Operations Simulator, a simulated company environment for policy-governed finance workflows.

The first implementation may start with expense reimbursement because the executable Level 1 seed is the StrongBench Expense Agent. The target simulator should be able to expand into invoices, purchase orders, vendor records, reconciliation, approval routing, audit logs, and exception handling.

Build the reference simulator bundle:

```bash
python3 -m environments.strongbench_finance
```

## Environment Loop

```text
Task
  |
  v
Agent
  |
  v
Action
  |
  v
Environment state transition
  |
  v
Observation + reward signal
  |
  v
Agent continues or stops
```

## StrongBench Finance Operations Simulator Scope

The first simulator should include:

- employees
- managers
- expense policies
- receipts
- trips
- reimbursement drafts
- approval requests
- tool permissions
- success checks
- verifier results
- audit logs

Later finance operations extensions may include:

- vendors
- invoices
- purchase orders
- payment status
- account codes
- reconciliation records
- exception queues

## Module Plan

Read the full lesson sequence in [lessons/README.md](lessons/README.md).

| Lesson | Topic | Artifact |
| --- | --- | --- |
| 1 | Environment thinking | State/action sketch |
| 2 | State and transitions | Environment state schema |
| 3 | Simulated tools | Tool simulator |
| 4 | Task generation | Task set |
| 5 | Verifiers, rewards, and success checks | Verifier and reward function |
| 6 | Reproducibility and realism | Environment manifest |
| 7 | Rollout analysis | Rollout dataset |

## Labs

| Lab | Description |
| --- | --- |
| [Lab 1: State Model](labs/lab-01-state-model.md) | Define the environment state schema. |
| [Lab 2: Simulated Tools](labs/lab-02-simulated-tools.md) | Build safe simulated tools. |
| [Lab 3: Task Generator](labs/lab-03-task-generator.md) | Generate tasks with expected outcomes. |
| [Lab 4: Reward Function](labs/lab-04-reward-function.md) | Score agent behavior automatically from verifier components. |

## Project

The Level 6 project is [StrongBench Finance Operations Simulator v1](project/strongbench-finance-operations-simulator-v1.md). The reference implementation is in
[`environments/strongbench_finance/`](../../environments/strongbench_finance/). The first implementation may start with expenses, then expand as the canonical domain decision is finalized.

## Exit Criteria

To complete Level 6, the learner must submit:

1. A documented environment state schema.
2. At least five simulated tools.
3. At least 100 generated tasks.
4. Deterministic, state, and constraint verifiers.
5. A reward function derived from verifier components, with known limitations.
6. Reproducible rollout logs.
7. A realism and simulator-bias note.
