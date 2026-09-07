# Lesson 2: Schemas and Formats

## Core Idea

Datasets need contracts just like tools do.

## Recommended Formats

- JSONL for examples and traces
- Parquet for larger structured datasets
- Markdown for dataset cards
- YAML or JSON for manifests

## Example Fields

- example id
- source trace id
- task
- input messages
- target output
- tool calls
- failure label
- quality score
- split
- provenance

## Common Failure Modes

- Adding rows whose shape changes silently across files.
- Putting important fields inside unstructured text.
- Versioning the dataset card but not the row schema.

## Exercise

Name four fields every StrongBench dataset row needs.

Check your answer:

```text
`schema_version`, `example_id`, `messages`, `target_final_answer`, plus provenance and split fields for training discipline.
```

Use the StrongBench training dataset to confirm the answer against the data workflow rather than relying on memory.

## Checkpoint

You are ready to move on when every row has a documented schema and provenance field.
