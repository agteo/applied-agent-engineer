# Acme RL Reliability Report

## Decision

Do not claim RL improvement yet. The local simulator and reward analysis are executable, but no training run has been performed.

## Evidence

- scripted_reference success_rate: 1.000
- scripted_reference average_reward: 1.750
- weak_submitter success_rate: 0.000
- weak_submitter unsafe_submission_failures: 120
- accepted rollouts: 240
- rejected rollouts: 0

## Interpretation

The reward function separates correct workflow completion from unsafe shortcut behavior. The next valid step is a smoke training run or a hosted-adapter evaluation, followed by heldout simulator and Level 2 benchmark checks.
