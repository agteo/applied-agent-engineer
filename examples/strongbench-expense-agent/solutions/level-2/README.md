# Level 2 Reference Solutions

These are the reference artifacts for the Level 2 evaluation labs.

| Lab | Reference artifact |
| --- | --- |
| Lab 1: Eval Task Schema | [`evals/strongbench_benchmark/schema.json`](../../../../evals/strongbench_benchmark/schema.json) and [`evals/strongbench_benchmark/tasks.jsonl`](../../../../evals/strongbench_benchmark/tasks.jsonl) |
| Lab 2: Deterministic Graders | [`evals/strongbench_benchmark/graders/deterministic.py`](../../../../evals/strongbench_benchmark/graders/deterministic.py) and [`evals/strongbench_benchmark/graders/contract.py`](../../../../evals/strongbench_benchmark/graders/contract.py) |
| Lab 3: Rubric Judge | [`evals/strongbench_benchmark/graders/rubric.md`](../../../../evals/strongbench_benchmark/graders/rubric.md), [`evals/strongbench_benchmark/graders/rubric.py`](../../../../evals/strongbench_benchmark/graders/rubric.py), and [`evals/strongbench_benchmark/calibration/human_reviewed.jsonl`](../../../../evals/strongbench_benchmark/calibration/human_reviewed.jsonl) |
| Lab 4: Eval Report | [`evals/report.py`](../../../../evals/report.py) and [`evals/reports/sample-report.md`](../../../../evals/reports/sample-report.md) |

The reference solution deliberately leaves visible failures in the scripted
baseline. A benchmark that only celebrates passing cases is not useful for
diagnosis, data work, or regression testing.

