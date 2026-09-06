"""Offline rubric grader and calibration agreement."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .deterministic import grade_task


def grade_quality(task: dict[str, Any], trace: dict[str, Any]) -> str:
    deterministic = grade_task(task, trace)
    if not deterministic["passed"]:
        return "low"
    answer = trace.get("final_answer") or {}
    cited = bool(answer.get("cited_policy_source_ids")) or any(
        line.get("policy_source_ids")
        for group in ("reimbursable_items", "non_reimbursable_items")
        for line in answer.get(group, [])
    )
    has_next_action = bool(answer.get("next_action"))
    if cited and has_next_action:
        return "high"
    return "medium"


def calibration_agreement(path: str | Path) -> dict[str, Any]:
    rows = []
    with open(path, encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    if not rows:
        return {"sample_size": 0, "matches": 0, "agreement_rate": 0.0}
    matches = sum(row["human_label"] == row["rubric_label"] for row in rows)
    return {
        "sample_size": len(rows),
        "matches": matches,
        "agreement_rate": round(matches / len(rows), 3),
    }

