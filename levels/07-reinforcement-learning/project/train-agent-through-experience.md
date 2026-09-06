# Project: Train an Agent Through Experience

## Objective

Use Acme Finance Operations Simulator to test whether environment experience improves Acme agent reliability.

Current maturity note: this is an analysis project. The repo includes a local RL
literacy bundle and a Prime Intellect adapter you can load offline. No training
run has been performed here, and a completed RL training claim still requires
actual training logs, learning curves, sampled rollouts, and benchmark
comparison.

## Required Inputs

- Acme Finance Operations Simulator v1
- verifier-derived reward function
- rollout dataset
- baseline agent
- Level 2 benchmark
- Level 3 failure taxonomy

## Required Outputs

- RL framing: [`rl_reliability/acme/mdp-framing.md`](../../../rl_reliability/acme/mdp-framing.md)
- rollout dataset: [`rl_reliability/acme/rl-rollouts.jsonl`](../../../rl_reliability/acme/rl-rollouts.jsonl)
- verifier and reward hacking review: [`rl_reliability/acme/reward-hacking-review.md`](../../../rl_reliability/acme/reward-hacking-review.md)
- experiment plan: [`rl_reliability/acme/experiment-plan.md`](../../../rl_reliability/acme/experiment-plan.md)
- local experiment report: [`rl_reliability/acme/experiment-report.md`](../../../rl_reliability/acme/experiment-report.md)
- hosted training report template: [`rl_reliability/acme/hosted-rl-report-template.md`](../../../rl_reliability/acme/hosted-rl-report-template.md)
- Prime eval template: [`rl_reliability/acme/prime-eval-template.toml`](../../../rl_reliability/acme/prime-eval-template.toml)
- Prime RL smoke template: [`rl_reliability/acme/prime-rl-smoke-template.toml`](../../../rl_reliability/acme/prime-rl-smoke-template.toml)
- Prime RL small-experiment template: [`rl_reliability/acme/prime-rl-small-template.toml`](../../../rl_reliability/acme/prime-rl-small-template.toml)
- Prime adapter, loadable offline: [`integrations/prime-intellect/environments/acme_finance_reliability/`](../../../integrations/prime-intellect/environments/acme_finance_reliability/)
- what the hosted path does not validate: [`integrations/prime-intellect/VALIDATION.md`](../../../integrations/prime-intellect/VALIDATION.md)
- learning curves if training is run
- benchmark comparison if training is run
- post-training failure analysis if training is run

Build the reference bundle:

```bash
python3 -m rl_reliability.acme
```

## Assessment Anchor

Compare your reward and reward-hacking review against the reward-design
examples and rubric in
[`examples/reference-artifacts/reward-design/`](../../../examples/reference-artifacts/reward-design/).

## Submission Checklist

- [ ] Environment version documented.
- [ ] Verifier version documented.
- [ ] Reward version documented.
- [ ] Rollout data collected and filtered.
- [ ] Training method documented as a design, with its decision rule.
- [ ] Reward hacking review names an exploit the current verifiers miss.
- [ ] Critique of a training result you did not produce.
- [ ] If training was actually run: evaluation uses the Level 2 benchmark,
      failure analysis uses the Level 3 taxonomy, and the recommendation
      explains whether experience improved behavior.
