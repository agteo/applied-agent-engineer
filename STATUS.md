# Project Status

Levels 1-4 are executable. Levels 5-7 are still specification.

## Current State

What runs today, offline, with no API key:

```bash
cd examples/acme-expense-agent
python3 run_agent.py --all --quiet
python3 -m acme_agent.check_traces traces/level-1.jsonl
python3 -m pytest
cd ../..
python3 -m evals.runner --model scripted
python3 -m evals.operations
python3 -m datasets.acme
```

What exists as code:

- Acme Expense Agent v1 harness: loop, tool validation, step budget, error handling
- four tools over local fixtures: `search_policy`, `lookup_receipt`, `calculate_reimbursement`, `request_human_approval`
- policy, receipt, employee, and task fixtures
- two model adapters: a deterministic offline planner and Anthropic
- trace schema, trace writer, and a documented JSONL format
- an automated Level 1 check with per-field failure messages
- reference solutions for all four Level 1 labs
- 50 tests
- CI workflow running the tests, the full task set, and the trace check
- 100-task Acme benchmark with deterministic graders, a report writer, and a CI release gate
- Phase 3 eval-ops bundle: annotated failures, regression pack, taxonomy, release recommendation, instructor guide, and failure report
- Phase 4 dataset bundle: trace-to-dataset builder, cleaned dataset, rejected-row log, train/dev/heldout splits, schema, metrics, synthetic-generation note, and dataset card

What exists as specification only:

- course framework, syllabus, mental models, glossary
- module outlines, lesson, lab, and project specs for Levels 1-7
- structure for environments

What does not exist yet:

- model-improvement decision track and optional training implementation (Phase 5)
- Acme Finance Operations Simulator implementation (Phase 6)
- verifier/reward design for deterministic, state, constraint, and model-based checks (Phase 6)
- Prime Intellect adapter and RL reliability experiment (Phase 6/7)
- training scripts and LoRA configs (Phase 5)

## Honest Claim

A learner can now build Level 1 against a working reference: run the agent, run the labs, diff their harness against a solution that executes, and get an automated pass/fail on their own trace bundle.

They can now evaluate the Acme Expense Agent against a 100-task benchmark, get a deterministic release-gate report, turn failures into annotated diagnosis and regression artifacts, and convert traces, corrections, and synthetic gap examples into a cleaned dataset with a reference dataset card. They cannot yet make or validate a model-improvement decision with executable training or serving infrastructure. That is the next gap before Level 5 becomes solo-learner executable.

## Near-Term Definition of Done

The first usable release supports Levels 1-2 end to end:

1. Learner can run Acme Expense Agent v1 locally. **Done.**
2. Learner can run the Level 1 labs. **Done.**
3. Learner can compare their work against reference solutions. **Done.**
4. Learner can see automated pass/fail checks on Level 1 output. **Done.**
5. Learner can run a 100-task benchmark. **Done.**
6. Learner can produce an eval report from real benchmark output. **Done.**
7. Learner can use the eval report as a CI release gate. **Done.**
8. Learner can turn failed traces into new eval cases. **Done.**
9. Learner can convert traces and failure corrections into a cleaned dataset. **Done.**
10. Learner can grade eval reports, failure analyses, dataset cards, model decisions, and reward designs against anchored examples. **Done.**

## Canonical System Direction

The current executable seed is the Acme Expense Agent. The final canonical system should remain contingent on where companies are actually deploying agents and need evaluation capability.

The current working hypothesis is to expand from expense reimbursement into an Acme Finance Operations Agent because finance operations supports realistic workflows, approvals, compliance, structured records, deterministic/state verification, and later RL environments.

See [curriculum/canonical-system-strategy.md](curriculum/canonical-system-strategy.md).

## Rule Of Construction

The failure mode this project watches for is specification work crowding out executable work: writing another curriculum document is pleasant, legible, and can absorb unlimited effort while the runnable core stays at zero.

So: no new curriculum documents while an unshipped phase is the next priority. A phase ships when its code runs in CI, not when its spec reads well.
