"""Domain-agnostic environment runner.

Example:
    python3 -m environments.runner environments.code_repair
"""

from __future__ import annotations

import argparse
import importlib
import json
from pathlib import Path

from environments.contract import write_validated_environment


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build any course environment that implements the shared contract.")
    parser.add_argument("module", help="Import path, for example environments.code_repair")
    parser.add_argument("--out", required=True, help="Output directory for generated artifacts")
    parser.add_argument("--tasks", type=int, default=None, help="Optional task count override")
    args = parser.parse_args(argv)

    module = importlib.import_module(args.module)
    metrics = write_validated_environment(module, Path(args.out), task_count=args.tasks)
    print(json.dumps({"module": args.module, "metrics": metrics}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
