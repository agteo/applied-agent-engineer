# Good Model Improvement Decision: Acme Expense Agent v1

## Decision

Do not fine-tune yet. Fix retrieval/tool arguments and add regression tests
before spending GPU time.

## Evidence

- Current benchmark: 89/100 with the scripted baseline.
- Dominant failures: receipt lookup, policy-boundary interpretation, and
  approval-gated submission behavior.
- Dataset readiness: Level 4 now provides 78 train, 47 dev, and 27 heldout
  examples, but much of the new data targets tool-use and policy-routing gaps.

## Rationale

The largest failures are not obviously language-model knowledge gaps. They are
workflow and evidence-selection gaps. Fine-tuning on corrected final answers
could make the output shape look better while the agent still calls the wrong
tool arguments.

## Next Step

Change the receipt lookup planner, add regression cases from
`evals/operations/acme/regression-pack.jsonl`, and rerun the Level 2 benchmark.
Only consider SFT after the tool behavior plateaus and the remaining failures
look like answer-generation errors.

## Why This Is Good

This memo makes a decision, cites benchmark and dataset evidence, rejects a
popular but unjustified intervention, and names the next experiment.
