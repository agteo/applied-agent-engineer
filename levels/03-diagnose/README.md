# Level 3: Production Eval Operations and Diagnose

## Goal

Operate the production quality loop around an agent, then explain why it failed using evidence from traces, benchmark results, and grader outputs.

Level 2 asked: how good is the agent?

Level 3 asks: how do failures become regression tests, release decisions, and targeted interventions?

## Learning Outcomes

By the end of this level, learners can:

1. Read agent trajectories step by step.
2. Convert traces and failures into eval datasets and regression packs.
3. Set release-gate thresholds for agent changes.
4. Classify failures using a structured taxonomy.
5. Separate model, harness, tool, retrieval, memory, environment, and grader failures.
6. Identify dominant failure modes across a benchmark run.
7. Form evidence-backed hypotheses.
8. Design targeted interventions.
9. Run experiments that confirm or reject those interventions.

## Required Build

Learners create a production-style eval operations report and Agent Failure Report for StrongBench Expense Agent v1 using the Level 2 benchmark.

## Production Eval Operations Flow

```text
Production traces
    |
    v
Failure review
    |
    v
Eval dataset
    |
    v
Regression pack
    |
    v
Release gate
    |
    +------ PASS -> deploy
    |
    +------ FAIL
             |
             v
        Diagnose
             |
             v
        New test case
```

## Diagnostic Flow

```text
Eval failures
    |
    v
Trace inspection
    |
    v
Failure taxonomy
    |
    v
Hypothesis
    |
    v
Intervention
    |
    v
Experiment
    |
    v
Result
```

## Core Taxonomy

Use this taxonomy as the starting point:

```text
MODEL
  reasoning
  instruction_following
  knowledge
  hallucination

HARNESS
  prompt
  context
  routing
  state
  stopping

TOOLS
  selection
  arguments
  execution
  interpretation

RETRIEVAL
  query
  recall
  ranking
  citation
  stale_source

MEMORY
  retrieval
  relevance
  persistence
  contamination

ENVIRONMENT
  ambiguity
  permissions
  state
  simulator_error

EVALUATION
  grader_wrong
  rubric_unclear
  expected_answer_wrong
  dataset_gap
```

## Module Plan

Read the full lesson sequence in [lessons/README.md](lessons/README.md).

| Lesson | Topic | Artifact |
| --- | --- | --- |
| 1 | Reading trajectories | Annotated trace |
| 2 | Failure taxonomy | Taxonomy file |
| 3 | Root cause analysis | Failure labels |
| 4 | Hypotheses and interventions | Intervention plan |
| 5 | Experiment design | Experiment record |
| 6 | Production eval operations | Regression pack and release gate |
| 7 | Reporting diagnosis | Failure report |

## Labs

| Lab | Description |
| --- | --- |
| [Lab 1: Trace Annotation](labs/lab-01-trace-annotation.md) | Annotate failed trajectories from Level 2. |
| [Lab 2: Failure Taxonomy](labs/lab-02-failure-taxonomy.md) | Create a taxonomy and label set. |
| [Lab 3: Intervention Experiment](labs/lab-03-intervention-experiment.md) | Test a targeted fix against the benchmark. |
| [Lab 4: Failure Report](labs/lab-04-failure-report.md) | Write an evidence-backed diagnostic report. |

## Project

The Level 3 project is [StrongBench Expense Agent Failure Report v1](project/strongbench-expense-agent-failure-report-v1.md).

## Exit Criteria

To complete Level 3, the learner must submit:

1. At least 30 annotated failed traces.
2. A regression pack generated from failures.
3. A release-gate recommendation.
4. A failure taxonomy with examples.
5. Aggregate failure counts by category.
6. At least three evidence-backed hypotheses.
7. At least one tested intervention.
8. A failure report with recommendations for Level 4 data work.
