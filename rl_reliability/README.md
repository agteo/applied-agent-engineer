# RL Reliability

This folder contains the executable Level 7 local analysis path.

Build the Acme RL reliability bundle:

```bash
python3 -m rl_reliability.acme
```

The command consumes the Level 6 Acme Finance simulator rollouts and writes:

```text
rl_reliability/
  acme/
    rl-rollouts.jsonl
    rl-rollouts-rejected.jsonl
    rollout-schema.json
    metrics.json
    mdp-framing.md
    reward-hacking-review.md
    experiment-plan.md
    experiment-report.md
    prime-eval-template.toml
    prime-rl-smoke-template.toml
    hosted-rl-report-template.md
```

It also writes Prime Intellect adapter templates under
`integrations/prime-intellect/`.

This is not a claim that RL training has improved the agent. It is the local
analysis and experiment-design path: rollouts, rewards, failure controls,
reward-hacking review, and the evidence gate required before a hosted or local
training run can count.
