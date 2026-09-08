import importlib

import pytest

from environments.contract import validate_environment_module


@pytest.mark.parametrize(
    "module_name",
    [
        "environments.strongbench_finance",
        "environments.code_repair",
    ],
)
def test_environment_modules_implement_shared_contract(module_name):
    module = importlib.import_module(module_name)
    metrics = validate_environment_module(module, task_count=6)

    assert metrics["task_count"] == 6
    assert metrics["reward_hacker_catch_rate"] == 1.0
