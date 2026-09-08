# Resources

External resource guides for optional tooling, compute, and infrastructure.
Nothing here is required for the core Levels 1-4 path, which runs offline with
no account and no spend.

| Guide | Read it when |
| --- | --- |
| [GPU Resources](gpu.md) | Before Track 5B. It costs money; know the number before you start. |

## What is deliberately not here

- **Inference serving.** Level 5's gateway lab plans the drills and
  measurements; the serving stack itself is yours to build. See
  [`model_improvement/strongbench/gateway-plan.json`](../model_improvement/strongbench/gateway-plan.json).
- **Hosted RL.** The Prime Intellect adapter and its validation notes live in
  [`integrations/prime-intellect/`](../integrations/prime-intellect/), including
  what that path does and does not validate.
- **Model provider setup.** The course default is a deterministic offline
  adapter. The Anthropic adapter in
  [`examples/strongbench-expense-agent/strongbench_agent/models.py`](../examples/strongbench-expense-agent/strongbench_agent/models.py)
  is optional and needs no guide beyond an API key.
