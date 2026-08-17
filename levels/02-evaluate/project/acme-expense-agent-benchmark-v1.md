# Project: Acme Expense Agent Benchmark v1

## Objective

Build a reproducible benchmark for Acme Expense Agent v1.

The benchmark should measure whether the agent completes realistic expense tasks correctly, safely, and efficiently.

## Required Dataset

Create at least 100 tasks.

The dataset should include:

- task id
- user request
- category
- difficulty
- required tools
- expected outputs
- expected policy source ids
- expected approvals
- grading notes

## Required Categories

Include tasks for:

- policy questions
- receipt lookup
- reimbursement calculation
- missing receipts
- manager approval
- multi-item trips
- ambiguous requests
- unsafe submission requests
- edge cases

## Required Graders

Implement at least these deterministic graders:

1. structured output validity
2. policy citation accuracy
3. approval safety
4. reimbursable total accuracy
5. unsafe action refusal

Add one rubric grader or LLM judge for answer quality.

## Required Report

The report must compare at least two configurations.

Example comparison:

```text
Configuration A:
  model: baseline
  prompt_version: v1
  retrieval: keyword

Configuration B:
  model: baseline
  prompt_version: v2
  retrieval: keyword
```

## Report Metrics

Include:

- overall task success
- success by category
- structured output validity
- policy citation accuracy
- approval safety rate
- unsafe action failure count
- average cost if available
- p50 and p95 latency if available
- judge and human agreement

## Submission Checklist

- [ ] 100+ benchmark tasks.
- [ ] Dataset schema is documented.
- [ ] Benchmark can run reproducibly.
- [ ] Deterministic graders are implemented.
- [ ] Rubric grader or LLM judge is implemented.
- [ ] Human calibration sample is included.
- [ ] At least two agent configurations are compared.
- [ ] Report includes recommendation and limitations.

## Exit Standard

The project is complete when another engineer can run the benchmark, inspect the report, and understand whether the newer agent version should be adopted.

