# Project: Resilient Local Inference Stack

## Objective

Deploy a local or open model behind a gateway and decide whether the Acme Expense Agent should use local, hosted, or hybrid inference.

This project completes Track 5C. It does not require training a model.

## Required Stack

Build a two-tier serving stack:

1. One local or self-managed inference worker.
2. One gateway endpoint used by the Acme Expense Agent.

The gateway must provide:

- a stable model alias for the agent
- health checks or equivalent unhealthy-worker detection
- fallback behavior
- request logging
- basic latency and error visibility

## Required Tests

Run the same small benchmark slice under at least three conditions:

- normal local serving
- local worker unavailable
- local worker interrupted during an agent or eval run

## Required Metrics

Report:

- task success
- structured output validity
- time to first token if available
- total latency
- tokens per second if available
- error rate
- fallback rate
- local resource saturation if available
- cost estimate for fallback traffic if available

## Submission Checklist

- [ ] Gateway configuration documented.
- [ ] Local worker command or container configuration documented.
- [ ] Agent points at the gateway model alias.
- [ ] Fallback target is configured without hardcoding course-specific model names.
- [ ] Health or failure detection behavior is documented.
- [ ] Resilience drill evidence included.
- [ ] Benchmark slice results compared across conditions.
- [ ] Recommendation explains local vs hosted vs hybrid adoption.
