# Evals

This folder contains the Level 2 benchmark, graders, reports, release gate, and
Level 3 failure operations bundle.

Run the Acme benchmark with no API key:

```bash
python3 -m evals.runner --model scripted
```

The command runs 100 tasks, grades each final answer, writes
[`reports/sample-report.md`](reports/sample-report.md), and exits non-zero when
the committed threshold in
[`acme_benchmark/thresholds.json`](acme_benchmark/thresholds.json) is not met.

What Phase 2 builds against, which already exists:

- a runnable agent: [`examples/acme-expense-agent/`](../examples/acme-expense-agent/)
- a final-answer contract to grade: `acme_agent/schemas.py`
- a trace format to read: [`docs/trace-schema.md`](../examples/acme-expense-agent/docs/trace-schema.md)
- fixtures with known-correct answers: `fixtures/policies.json`, `fixtures/receipts.json`
- a deterministic, zero-cost model adapter, so a 100-task benchmark run is free and reproducible in CI

Contents:

```text
evals/
  acme_benchmark/
    tasks.jsonl
    schema.json
    thresholds.json
    graders/
    calibration/
  runner.py
  report.py
  reports/sample-report.md
  operations/
  tests/
```

The scripted baseline intentionally does not pass every task. Its failures are
teaching material for Level 3: receipt disambiguation, room-service category
parsing, missing-receipt handling, and preparation/submission boundaries.

Build the Level 3 failure bundle:

```bash
python3 -m evals.operations
```

Use its failure annotations as the input to the Level 4 dataset builder:

```bash
python3 -m datasets.acme
```
