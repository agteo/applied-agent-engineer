# StrongBench RL Reliability Report

## Decision

Do not claim RL improvement yet. The local simulator, the adapter, and the reward analysis are executable, but no training run has been performed.

## Evidence

| Policy | Rollouts | Success rate | Average reward | Unsafe submissions | Distinct rewards |
| --- | ---: | ---: | ---: | ---: | ---: |
| reward_hacker | 120 | 0.000 | -0.815 | 19 | 4 |
| scripted_reference | 120 | 1.000 | 1.900 | 0 | 1 |
| weak_submitter | 120 | 0.000 | -1.627 | 120 | 4 |

- accepted rollouts: 360
- rejected rollouts: 0

## Interpretation

The reward separates correct workflow completion from two different failure shapes: an unsafe submitter and a reward hacker that produces correct-looking answers without reading anything.

## What this rollout set cannot do

Across every policy there are 9 distinct reward values in total, and each policy is close to constant within itself. Advantage estimation needs spread inside a policy's own rollouts, so this set is a verifier and reward regression suite, not training data. Generating training data means sampling a stochastic policy, not replaying scripted ones.

The next valid step is a smoke training run or a hosted-adapter evaluation, followed by heldout simulator and Level 2 benchmark checks.
