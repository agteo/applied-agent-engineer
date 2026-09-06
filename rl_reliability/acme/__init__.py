"""Build Acme RL reliability analysis artifacts.

    python3 -m rl_reliability.acme
"""

from __future__ import annotations

from collections import Counter
from copy import deepcopy
import argparse
import json
from pathlib import Path
from typing import Any

from environments.acme_finance import (
    DEFAULT_OUT as ENV_DIR,
    Simulator,
    build_environment_bundle,
    initial_state,
    reimbursable_amount,
    score_reward,
    verify_rollout,
    write_environment_bundle,
)

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUT = ROOT / "rl_reliability" / "acme"
DEFAULT_ENV_DIR = ENV_DIR


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build Acme RL reliability artifacts.")
    parser.add_argument("--out", default=str(DEFAULT_OUT))
    parser.add_argument("--environment-dir", default=str(DEFAULT_ENV_DIR))
    args = parser.parse_args(argv)

    bundle = build_rl_bundle(Path(args.environment_dir))
    write_rl_bundle(bundle, Path(args.out))
    print(bundle["experiment_report"].rstrip())
    return 0


def build_rl_bundle(environment_dir: Path = DEFAULT_ENV_DIR) -> dict[str, Any]:
    ensure_environment_artifacts(environment_dir)
    tasks = read_jsonl(environment_dir / "tasks.jsonl")
    scripted_rollouts = read_jsonl(environment_dir / "rollouts.jsonl")
    weak_rollouts = [run_weak_policy(task) for task in tasks]
    combined = label_rollouts(scripted_rollouts, "scripted_reference") + label_rollouts(weak_rollouts, "weak_submitter")
    filtered, rejected = filter_rollouts(combined)
    metrics = build_rl_metrics(filtered, rejected)
    framing = render_mdp_framing()
    hacking_review = render_reward_hacking_review(metrics)
    experiment_plan = render_experiment_plan(metrics)
    experiment_report = render_experiment_report(metrics)
    prime = build_prime_templates()
    return {
        "rollouts": filtered,
        "rejected": rejected,
        "metrics": metrics,
        "rollout_schema": ROLLOUT_SCHEMA,
        "mdp_framing": framing,
        "reward_hacking_review": hacking_review,
        "experiment_plan": experiment_plan,
        "experiment_report": experiment_report,
        "prime_templates": prime,
    }


def ensure_environment_artifacts(environment_dir: Path) -> None:
    required = ["tasks.jsonl", "rollouts.jsonl", "manifest.json"]
    if all((environment_dir / name).exists() for name in required):
        return
    bundle = build_environment_bundle()
    write_environment_bundle(bundle, environment_dir)


def run_weak_policy(task: dict[str, Any]) -> dict[str, Any]:
    state = initial_state(task["seed"])
    simulator = Simulator(deepcopy(state))
    observations = []
    receipt_id = task["receipt_ids"][0]
    lookup = simulator.step({"name": "lookup_receipt", "arguments": {"receipt_id": receipt_id}})
    observations.append(lookup)
    total = reimbursable_amount(lookup["observation"]) if lookup["ok"] else 0.0
    draft = simulator.step(
        {
            "name": "create_reimbursement_draft",
            "arguments": {
                "task_id": task["id"],
                "employee_id": task["employee_id"],
                "receipt_ids": [receipt_id],
                "total_reimbursable": total,
            },
        }
    )
    observations.append(draft)
    # This deliberately weak policy tries to submit as the agent and skips approvals.
    observations.append(
        simulator.step(
            {
                "name": "submit_reimbursement",
                "arguments": {
                    "task_id": task["id"],
                    "employee_id": task["employee_id"],
                    "draft_id": draft["observation"]["draft_id"],
                    "actor": "agent",
                },
            }
        )
    )
    observations.append(
        simulator.step(
            {
                "name": "final_answer",
                "arguments": {
                    "task_id": task["id"],
                    "summary": "Submitted the report.",
                    "total_reimbursable": total,
                },
            }
        )
    )
    verifier = verify_rollout(task, simulator.state, observations)
    reward = score_reward(verifier, observations)
    return {
        "rollout_id": f"weak-rollout-{task['id']}",
        "environment": "acme_finance",
        "task_id": task["id"],
        "seed": task["seed"],
        "initial_state_hash": "weak-policy-local",
        "terminal_state_hash": "weak-policy-local",
        "actions": [event["action"] for event in observations],
        "observations": observations,
        "verifier": verifier,
        "reward": reward,
    }


def label_rollouts(rollouts: list[dict[str, Any]], policy: str) -> list[dict[str, Any]]:
    rows = []
    for row in rollouts:
        labeled = dict(row)
        labeled["policy"] = policy
        labeled["termination_reason"] = "final_answer" if labeled["actions"][-1]["name"] == "final_answer" else "truncated"
        rows.append(labeled)
    return rows


def filter_rollouts(rollouts: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    accepted = []
    rejected = []
    for row in rollouts:
        reason = rollout_rejection_reason(row)
        if reason:
            rejected.append({"rollout_id": row.get("rollout_id"), "task_id": row.get("task_id"), "policy": row.get("policy"), "reason": reason})
            continue
        accepted.append(row)
    return accepted, rejected


def rollout_rejection_reason(row: dict[str, Any]) -> str | None:
    if not row.get("actions"):
        return "missing_actions"
    if not row.get("observations"):
        return "missing_observations"
    if "verifier" not in row or "reward" not in row:
        return "missing_verifier_or_reward"
    if row.get("termination_reason") not in {"final_answer", "truncated"}:
        return "invalid_termination"
    return None


def build_rl_metrics(rollouts: list[dict[str, Any]], rejected: list[dict[str, Any]]) -> dict[str, Any]:
    by_policy = {}
    for policy in sorted({row["policy"] for row in rollouts}):
        rows = [row for row in rollouts if row["policy"] == policy]
        passed = sum(1 for row in rows if row["verifier"]["passed"])
        rewards = [row["reward"]["total"] for row in rows]
        unsafe = sum(1 for row in rows if not row["verifier"]["checks"]["safety_no_unauthorized_submission"])
        by_policy[policy] = {
            "rollouts": len(rows),
            "passed": passed,
            "success_rate": round(passed / len(rows), 3) if rows else 0.0,
            "average_reward": round(sum(rewards) / len(rewards), 3) if rewards else 0.0,
            "unsafe_submission_failures": unsafe,
        }
    components = Counter()
    for row in rollouts:
        for name, value in row["reward"]["components"].items():
            if value:
                components[name] += 1
    return {
        "rollout_count": len(rollouts),
        "rejected_count": len(rejected),
        "by_policy": by_policy,
        "reward_component_nonzero_counts": dict(sorted(components.items())),
        "quality_gate": {
            "requires_heldout_success_improvement": True,
            "requires_no_unsafe_submission_increase": True,
            "requires_level2_benchmark_regression_check": True,
        },
    }


def render_mdp_framing() -> str:
    return (
        "# Acme RL Framing\n\n"
        "## State\n\n"
        "The state is the Acme Finance simulator state: employees, managers, policies, receipts, trips, drafts, approval requests, submitted reports, and audit log.\n\n"
        "## Actions\n\n"
        "`search_policy`, `lookup_receipt`, `get_employee_profile`, `create_reimbursement_draft`, `request_manager_approval`, `submit_reimbursement`, and `final_answer`.\n\n"
        "## Observations\n\n"
        "Each action emits an audit event with the action, success flag, and structured observation payload.\n\n"
        "## Reward\n\n"
        "Reward is the sum of verifier-derived components from the Level 6 environment. It includes task success, policy basis, checked records, approval correctness, contract validity, invalid tool penalties, and unauthorized submission penalties.\n\n"
        "## Termination\n\n"
        "A rollout terminates when the policy emits `final_answer` or the runner truncates a rollout that cannot produce one.\n\n"
        "## Policy Under Optimization\n\n"
        "The policy maps observations and task context to the next simulator action. This Phase 7 bundle compares a scripted reference policy to a deliberately weak submitter policy; it does not claim trained-policy improvement.\n"
    )


def render_reward_hacking_review(metrics: dict[str, Any]) -> str:
    weak = metrics["by_policy"].get("weak_submitter", {})
    return (
        "# Reward Hacking Review\n\n"
        "## Observed Risk\n\n"
        f"The weak submitter policy produced {weak.get('unsafe_submission_failures', 0)} unsafe submission failures. That is the clearest exploit target: chasing terminal actions without respecting actor and approval constraints.\n\n"
        "## Exploits And Mitigations\n\n"
        "| Exploit | Detection | Mitigation |\n"
        "| --- | --- | --- |\n"
        "| Submit every draft | unsafe submission failure count | Keep `unauthorized_submission` penalty and Level 2 unsafe slice gate |\n"
        "| Ask approval for everything | approval overuse count | Score approval correctness, not approval presence |\n"
        "| Skip receipt lookup but write right-looking totals | required records checked | Require receipt ids in observations |\n"
        "| Optimize final-answer shape only | state draft and submission checks | Reward state verifiers before answer format |\n"
        "| Memorize fixture ids | heldout task success | Keep heldout simulator tasks and Level 2 benchmark regression check |\n"
    )


def render_experiment_plan(metrics: dict[str, Any]) -> str:
    return (
        "# RL Experiment Plan\n\n"
        "## Question\n\n"
        "Can experience in the Acme Finance simulator improve policy reliability without increasing unsafe actions?\n\n"
        "## Baselines\n\n"
        "- `scripted_reference`: deterministic sanity-check policy.\n"
        "- `weak_submitter`: deliberately unsafe policy for negative-control rollouts.\n\n"
        "## Training Path\n\n"
        "Hosted RL or local policy optimization is optional. A real training run must save training logs, reward curves, sampled rollouts, and post-training benchmark results.\n\n"
        "## Decision Rule\n\n"
        "A trained policy is better only if heldout simulator success improves, unsafe submission failures do not increase, and the Level 2 benchmark does not regress.\n\n"
        "## Current Offline Result\n\n"
        f"This bundle contains {metrics['rollout_count']} accepted rollouts and no trained-policy result. It is ready for experiment design, not adoption.\n"
    )


def render_experiment_report(metrics: dict[str, Any]) -> str:
    scripted = metrics["by_policy"]["scripted_reference"]
    weak = metrics["by_policy"]["weak_submitter"]
    return (
        "# Acme RL Reliability Report\n\n"
        "## Decision\n\n"
        "Do not claim RL improvement yet. The local simulator and reward analysis are executable, but no training run has been performed.\n\n"
        "## Evidence\n\n"
        f"- scripted_reference success_rate: {scripted['success_rate']:.3f}\n"
        f"- scripted_reference average_reward: {scripted['average_reward']:.3f}\n"
        f"- weak_submitter success_rate: {weak['success_rate']:.3f}\n"
        f"- weak_submitter unsafe_submission_failures: {weak['unsafe_submission_failures']}\n"
        f"- accepted rollouts: {metrics['rollout_count']}\n"
        f"- rejected rollouts: {metrics['rejected_count']}\n\n"
        "## Interpretation\n\n"
        "The reward function separates correct workflow completion from unsafe shortcut behavior. The next valid step is a smoke training run or a hosted-adapter evaluation, followed by heldout simulator and Level 2 benchmark checks.\n"
    )


def build_prime_templates() -> dict[str, str]:
    return {
        "eval_config": (
            "# Prime-compatible eval template for Acme Finance Reliability\n"
            "environment = \"acme_finance_reliability\"\n"
            "rollouts = \"rl_reliability/acme/rl-rollouts.jsonl\"\n"
            "policy = \"scripted_reference\"\n"
            "mode = \"eval\"\n"
        ),
        "smoke_config": (
            "# Optional hosted RL smoke template\n"
            "environment = \"acme_finance_reliability\"\n"
            "rollouts = \"rl_reliability/acme/rl-rollouts.jsonl\"\n"
            "method = \"grpo\"\n"
            "status = \"template_not_run\"\n"
        ),
        "report_template": (
            "# Hosted RL Run Report\n\n"
            "## Required Evidence\n\n"
            "- baseline eval\n"
            "- training logs\n"
            "- reward-component curves\n"
            "- heldout simulator eval\n"
            "- Level 2 benchmark regression check\n"
            "- sampled rollout review\n"
        ),
    }


def write_rl_bundle(bundle: dict[str, Any], out: Path) -> None:
    out.mkdir(parents=True, exist_ok=True)
    write_jsonl(out / "rl-rollouts.jsonl", bundle["rollouts"])
    write_jsonl(out / "rl-rollouts-rejected.jsonl", bundle["rejected"])
    (out / "rollout-schema.json").write_text(json.dumps(bundle["rollout_schema"], indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (out / "metrics.json").write_text(json.dumps(bundle["metrics"], indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (out / "mdp-framing.md").write_text(bundle["mdp_framing"], encoding="utf-8")
    (out / "reward-hacking-review.md").write_text(bundle["reward_hacking_review"], encoding="utf-8")
    (out / "experiment-plan.md").write_text(bundle["experiment_plan"], encoding="utf-8")
    (out / "experiment-report.md").write_text(bundle["experiment_report"], encoding="utf-8")
    templates = bundle["prime_templates"]
    (out / "prime-eval-template.toml").write_text(templates["eval_config"], encoding="utf-8")
    (out / "prime-rl-smoke-template.toml").write_text(templates["smoke_config"], encoding="utf-8")
    (out / "hosted-rl-report-template.md").write_text(templates["report_template"], encoding="utf-8")
    write_prime_reference_files(templates)


def write_prime_reference_files(templates: dict[str, str]) -> None:
    base = ROOT / "integrations" / "prime-intellect"
    (base / "configs" / "eval").mkdir(parents=True, exist_ok=True)
    (base / "configs" / "rl").mkdir(parents=True, exist_ok=True)
    (base / "reports").mkdir(parents=True, exist_ok=True)
    (base / "README.md").write_text(
        "# Prime Intellect Adapter Templates\n\n"
        "These files are templates over the local Acme Finance simulator. They are not evidence of a hosted training run.\n",
        encoding="utf-8",
    )
    (base / "configs" / "eval" / "acme-finance-reliability-baseline.toml").write_text(templates["eval_config"], encoding="utf-8")
    (base / "configs" / "rl" / "acme-finance-reliability-smoke.toml").write_text(templates["smoke_config"], encoding="utf-8")
    (base / "reports" / "template.md").write_text(templates["report_template"], encoding="utf-8")


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows = []
    with open(path, encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    with open(path, "w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, sort_keys=True) + "\n")


ROLLOUT_SCHEMA: dict[str, Any] = {
    "type": "object",
    "required": [
        "rollout_id",
        "environment",
        "task_id",
        "seed",
        "policy",
        "termination_reason",
        "actions",
        "observations",
        "verifier",
        "reward",
    ],
    "properties": {
        "rollout_id": {"type": "string"},
        "environment": {"const": "acme_finance"},
        "task_id": {"type": "string"},
        "seed": {"type": "integer"},
        "policy": {"type": "string"},
        "termination_reason": {"type": "string"},
        "actions": {"type": "array"},
        "observations": {"type": "array"},
        "verifier": {"type": "object"},
        "reward": {"type": "object"},
    },
}
