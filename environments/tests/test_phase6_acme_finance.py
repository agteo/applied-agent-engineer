import json

from environments.acme_finance import (
    DEFAULT_OUT,
    Simulator,
    build_environment_bundle,
    generate_tasks,
    initial_state,
    run_scripted_policy,
    score_reward,
    verify_rollout,
    write_environment_bundle,
)


def test_phase6_generates_required_task_coverage():
    tasks = generate_tasks(seed=42, count=120)
    categories = {task["category"] for task in tasks}

    assert len(tasks) == 120
    assert {
        "straightforward_reimbursement",
        "missing_receipt",
        "meal_limit",
        "ambiguous_receipt_lookup",
        "unsafe_submission",
        "multi_step_trip",
        "edge_case_under_receipt_threshold",
    } <= categories
    assert all(task["expected"]["draft_required"] for task in tasks)
    assert all(task["expected"]["required_policy_ids"] for task in tasks)


def test_simulated_tools_update_state_and_log_observations():
    state = initial_state(seed=7)
    simulator = Simulator(state)

    profile = simulator.step({"name": "get_employee_profile", "arguments": {"employee_id": "emp-001"}})
    draft = simulator.step(
        {
            "name": "create_reimbursement_draft",
            "arguments": {
                "task_id": "unit-task",
                "employee_id": "emp-001",
                "receipt_ids": ["rcpt-001"],
                "total_reimbursable": 68.0,
            },
        }
    )
    approval = simulator.step(
        {
            "name": "request_manager_approval",
            "arguments": {"task_id": "unit-task", "employee_id": "emp-001", "reason": "test"},
        }
    )

    assert profile["ok"] is True
    assert draft["observation"]["draft_id"] == "draft-unit-task"
    assert approval["observation"]["manager_id"] == "mgr-001"
    assert len(state["audit_log"]) == 3


def test_scripted_rollout_passes_verifiers_and_scores_reward():
    task = generate_tasks(seed=42, count=1)[0]
    rollout = run_scripted_policy(task, initial_state(seed=42))

    assert rollout["verifier"]["passed"] is True
    assert rollout["reward"]["total"] > 1.0
    assert rollout["initial_state_hash"] != rollout["terminal_state_hash"]
    assert rollout["actions"][-1]["name"] == "final_answer"


def test_verifier_and_reward_penalize_missing_approval():
    task = next(task for task in generate_tasks(seed=42, count=20) if task["expected"]["approval_required"])
    state = initial_state(seed=42)
    simulator = Simulator(state)
    observations = []
    observations.append(simulator.step({"name": "lookup_receipt", "arguments": {"receipt_id": task["receipt_ids"][0]}}))
    observations.append(
        simulator.step(
            {
                "name": "create_reimbursement_draft",
                "arguments": {
                    "task_id": task["id"],
                    "employee_id": task["employee_id"],
                    "receipt_ids": task["receipt_ids"],
                    "total_reimbursable": task["expected"]["total_reimbursable"],
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
                    "summary": "Draft prepared without approval.",
                    "total_reimbursable": task["expected"]["total_reimbursable"],
                },
            }
        )
    )

    verifier = verify_rollout(task, state, observations)
    reward = score_reward(verifier, observations)

    assert verifier["passed"] is False
    assert verifier["checks"]["state_approval_correct"] is False
    assert reward["components"]["correct_approval_behavior"] == -0.5


def test_phase6_writes_environment_artifacts(tmp_path):
    bundle = build_environment_bundle(seed=42, task_count=120)
    write_environment_bundle(bundle, tmp_path)

    expected = {
        "manifest.json",
        "state-schema.json",
        "initial-state.json",
        "tool-schemas.json",
        "tasks.jsonl",
        "rollouts.jsonl",
        "metrics.json",
        "reward-design.md",
        "verifier-report.md",
        "simulator-bias-note.md",
    }
    assert expected <= {path.name for path in tmp_path.iterdir()}

    metrics = json.loads((tmp_path / "metrics.json").read_text(encoding="utf-8"))
    assert metrics["task_count"] == 120
    assert metrics["tool_count"] >= 6
    assert set(metrics["verifier_types"]) == {"deterministic", "state", "constraint"}
    assert len((tmp_path / "tasks.jsonl").read_text(encoding="utf-8").splitlines()) == 120


def test_default_phase6_output_path_is_under_environments():
    assert "environments/acme_finance" in str(DEFAULT_OUT)
