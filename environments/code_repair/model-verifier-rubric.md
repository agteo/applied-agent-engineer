# Code Repair Model-Based Verifier Rubric v1

This reference verifier is deterministic and offline. It stands in for an LLM judge so CI can exercise the model-based verifier contract without a network call.

## Inputs

- task expected changed file
- trace evidence for file reads, test runs, and static checks
- final-answer summary
- final-answer changed-file list and test status

## Rubric

- `0.25` answer describes the repair.
- `0.25` answer mentions test evidence that appears in the trace.
- `0.20` answer mentions static or syntax evidence that appears in the trace.
- `0.20` answer names the expected changed file.
- `0.10` answer reports passing tests only after the target file was read and tests actually passed.

Pass threshold: `0.80`.

The point is not that keyword matching is a good model judge. The point is that model-based verification has an explicit input contract, rubric, score, threshold, and recorded reasons.
