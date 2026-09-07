# Lesson 3: Cleaning and Deduplication

## Core Idea

More data is not automatically better data.

## Filters

Filter out examples with:

- malformed JSON
- missing provenance
- private or secret data
- duplicate tasks
- invalid target outputs
- unclear corrections
- low-quality synthetic generations

## Deduplication

Deduplicate by:

- exact text match
- normalized task text
- semantic similarity
- shared source trace

## Common Failure Modes

- Removing duplicates without recording what was rejected.
- Keeping rows with missing provenance.
- Deduplicating only by id when prompt and target are duplicated.

## Exercise

Why does the Phase 4 builder write `rejected.jsonl`?

Check your answer:

```text
So reviewers can inspect filtered rows and confirm the cleaner removed duplicates, missing provenance, and invalid target contracts.
```

Use the StrongBench training dataset to confirm the answer against the data workflow rather than relying on memory.

## Checkpoint

You are ready to move on when you can explain why each removed row was removed.
