# Acme Expense Agent Failure Report v1

## Executive Summary

- scripted baseline: 89/100 tasks passed
- weak no-tool baseline: 0/30 tasks passed on the calibration slice
- annotated failures: 30
- release recommendation: hold changes that reduce benchmark success or increase submission-gate failures

## Failure Distribution

| Label | Count |
| --- | ---: |
| MODEL.instruction_following | 4 |
| MODEL.reasoning | 9 |
| RETRIEVAL.citation | 20 |
| TOOLS.arguments | 7 |
| TOOLS.interpretation | 3 |
| TOOLS.selection | 19 |

## Dominant Hypotheses

- 19x: The model is answering from the prompt without using the evidence-producing tools required by policy.
- 7x: Receipt lookup is under-specified, so the agent retrieves the wrong receipt set before calculating.
- 2x: The agent does not reliably preserve approval and submission boundaries in the final answer.
- 1x: The item parser is losing category/date context before the reimbursement calculator runs.
- 1x: The benchmark exposed an ambiguity that needs trace review before changing the agent.

## Recommended Interventions

1. Fix receipt lookup argument extraction before expanding receipt-heavy tasks.
2. Add parser tests for room service and same-day meal limits.
3. Add prepare-vs-submit examples to preserve the employee submission gate.
4. Promote the regression pack into the Level 2 benchmark after each fix lands.

## Level 4 Data Recommendation

Use the annotated failures as seed data for correction examples: original prompt, bad trace evidence, corrected tool plan, corrected final answer, and failure label.
