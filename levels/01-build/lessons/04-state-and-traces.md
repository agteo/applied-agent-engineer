# Lesson 4: State and Traces

## Core Idea

If you cannot see what the agent did, you cannot evaluate or diagnose it.

State is for the running system. Traces are for the engineers who need to understand behavior later.

## State

Runtime state should include:

- task id
- messages
- tool calls
- observations
- approval status
- final answer
- errors

## Trace

A trace should preserve enough information to replay or inspect the run:

- input task
- model and prompt version
- step-by-step decisions
- tool arguments before and after validation
- tool outputs
- final answer
- cost and latency if available

## Trace Quality

A good trace is:

- structured
- complete
- loadable by scripts
- safe to store
- free of real secrets or private data

## Checkpoint

You are ready to move on when 20 manual tasks produce valid JSONL traces.

