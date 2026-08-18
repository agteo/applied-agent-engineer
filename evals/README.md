# Evals

This folder is reserved for benchmark tasks, graders, reports, and regression scripts.

Level 2 defines the first formal benchmark for Acme Expense Agent v1. Start with [../levels/02-evaluate/README.md](../levels/02-evaluate/README.md).

What Phase 2 builds against, which already exists:

- a runnable agent: [`examples/acme-expense-agent/`](../examples/acme-expense-agent/)
- a final-answer contract to grade: `acme_agent/schemas.py`
- a trace format to read: [`docs/trace-schema.md`](../examples/acme-expense-agent/docs/trace-schema.md)
- fixtures with known-correct answers: `fixtures/policies.json`, `fixtures/receipts.json`
- a deterministic, zero-cost model adapter, so a 100-task benchmark run is free and reproducible in CI

Expected contents:

```text
evals/
  tasks/
  graders/
  reports/
  fixtures/
```
