# Project: Train an Agent Through Experience

## Objective

Use Acme Finance Operations Simulator to test whether environment experience improves Acme agent reliability.

Current maturity note: until the simulator, rollout runner, and training scripts exist, this project should be treated as an analysis and experiment-design project. A completed RL training claim requires actual training logs, learning curves, and benchmark comparison.

## Required Inputs

- Acme Finance Operations Simulator v1
- verifier-derived reward function
- rollout dataset
- baseline agent
- Level 2 benchmark
- Level 3 failure taxonomy

## Required Outputs

- RL framing
- rollout dataset
- verifier and reward hacking review
- experiment plan
- learning curves if training is run
- benchmark comparison
- post-training failure analysis

## Assessment Anchor

Compare your reward and reward-hacking review against the reward-design
examples and rubric in
[`examples/reference-artifacts/reward-design/`](../../../examples/reference-artifacts/reward-design/).

## Submission Checklist

- [ ] Environment version documented.
- [ ] Verifier version documented.
- [ ] Reward version documented.
- [ ] Rollout data collected and filtered.
- [ ] Training method documented.
- [ ] Evaluation uses Level 2 benchmark.
- [ ] Failure analysis uses Level 3 taxonomy.
- [ ] Recommendation explains whether experience improved behavior.
