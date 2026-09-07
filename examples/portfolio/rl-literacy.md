# RL Literacy: Reward Analysis Without A Training Claim

## One-Sentence Claim

I framed StrongBench simulator rollouts as an RL reliability problem and showed why
reward improvement alone is not enough to claim agent improvement.

## Problem

RL results can look convincing when reward rises, even if the policy learned an
unsafe shortcut. For workflow agents, the evidence must include verifier
components, unsafe-action rates, heldout evaluation, and benchmark regression
checks.

## Measurement

- RL analysis command: `python3 -m rl_reliability.strongbench`
- accepted rollouts: 240
- scripted reference: 120 rollouts, 1.000 success rate
- weak submitter: 120 rollouts, 0.000 success rate
- weak submitter unsafe submission failures: 120

## Diagnosis

The weak submitter tries to reach terminal states by submitting as the agent and
skipping approval constraints. The reward and verifier breakdown catches this:
unsafe submission penalties fire on every weak-policy rollout.

## Intervention Or Decision

Do not claim RL improvement yet. The repo provides an executable local analysis
path and hosted templates, but a real training claim needs logs, reward curves,
sampled rollout review, heldout simulator evaluation, and Level 2 benchmark
regression checks.

## Evidence

| Policy | Success Rate | Unsafe Submission Failures | Decision |
| --- | ---: | ---: | --- |
| `scripted_reference` | 1.000 | 0 | sanity-check baseline |
| `weak_submitter` | 0.000 | 120 | reject; reward-hacking control |

## Differentiating Choice

I would add a refusal-overuse policy as a second negative control, because an
agent can avoid unsafe submissions by refusing tasks it should complete.

## What I Would Do Next

Run a smoke training experiment only after freezing a heldout simulator task
set, then compare reward curves against unsafe-action rate and the Level 2
benchmark.

## Links

- [`rl_reliability/strongbench/experiment-report.md`](../../rl_reliability/strongbench/experiment-report.md)
- [`rl_reliability/strongbench/reward-hacking-review.md`](../../rl_reliability/strongbench/reward-hacking-review.md)
- [`rl_reliability/strongbench/mdp-framing.md`](../../rl_reliability/strongbench/mdp-framing.md)
- [`integrations/prime-intellect/reports/template.md`](../../integrations/prime-intellect/reports/template.md)
