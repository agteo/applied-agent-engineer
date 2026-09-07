from evals.operations import DEFAULT_OUT, build_bundle, write_bundle
from evals.runner import BENCHMARK_DIR, load_tasks


def test_phase3_bundle_has_annotated_failures_and_regression_pack(tmp_path):
    bundle = build_bundle(load_tasks(BENCHMARK_DIR / "tasks.jsonl"))
    assert len(bundle["annotations"]) >= 30
    assert bundle["distribution"]["annotation_count"] == len(bundle["annotations"])
    assert bundle["regression_pack"]
    first = bundle["annotations"][0]
    assert first["taxonomy_labels"]
    assert first["trace"]["task_id"] == first["task_id"]

    write_bundle(bundle, tmp_path)
    assert (tmp_path / "annotated-failures.jsonl").exists()
    assert (tmp_path / "regression-pack.jsonl").exists()
    assert (tmp_path / "failure-report.md").exists()
    assert (tmp_path / "instructor-review-guide.md").exists()
    assert (tmp_path / "intervention-experiment.md").exists()


def test_default_phase3_output_path_is_under_evals():
    assert "evals/operations/strongbench" in str(DEFAULT_OUT)
