"""Render Acme benchmark results as a deterministic Markdown report."""

from __future__ import annotations

from collections import defaultdict
from typing import Any


def build_report(summary: dict[str, Any]) -> str:
    lines = [
        "# Acme Benchmark Report",
        "",
        f"- model: {summary['model']}",
        f"- tasks: {summary['task_count']}",
        f"- passed: {summary['passed']}",
        f"- success_rate: {summary['success_rate']:.3f}",
        f"- cost_usd: {summary['cost_usd']:.4f}",
        f"- latency_ms_p50: {summary['latency_ms_p50']}",
        f"- latency_ms_p95: {summary['latency_ms_p95']}",
        f"- rubric_agreement_rate: {summary['rubric_agreement']['agreement_rate']:.3f}",
        f"- rubric_agreement_sample_size: {summary['rubric_agreement']['sample_size']}",
        "",
        "## Success By Tag",
        "",
        "| Tag | Passed | Total | Rate |",
        "| --- | ---: | ---: | ---: |",
    ]
    for tag, stats in sorted(summary["by_tag"].items()):
        lines.append(f"| {tag} | {stats['passed']} | {stats['total']} | {stats['rate']:.3f} |")
    lines.extend(["", "## Failures", ""])
    failures = [result for result in summary["results"] if not result["passed"]]
    if not failures:
        lines.append("No benchmark failures.")
    for result in failures:
        lines.append(f"### {result['task_id']}")
        for failure in result["failures"]:
            lines.append(f"- {failure}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def summarize(results: list[dict[str, Any]], model: str, rubric_agreement: dict[str, Any]) -> dict[str, Any]:
    passed = sum(1 for result in results if result["passed"])
    latencies = sorted(result["latency_ms"] for result in results)
    by_tag: dict[str, dict[str, int | float]] = defaultdict(lambda: {"passed": 0, "total": 0, "rate": 0.0})
    for result in results:
        for tag in result["tags"]:
            by_tag[tag]["total"] += 1
            by_tag[tag]["passed"] += int(result["passed"])
    for stats in by_tag.values():
        stats["rate"] = round(stats["passed"] / stats["total"], 3) if stats["total"] else 0.0
    return {
        "model": model,
        "task_count": len(results),
        "passed": passed,
        "success_rate": round(passed / len(results), 3) if results else 0.0,
        "cost_usd": round(sum(result["cost_usd"] for result in results), 4),
        "latency_ms_p50": _percentile(latencies, 50),
        "latency_ms_p95": _percentile(latencies, 95),
        "rubric_agreement": rubric_agreement,
        "by_tag": dict(by_tag),
        "results": results,
    }


def _percentile(values: list[int], percentile: int) -> int:
    if not values:
        return 0
    index = round((len(values) - 1) * percentile / 100)
    return values[index]

