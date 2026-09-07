# Eval Operations

Phase 3 turns Level 2 benchmark output into diagnosis and regression artifacts.

Run:

```bash
python3 -m evals.operations
```

Outputs:

```text
evals/operations/strongbench/
  annotated-failures.jsonl
  regression-pack.jsonl
  failure-distribution.json
  failure-report.md
  intervention-experiment.md
  release-recommendation.md
  instructor-review-guide.md
  taxonomy.md
```

The bundle includes the real scripted-baseline failures and a deliberately weak
no-tool baseline. The weak baseline gives learners enough failed traces to
practice annotation while keeping the real benchmark failures separate and
traceable.
