from pathlib import Path

from evals.strongbench_benchmark.graders.deterministic import grade_task
from evals.strongbench_benchmark.graders.rubric import calibration_agreement
from evals.runner import BENCHMARK_DIR, load_tasks, run_benchmark
from evals.report import build_report, summarize


def test_benchmark_has_100_tasks_and_domain_field():
    tasks = load_tasks(BENCHMARK_DIR / "tasks.jsonl")
    assert len(tasks) == 100
    assert {task["domain"] for task in tasks} == {"strongbench_expense"}
    assert len({task["id"] for task in tasks}) == 100


def test_grader_failure_names_task_id_and_field():
    task = load_tasks(BENCHMARK_DIR / "tasks.jsonl")[20]
    trace = {"task_id": task["id"], "final_answer": {"total_reimbursable": 999.0}, "steps": []}
    result = grade_task(task, trace)
    assert not result["passed"]
    assert any(failure.startswith(f"{task['id']}: total_reimbursable:") for failure in result["failures"])


def test_scripted_benchmark_clears_release_gate():
    tasks = load_tasks(BENCHMARK_DIR / "tasks.jsonl")
    results = run_benchmark(tasks, "scripted")
    summary = summarize(results, "scripted", calibration_agreement(BENCHMARK_DIR / "calibration" / "human_reviewed.jsonl"))
    assert summary["task_count"] == 100
    assert summary["success_rate"] >= 0.72
    assert "calculation" in summary["by_tag"]


def test_report_is_deterministic_for_same_results(tmp_path):
    results = run_benchmark(load_tasks(BENCHMARK_DIR / "tasks.jsonl"), "scripted")
    agreement = calibration_agreement(BENCHMARK_DIR / "calibration" / "human_reviewed.jsonl")
    first = build_report(summarize(results, "scripted", agreement))
    second = build_report(summarize(results, "scripted", agreement))
    assert first == second
    path = Path(tmp_path / "report.md")
    path.write_text(first, encoding="utf-8")
    assert "rubric_agreement_rate" in first

