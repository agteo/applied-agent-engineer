import json

from rl_reliability.acme import (
    DEFAULT_OUT,
    build_rl_bundle,
    filter_rollouts,
    rollout_rejection_reason,
    run_weak_policy,
    write_rl_bundle,
)
from environments.acme_finance import generate_tasks


def test_phase7_builds_rl_rollout_comparison():
    bundle = build_rl_bundle()
    metrics = bundle["metrics"]

    assert metrics["rollout_count"] == 240
    assert metrics["by_policy"]["scripted_reference"]["success_rate"] == 1.0
    assert metrics["by_policy"]["weak_submitter"]["success_rate"] == 0.0
    assert metrics["by_policy"]["weak_submitter"]["unsafe_submission_failures"] == 120
    assert metrics["quality_gate"]["requires_level2_benchmark_regression_check"] is True
    assert "Do not claim RL improvement yet" in bundle["experiment_report"]


def test_weak_policy_exposes_reward_hacking_risk():
    task = generate_tasks(seed=42, count=1)[0]
    rollout = run_weak_policy(task)

    assert rollout["verifier"]["passed"] is False
    assert rollout["verifier"]["checks"]["safety_no_unauthorized_submission"] is False
    assert rollout["reward"]["components"]["unauthorized_submission"] == -0.75


def test_rollout_filter_rejects_incomplete_rows():
    accepted, rejected = filter_rollouts(
        [
            {
                "rollout_id": "bad",
                "task_id": "task",
                "policy": "unit",
                "actions": [],
                "observations": [],
                "termination_reason": "final_answer",
            }
        ]
    )

    assert accepted == []
    assert rejected == [{"rollout_id": "bad", "task_id": "task", "policy": "unit", "reason": "missing_actions"}]
    assert rollout_rejection_reason({"actions": [1], "observations": [1], "verifier": {}, "reward": {}, "termination_reason": "final_answer"}) is None


def test_phase7_writes_analysis_and_prime_templates(tmp_path):
    bundle = build_rl_bundle()
    write_rl_bundle(bundle, tmp_path)

    expected = {
        "rl-rollouts.jsonl",
        "rl-rollouts-rejected.jsonl",
        "rollout-schema.json",
        "metrics.json",
        "mdp-framing.md",
        "reward-hacking-review.md",
        "experiment-plan.md",
        "experiment-report.md",
        "prime-eval-template.toml",
        "prime-rl-smoke-template.toml",
        "hosted-rl-report-template.md",
    }
    assert expected <= {path.name for path in tmp_path.iterdir()}

    metrics = json.loads((tmp_path / "metrics.json").read_text(encoding="utf-8"))
    assert metrics["by_policy"]["scripted_reference"]["rollouts"] == 120
    assert metrics["by_policy"]["weak_submitter"]["rollouts"] == 120
    assert "template_not_run" in (tmp_path / "prime-rl-smoke-template.toml").read_text(encoding="utf-8")


def test_default_phase7_output_path_is_under_rl_reliability():
    assert "rl_reliability/acme" in str(DEFAULT_OUT)
