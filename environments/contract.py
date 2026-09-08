"""Shared environment contract checks for Level 6 and Workstream D."""

from __future__ import annotations

from pathlib import Path
from types import ModuleType
from typing import Any


REQUIRED_FUNCTIONS = [
    "build_environment_bundle",
    "generate_tasks",
    "run_scripted_policy",
    "run_reward_hacking_policy",
    "verify_rollout",
    "score_reward",
    "write_environment_bundle",
]

REQUIRED_BUNDLE_KEYS = {
    "manifest",
    "initial_state",
    "state_schema",
    "tool_schemas",
    "tasks",
    "rollouts",
    "probe_rollouts",
    "metrics",
    "reward_design",
    "verifier_report",
}


def validate_environment_module(module: ModuleType, task_count: int = 6) -> dict[str, Any]:
    missing_functions = [name for name in REQUIRED_FUNCTIONS if not callable(getattr(module, name, None))]
    if missing_functions:
        raise AssertionError(f"{module.__name__} missing functions: {missing_functions}")

    bundle = module.build_environment_bundle(seed=42, task_count=task_count)
    missing_keys = sorted(REQUIRED_BUNDLE_KEYS - set(bundle))
    if missing_keys:
        raise AssertionError(f"{module.__name__} bundle missing keys: {missing_keys}")

    tasks = bundle["tasks"]
    rollouts = bundle["rollouts"]
    probes = bundle["probe_rollouts"]
    if len(tasks) != task_count:
        raise AssertionError(f"{module.__name__} returned {len(tasks)} tasks, expected {task_count}")
    if len(rollouts) != task_count or len(probes) != task_count:
        raise AssertionError(f"{module.__name__} did not emit one rollout and probe per task")
    if not all(row["verifier"]["passed"] for row in rollouts):
        raise AssertionError(f"{module.__name__} scripted policy did not pass every task")
    if not all(not row["verifier"]["passed"] for row in probes):
        raise AssertionError(f"{module.__name__} reward-hacking probe was not caught")
    if set(bundle["metrics"]["verifier_types"]) != {"deterministic", "state", "constraint"}:
        raise AssertionError(f"{module.__name__} verifier types drifted")
    return bundle["metrics"]


def write_validated_environment(module: ModuleType, out: Path, task_count: int | None = None) -> dict[str, Any]:
    kwargs = {"seed": 42}
    if task_count is not None:
        kwargs["task_count"] = task_count
    bundle = module.build_environment_bundle(**kwargs)
    module.write_environment_bundle(bundle, out)
    validate_environment_module(module, task_count=len(bundle["tasks"]))
    return bundle["metrics"]
