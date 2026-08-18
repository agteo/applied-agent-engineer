from acme_agent import fixtures
from acme_agent.tools import (
    calculate_reimbursement,
    lookup_receipt,
    request_human_approval,
    search_policy,
)


def test_policy_search_finds_the_missing_receipt_section():
    results = search_policy("I lost my hotel receipt")["results"]
    assert results[0]["source_id"] == "policy-receipts-001"
    assert all("score" in result for result in results)


def test_policy_search_respects_category_filter():
    results = search_policy("limit", category="lodging")["results"]
    assert {result["category"] for result in results} == {"lodging"}


def test_lookup_flags_ambiguity():
    result = lookup_receipt("emp-1001")
    assert result["match_count"] > 1
    assert result["ambiguous"] is True


def test_lookup_unknown_employee_returns_an_error_not_a_crash():
    result = lookup_receipt("emp-9999")
    assert result["matches"] == []
    assert "unknown employee_id" in result["error"]


def test_lookup_filters_combine():
    result = lookup_receipt("emp-1001", category="lodging", date="2026-03-12")
    assert result["match_count"] == 1
    assert result["matches"][0]["receipt_id"] == "rec-0003"


def test_canonical_task_totals():
    result = calculate_reimbursement(
        [
            {"description": "Airport parking", "amount": 47.0, "category": "travel"},
            {"description": "Dinner", "amount": 68.0, "category": "meals", "date": "2026-03-12"},
            {"description": "Hotel", "amount": 214.0, "category": "lodging", "has_receipt": False},
        ]
    )
    assert result["total_reimbursable"] == 329.0
    assert any("Hotel" in note for note in result["missing_information"])
    assert result["approvals_required"][0]["approval_type"] == "manager"


def test_meal_daily_limit_splits_the_item():
    result = calculate_reimbursement(
        [
            {"description": "Dinner", "amount": 68.0, "category": "meals", "date": "2026-03-12"},
            {"description": "Room service", "amount": 40.0, "category": "meals", "date": "2026-03-12"},
        ]
    )
    assert result["total_reimbursable"] == 75.0
    assert result["non_reimbursable_items"][0]["amount"] == 33.0


def test_lodging_over_the_nightly_limit_needs_approval():
    result = calculate_reimbursement(
        [{"description": "Hyatt", "amount": 289.0, "category": "lodging"}]
    )
    assert result["total_reimbursable"] == 250.0
    assert result["non_reimbursable_items"][0]["amount"] == 39.0
    assert result["approvals_required"]


def test_alcohol_is_never_reimbursable():
    result = calculate_reimbursement(
        [{"description": "Bar tab", "amount": 96.0, "category": "alcohol"}]
    )
    assert result["total_reimbursable"] == 0
    assert result["non_reimbursable_items"][0]["policy_source_ids"] == ["policy-meals-002"]


def test_small_expense_without_a_receipt_is_fine():
    result = calculate_reimbursement(
        [{"description": "Coffee", "amount": 18.5, "category": "meals", "has_receipt": False}]
    )
    assert result["missing_information"] == []
    assert result["total_reimbursable"] == 18.5


def test_single_item_over_threshold_needs_manager_approval():
    result = calculate_reimbursement(
        [{"description": "United", "amount": 512.4, "category": "travel"}]
    )
    assert any("approval threshold" in entry["reason"] for entry in result["approvals_required"])


def test_every_decision_cites_a_real_policy_id():
    known = {section["source_id"] for section in fixtures.policy_sections()}
    result = calculate_reimbursement(
        [
            {"description": "Bar tab", "amount": 96.0, "category": "alcohol"},
            {"description": "Event", "amount": 640.0, "category": "entertainment"},
            {"description": "Hotel", "amount": 289.0, "category": "lodging"},
        ]
    )
    cited = {
        source_id
        for group in ("reimbursable_items", "non_reimbursable_items")
        for line in result[group]
        for source_id in line["policy_source_ids"]
    }
    assert cited <= known


def test_agent_may_prepare_but_never_submit():
    assert request_human_approval("prepare_report", "draft")["approved"] is True
    denied = request_human_approval("submit_report", "user asked")
    assert denied["approved"] is False
    assert "policy-submission-001" in denied["note"]
