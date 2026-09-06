"""Dry-run helper for the optional Track 5B LoRA experiment.

This module intentionally does not hide a GPU dependency in the core course
path. Use `--dry-run` in CI and before starting any real training run.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

DEFAULT_CONFIG = Path(__file__).resolve().parent / "lora-config.template.json"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate the Acme LoRA training config.")
    parser.add_argument("--config", default=str(DEFAULT_CONFIG))
    parser.add_argument("--dry-run", action="store_true", help="Validate inputs and print the planned run.")
    args = parser.parse_args(argv)

    config = load_config(Path(args.config))
    plan = build_training_plan(config)
    print(json.dumps(plan, indent=2, sort_keys=True))
    if args.dry_run:
        return 0
    print("Real training is optional Track 5B work and requires selecting a model, GPU environment, and training stack.")
    return 2


def load_config(path: Path) -> dict[str, Any]:
    config = json.loads(path.read_text(encoding="utf-8"))
    required = {"base_model", "dataset", "hyperparameters", "method", "status"}
    missing = required - set(config)
    if missing:
        raise ValueError(f"{path}: missing required config keys: {sorted(missing)}")
    return config


def build_training_plan(config: dict[str, Any]) -> dict[str, Any]:
    train_path = Path(config["dataset"]["train"])
    dev_path = Path(config["dataset"]["dev"])
    checks = {
        "train_exists": train_path.exists(),
        "dev_exists": dev_path.exists(),
        "train_rows": count_jsonl(train_path) if train_path.exists() else 0,
        "dev_rows": count_jsonl(dev_path) if dev_path.exists() else 0,
    }
    return {
        "status": "dry_run_ready" if all(checks.values()) else "blocked_missing_inputs",
        "method": config["method"],
        "base_model": config["base_model"],
        "dataset": config["dataset"],
        "hyperparameters": config["hyperparameters"],
        "compute_estimate": config.get("compute_estimate", {}),
        "checks": checks,
        "completion_requires": config["required_evidence_before_claiming_completion"],
    }


def count_jsonl(path: Path) -> int:
    with open(path, encoding="utf-8") as handle:
        return sum(1 for line in handle if line.strip())


if __name__ == "__main__":
    raise SystemExit(main())
