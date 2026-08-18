"""Fixture integrity. Broken fixtures produce confusing agent failures, so the
cheapest place to catch them is here."""

from acme_agent import fixtures
from acme_agent.schemas import EXPENSE_CATEGORIES


def test_policy_rules_reference_real_sections():
    known = {section["source_id"] for section in fixtures.policy_sections()}
    referenced = {
        value
        for key, value in fixtures.rules().items()
        if key.endswith("_source_id")
    }
    assert referenced <= known


def test_policy_source_ids_are_unique():
    ids = [section["source_id"] for section in fixtures.policy_sections()]
    assert len(ids) == len(set(ids))


def test_lab_3_requires_at_least_five_policy_areas():
    categories = {section["category"] for section in fixtures.policy_sections()}
    assert {"meals", "travel", "lodging", "receipts", "approval"} <= categories


def test_receipts_belong_to_known_employees_and_categories():
    employee_ids = {employee["employee_id"] for employee in fixtures.employees()}
    for receipt in fixtures.receipts():
        assert receipt["employee_id"] in employee_ids
        assert receipt["category"] in EXPENSE_CATEGORIES
        assert receipt["amount"] > 0


def test_exit_criteria_needs_twenty_manual_tasks():
    tasks = fixtures.tasks()
    assert len(tasks) >= 20
    assert len({task["task_id"] for task in tasks}) == len(tasks)
