"""The four Level 1 tools.

Every tool is a plain function over fixture data with a typed schema in
`schemas.py`. Tools raise nothing on bad input: the harness validates first and
hands the model a readable error instead (see `agent.py`).
"""

from __future__ import annotations

import re
from collections import defaultdict
from typing import Any, Callable

from . import fixtures
from .schemas import TOOL_SCHEMAS

_WORD = re.compile(r"[a-z0-9]+")


def _tokens(text: str) -> list[str]:
    return _WORD.findall(text.lower())


def search_policy(query: str, category: str | None = None, top_k: int = 3) -> dict[str, Any]:
    """Keyword search over the policy corpus.

    Scoring is deliberately simple: keyword hits are worth more than title hits,
    which are worth more than body hits. Lab 3's stretch goal replaces this with
    embeddings; the return shape stays the same either way.
    """
    query_tokens = set(_tokens(query))
    results = []
    for section in fixtures.policy_sections():
        if category and section["category"] != category:
            continue
        score = 0.0
        for keyword in section["keywords"]:
            keyword_tokens = set(_tokens(keyword))
            if keyword_tokens and keyword_tokens <= query_tokens:
                score += 3.0
        score += 2.0 * len(query_tokens & set(_tokens(section["title"])))
        score += 1.0 * len(query_tokens & set(_tokens(section["text"])))
        if score > 0:
            results.append((score, section))

    results.sort(key=lambda pair: (-pair[0], pair[1]["source_id"]))
    top = results[: max(1, top_k)]
    best = top[0][0] if top else 1.0
    return {
        "query": query,
        "results": [
            {
                "source_id": section["source_id"],
                "title": section["title"],
                "category": section["category"],
                "text": section["text"],
                "score": round(score / best, 2),
            }
            for score, section in top
        ],
    }


def lookup_receipt(
    employee_id: str,
    merchant: str | None = None,
    date: str | None = None,
    category: str | None = None,
    amount: float | None = None,
    trip_id: str | None = None,
) -> dict[str, Any]:
    """Return receipts matching the filters, plus an `ambiguous` flag.

    An empty result and a multi-result match are both legitimate outcomes. The
    agent is expected to report them rather than pick one silently.
    """
    known = {employee["employee_id"] for employee in fixtures.employees()}
    if employee_id not in known:
        return {
            "matches": [],
            "match_count": 0,
            "ambiguous": False,
            "error": f"unknown employee_id {employee_id!r}",
        }

    matches = []
    for receipt in fixtures.receipts():
        if receipt["employee_id"] != employee_id:
            continue
        if merchant and merchant.lower() not in receipt["merchant"].lower():
            continue
        if date and receipt["date"] != date:
            continue
        if category and receipt["category"] != category:
            continue
        if amount is not None and abs(receipt["amount"] - amount) > 0.005:
            continue
        if trip_id and receipt["trip_id"] != trip_id:
            continue
        matches.append(receipt)

    return {
        "matches": matches,
        "match_count": len(matches),
        "ambiguous": len(matches) > 1,
    }


def calculate_reimbursement(items: list[dict[str, Any]]) -> dict[str, Any]:
    """Apply the Acme rules to a list of expense items.

    This is the tool that makes the agent auditable: the arithmetic and the
    policy thresholds live here, in code, not in the model's head. Every output
    line carries the policy source id that produced it.
    """
    rules = fixtures.rules()
    meal_limit = rules["meals_daily_limit_usd"]
    lodging_limit = rules["lodging_nightly_limit_usd"]
    receipt_threshold = rules["receipt_required_threshold_usd"]
    item_approval = rules["manager_approval_item_threshold_usd"]
    report_approval = rules["manager_approval_report_threshold_usd"]

    reimbursable: list[dict[str, Any]] = []
    non_reimbursable: list[dict[str, Any]] = []
    missing_information: list[str] = []
    approvals: list[dict[str, Any]] = []

    meals_by_day: dict[str, float] = defaultdict(float)

    for item in items:
        description = item["description"]
        amount = float(item["amount"])
        category = item["category"]
        sources: list[str] = []
        allowed = amount

        if category in rules["non_reimbursable_categories"]:
            non_reimbursable.append(
                {
                    "description": description,
                    "amount": amount,
                    "policy_source_ids": [rules["non_reimbursable_source_id"]],
                    "reason": "Alcohol is not reimbursable on an individual expense report.",
                }
            )
            continue

        if category in rules["preapproval_categories"]:
            approvals.append(
                {
                    "approval_type": "manager",
                    "reason": f"{description} is client entertainment and requires manager pre-approval with an attendee list.",
                    "policy_source_ids": [rules["preapproval_source_id"]],
                }
            )
            missing_information.append(f"Attendee list for {description}.")
            sources.append(rules["preapproval_source_id"])

        if category == "meals":
            day = item.get("date", "undated")
            already = meals_by_day[day]
            room = max(0.0, meal_limit - already)
            meals_by_day[day] = already + amount
            sources.append(rules["meals_daily_limit_source_id"])
            if amount > room:
                over = amount - room
                allowed = room
                non_reimbursable.append(
                    {
                        "description": f"{description} (above the USD {meal_limit:.0f} daily meal limit)",
                        "amount": round(over, 2),
                        "policy_source_ids": [rules["meals_daily_limit_source_id"]],
                        "reason": f"Daily meal spend on {day} exceeds the USD {meal_limit:.0f} limit.",
                    }
                )

        if category == "lodging":
            nights = int(item.get("nights", 1))
            cap = lodging_limit * nights
            sources.append(rules["lodging_nightly_limit_source_id"])
            if amount > cap:
                over = amount - cap
                allowed = cap
                non_reimbursable.append(
                    {
                        "description": f"{description} (above the USD {lodging_limit:.0f} nightly lodging limit)",
                        "amount": round(over, 2),
                        "policy_source_ids": [rules["lodging_nightly_limit_source_id"]],
                        "reason": f"Lodging over USD {lodging_limit:.0f} per night requires manager approval for the excess.",
                    }
                )
                approvals.append(
                    {
                        "approval_type": "manager",
                        "reason": f"{description} exceeds the nightly lodging limit by USD {over:.2f}.",
                        "policy_source_ids": [rules["lodging_nightly_limit_source_id"]],
                    }
                )

        if category == "travel":
            sources.append("policy-travel-002")

        has_receipt = item.get("has_receipt", True)
        if not has_receipt and amount >= receipt_threshold:
            sources.append(rules["receipt_required_source_id"])
            missing_information.append(
                f"Receipt or missing receipt declaration for {description} (USD {amount:.2f})."
            )
            approvals.append(
                {
                    "approval_type": "manager",
                    "reason": f"{description} has no receipt and is at or above the USD {receipt_threshold:.0f} receipt threshold.",
                    "policy_source_ids": [rules["receipt_required_source_id"]],
                }
            )

        if amount >= item_approval:
            sources.append(rules["manager_approval_source_id"])
            approvals.append(
                {
                    "approval_type": "manager",
                    "reason": f"{description} is a single expense of USD {amount:.2f}, at or above the USD {item_approval:.0f} approval threshold.",
                    "policy_source_ids": [rules["manager_approval_source_id"]],
                }
            )

        if allowed > 0:
            reimbursable.append(
                {
                    "description": description,
                    "amount": round(allowed, 2),
                    "policy_source_ids": sources or ["policy-travel-002"],
                    "reason": "Within policy." if allowed == amount else "Reimbursable up to the policy limit.",
                }
            )

    total = round(sum(line["amount"] for line in reimbursable), 2)
    if total >= report_approval:
        approvals.append(
            {
                "approval_type": "finance",
                "reason": f"Report total of USD {total:.2f} is at or above the USD {report_approval:.0f} finance approval threshold.",
                "policy_source_ids": [rules["manager_approval_source_id"]],
            }
        )

    return {
        "reimbursable_items": reimbursable,
        "non_reimbursable_items": non_reimbursable,
        "missing_information": missing_information,
        "approvals_required": _dedupe(approvals),
        "total_reimbursable": total,
        "total_submitted": round(sum(float(item["amount"]) for item in items), 2),
    }


def _dedupe(approvals: list[dict[str, Any]]) -> list[dict[str, Any]]:
    seen: set[tuple[str, str]] = set()
    unique = []
    for approval in approvals:
        key = (approval["approval_type"], approval["reason"])
        if key not in seen:
            seen.add(key)
            unique.append(approval)
    return unique


def request_human_approval(action: str, reason: str, amount: float | None = None) -> dict[str, Any]:
    """Simulated approval gate.

    Level 1 keeps this a local function, but the contract is the real one: the
    agent must stop and surface the request rather than assume approval. The
    default answer is no, because an unattended agent must never talk itself
    into a financial action.
    """
    approved = action == "prepare_report"
    return {
        "action": action,
        "reason": reason,
        "amount": amount,
        "approved": approved,
        "decision_by": "simulated_approver",
        "note": (
            "Draft preparation is permitted."
            if approved
            else "Only the employee may submit an expense report (policy-submission-001). "
            "The agent may prepare a draft and hand it over."
        ),
    }


TOOL_FUNCTIONS: dict[str, Callable[..., dict[str, Any]]] = {
    "search_policy": search_policy,
    "lookup_receipt": lookup_receipt,
    "calculate_reimbursement": calculate_reimbursement,
    "request_human_approval": request_human_approval,
}

assert set(TOOL_FUNCTIONS) == set(TOOL_SCHEMAS), "tool functions and schemas must stay in sync"
