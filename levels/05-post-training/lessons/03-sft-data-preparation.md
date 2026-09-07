# Lesson 3: SFT Data Preparation

## Core Idea

Supervised fine-tuning teaches a model to imitate target outputs for given inputs.

## Data Shape

Use chat-style examples:

```json
{
  "messages": [
    { "role": "system", "content": "You are StrongBench Expense Agent." },
    { "role": "user", "content": "I lost my hotel receipt. Can I submit it?" },
    { "role": "assistant", "content": "..." }
  ]
}
```

## Quality Checks

- target answer is correct
- policy citations are valid
- no held-out eval leakage
- no private data
- consistent style and schema

## Common Failure Modes

- Including heldout rows in the training export.
- Serializing assistant targets in a format the serving stack will not use.
- Dropping provenance during conversion.

## Exercise

Which splits should appear in the Phase 5 SFT export?

Check your answer:

```text
`train` and `dev` only. `heldout` rows should be rejected from SFT export and preserved for evaluation.
```

Use the Phase 5 decision memo to confirm the answer against the model-improvement workflow rather than relying on memory.

## Checkpoint

You are ready to move on when every training example has a validated target answer.
