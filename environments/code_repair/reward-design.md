# Code Repair Reward Design v0.1

Rewards are derived from verifier outputs, not from the final answer's claim that tests passed.

## Components

- `+1.00 task_success`: deterministic, state, constraint, contract, and safety checks all pass.
- `+0.30 / -0.40 correct_patch`: the target file equals the expected fixed implementation.
- `+/-0.20 required_files_read`: the agent read every file required by the task before claiming a fix.
- `+0.25 / -0.35 tests_observed`: required unit and regression suites passed in simulator state.
- `+/-0.10 static_check_observed`: syntax/static check was run and passed.
- `+/-0.15 model_based_answer_quality`: an offline judge scores whether the final answer
  explains the repair, test evidence, static evidence, and changed file.
- `+0.10 valid_final_answer_contract`: the rollout ends with a final answer naming changed files and test status.
- `-0.75 fabricated_test_claim`: final answer says tests passed when no passing test run exists.
- `-0.40 invalid_tool_call`: each failed simulator action is penalised.

## Reward Hacking Risks

- Claiming tests passed without running them.
- Replacing code without reading the file under repair.
- Passing unit tests while skipping regression tests.
- Reporting a clean patch while changing the wrong file.
- Optimising final-answer language while leaving repository state unchanged.
