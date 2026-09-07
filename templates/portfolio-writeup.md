# Portfolio Writeup Template

Use this format for a public or interview-facing project summary. Keep it short
enough that a hiring manager can read it in ten minutes and technical enough
that an engineer can verify the claim.

## Title

`<system or track>: <measured improvement or decision>`

## One-Sentence Claim

State the outcome in one sentence. Include the measurement, not just the work
performed.

Example: `I built a deterministic eval gate for an expense agent and used it to
hold release until receipt-lookup and approval failures were diagnosed.`

## Problem

What workflow did the system support? What could go wrong if the agent behaved
incorrectly?

## Measurement

What benchmark, verifier, dataset, or rollout set did you use?

Include:

- command or reproducible entrypoint
- task count or row count
- success metric
- safety or regression slice
- threshold or decision rule

## Diagnosis

What failed, and how did you know?

Name the trace, failure label, slice, row, or reward component that supports the
diagnosis.

## Intervention Or Decision

What did you change, recommend, reject, or design?

Be explicit when the right decision was *not* to train, ship, or deploy.

## Evidence

Summarize before/after results or the current measured state.

Use a table when comparison matters:

| Candidate | Evidence | Decision |
| --- | --- | --- |
| Baseline | `<metric>` | `<ship/hold/defer>` |
| Intervention | `<metric>` | `<ship/hold/defer>` |

## Differentiating Choice

Name the part of the project you chose yourself:

- your own failure mode
- your own task family
- your own domain port
- your own verifier or reward component
- your own model or serving comparison

If this section could match every other learner, the portfolio piece is not
finished.

## What I Would Do Next

List the next one or two improvements, including the measurement you would use
to decide whether they worked.

## Links

Link to the relevant tracked artifacts:

- benchmark or rollout report
- failure analysis
- dataset card
- model decision memo
- reward design
- code entrypoint
