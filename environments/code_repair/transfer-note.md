# Domain Transfer Note

Workstream D ports the Level 6 verifier pattern from finance operations to code repair.

## What Carried Over

- The environment emits the same artifact family: manifest, state schema, tools, tasks, rollouts, probe rollouts, metrics, reward design, and verifier report.
- The verifier still combines deterministic, state, constraint, contract, and safety checks.
- Reward components still come from verifier evidence, not from a model's final-answer prose.
- A negative-control policy proves the verifier catches a plausible shortcut.

## What Changed

- Finance state records became repository files, patch records, test runs, static checks, and final answers.
- Receipts and policy citations became source reads, changed files, unit/regression test evidence, and static-check evidence.
- Unauthorized submission became fabricated test claims: saying the gate passed when the simulator never recorded it.

## Interface Pressure

The finance simulator and the code-repair simulator now expose matching build, rollout, verifier, reward, and artifact-writing functions. The next extraction should be a small shared runner that imports any environment module by name and checks this contract before CI calls domain-specific commands.

This build generated 60 code-repair tasks and caught 60 reward-hacking probes.
