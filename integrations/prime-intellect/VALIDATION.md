# Validation Note: Prime CLI And Account Differences

Read this before treating anything under `integrations/prime-intellect/` as a
working hosted path.

## What is validated

- The adapter loads, serves 120 tasks, rolls out two policies, and scores them
  with the local verifiers. This runs in CI on every push:

  ```bash
  python3 integrations/prime-intellect/environments/acme_finance_reliability/acme_finance_reliability.py
  ```

- The reward separates the reference policy from the reward-hacking probe.

## What is NOT validated

- `load_verifiers_environment()`. No hosted run has exercised it. The
  `verifiers` package API is not pinned by this repo, and the wrapper is
  written against the `SingleTurnEnv` + `Rubric` shape. Expect to adjust it.
- The `configs/` TOML files. They record intent — environment id, policy,
  method, task distribution. They are not a schema this repo can verify,
  because the Prime CLI validates its own config format server-side.
- Anything about cost, quota, or throughput.

## Differences you will hit

| Area | What varies | What to do |
| --- | --- | --- |
| CLI version | Config keys and subcommand names move between releases | Run `prime --version` and record it in your run report |
| Account tier | Available GPU types, max concurrent jobs, and queue time | Check quota before sizing the smoke run |
| Environment registry | Whether a custom environment must be published before it can be referenced by id | Publish from `environments/acme_finance_reliability/` and use the returned id |
| Auth | API key vs. browser login, and per-org scoping | Never commit a key; use the CLI's own credential store |
| Reward reporting | Hosted trainers may expect a scalar, not a component dict | Send `reward["total"]`; keep `reward["components"]` in your own logs |

## The rule this repo does not bend

A hosted run produces a claim only when it ships baseline eval, training logs,
reward-component curves, held-out simulator eval, a Level 2 benchmark
regression check, and a sampled rollout review. Reward going up is not a
result. See `reports/template.md`.
