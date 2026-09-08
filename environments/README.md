# Environments

This folder contains simulated environments where agents can practice safely.

Build the Level 6 StrongBench Finance Operations Simulator:

```bash
python3 -m environments.strongbench_finance
```

The command generates:

```text
environments/
  strongbench_finance/
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
deterministic/state/constraint/model-based verifiers, reward components, and
rollout logs.

Build the Workstream D code-repair transfer environment:

```bash
python3 -m environments.code_repair
```

The command generates:

```text
environments/
  code_repair/
    manifest.json
    state-schema.json
    initial-state.json
    tool-schemas.json
    tasks.jsonl
    rollouts.jsonl
    probe-rollouts.jsonl
    metrics.json
    reward-design.md
    verifier-report.md
    transfer-note.md
```

The code-repair environment has 60 deterministic repair tasks, five simulated
tools, deterministic/state/constraint/model-based verifiers, reward components,
rollout logs, and a reward-hacking probe that claims tests passed without
recorded test evidence.

Both environments implement the shared contract checked by
[`contract.py`](contract.py). The domain-agnostic runner can build any module
with that interface:

```bash
python3 -m environments.runner environments.code_repair --out /tmp/code-repair-contract --tasks 12
```

Start with [../levels/06-environments/README.md](../levels/06-environments/README.md).
Level 7 uses these environments for rollout-based learning. See [../levels/07-reinforcement-learning/README.md](../levels/07-reinforcement-learning/README.md).
