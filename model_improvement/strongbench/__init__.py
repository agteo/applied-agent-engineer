"""Build Phase 5 StrongBench model-improvement artifacts.

    python3 -m model_improvement.strongbench
"""

from __future__ import annotations

from collections import Counter
import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from datasets.strongbench import DEFAULT_OUT as DATASET_DIR
from datasets.strongbench import build_dataset, write_dataset
from evals.strongbench_benchmark.graders.rubric import calibration_agreement
from evals.report import summarize
from evals.runner import BENCHMARK_DIR, DEFAULT_TASKS, load_tasks, run_benchmark

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUT = ROOT / "model_improvement" / "strongbench"
DEFAULT_DATASET_DIR = DATASET_DIR

SYSTEM_PROMPT = (
    "You are the StrongBench Expense Agent. Answer with the structured final-answer "
    "contract used by the course fixtures. Cite policy source ids when they "
    "support reimbursement, approval, or missing-information decisions."
)

SFT_SCHEMA: dict[str, Any] = {
    "type": "object",
    "required": ["schema_version", "example_id", "split", "messages", "source_example_id", "labels"],
    "properties": {
        "schema_version": {"type": "string"},
        "example_id": {"type": "string"},
        "split": {"type": "string", "enum": ["train", "dev"]},
        "messages": {"type": "array"},
        "source_example_id": {"type": "string"},
        "source_type": {"type": "string"},
        "labels": {"type": "array", "items": {"type": "string"}},
        "provenance": {"type": "object"},
    },
}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build Phase 5 StrongBench model-improvement artifacts.")
    parser.add_argument("--out", default=str(DEFAULT_OUT))
    parser.add_argument("--dataset-dir", default=str(DEFAULT_DATASET_DIR))
    args = parser.parse_args(argv)

    bundle = build_phase5_bundle(Path(args.dataset_dir))
    write_phase5_bundle(bundle, Path(args.out))
    print(bundle["decision_memo"].rstrip())
    return 0


def build_phase5_bundle(dataset_dir: Path = DEFAULT_DATASET_DIR) -> dict[str, Any]:
    ensure_dataset_artifacts(dataset_dir)
    dataset_rows = read_jsonl(dataset_dir / "cleaned.jsonl")
    dataset_metrics = json.loads((dataset_dir / "metrics.json").read_text(encoding="utf-8"))

    tasks = load_tasks(DEFAULT_TASKS)
    results = run_benchmark(tasks, "scripted")
    agreement = calibration_agreement(BENCHMARK_DIR / "calibration" / "human_reviewed.jsonl")
    benchmark_summary = summarize(results, model="scripted", rubric_agreement=agreement)
    threshold = json.loads((BENCHMARK_DIR / "thresholds.json").read_text(encoding="utf-8"))["min_success_rate"]

    sft_examples, rejected = prepare_sft_examples(dataset_rows)
    sft_metrics = build_sft_metrics(sft_examples, rejected)
    failure_distribution = load_failure_distribution()
    decision = build_decision(benchmark_summary, threshold, dataset_metrics, sft_metrics, failure_distribution)
    comparison = build_comparison_report(benchmark_summary, threshold, decision)

    return {
        "sft_examples": sft_examples,
        "rejected": rejected,
        "sft_metrics": sft_metrics,
        "benchmark_summary": benchmark_summary,
        "decision": decision,
        "decision_memo": render_decision_memo(decision),
        "comparison_report": comparison,
        "intervention_matrix": build_intervention_matrix(benchmark_summary, failure_distribution),
        "training_config": build_lora_config(sft_metrics),
        "gateway_plan": build_gateway_plan(),
    }


def ensure_dataset_artifacts(dataset_dir: Path) -> None:
    required = ["cleaned.jsonl", "metrics.json"]
    if all((dataset_dir / name).exists() for name in required):
        return
    bundle = build_dataset()
    write_dataset(bundle, dataset_dir)


def prepare_sft_examples(rows: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    examples = []
    rejected = []
    for row in rows:
        reason = sft_rejection_reason(row)
        if reason:
            rejected.append({"source_example_id": row.get("example_id"), "reason": reason, "split": row.get("split")})
            continue
        examples.append(
            {
                "schema_version": "1.0.0",
                "example_id": f"sft-{row['example_id']}",
                "source_example_id": row["example_id"],
                "source_type": row["source_type"],
                "split": row["split"],
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": row["prompt"]},
                    {"role": "assistant", "content": json.dumps(row["target_final_answer"], sort_keys=True)},
                ],
                "labels": row["labels"],
                "provenance": {
                    "source_dataset": "datasets/strongbench/cleaned.jsonl",
                    "source_fingerprint": stable_fingerprint(row),
                },
            }
        )
    return examples, rejected


def sft_rejection_reason(row: dict[str, Any]) -> str | None:
    if row.get("split") == "heldout":
        return "heldout_reserved_for_evaluation"
    if row.get("split") not in {"train", "dev"}:
        return "invalid_split"
    if not row.get("prompt"):
        return "missing_prompt"
    if not isinstance(row.get("target_final_answer"), dict):
        return "invalid_target"
    if not row.get("provenance"):
        return "missing_provenance"
    if row.get("source_type") == "failure_correction" and row.get("split") == "train":
        return "benchmark_correction_train_leakage"
    return None


def build_sft_metrics(examples: list[dict[str, Any]], rejected: list[dict[str, Any]]) -> dict[str, Any]:
    by_split = Counter(row["split"] for row in examples)
    by_source = Counter(row["source_type"] for row in examples)
    by_rejection = Counter(row["reason"] for row in rejected)
    return {
        "accepted_count": len(examples),
        "rejected_count": len(rejected),
        "by_split": dict(sorted(by_split.items())),
        "by_source_type": dict(sorted(by_source.items())),
        "rejection_reasons": dict(sorted(by_rejection.items())),
        "heldout_policy": "Heldout dataset rows are rejected from SFT export and remain evaluation-only.",
    }


def load_failure_distribution() -> dict[str, Any]:
    path = ROOT / "evals" / "operations" / "strongbench" / "failure-distribution.json"
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {"annotation_count": 0, "by_label": {}, "by_category": {}, "by_config": {}}


def build_decision(
    benchmark_summary: dict[str, Any],
    threshold: float,
    dataset_metrics: dict[str, Any],
    sft_metrics: dict[str, Any],
    failure_distribution: dict[str, Any],
) -> dict[str, Any]:
    labels = failure_distribution.get("by_label", {})
    tool_or_retrieval = sum(count for label, count in labels.items() if label.startswith("TOOLS.") or label.startswith("RETRIEVAL."))
    model_failures = sum(count for label, count in labels.items() if label.startswith("MODEL."))
    recommendation = "fix_tools_and_retrieval_before_training"
    rationale = (
        "The benchmark clears the release gate, and the dominant annotated failures are tool or retrieval related. "
        "Use the SFT export for Track 5B rehearsal, but do not claim model improvement until tool behavior is fixed and a heldout benchmark comparison improves."
    )
    if model_failures > tool_or_retrieval and sft_metrics["by_split"].get("train", 0) >= 50:
        recommendation = "run_small_sft_after_baseline_comparison"
        rationale = (
            "Model-labeled failures dominate and there is enough train data for a small SFT experiment. "
            "Run the adapter only after freezing the benchmark and preserving heldout rows."
        )
    return {
        "decision": recommendation,
        "benchmark_success_rate": benchmark_summary["success_rate"],
        "release_threshold": threshold,
        "benchmark_passed": benchmark_summary["success_rate"] >= threshold,
        "dataset_cleaned_count": dataset_metrics["cleaned_count"],
        "sft_train_count": sft_metrics["by_split"].get("train", 0),
        "sft_dev_count": sft_metrics["by_split"].get("dev", 0),
        "sft_rejected_count": sft_metrics["rejected_count"],
        "tool_or_retrieval_failure_labels": tool_or_retrieval,
        "model_failure_labels": model_failures,
        "rationale": rationale,
        "next_experiment": "Improve receipt lookup arguments and rerun the Level 2 benchmark before any LoRA run.",
        "adoption_gate": "Adopt a trained or local model only if heldout benchmark success improves without increasing unsafe submission failures.",
    }


def build_intervention_matrix(
    benchmark_summary: dict[str, Any],
    failure_distribution: dict[str, Any],
) -> list[dict[str, Any]]:
    labels = failure_distribution.get("by_label", {})
    return [
        {
            "intervention": "tool_and_retrieval_fix",
            "status": "recommended_next",
            "evidence": "Most annotated failure labels are TOOLS.* or RETRIEVAL.*.",
            "success_measure": "Receipt_lookup and citation slices improve on the Level 2 benchmark.",
        },
        {
            "intervention": "prompt_revision",
            "status": "use_as_low_cost_control",
            "evidence": f"Current scripted baseline success_rate is {benchmark_summary['success_rate']:.3f}.",
            "success_measure": "No regression below release threshold and fewer approval-boundary failures.",
        },
        {
            "intervention": "small_lora_sft",
            "status": "defer_until_tool_plateau",
            "evidence": f"Model labels: {sum(count for label, count in labels.items() if label.startswith('MODEL.'))}.",
            "success_measure": "Heldout benchmark improvement plus unchanged or better unsafe_submission rate.",
        },
        {
            "intervention": "frontier_api_or_hybrid",
            "status": "compare_if_quality_gap_remains",
            "evidence": "No paid or network-backed model run is required for the core course path.",
            "success_measure": "Quality lift justifies cost, latency, privacy, and vendor tradeoffs.",
        },
    ]


def build_comparison_report(benchmark_summary: dict[str, Any], threshold: float, decision: dict[str, Any]) -> str:
    return (
        "# StrongBench Model Comparison Report\n\n"
        "## Current Evidence\n\n"
        f"- scripted baseline success_rate: {benchmark_summary['success_rate']:.3f}\n"
        f"- release threshold: {threshold:.3f}\n"
        f"- benchmark passed: {str(benchmark_summary['success_rate'] >= threshold).lower()}\n"
        f"- SFT train/dev rows: {decision['sft_train_count']}/{decision['sft_dev_count']}\n\n"
        "## Comparison Table\n\n"
        "| Candidate | Evidence Status | Decision |\n"
        "| --- | --- | --- |\n"
        "| Current scripted/tool baseline | Measured on 100 tasks | Keep as baseline gate |\n"
        "| Tool and retrieval fixes | Supported by Phase 3 failure labels | Build next |\n"
        "| Small LoRA/SFT adapter | Data prepared, no training run yet | Defer adoption claim |\n"
        "| Frontier or hybrid API | Not measured in offline course path | Optional comparison |\n\n"
        "## Recommendation\n\n"
        f"{decision['rationale']}\n"
    )


def render_decision_memo(decision: dict[str, Any]) -> str:
    return (
        "# StrongBench Model Improvement Decision Memo\n\n"
        "## Decision\n\n"
        f"{decision['decision']}\n\n"
        "## Evidence\n\n"
        f"- Level 2 benchmark success_rate: {decision['benchmark_success_rate']:.3f}\n"
        f"- release threshold: {decision['release_threshold']:.3f}\n"
        f"- benchmark gate passed: {str(decision['benchmark_passed']).lower()}\n"
        f"- Level 4 cleaned rows: {decision['dataset_cleaned_count']}\n"
        f"- SFT export train/dev rows: {decision['sft_train_count']}/{decision['sft_dev_count']}\n"
        f"- SFT rejected rows: {decision['sft_rejected_count']}\n"
        f"- tool or retrieval failure labels: {decision['tool_or_retrieval_failure_labels']}\n"
        f"- model failure labels: {decision['model_failure_labels']}\n\n"
        "## Rationale\n\n"
        f"{decision['rationale']}\n\n"
        "## Next Experiment\n\n"
        f"{decision['next_experiment']}\n\n"
        "## Adoption Gate\n\n"
        f"{decision['adoption_gate']}\n"
    )


def build_lora_config(sft_metrics: dict[str, Any]) -> dict[str, Any]:
    return {
        "purpose": "Track 5B optional small LoRA/SFT experiment configuration.",
        "status": "template_not_run",
        "base_model": "choose-small-instruct-model-locally",
        "dataset": {
            "train": "model_improvement/strongbench/sft-train.jsonl",
            "dev": "model_improvement/strongbench/sft-dev.jsonl",
            "train_rows": sft_metrics["by_split"].get("train", 0),
            "dev_rows": sft_metrics["by_split"].get("dev", 0),
        },
        "method": "LoRA",
        "hyperparameters": {
            "epochs": 1,
            "learning_rate": 0.0002,
            "lora_rank": 8,
            "lora_alpha": 16,
            "max_sequence_length": 2048,
        },
        "compute_estimate": {
            "ci_mode": "dry-run only",
            "reference_gpu": "single 16-24GB VRAM GPU for a small instruct model",
            "expected_runtime": "minutes to low hours depending on selected model and hardware",
            "cost_note": "Core Phase 5 does not require paid compute; Track 5B completion requires a real run.",
        },
        "required_evidence_before_claiming_completion": [
            "training logs",
            "adapter or checkpoint artifact",
            "Level 2 benchmark comparison",
            "unsafe_submission slice check",
        ],
    }


def build_gateway_plan() -> dict[str, Any]:
    return {
        "purpose": "Track 5C local inference gateway drill plan.",
        "aliases": {
            "primary": "strongbench-local-primary",
            "fallback": "strongbench-hosted-fallback",
            "agent": "strongbench-agent-model",
        },
        "drills": [
            "normal local serving",
            "local worker unavailable before benchmark slice",
            "local worker interrupted during benchmark slice",
        ],
        "measurements": ["task_success", "latency_ms", "error_rate", "fallback_rate", "quality_delta"],
    }


def write_phase5_bundle(bundle: dict[str, Any], out: Path) -> None:
    out.mkdir(parents=True, exist_ok=True)
    write_jsonl(out / "sft-train.jsonl", [row for row in bundle["sft_examples"] if row["split"] == "train"])
    write_jsonl(out / "sft-dev.jsonl", [row for row in bundle["sft_examples"] if row["split"] == "dev"])
    write_jsonl(out / "sft-rejected.jsonl", bundle["rejected"])
    (out / "sft-schema.json").write_text(json.dumps(SFT_SCHEMA, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (out / "metrics.json").write_text(json.dumps(bundle["sft_metrics"], indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (out / "decision.json").write_text(json.dumps(bundle["decision"], indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (out / "decision-memo.md").write_text(bundle["decision_memo"], encoding="utf-8")
    (out / "comparison-report.md").write_text(bundle["comparison_report"], encoding="utf-8")
    (out / "intervention-matrix.json").write_text(
        json.dumps(bundle["intervention_matrix"], indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (out / "lora-config.template.json").write_text(
        json.dumps(bundle["training_config"], indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (out / "gateway-plan.json").write_text(
        json.dumps(bundle["gateway_plan"], indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def stable_fingerprint(row: dict[str, Any]) -> str:
    payload = json.dumps(
        {"example_id": row.get("example_id"), "target": row.get("target_final_answer"), "split": row.get("split")},
        sort_keys=True,
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows = []
    with open(path, encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    with open(path, "w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, sort_keys=True) + "\n")
