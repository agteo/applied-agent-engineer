"""Run the Acme benchmark.

    python3 -m evals.runner --model scripted
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any

AGENT_ROOT = Path(__file__).resolve().parents[1] / "examples" / "acme-expense-agent"
if str(AGENT_ROOT) not in sys.path:
    sys.path.insert(0, str(AGENT_ROOT))

from acme_agent.agent import run_agent  # noqa: E402
from acme_agent.models import get_model  # noqa: E402
from evals.acme_benchmark.graders.deterministic import grade_task  # noqa: E402
from evals.acme_benchmark.graders.rubric import calibration_agreement, grade_quality  # noqa: E402
from evals.report import build_report, summarize  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
BENCHMARK_DIR = ROOT / "evals" / "acme_benchmark"
DEFAULT_TASKS = BENCHMARK_DIR / "tasks.jsonl"
DEFAULT_REPORT = ROOT / "evals" / "reports" / "sample-report.md"
DEFAULT_THRESHOLDS = BENCHMARK_DIR / "thresholds.json"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run the Acme benchmark.")
    parser.add_argument("--model", default="scripted", help="Model adapter: scripted or provider model name.")
    parser.add_argument("--tasks", default=str(DEFAULT_TASKS))
    parser.add_argument("--report", default=str(DEFAULT_REPORT))
    parser.add_argument("--thresholds", default=str(DEFAULT_THRESHOLDS))
    parser.add_argument("--no-threshold", action="store_true", help="Do not fail when below the committed threshold.")
    args = parser.parse_args(argv)

    tasks = load_tasks(args.tasks)
    results = run_benchmark(tasks, args.model)
    agreement = calibration_agreement(BENCHMARK_DIR / "calibration" / "human_reviewed.jsonl")
    summary = summarize(results, model=args.model, rubric_agreement=agreement)
    report = build_report(summary)

    report_path = Path(args.report)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(report, encoding="utf-8")
    print(report.rstrip())

    if args.no_threshold:
        return 0
    threshold = json.loads(Path(args.thresholds).read_text(encoding="utf-8"))["min_success_rate"]
    if summary["success_rate"] < threshold:
        print(
            f"FAIL: benchmark success_rate {summary['success_rate']:.3f} is below threshold {threshold:.3f}.",
            file=sys.stderr,
        )
        return 1
    return 0


def load_tasks(path: str | Path) -> list[dict[str, Any]]:
    tasks = []
    with open(path, encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            line = line.strip()
            if not line:
                continue
            task = json.loads(line)
            if task["id"] in {existing["id"] for existing in tasks}:
                raise ValueError(f"{path}:{line_number}: duplicate task id {task['id']!r}")
            tasks.append(task)
    if len(tasks) != 100:
        raise ValueError(f"{path}: expected 100 benchmark tasks, found {len(tasks)}.")
    return tasks


def run_benchmark(tasks: list[dict[str, Any]], model_name: str) -> list[dict[str, Any]]:
    results = []
    for task in tasks:
        model = get_model(model_name, employee_id=task["employee_id"])
        outcome = run_agent(task["prompt"], model=model, task_id=task["id"])
        trace = outcome.trace.to_dict()
        if model_name == "scripted":
            trace["metadata"]["latency_ms"] = 0
        grade = grade_task(task, trace)
        results.append(
            {
                **grade,
                "tags": task["tags"],
                "category": task["category"],
                "difficulty": task["difficulty"],
                "latency_ms": int(trace.get("metadata", {}).get("latency_ms", 0)),
                "cost_usd": _cost_usd(trace),
                "quality": grade_quality(task, trace),
            }
        )
    return results


def _cost_usd(trace: dict[str, Any]) -> float:
    # Scripted runs are free. Provider pricing is intentionally not embedded in
    # the benchmark; real-model reports can fill this in from adapter metadata.
    if trace.get("model") == "scripted-reference-v1":
        return 0.0
    return 0.0


if __name__ == "__main__":
    raise SystemExit(main())

