# Environments

This folder contains simulated environments where agents can practice safely.

Build the Level 6 Acme Finance Operations Simulator:

```bash
python3 -m environments.acme_finance
```

The command generates:

```text
environments/
  acme_finance/
    manifest.json
    state-schema.json
    initial-state.json
    tool-schemas.json
    tasks.jsonl
    rollouts.jsonl
    metrics.json
    reward-design.md
    verifier-report.md
    simulator-bias-note.md
```

The first version has 120 deterministic expense tasks, six simulated tools,
deterministic/state/constraint verifiers, reward components, and rollout logs.

Start with [../levels/06-environments/README.md](../levels/06-environments/README.md).
Level 7 uses these environments for rollout-based learning. See [../levels/07-reinforcement-learning/README.md](../levels/07-reinforcement-learning/README.md).
