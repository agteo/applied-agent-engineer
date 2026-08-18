"""Tool schemas and the final-answer contract for Acme Expense Agent v1.

Schemas are data, not code. Level 2 graders, Level 3 diagnosis, and Level 4
dataset conversion all read these same definitions, so keep them stable and
version them when they change.
"""

from __future__ import annotations

from typing import Any

EXPENSE_CATEGORIES = ["meals", "travel", "lodging", "entertainment", "alcohol", "other"]

SEARCH_POLICY_SCHEMA: dict[str, Any] = {
    "name": "search_policy",
    "description": (
        "Search the Acme expense policy corpus and return the most relevant "
        "sections with their source ids. Use this before making any claim "
        "about what policy allows."
    ),
    "permission": "read",
    "input_schema": {
        "type": "object",
        "properties": {
            "query": {"type": "string"},
            "category": {"type": "string", "enum": ["meals", "travel", "lodging", "receipts", "approval", "submission"]},
            "top_k": {"type": "integer", "minimum": 1, "maximum": 10},
        },
        "required": ["query"],
        "additionalProperties": False,
    },
}

LOOKUP_RECEIPT_SCHEMA: dict[str, Any] = {
    "name": "lookup_receipt",
    "description": "Look up receipts for an employee, optionally filtered by merchant, date, category, or amount.",
    "permission": "read",
    "input_schema": {
        "type": "object",
        "properties": {
            "employee_id": {"type": "string"},
            "merchant": {"type": "string"},
            "date": {"type": "string", "format": "date"},
            "category": {"type": "string", "enum": EXPENSE_CATEGORIES},
            "amount": {"type": "number", "minimum": 0},
            "trip_id": {"type": "string"},
        },
        "required": ["employee_id"],
        "additionalProperties": False,
    },
}

CALCULATE_REIMBURSEMENT_SCHEMA: dict[str, Any] = {
    "name": "calculate_reimbursement",
    "description": (
        "Apply the Acme expense rules to a list of items and return the "
        "reimbursable total, non-reimbursable items, missing information, and "
        "approvals required. Every decision comes back with a policy source id."
    ),
    "permission": "read",
    "input_schema": {
        "type": "object",
        "properties": {
            "items": {
                "type": "array",
                "minItems": 1,
                "items": {
                    "type": "object",
                    "properties": {
                        "description": {"type": "string"},
                        "amount": {"type": "number", "minimum": 0},
                        "category": {"type": "string", "enum": EXPENSE_CATEGORIES},
                        "date": {"type": "string", "format": "date"},
                        "has_receipt": {"type": "boolean"},
                        "nights": {"type": "integer", "minimum": 1},
                        "receipt_id": {"type": "string"},
                    },
                    "required": ["description", "amount", "category"],
                    "additionalProperties": False,
                },
            }
        },
        "required": ["items"],
        "additionalProperties": False,
    },
}

REQUEST_HUMAN_APPROVAL_SCHEMA: dict[str, Any] = {
    "name": "request_human_approval",
    "description": (
        "Ask a human before preparing or submitting anything with financial or "
        "external consequences. Required before any submit action."
    ),
    "permission": "write",
    "input_schema": {
        "type": "object",
        "properties": {
            "action": {"type": "string", "enum": ["prepare_report", "submit_report", "notify_manager"]},
            "reason": {"type": "string"},
            "amount": {"type": "number", "minimum": 0},
        },
        "required": ["action", "reason"],
        "additionalProperties": False,
    },
}

TOOL_SCHEMAS: dict[str, dict[str, Any]] = {
    schema["name"]: schema
    for schema in (
        SEARCH_POLICY_SCHEMA,
        LOOKUP_RECEIPT_SCHEMA,
        CALCULATE_REIMBURSEMENT_SCHEMA,
        REQUEST_HUMAN_APPROVAL_SCHEMA,
    )
}

_LINE_ITEM_SCHEMA = {
    "type": "object",
    "properties": {
        "description": {"type": "string"},
        "amount": {"type": "number", "minimum": 0},
        "policy_source_ids": {"type": "array", "items": {"type": "string"}},
        "reason": {"type": "string"},
    },
    "required": ["description", "amount", "policy_source_ids"],
    "additionalProperties": False,
}

FINAL_ANSWER_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "summary": {"type": "string"},
        "reimbursable_items": {"type": "array", "items": _LINE_ITEM_SCHEMA},
        "non_reimbursable_items": {"type": "array", "items": _LINE_ITEM_SCHEMA},
        "missing_information": {"type": "array", "items": {"type": "string"}},
        "approvals_required": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "approval_type": {"type": "string", "enum": ["manager", "finance", "employee"]},
                    "reason": {"type": "string"},
                    "policy_source_ids": {"type": "array", "items": {"type": "string"}},
                },
                "required": ["approval_type", "reason"],
                "additionalProperties": False,
            },
        },
        "total_reimbursable": {"type": "number", "minimum": 0},
        "confidence": {"type": "string", "enum": ["low", "medium", "high"]},
        "next_action": {"type": "string"},
        # Not required, so an answer matching the contract in the Level 1
        # project spec still validates. Populate it: a policy answer with no
        # line items has nowhere else to show its grounding.
        "cited_policy_source_ids": {"type": "array", "items": {"type": "string"}},
    },
    "required": [
        "summary",
        "reimbursable_items",
        "non_reimbursable_items",
        "missing_information",
        "approvals_required",
        "total_reimbursable",
        "confidence",
        "next_action",
    ],
    "additionalProperties": False,
}


def anthropic_tool_definitions() -> list[dict[str, Any]]:
    """Render the tool schemas in the shape the Anthropic Messages API expects."""
    return [
        {
            "name": schema["name"],
            "description": schema["description"],
            "input_schema": schema["input_schema"],
        }
        for schema in TOOL_SCHEMAS.values()
    ]
