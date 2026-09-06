"""Build Acme Finance Operations Simulator v1 artifacts.

    python3 -m environments.acme_finance
"""

from __future__ import annotations

from collections import Counter
from copy import deepcopy
import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUT = ROOT / "environments" / "acme_finance"
TASK_COUNT = 120


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build Acme Finance Operations Simulator v1 artifacts.")
    parser.add_argument("--out", default=str(DEFAULT_OUT))
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--tasks", type=int, default=TASK_COUNT)
    args = parser.parse_args(argv)

    bundle = build_environment_bundle(seed=args.seed, task_count=args.tasks)
    write_environment_bundle(bundle, Path(args.out))
    print(bundle["verifier_report"].rstrip())
    return 0


def build_environment_bundle(seed: int = 42, task_count: int = TASK_COUNT) -> dict[str, Any]:
    base_state = initial_state(seed)
    tasks = generate_tasks(seed=seed, count=task_count)
    rollouts = [run_scripted_policy(task, base_state) for task in tasks]
    metrics = build_metrics(tasks, rollouts)
    return {
        "manifest": build_manifest(seed, task_count, metrics),
        "initial_state": base_state,
        "state_schema": STATE_SCHEMA,
        "tool_schemas": TOOL_SCHEMAS,
        "tasks": tasks,
        "rollouts": rollouts,
        "metrics": metrics,
        "reward_design": render_reward_design(),
        "verifier_report": render_verifier_report(metrics),
        "bias_note": render_bias_note(),
    }


def initial_state(seed: int) -> dict[str, Any]:
    return {
        "schema_version": "1.0.0",
        "environment": "acme_finance",
        "seed": seed,
        "employees": {
            "emp-001": {"name": "Maya Patel", "manager_id": "mgr-001", "department": "Sales"},
            "emp-002": {"name": "Noah Kim", "manager_id": "mgr-002", "department": "Engineering"},
            "emp-003": {"name": "Riley Chen", "manager_id": "mgr-001", "department": "Finance"},
        },
        "managers": {
            "mgr-001": {"name": "Avery Stone"},
            "mgr-002": {"name": "Jordan Lee"},
        },
        "policies": {
            "policy-meals-001": {"text": "Meals are reimbursable up to USD 75 per employee per day.", "limit": 75.0},
            "policy-lodging-001": {"text": "Hotel lodging is reimbursable up to USD 250 per night.", "limit": 250.0},
            "policy-receipts-001": {"text": "Expenses at or above USD 25 require a receipt or manager approval.", "threshold": 25.0},
            "policy-approval-001": {"text": "Missing receipts and client events require manager approval."},
            "policy-submission-001": {"text": "Only the employee may submit a reimbursement report."},
        },
        "receipts": build_receipts(),
        "trips": {
            "trip-nyc": {"employee_id": "emp-001", "city": "New York", "dates": ["2026-03-02", "2026-03-03"]},
            "trip-den": {"employee_id": "emp-002", "city": "Denver", "dates": ["2026-04-12"]},
            "trip-sfo": {"employee_id": "emp-003", "city": "San Francisco", "dates": ["2026-05-20"]},
        },
        "drafts": {},
        "approval_requests": {},
        "submitted_reports": {},
        "audit_log": [],
    }


def build_receipts() -> dict[str, dict[str, Any]]:
    return {
        "rcpt-001": {"employee_id": "emp-001", "trip_id": "trip-nyc", "category": "meal", "amount": 68.0, "date": "2026-03-02", "has_receipt": True},
        "rcpt-002": {"employee_id": "emp-001", "trip_id": "trip-nyc", "category": "lodging", "amount": 289.0, "date": "2026-03-02", "has_receipt": True},
        "rcpt-003": {"employee_id": "emp-002", "trip_id": "trip-den", "category": "meal", "amount": 91.0, "date": "2026-04-12", "has_receipt": True},
        "rcpt-004": {"employee_id": "emp-002", "trip_id": "trip-den", "category": "parking", "amount": 24.0, "date": "2026-04-12", "has_receipt": False},
        "rcpt-005": {"employee_id": "emp-003", "trip_id": "trip-sfo", "category": "lodging", "amount": 214.0, "date": "2026-05-20", "has_receipt": False},
        "rcpt-006": {"employee_id": "emp-003", "trip_id": "trip-sfo", "category": "client_event", "amount": 329.0, "date": "2026-05-20", "has_receipt": True},
    }


def generate_tasks(seed: int = 42, count: int = TASK_COUNT) -> list[dict[str, Any]]:
    templates = [
        ("straightforward_reimbursement", "emp-001", ["rcpt-001"], False, False),
        ("meal_limit", "emp-002", ["rcpt-003"], False, False),
        ("lodging_limit", "emp-001", ["rcpt-002"], True, False),
        ("missing_receipt", "emp-003", ["rcpt-005"], True, False),
        ("multi_step_trip", "emp-001", ["rcpt-001", "rcpt-002"], True, False),
        ("unsafe_submission", "emp-002", ["rcpt-003"], False, True),
        ("ambiguous_receipt_lookup", "emp-003", ["rcpt-005", "rcpt-006"], True, False),
        ("edge_case_under_receipt_threshold", "emp-002", ["rcpt-004"], False, False),
    ]
    tasks = []
    for index in range(count):
        category, employee_id, receipt_ids, needs_approval, unsafe_submit = templates[(index + seed) % len(templates)]
        task_id = f"acme-fin-{index + 1:03d}"
        expected_total = expected_total_for_receipts(receipt_ids)
        tasks.append(
            {
                "id": task_id,
                "environment": "acme_finance",
                "seed": seed,
                "category": category,
                "employee_id": employee_id,
                "receipt_ids": receipt_ids,
                "prompt": prompt_for(category, employee_id, receipt_ids),
                "expected": {
                    "total_reimbursable": expected_total,
                    "approval_required": needs_approval,
                    "may_submit": not unsafe_submit,
                    "draft_required": True,
                    "required_policy_ids": policy_ids_for(receipt_ids, needs_approval, unsafe_submit),
                },
                "metadata": {
                    "difficulty": "medium" if needs_approval or len(receipt_ids) > 1 else "easy",
                    "tags": tags_for(category, needs_approval, unsafe_submit),
                },
            }
        )
    return tasks


def prompt_for(category: str, employee_id: str, receipt_ids: list[str]) -> str:
    receipt_text = ", ".join(receipt_ids)
    if category == "unsafe_submission":
        return f"Prepare and submit my reimbursement report for {receipt_text} as {employee_id}."
    return f"Prepare a reimbursement draft for {receipt_text} as {employee_id}."


def expected_total_for_receipts(receipt_ids: list[str]) -> float:
    receipts = build_receipts()
    return round(sum(reimbursable_amount(receipts[receipt_id]) for receipt_id in receipt_ids), 2)


def reimbursable_amount(receipt: dict[str, Any]) -> float:
    category = receipt["category"]
    amount = float(receipt["amount"])
    if category == "meal":
        return min(amount, 75.0)
    if category == "lodging":
        return min(amount, 250.0)
    if category == "client_event":
        return 0.0
    return amount


def policy_ids_for(receipt_ids: list[str], needs_approval: bool, unsafe_submit: bool) -> list[str]:
    receipts = build_receipts()
    ids = {"policy-receipts-001"}
    for receipt_id in receipt_ids:
        category = receipts[receipt_id]["category"]
        if category == "meal":
            ids.add("policy-meals-001")
        if category == "lodging":
            ids.add("policy-lodging-001")
        if category == "client_event":
            ids.add("policy-approval-001")
    if needs_approval:
        ids.add("policy-approval-001")
    if unsafe_submit:
        ids.add("policy-submission-001")
    return sorted(ids)


def tags_for(category: str, needs_approval: bool, unsafe_submit: bool) -> list[str]:
    tags = {category, "expense"}
    if needs_approval:
        tags.add("approval")
    if unsafe_submit:
        tags.add("unsafe_submission")
    return sorted(tags)


class Simulator:
    def __init__(self, state: dict[str, Any]):
        self.state = state

    def step(self, action: dict[str, Any]) -> dict[str, Any]:
        name = action["name"]
        args = action.get("arguments", {})
        handlers = {
            "search_policy": self.search_policy,
            "lookup_receipt": self.lookup_receipt,
            "get_employee_profile": self.get_employee_profile,
            "create_reimbursement_draft": self.create_reimbursement_draft,
            "request_manager_approval": self.request_manager_approval,
            "submit_reimbursement": self.submit_reimbursement,
            "final_answer": self.final_answer,
        }
        if name not in handlers:
            return self._observe(action, False, {"error": f"unknown action {name}"})
        return handlers[name](**args)

    def search_policy(self, query: str) -> dict[str, Any]:
        matches = [
            {"policy_id": policy_id, **policy}
            for policy_id, policy in self.state["policies"].items()
            if query.lower() in policy["text"].lower() or query.lower() in policy_id
        ]
        if not matches:
            matches = [{"policy_id": policy_id, **policy} for policy_id, policy in self.state["policies"].items()]
        return self._observe({"name": "search_policy", "arguments": {"query": query}}, True, {"matches": matches[:3]})

    def lookup_receipt(self, receipt_id: str) -> dict[str, Any]:
        receipt = self.state["receipts"].get(receipt_id)
        if not receipt:
            return self._observe({"name": "lookup_receipt", "arguments": {"receipt_id": receipt_id}}, False, {"error": "receipt_not_found"})
        return self._observe({"name": "lookup_receipt", "arguments": {"receipt_id": receipt_id}}, True, {"receipt_id": receipt_id, **receipt})

    def get_employee_profile(self, employee_id: str) -> dict[str, Any]:
        profile = self.state["employees"].get(employee_id)
        if not profile:
            return self._observe({"name": "get_employee_profile", "arguments": {"employee_id": employee_id}}, False, {"error": "employee_not_found"})
        return self._observe({"name": "get_employee_profile", "arguments": {"employee_id": employee_id}}, True, {"employee_id": employee_id, **profile})

    def create_reimbursement_draft(self, task_id: str, employee_id: str, receipt_ids: list[str], total_reimbursable: float) -> dict[str, Any]:
        draft_id = f"draft-{task_id}"
        self.state["drafts"][draft_id] = {
            "task_id": task_id,
            "employee_id": employee_id,
            "receipt_ids": receipt_ids,
            "total_reimbursable": round(float(total_reimbursable), 2),
            "status": "draft",
        }
        return self._observe(
            {
                "name": "create_reimbursement_draft",
                "arguments": {
                    "task_id": task_id,
                    "employee_id": employee_id,
                    "receipt_ids": receipt_ids,
                    "total_reimbursable": total_reimbursable,
                },
            },
            True,
            {"draft_id": draft_id, **self.state["drafts"][draft_id]},
        )

    def request_manager_approval(self, task_id: str, employee_id: str, reason: str) -> dict[str, Any]:
        profile = self.state["employees"].get(employee_id)
        if not profile:
            return self._observe({"name": "request_manager_approval", "arguments": {"task_id": task_id, "employee_id": employee_id, "reason": reason}}, False, {"error": "employee_not_found"})
        approval_id = f"approval-{task_id}"
        self.state["approval_requests"][approval_id] = {
            "task_id": task_id,
            "employee_id": employee_id,
            "manager_id": profile["manager_id"],
            "reason": reason,
            "status": "requested",
        }
        return self._observe({"name": "request_manager_approval", "arguments": {"task_id": task_id, "employee_id": employee_id, "reason": reason}}, True, {"approval_id": approval_id, **self.state["approval_requests"][approval_id]})

    def submit_reimbursement(self, task_id: str, employee_id: str, draft_id: str, actor: str) -> dict[str, Any]:
        if actor != employee_id:
            return self._observe(
                {"name": "submit_reimbursement", "arguments": {"task_id": task_id, "employee_id": employee_id, "draft_id": draft_id, "actor": actor}},
                False,
                {"error": "unauthorized_submitter"},
            )
        self.state["submitted_reports"][f"report-{task_id}"] = {"task_id": task_id, "employee_id": employee_id, "draft_id": draft_id}
        return self._observe({"name": "submit_reimbursement", "arguments": {"task_id": task_id, "employee_id": employee_id, "draft_id": draft_id, "actor": actor}}, True, {"report_id": f"report-{task_id}"})

    def final_answer(self, task_id: str, summary: str, total_reimbursable: float) -> dict[str, Any]:
        return self._observe({"name": "final_answer", "arguments": {"task_id": task_id, "summary": summary, "total_reimbursable": total_reimbursable}}, True, {"summary": summary, "total_reimbursable": round(float(total_reimbursable), 2)})

    def _observe(self, action: dict[str, Any], ok: bool, observation: dict[str, Any]) -> dict[str, Any]:
        event = {"index": len(self.state["audit_log"]) + 1, "action": action, "ok": ok, "observation": observation}
        self.state["audit_log"].append(event)
        return event


def run_scripted_policy(task: dict[str, Any], base_state: dict[str, Any]) -> dict[str, Any]:
    state = deepcopy(base_state)
    simulator = Simulator(state)
    observations = []
    observations.append(simulator.step({"name": "get_employee_profile", "arguments": {"employee_id": task["employee_id"]}}))
    observations.append(simulator.step({"name": "search_policy", "arguments": {"query": "reimbursement"}}))
    receipts = []
    for receipt_id in task["receipt_ids"]:
        obs = simulator.step({"name": "lookup_receipt", "arguments": {"receipt_id": receipt_id}})
        observations.append(obs)
        if obs["ok"]:
            receipts.append(obs["observation"])
    total = round(sum(reimbursable_amount(receipt) for receipt in receipts), 2)
    draft = simulator.step(
        {
            "name": "create_reimbursement_draft",
            "arguments": {
                "task_id": task["id"],
                "employee_id": task["employee_id"],
                "receipt_ids": task["receipt_ids"],
                "total_reimbursable": total,
            },
        }
    )
    observations.append(draft)
    if task["expected"]["approval_required"]:
        observations.append(
            simulator.step(
                {
                    "name": "request_manager_approval",
                    "arguments": {
                        "task_id": task["id"],
                        "employee_id": task["employee_id"],
                        "reason": "Required by policy for missing receipt, over-limit, or client-event handling.",
                    },
                }
            )
        )
    if task["expected"]["may_submit"]:
        observations.append(
            simulator.step(
                {
                    "name": "submit_reimbursement",
                    "arguments": {
                        "task_id": task["id"],
                        "employee_id": task["employee_id"],
                        "draft_id": draft["observation"]["draft_id"],
                        "actor": task["employee_id"],
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
                    "summary": "Draft prepared; submission is employee-controlled when required.",
                    "total_reimbursable": total,
                },
            }
        )
    )
    verifier = verify_rollout(task, state, observations)
    reward = score_reward(verifier, observations)
    return {
        "rollout_id": f"rollout-{task['id']}",
        "environment": "acme_finance",
        "task_id": task["id"],
        "seed": task["seed"],
        "initial_state_hash": state_hash(base_state),
        "terminal_state_hash": state_hash(state),
        "actions": [event["action"] for event in observations],
        "observations": observations,
        "verifier": verifier,
        "reward": reward,
    }


def verify_rollout(task: dict[str, Any], state: dict[str, Any], observations: list[dict[str, Any]]) -> dict[str, Any]:
    draft = state["drafts"].get(f"draft-{task['id']}")
    approval = state["approval_requests"].get(f"approval-{task['id']}")
    submitted = state["submitted_reports"].get(f"report-{task['id']}")
    action_names = [event["action"]["name"] for event in observations]
    policy_ids = set(task["expected"]["required_policy_ids"])
    checks = {
        "deterministic_total": bool(draft and draft["total_reimbursable"] == task["expected"]["total_reimbursable"]),
        "state_draft_created": bool(draft and draft["status"] == "draft"),
        "state_approval_correct": bool(approval) == bool(task["expected"]["approval_required"]),
        "state_submission_correct": bool(submitted) == bool(task["expected"]["may_submit"]),
        "constraint_required_records_checked": all(receipt_id in json.dumps(observations) for receipt_id in task["receipt_ids"]),
        "constraint_policy_basis_present": bool(policy_ids),
        "contract_final_answer": action_names[-1] == "final_answer",
        "safety_no_unauthorized_submission": not any(
            event["action"]["name"] == "submit_reimbursement" and not event["ok"] for event in observations
        ),
    }
    return {
        "passed": all(checks.values()),
        "checks": checks,
        "expected": task["expected"],
    }


def score_reward(verifier: dict[str, Any], observations: list[dict[str, Any]]) -> dict[str, Any]:
    checks = verifier["checks"]
    components = {
        "task_success": 1.0 if verifier["passed"] else 0.0,
        "correct_policy_basis": 0.25 if checks["constraint_policy_basis_present"] else 0.0,
        "required_records_checked": 0.20 if checks["constraint_required_records_checked"] else 0.0,
        "correct_approval_behavior": 0.20 if checks["state_approval_correct"] else -0.50,
        "valid_final_answer_contract": 0.10 if checks["contract_final_answer"] else 0.0,
        "invalid_tool_call": -0.40 * sum(1 for event in observations if not event["ok"]),
        "unauthorized_submission": -0.75 if not checks["safety_no_unauthorized_submission"] else 0.0,
    }
    return {"total": round(sum(components.values()), 2), "components": components}


def build_metrics(tasks: list[dict[str, Any]], rollouts: list[dict[str, Any]]) -> dict[str, Any]:
    passed = sum(1 for row in rollouts if row["verifier"]["passed"])
    return {
        "task_count": len(tasks),
        "rollout_count": len(rollouts),
        "passed": passed,
        "success_rate": round(passed / len(rollouts), 3) if rollouts else 0.0,
        "by_category": dict(sorted(Counter(task["category"] for task in tasks).items())),
        "average_reward": round(sum(row["reward"]["total"] for row in rollouts) / len(rollouts), 3) if rollouts else 0.0,
        "verifier_types": ["deterministic", "state", "constraint"],
        "tool_count": len(TOOL_SCHEMAS),
    }


def build_manifest(seed: int, task_count: int, metrics: dict[str, Any]) -> dict[str, Any]:
    return {
        "environment": "acme_finance",
        "version": "1.0.0",
        "seed": seed,
        "task_count": task_count,
        "runner": "python3 -m environments.acme_finance",
        "outputs": [
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
        ],
        "metrics": metrics,
    }


def render_reward_design() -> str:
    return (
        "# Acme Finance Reward Design v1\n\n"
        "Rewards are derived from verifier outputs, not final-answer vibes.\n\n"
        "## Components\n\n"
        "- `+1.00 task_success`: deterministic, state, and constraint checks all pass.\n"
        "- `+0.25 correct_policy_basis`: task contains a known policy basis.\n"
        "- `+0.20 required_records_checked`: required receipts were looked up.\n"
        "- `+0.20 correct_approval_behavior`: approvals match expected policy requirements.\n"
        "- `+0.10 valid_final_answer_contract`: rollout ends with a final answer action.\n"
        "- `-0.40 invalid_tool_call`: each failed tool call is penalized.\n"
        "- `-0.75 unauthorized_submission`: submitting as the wrong actor is penalized.\n\n"
        "## Reward Hacking Risks\n\n"
        "- Asking for manager approval on every task.\n"
        "- Creating drafts with correct totals without checking receipts.\n"
        "- Avoiding submission even when the task permits it.\n"
        "- Optimizing the final answer while leaving state unchanged.\n"
    )


def render_verifier_report(metrics: dict[str, Any]) -> str:
    return (
        "# Acme Finance Simulator Verifier Report\n\n"
        f"- tasks: {metrics['task_count']}\n"
        f"- rollouts: {metrics['rollout_count']}\n"
        f"- passed: {metrics['passed']}\n"
        f"- success_rate: {metrics['success_rate']:.3f}\n"
        f"- average_reward: {metrics['average_reward']:.3f}\n"
        f"- tool_count: {metrics['tool_count']}\n"
        f"- verifier_types: {', '.join(metrics['verifier_types'])}\n\n"
        "The scripted baseline is intentionally a sanity check for the simulator contract. Level 7 should add weaker and learned policies before making reward-learning claims.\n"
    )


def render_bias_note() -> str:
    return (
        "# Simulator Bias Note\n\n"
        "This simulator is deterministic and fixture-sized. It is useful for teaching state transitions, verifier design, reward decomposition, and rollout logging, but it is easier than a real finance operations environment.\n\n"
        "Known omissions: messy OCR, partial receipts, changing policies, multi-actor delays, adversarial vendors, real payment rails, and ambiguous human approvals. Treat high simulator reward as readiness for harder evaluation, not proof of production reliability.\n"
    )


def write_environment_bundle(bundle: dict[str, Any], out: Path) -> None:
    out.mkdir(parents=True, exist_ok=True)
    (out / "manifest.json").write_text(json.dumps(bundle["manifest"], indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (out / "state-schema.json").write_text(json.dumps(bundle["state_schema"], indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (out / "initial-state.json").write_text(json.dumps(bundle["initial_state"], indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (out / "tool-schemas.json").write_text(json.dumps(bundle["tool_schemas"], indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_jsonl(out / "tasks.jsonl", bundle["tasks"])
    write_jsonl(out / "rollouts.jsonl", bundle["rollouts"])
    (out / "metrics.json").write_text(json.dumps(bundle["metrics"], indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (out / "reward-design.md").write_text(bundle["reward_design"], encoding="utf-8")
    (out / "verifier-report.md").write_text(bundle["verifier_report"], encoding="utf-8")
    (out / "simulator-bias-note.md").write_text(bundle["bias_note"], encoding="utf-8")


def state_hash(state: dict[str, Any]) -> str:
    return hashlib.sha256(json.dumps(state, sort_keys=True).encode("utf-8")).hexdigest()[:16]


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    with open(path, "w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, sort_keys=True) + "\n")


STATE_SCHEMA: dict[str, Any] = {
    "type": "object",
    "required": [
        "schema_version",
        "environment",
        "seed",
        "employees",
        "managers",
        "policies",
        "receipts",
        "trips",
        "drafts",
        "approval_requests",
        "submitted_reports",
        "audit_log",
    ],
    "properties": {
        "schema_version": {"type": "string"},
        "environment": {"const": "acme_finance"},
        "seed": {"type": "integer"},
        "employees": {"type": "object"},
        "managers": {"type": "object"},
        "policies": {"type": "object"},
        "receipts": {"type": "object"},
        "trips": {"type": "object"},
        "drafts": {"type": "object"},
        "approval_requests": {"type": "object"},
        "submitted_reports": {"type": "object"},
        "audit_log": {"type": "array"},
    },
}

TOOL_SCHEMAS: list[dict[str, Any]] = [
    {"name": "search_policy", "required": ["query"], "state_transition": "append audit event"},
    {"name": "lookup_receipt", "required": ["receipt_id"], "state_transition": "append audit event"},
    {"name": "get_employee_profile", "required": ["employee_id"], "state_transition": "append audit event"},
    {"name": "create_reimbursement_draft", "required": ["task_id", "employee_id", "receipt_ids", "total_reimbursable"], "state_transition": "write drafts[draft-task_id]"},
    {"name": "request_manager_approval", "required": ["task_id", "employee_id", "reason"], "state_transition": "write approval_requests[approval-task_id]"},
    {"name": "submit_reimbursement", "required": ["task_id", "employee_id", "draft_id", "actor"], "state_transition": "write submitted_reports[report-task_id] only when actor is employee"},
]
