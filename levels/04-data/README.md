# Level 4: Data and Feedback

## Goal

Turn agent traces, failures, human corrections, and synthetic examples into a defensible dataset for improvement.

Level 3 asked: why did the agent fail?

Level 4 asks: what data would help it improve?

## Learning Outcomes

By the end of this level, learners can:

1. Design schemas for agent training and evaluation data.
2. Clean and deduplicate messy traces.
3. Convert failures into demonstrations, corrections, and preference examples.
4. Generate synthetic examples with quality filters.
5. Separate training, development, and evaluation data.
6. Document dataset provenance, limitations, and quality metrics.
7. Publish a dataset card.

## Pipeline

```text
Production traces
      +
Eval failures
      +
Human examples
      +
Synthetic examples
      |
      v
Clean -> Classify -> Deduplicate -> Filter -> Score -> Dataset
```

## Module Plan

Read the full lesson sequence in [lessons/README.md](lessons/README.md).

| Lesson | Topic | Artifact |
| --- | --- | --- |
| 1 | Agent data types | Data inventory |
| 2 | Schemas and formats | JSONL schema |
| 3 | Cleaning and deduplication | Cleaned dataset |
| 4 | Synthetic data | Generated examples |
| 5 | Preference and correction data | Preference pairs |
| 6 | Splits and contamination | Split manifest |
| 7 | Dataset cards | Dataset card |

## Labs

| Lab | Description |
| --- | --- |
| [Lab 1: Trace to Dataset](labs/lab-01-trace-to-dataset.md) | Convert traces into structured examples. |
| [Lab 2: Cleaning Filters](labs/lab-02-cleaning-filters.md) | Deduplicate and filter low-quality rows. |
| [Lab 3: Synthetic Examples](labs/lab-03-synthetic-examples.md) | Generate examples from diagnosed failures. |
| [Lab 4: Dataset Card](labs/lab-04-dataset-card.md) | Document the dataset for future training. |

## Project

The Level 4 project is [Agent Training Dataset v1](project/agent-training-dataset-v1.md).

## Exit Criteria

To complete Level 4, the learner must submit:

1. A dataset schema.
2. A raw data inventory.
3. A cleaned and filtered dataset.
4. Training, development, and held-out splits.
5. Quality metrics.
6. Provenance documentation.
7. A dataset card.

