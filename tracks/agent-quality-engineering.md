# Agent Quality Engineering

## Focus

Agent Quality Engineering is the production discipline around agent reliability.

The learner should be able to operate this loop:

```text
production traces
  -> failure review
  -> eval datasets
  -> regression packs
  -> release gates
  -> monitoring
  -> new test cases
```

## Core Skills

- trace inspection
- tool-call and latency analysis
- eval dataset curation
- deterministic grading
- LLM-judge calibration
- regression detection
- adversarial testing
- release gates in CI
- production feedback loops

## Reference Stack

The preferred reference stack is open-source-first:

```text
Python + pytest
Langfuse
Inspect AI
GitHub Actions
```

Hosted tools such as Braintrust, LangSmith, and managed Langfuse should be treated as production variants, not prerequisites.

## Portfolio Evidence

A learner completing this track should have:

- a benchmark with deterministic graders
- a production-style eval report
- a failed-trace bundle
- a regression pack
- a CI release gate
- a failure analysis report
- a recommendation about whether a candidate agent version should ship

Portfolio example:

- [`examples/portfolio/agent-quality-engineering.md`](../examples/portfolio/agent-quality-engineering.md)
