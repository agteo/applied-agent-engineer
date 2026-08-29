# Lab 5: Gateway Failover Drill

## Objective

Route the Acme Expense Agent through a local inference gateway and prove that it can continue when the local worker fails.

## Setup

Use generic aliases instead of hardcoded model names:

- `acme-local-primary`
- `acme-hosted-fallback`
- `acme-agent-model`

The alias `acme-agent-model` should route to the local primary first and use a hosted or secondary fallback only when the primary is unavailable or unhealthy.

## Drill

Run three eval slices from the Level 2 benchmark:

1. Normal local serving.
2. Local worker unavailable before the run starts.
3. Local worker interrupted during a run.

## Deliverable

Submit:

- gateway configuration
- local worker command or container configuration
- agent model configuration
- health check behavior
- fallback behavior evidence
- latency and error observations
- notes on quality differences between primary and fallback responses

## Checks

The lab passes if:

- the agent calls the gateway, not the worker directly
- the local worker can be marked unhealthy
- fallback behavior is observable
- the agent completes at least one benchmark slice during local worker failure
- the report separates serving reliability from model quality
