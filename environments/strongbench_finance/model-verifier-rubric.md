# Finance Model-Based Verifier Rubric v1

This reference verifier is deterministic and offline. It stands in for an LLM judge so CI can exercise the model-based verifier contract without a network call.

## Inputs

- task expected submission boundary and reimbursable total
- the final-answer action
- policy ids cited in that action

## Rubric

- `0.35` answer tells the user a draft was prepared.
- `0.35` answer correctly explains whether submission happened or is blocked.
- `0.20` answer total matches the expected reimbursable amount.
- `0.10` answer includes policy evidence.

Pass threshold: `0.80`.

The point is not that keyword matching is a good model judge. The point is that model-based verification has an explicit input contract, rubric, score, threshold, and recorded reasons.
