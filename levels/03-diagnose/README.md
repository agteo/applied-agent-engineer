# Level 3: Diagnose

## Goal

Explain why an agent failed using evidence from traces, benchmark results, and grader outputs.

Level 2 asked: how good is the agent?

Level 3 asks: why did it fail, and what should we try next?

## Learning Outcomes

By the end of this level, learners can:

1. Read agent trajectories step by step.
2. Classify failures using a structured taxonomy.
3. Separate model, harness, tool, retrieval, memory, environment, and grader failures.
4. Identify dominant failure modes across a benchmark run.
5. Form evidence-backed hypotheses.
6. Design targeted interventions.
7. Run experiments that confirm or reject those interventions.

## Required Build

Learners create an Agent Failure Report for Acme Expense Agent v1 using the Level 2 benchmark.

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
| 6 | Reporting diagnosis | Failure report |

## Labs

| Lab | Description |
| --- | --- |
| [Lab 1: Trace Annotation](labs/lab-01-trace-annotation.md) | Annotate failed trajectories from Level 2. |
| [Lab 2: Failure Taxonomy](labs/lab-02-failure-taxonomy.md) | Create a taxonomy and label set. |
| [Lab 3: Intervention Experiment](labs/lab-03-intervention-experiment.md) | Test a targeted fix against the benchmark. |
| [Lab 4: Failure Report](labs/lab-04-failure-report.md) | Write an evidence-backed diagnostic report. |

## Project

The Level 3 project is [Acme Expense Agent Failure Report v1](project/acme-expense-agent-failure-report-v1.md).

## Exit Criteria

To complete Level 3, the learner must submit:

1. At least 30 annotated failed traces.
2. A failure taxonomy with examples.
3. Aggregate failure counts by category.
4. At least three evidence-backed hypotheses.
5. At least one tested intervention.
6. A failure report with recommendations for Level 4 data work.

