import json

from datasets.strongbench import DEFAULT_OUT, build_dataset, write_dataset


def test_phase4_dataset_builds_cleaned_splits_and_card(tmp_path):
    bundle = build_dataset()
    assert bundle["metrics"]["raw_count"] >= 150
    assert bundle["metrics"]["cleaned_count"] >= 100
    assert bundle["metrics"]["cleaned_count"] < bundle["metrics"]["raw_count"]
    assert bundle["metrics"]["rejected_count"] >= 3
    assert {"duplicate_prompt_target", "invalid_target_contract", "missing_provenance"} <= set(
        bundle["metrics"]["rejection_reasons"]
    )
    assert {"train", "dev", "heldout"} <= set(bundle["metrics"]["by_split"])
    assert "failure_correction" in bundle["metrics"]["by_source_type"]
    assert "Synthetic examples are template-generated" in bundle["card"]

    write_dataset(bundle, tmp_path)
    assert (tmp_path / "cleaned.jsonl").exists()
    assert (tmp_path / "train.jsonl").exists()
    assert (tmp_path / "dev.jsonl").exists()
    assert (tmp_path / "heldout.jsonl").exists()
    assert (tmp_path / "dataset-card.md").exists()
    assert (tmp_path / "rejected.jsonl").read_text(encoding="utf-8").strip()
    first = json.loads((tmp_path / "cleaned.jsonl").read_text(encoding="utf-8").splitlines()[0])
    assert first["provenance"]


def test_default_phase4_output_path_is_under_datasets():
    assert "datasets/strongbench" in str(DEFAULT_OUT)
