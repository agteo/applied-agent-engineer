# RL Experiment Plan

## Question

Can experience in the StrongBench Finance simulator improve policy reliability without increasing unsafe actions?

## Baselines

- `scripted_reference`: deterministic sanity-check policy.
- `weak_submitter`: deliberately unsafe policy for negative-control rollouts.

## Training Path

Hosted RL or local policy optimization is optional. A real training run must save training logs, reward curves, sampled rollouts, and post-training benchmark results.

## Decision Rule

A trained policy is better only if heldout simulator success improves, unsafe submission failures do not increase, and the Level 2 benchmark does not regress.

## Current Offline Result

This bundle contains 360 accepted rollouts and no trained-policy result. It is ready for experiment design, not adoption.
