# Level 7: RL for Agent Reliability

## Goal

Analyze whether and how an agent could improve through experience using environment rollouts, verifier-derived rewards, and reproducible experiments.

Level 6 asked: can we create a world where the agent can practice?

Level 7 asks: can experience improve behavior, and how would we know?

## Scope

Level 7 now has an executable local analysis path over the Acme Finance
Operations Simulator. Running RL training is still an optional advanced
implementation path, not a default course completion requirement.

## Learning Outcomes

By the end of this level, learners can:

1. Explain the reinforcement learning framing for agent tasks.
2. Distinguish offline, online, and environment-based learning.
3. Design rewards from deterministic, state, constraint, and model-based verifiers.
4. Generate and filter rollouts.
5. Understand RLHF, RLVR, PPO, and GRPO conceptually.
6. Produce a rigorous training experiment design.
7. Evaluate any trained agent against the same benchmark used earlier.
8. Analyze learning curves and failure modes after training.

## Required Build

Learners use the simulator from Level 6 to generate or inspect rollouts and design an experiment that could test whether training through experience improves the agent.

Prime Intellect / Verifiers is the proposed hosted RL adapter once the local simulator and verifier contracts are real. The local analysis path remains valid without hosted training.

Build the reference RL reliability bundle:

```bash
python3 -m rl_reliability.acme
```

## Training Loop

```text
Model
  |
  v
Rollout in environment
  |
  v
Verifier components, reward, and trajectory
  |
  v
Training update
  |
  v
Updated model or policy
  |
  v
Benchmark and diagnosis
```

## Module Plan

Read the full lesson sequence in [lessons/README.md](lessons/README.md).

| Lesson | Topic | Artifact |
| --- | --- | --- |
| 1 | RL framing | MDP sketch |
| 2 | Verifiers, rewards, and reward hacking | Reward risk review |
| 3 | Rollouts and filtering | Rollout dataset |
| 4 | RLHF and RLVR | Concept map |
| 5 | PPO, GRPO, and hosted RL adapters | Training plan |
| 6 | Training experiments | Experiment record |
| 7 | Post-RL evaluation | Final comparison report |

## Labs

| Lab | Description |
| --- | --- |
| [Lab 1: MDP Framing](labs/lab-01-mdp-framing.md) | Frame Acme tasks as states, actions, verifier outputs, rewards, and policies. |
| [Lab 2: Rollout Dataset](labs/lab-02-rollout-dataset.md) | Generate and filter environment rollouts. |
| [Lab 3: Reward Hacking Review](labs/lab-03-reward-hacking-review.md) | Identify reward exploits before training. |
| [Lab 4: RL Experiment Report](labs/lab-04-rl-experiment-report.md) | Report whether experience improved behavior. |

## Project

The Level 7 project is [Train an Agent Through Experience](project/train-agent-through-experience.md). The reference implementation is in
[`rl_reliability/acme/`](../../rl_reliability/acme/). It provides the local
analysis bundle and Prime adapter templates; a completed training claim still
requires real training logs, learning curves, sampled rollouts, and benchmark
comparison.

## Exit Criteria

To complete Level 7, the learner must submit:

1. An RL framing of the Acme environment.
2. Rollout data with rewards and termination reasons.
3. Verifier and reward hacking risk analysis.
4. A rigorous experiment design.
5. Learning curves and training logs if optional training is run.
6. Evaluation against the Level 2 benchmark.
7. Failure analysis comparing pre-training and post-training behavior.
