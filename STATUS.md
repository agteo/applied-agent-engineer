# Project Status

Level 1 is executable. Levels 2-7 are still specification.

## Current State

What runs today, offline, with no API key:

```bash
cd examples/acme-expense-agent
python run_agent.py --all --quiet
python -m acme_agent.check_traces traces/level-1.jsonl
python -m pytest
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

What exists as specification only:

- course framework, syllabus, mental models, glossary
- module outlines, lesson, lab, and project specs for Levels 1-7
- structure for evals, datasets, and environments

What does not exist yet:

- 100-task golden benchmark and graders (Phase 2)
- annotated failure bundle and failure taxonomy examples (Phase 4)
- trace-to-dataset converter and a reference dataset card (Phase 4)
- Acme Corp Simulator implementation (Phase 6)
- training scripts and LoRA configs (Phase 5)

## Honest Claim

A learner can now build Level 1 against a working reference: run the agent, run the labs, diff their harness against a solution that executes, and get an automated pass/fail on their own trace bundle.

They cannot yet evaluate their agent against a real benchmark, which is the difference between "I built an agent" and "I know whether it works". That is Phase 2, and until it ships, Levels 2-7 remain instructor-readable specification rather than a course a solo learner can complete.

## Near-Term Definition of Done

The first usable release supports Levels 1-2 end to end:

1. Learner can run Acme Expense Agent v1 locally. **Done.**
2. Learner can run the Level 1 labs. **Done.**
3. Learner can compare their work against reference solutions. **Done.**
4. Learner can see automated pass/fail checks on Level 1 output. **Done.**
5. Learner can run a 100-task benchmark. **Not started.**
6. Learner can produce an eval report from real benchmark output. **Not started.**

## Rule Of Construction

The failure mode this project watches for is specification work crowding out executable work: writing another curriculum document is pleasant, legible, and can absorb unlimited effort while the runnable core stays at zero.

So: no new curriculum documents while an unshipped phase is the next priority. A phase ships when its code runs in CI, not when its spec reads well.
