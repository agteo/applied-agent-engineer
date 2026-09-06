"""Prime Intellect / Verifiers adapter over the local Acme Finance simulator.

The local simulator and its verifiers are the source of truth. This module is an
adapter: it exposes the same tasks, the same state transitions, and the same
verifier-derived reward through a Verifiers-shaped surface, and adds no scoring
logic of its own.

Two entry points:

- `load_environment()` returns a plain-Python environment object that works with
  no third-party dependencies. Everything in this repo's CI uses this path.
- `load_verifiers_environment()` wraps the same object for the `verifiers`
  package when it is installed. That binding is UNVALIDATED against a live Prime
  account — see `../../VALIDATION.md` before trusting it.

Run the offline smoke check:

    python3 integrations/prime-intellect/environments/acme_finance_reliability/acme_finance_reliability.py
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Callable
import json
import sys

# The adapter lives outside the package tree, so make the repo root importable
# when this file is executed directly.
ROOT = Path(__file__).resolve().parents[4]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from environments.acme_finance import (  # noqa: E402
    build_environment_bundle,
    initial_state,
    run_reward_hacking_policy,
    run_scripted_policy,
    score_reward,
    verify_rollout,
)

ENVIRONMENT_ID = "acme_finance_reliability"
ENVIRONMENT_VERSION = "0.1.0"

# Policies the adapter can roll out. Anything hosted training plugs in replaces
# the callable, not the reward.
BUILTIN_POLICIES: dict[str, Callable[[dict[str, Any], dict[str, Any]], dict[str, Any]]] = {
    "scripted_reference": run_scripted_policy,
    "reward_hacker": run_reward_hacking_policy,
}


class AcmeFinanceReliabilityEnv:
    """A task set, a step function, and a verifier-derived reward.

    This is deliberately small. The environment does not know what a trainer is;
    it hands out tasks and scores rollouts.
    """

    id = ENVIRONMENT_ID
    version = ENVIRONMENT_VERSION

    def __init__(self, seed: int = 42, task_count: int = 120):
        self.seed = seed
        bundle = build_environment_bundle(seed=seed, task_count=task_count)
        self.tasks: list[dict[str, Any]] = bundle["tasks"]
        self.base_state: dict[str, Any] = bundle["initial_state"]
        self.tool_schemas: list[dict[str, Any]] = bundle["tool_schemas"]
        self.state_schema: dict[str, Any] = bundle["state_schema"]

    # -- dataset ---------------------------------------------------------

    def dataset(self) -> list[dict[str, Any]]:
        """Prompt/answer pairs in the shape most RL harnesses expect."""
        return [
            {
                "id": task["id"],
                "prompt": task["prompt"],
                "info": {
                    "actor": task["actor"],
                    "employee_id": task["employee_id"],
                    "receipt_ids": task["receipt_ids"],
                    "tools": [schema["name"] for schema in self.tool_schemas],
                },
                # The expected block is the grading key. A policy must never be
                # given this at rollout time.
                "answer": task["expected"],
            }
            for task in self.tasks
        ]

    def task(self, task_id: str) -> dict[str, Any]:
        for task in self.tasks:
            if task["id"] == task_id:
                return task
        raise KeyError(f"unknown task: {task_id}")

    # -- rollout and scoring ---------------------------------------------

    def rollout(self, task_id: str, policy: str | Callable = "scripted_reference") -> dict[str, Any]:
        task = self.task(task_id)
        fn = BUILTIN_POLICIES[policy] if isinstance(policy, str) else policy
        return fn(task, self.base_state)

    def score(self, task_id: str, observations: list[dict[str, Any]], terminal_state: dict[str, Any]) -> dict[str, Any]:
        """Score an externally produced rollout with the local verifiers."""
        task = self.task(task_id)
        verifier = verify_rollout(task, terminal_state, observations)
        return {"verifier": verifier, "reward": score_reward(verifier, observations)}

    def reward(self, task_id: str, observations: list[dict[str, Any]], terminal_state: dict[str, Any]) -> float:
        return self.score(task_id, observations, terminal_state)["reward"]["total"]

    # -- evaluation ------------------------------------------------------

    def evaluate(self, policy: str | Callable = "scripted_reference") -> dict[str, Any]:
        rollouts = [self.rollout(task["id"], policy) for task in self.tasks]
        passed = sum(1 for row in rollouts if row["verifier"]["passed"])
        rewards = [row["reward"]["total"] for row in rollouts]
        unsafe = sum(
            1 for row in rollouts if not row["verifier"]["checks"]["safety_no_unauthorized_submission"]
        )
        return {
            "environment": self.id,
            "version": self.version,
            "policy": policy if isinstance(policy, str) else getattr(policy, "__name__", "callable"),
            "rollouts": len(rollouts),
            "passed": passed,
            "success_rate": round(passed / len(rollouts), 3) if rollouts else 0.0,
            "average_reward": round(sum(rewards) / len(rewards), 3) if rewards else 0.0,
            "unsafe_submission_failures": unsafe,
        }


def load_environment(seed: int = 42, task_count: int = 120) -> AcmeFinanceReliabilityEnv:
    """Dependency-free entry point. This is what CI exercises."""
    return AcmeFinanceReliabilityEnv(seed=seed, task_count=task_count)


def load_verifiers_environment(seed: int = 42, task_count: int = 120):
    """Wrap the local environment for the `verifiers` package.

    UNVALIDATED. No hosted run has exercised this path, and the `verifiers` API
    surface is pinned by whatever version the caller installed. Treat a failure
    here as an integration task, not as a defect in the local environment.
    """
    try:
        import verifiers as vf  # type: ignore
    except ImportError as exc:  # pragma: no cover - exercised only with the extra installed
        raise ImportError(
            "The `verifiers` package is not installed. The local environment works without it: "
            "use load_environment(). To install the hosted adapter path, see "
            "integrations/prime-intellect/VALIDATION.md"
        ) from exc

    env = load_environment(seed=seed, task_count=task_count)

    def reward_fn(completion, answer, state, **kwargs):  # pragma: no cover - needs the extra
        return env.reward(state["task_id"], state["observations"], state["terminal_state"])

    return vf.SingleTurnEnv(
        dataset=env.dataset(),
        rubric=vf.Rubric(funcs=[reward_fn], weights=[1.0]),
    )


def _smoke() -> int:
    env = load_environment()
    reference = env.evaluate("scripted_reference")
    hacker = env.evaluate("reward_hacker")
    print(json.dumps({"reference": reference, "reward_hacker": hacker}, indent=2, sort_keys=True))
    if reference["success_rate"] <= hacker["success_rate"]:
        print("FAIL: the adapter's reward does not separate the reference policy from the probe.")
        return 1
    print("OK: adapter loaded, tasks served, and the local verifiers separate the two policies.")
    return 0


if __name__ == "__main__":
    raise SystemExit(_smoke())
