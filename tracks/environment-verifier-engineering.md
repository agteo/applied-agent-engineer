# Environment and Verifier Engineering

## Focus

Environment and Verifier Engineering teaches learners to build reproducible worlds where agents can act, fail, recover, and be scored.

A verifier answers:

> Did the agent actually accomplish the task?

That is stronger than asking whether the final response sounds good.

## Verifier Types

| Type | Example |
| --- | --- |
| Deterministic verifier | `assert invoice.total == 183.42` |
| State verifier | Check that a simulated database, calendar, ticket, or approval state changed correctly. |
| Constraint verifier | Score partial completion across required conditions. |
| Model-based verifier | Use an LLM judge for subjective quality that cannot be checked deterministically. |

## Core Skills

- task design
- state modeling
- action and observation schemas
- simulated tools
- sandboxing
- deterministic checks
- state and constraint verification
- reward component design
- reward hacking analysis
- rollout logging

## Reference Stack

The preferred reference stack is:

```text
Python + pytest
Docker
local simulator
Inspect AI for eval integration
Prime Intellect / Verifiers as an advanced hosted adapter
```

BrowserGym, Browserbase, E2B, and METR Task Standard are useful comparison paths for browser, sandbox, and portable task environments.

## Portfolio Evidence

A learner completing this track should have:

- a simulated environment
- generated task sets
- state transition logs
- deterministic and state verifiers
- constraint scoring examples
- reward functions with known limitations
- rollout logs
- reward hacking examples

Portfolio example:

- [`examples/portfolio/environment-verifier-engineering.md`](../examples/portfolio/environment-verifier-engineering.md)
