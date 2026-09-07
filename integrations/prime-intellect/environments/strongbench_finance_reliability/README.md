# strongbench_finance_reliability

A Verifiers-shaped adapter over `environments/strongbench_finance`. It adds no scoring
logic: tasks, state transitions, verifiers, and rewards all come from the local
simulator, which stays the source of truth.

## Run it offline

```bash
python3 integrations/prime-intellect/environments/strongbench_finance_reliability/strongbench_finance_reliability.py
```

That serves 120 tasks, rolls out the reference policy and the reward-hacking
probe, and fails if the reward does not separate them.

## Use it as a library

```python
from strongbench_finance_reliability import load_environment

env = load_environment(seed=42, task_count=120)
rows = env.dataset()                     # prompt / info / answer
result = env.evaluate("scripted_reference")
reward = env.reward(task_id, observations, terminal_state)
```

`env.score()` and `env.reward()` accept rollouts produced by any policy,
including one running on hosted infrastructure. The grading key (`answer`) must
never be handed to a policy at rollout time.

## Hosted path

`load_verifiers_environment()` wraps the same object for the `verifiers`
package. It is **unvalidated** — no hosted run has exercised it. Read
[`../../VALIDATION.md`](../../VALIDATION.md) first.
