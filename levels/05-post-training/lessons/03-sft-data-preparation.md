# Lesson 3: SFT Data Preparation

## Core Idea

Supervised fine-tuning teaches a model to imitate target outputs for given inputs.

## Data Shape

Use chat-style examples:

```json
{
  "messages": [
    { "role": "system", "content": "You are Acme Expense Agent." },
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

## Checkpoint

You are ready to move on when every training example has a validated target answer.

