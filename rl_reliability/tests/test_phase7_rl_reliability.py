import json
import sys
from pathlib import Path

import pytest

from rl_reliability.acme import (
    DEFAULT_OUT,
    build_rl_bundle,
    filter_rollouts,
    label_rollouts,
    rollout_rejection_reason,
    run_weak_policy,
    write_rl_bundle,
)
from environments.acme_finance import generate_tasks

ADAPTER_DIR = (
    Path(__file__).resolve().parents[2]
    / "integrations"
    / "prime-intellect"
    / "environments"
    / "acme_finance_reliability"
)
sys.path.insert(0, str(ADAPTER_DIR))
from acme_finance_reliability import load_environment as load_adapter_environment  # noqa: E402


def test_phase7_builds_rl_rollout_comparison():
    bundle = build_rl_bundle()
    metrics = bundle["metrics"]

    assert metrics["rollout_count"] == 360
    assert set(metrics["by_policy"]) == {"scripted_reference", "weak_submitter", "reward_hacker"}
    assert metrics["by_policy"]["scripted_reference"]["success_rate"] == 1.0
    assert metrics["by_policy"]["weak_submitter"]["success_rate"] == 0.0
    assert metrics["by_policy"]["weak_submitter"]["unsafe_submission_failures"] == 120
    assert metrics["by_policy"]["reward_hacker"]["success_rate"] == 0.0
    assert metrics["quality_gate"]["requires_level2_benchmark_regression_check"] is True
    assert "Do not claim RL improvement yet" in bundle["experiment_report"]


def test_report_states_the_rollout_set_cannot_train():
    bundle = build_rl_bundle()

    # Every policy here is scripted, so reward is near-constant within a policy
    # and there is no advantage signal. The report must say so.
    assert bundle["metrics"]["by_policy"]["scripted_reference"]["distinct_rewards"] == 1
    assert "not training data" in bundle["experiment_report"]


def test_weak_rollouts_carry_real_state_hashes():
    task = generate_tasks(seed=42, count=1)[0]
    rollout = run_weak_policy(task)

    # These were the literal string "weak-policy-local" before.
    assert len(rollout["initial_state_hash"]) == 16
    assert len(rollout["terminal_state_hash"]) == 16
    assert rollout["initial_state_hash"] != rollout["terminal_state_hash"]
    assert int(rollout["initial_state_hash"], 16) >= 0


def test_label_rollouts_refuses_to_relabel_a_policy():
    task = generate_tasks(seed=42, count=1)[0]
    rollout = run_weak_policy(task)

    with pytest.raises(ValueError):
        label_rollouts([rollout], "scripted_reference")


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


def test_writing_elsewhere_does_not_touch_the_repo_integrations_tree(tmp_path):
    """--out used to be ignored by the Prime writer, which rewrote tracked files."""
    from rl_reliability.acme import DEFAULT_PRIME_DIR

    before = sorted((p, p.stat().st_mtime_ns) for p in DEFAULT_PRIME_DIR.rglob("*") if p.is_file())
    write_rl_bundle(build_rl_bundle(), tmp_path)
    after = sorted((p, p.stat().st_mtime_ns) for p in DEFAULT_PRIME_DIR.rglob("*") if p.is_file())

    assert before == after
    assert (tmp_path / "prime-intellect" / "configs" / "rl" / "acme-finance-reliability-small.toml").exists()


def test_prime_adapter_loads_and_separates_policies():
    env = load_adapter_environment()
    reference = env.evaluate("scripted_reference")
    hacker = env.evaluate("reward_hacker")

    assert env.id == "acme_finance_reliability"
    assert len(env.dataset()) == 120
    assert reference["success_rate"] > hacker["success_rate"]
    assert reference["unsafe_submission_failures"] == 0


def test_prime_adapter_never_hands_the_grading_key_to_a_policy():
    env = load_adapter_environment()
    row = env.dataset()[0]

    assert set(row) == {"id", "prompt", "info", "answer"}
    assert "total_reimbursable" not in json.dumps(row["info"])


def test_default_phase7_output_path_is_under_rl_reliability():
    assert "rl_reliability/acme" in str(DEFAULT_OUT)
