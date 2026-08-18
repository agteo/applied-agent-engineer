# Lab 3: Policy Search

## Objective

Ground agent answers in a local policy corpus.

## Build

Create a small expense policy corpus with at least five sections:

1. meals
2. travel
3. lodging
4. missing receipts
5. manager approval

Implement `search_policy(query)` over the corpus.

The first version can use keyword search. A stretch version can use embeddings.

## Required Output

The tool should return policy snippets with source ids:

```json
{
  "results": [
    {
      "source_id": "policy-meals-001",
      "title": "Meals",
      "text": "Dinner while traveling is reimbursable up to the daily meal limit.",
      "score": 0.82
    }
  ]
}
```

## Test Tasks

Use at least these tasks:

1. "Can I reimburse dinner during business travel?"
2. "What happens if I lost a hotel receipt?"
3. "Which expenses need manager approval?"

## Deliverable

Submit:

- policy fixture data
- search tool implementation
- three traces with policy citations
- a note describing known search limitations

## Checks

The lab passes if final answers cite retrieved policy source ids and do not invent policy details that were not retrieved.

## Reference Solution

Write your own version first, then compare: [`solutions/lab_03_policy_search.py`](../../../examples/acme-expense-agent/solutions/lab_03_policy_search.py).

```bash
cd examples/acme-expense-agent
python solutions/lab_03_policy_search.py
```

The corpus is `fixtures/policies.json`. Write your own limitations list before reading the one it prints. [How to compare](../../../examples/acme-expense-agent/solutions/README.md).
