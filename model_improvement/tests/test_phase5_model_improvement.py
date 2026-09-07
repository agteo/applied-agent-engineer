import json

from model_improvement.strongbench import DEFAULT_OUT, build_phase5_bundle, write_phase5_bundle
from model_improvement.strongbench.train_lora import build_training_plan, load_config


def test_phase5_decision_uses_benchmark_failures_and_dataset():
    bundle = build_phase5_bundle()
    decision = bundle["decision"]
    metrics = bundle["sft_metrics"]

    assert decision["benchmark_success_rate"] == 0.89
    assert decision["benchmark_passed"] is True
    assert decision["decision"] == "fix_tools_and_retrieval_before_training"
    assert decision["tool_or_retrieval_failure_labels"] > decision["model_failure_labels"]
    assert metrics["by_split"]["train"] == 78
    assert metrics["by_split"]["dev"] == 47
    assert metrics["rejected_count"] == 27
    assert metrics["rejection_reasons"] == {"heldout_reserved_for_evaluation": 27}


def test_phase5_writes_sft_export_and_decision_artifacts(tmp_path):
    bundle = build_phase5_bundle()
    write_phase5_bundle(bundle, tmp_path)

    expected_files = {
        "sft-train.jsonl",
        "sft-dev.jsonl",
        "sft-rejected.jsonl",
        "sft-schema.json",
        "metrics.json",
        "decision.json",
        "decision-memo.md",
        "comparison-report.md",
        "intervention-matrix.json",
        "lora-config.template.json",
        "gateway-plan.json",
    }
    assert expected_files <= {path.name for path in tmp_path.iterdir()}

    first_train = json.loads((tmp_path / "sft-train.jsonl").read_text(encoding="utf-8").splitlines()[0])
    assert first_train["messages"][0]["role"] == "system"
    assert first_train["messages"][-1]["role"] == "assistant"
    assert first_train["split"] == "train"
    assert first_train["provenance"]["source_dataset"] == "datasets/strongbench/cleaned.jsonl"

    config = json.loads((tmp_path / "lora-config.template.json").read_text(encoding="utf-8"))
    assert config["status"] == "template_not_run"
    assert "Level 2 benchmark comparison" in config["required_evidence_before_claiming_completion"]


def test_default_phase5_output_path_is_under_model_improvement():
    assert "model_improvement/strongbench" in str(DEFAULT_OUT)


def test_lora_dry_run_plan_validates_generated_config(tmp_path):
    bundle = build_phase5_bundle()
    write_phase5_bundle(bundle, tmp_path)

    config = load_config(tmp_path / "lora-config.template.json")
    plan = build_training_plan(config)

    assert plan["status"] == "dry_run_ready"
    assert plan["checks"]["train_rows"] == 78
    assert plan["checks"]["dev_rows"] == 47
    assert plan["compute_estimate"]["ci_mode"] == "dry-run only"
