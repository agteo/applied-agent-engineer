"""Fixture loading. All Acme data is local JSON, never a live system."""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any

FIXTURE_DIR = Path(__file__).resolve().parent.parent / "fixtures"


@lru_cache(maxsize=None)
def _load(name: str) -> dict[str, Any]:
    with open(FIXTURE_DIR / name, encoding="utf-8") as handle:
        return json.load(handle)


def policies() -> dict[str, Any]:
    return _load("policies.json")


def policy_sections() -> list[dict[str, Any]]:
    return policies()["sections"]


def rules() -> dict[str, Any]:
    return policies()["rules"]


def receipts() -> list[dict[str, Any]]:
    return _load("receipts.json")["receipts"]


def employees() -> list[dict[str, Any]]:
    return _load("employees.json")["employees"]


def tasks() -> list[dict[str, Any]]:
    return _load("tasks.json")["tasks"]
