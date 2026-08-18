import json

from acme_agent import fixtures
from acme_agent.agent import run_agent
from acme_agent.check_traces import check
from acme_agent.models import ScriptedModel
from acme_agent.trace import TRACE_SCHEMA_VERSION, TraceWriter, load_traces


def _run_all(path):
    writer = TraceWriter(path)
    for task in fixtures.tasks():
        run_agent(
            task["task"],
            ScriptedModel(employee_id=task["employee_id"]),
            task_id=task["task_id"],
            writer=writer,
        )
    return path


def test_every_row_loads_without_special_casing(tmp_path):
    path = _run_all(tmp_path / "traces.jsonl")
    with open(path, encoding="utf-8") as handle:
        rows = [json.loads(line) for line in handle if line.strip()]
    assert len(rows) == len(fixtures.tasks())


def test_trace_records_the_full_step_detail(tmp_path):
    path = tmp_path / "one.jsonl"
    writer = TraceWriter(path)
    run_agent(
        "I spent $47 on parking and $68 on dinner. What is my total?",
        ScriptedModel(),
        task_id="trace-001",
        writer=writer,
    )
    trace = load_traces(path)[0]
    assert trace["trace_schema_version"] == TRACE_SCHEMA_VERSION
    assert trace["task_id"] == "trace-001"
    assert trace["prompt_version"]
    tool_step = next(step for step in trace["steps"] if step["tool_name"])
    assert tool_step["tool_arguments"] is not None
    assert tool_step["validated_arguments"] is not None
    assert tool_step["observation"] is not None
    assert trace["metadata"]["stop_reason"] == "final_answer"
    assert trace["metadata"]["latency_ms"] >= 0


def test_the_level_1_bundle_passes_the_automated_check(tmp_path):
    path = _run_all(tmp_path / "traces.jsonl")
    assert check(path) == []


def test_the_check_catches_a_bad_bundle(tmp_path):
    path = tmp_path / "bad.jsonl"
    path.write_text(json.dumps({"task_id": "x", "steps": [], "final_answer": None}) + "\n")
    problems = check(path)
    assert any("at least 20" in problem for problem in problems)
    assert any("no steps" in problem for problem in problems)
    assert any("no final answer" in problem for problem in problems)


def test_malformed_json_names_the_line(tmp_path):
    path = tmp_path / "broken.jsonl"
    path.write_text('{"task_id": "ok"}\nnot json\n')
    try:
        load_traces(path)
    except ValueError as error:
        assert ":2" in str(error)
    else:
        raise AssertionError("expected a ValueError naming the bad line")
