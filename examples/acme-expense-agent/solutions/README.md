# Level 1 Reference Solutions

Four runnable solutions, one per Level 1 lab. Each is self-contained and prints what it did, so you can diff behaviour, not just code.

| Lab | Solution | Run it |
| --- | --- | --- |
| [Lab 1: Minimal Agent Loop](../../../levels/01-build/labs/lab-01-minimal-agent-loop.md) | [`lab_01_minimal_agent_loop.py`](lab_01_minimal_agent_loop.py) | `python solutions/lab_01_minimal_agent_loop.py` |
| [Lab 2: Tool Schemas](../../../levels/01-build/labs/lab-02-tool-schemas.md) | [`lab_02_tool_schemas.py`](lab_02_tool_schemas.py) | `python solutions/lab_02_tool_schemas.py` |
| [Lab 3: Policy Search](../../../levels/01-build/labs/lab-03-policy-search.md) | [`lab_03_policy_search.py`](lab_03_policy_search.py) | `python solutions/lab_03_policy_search.py` |
| [Lab 4: Trace Capture](../../../levels/01-build/labs/lab-04-trace-capture.md) | [`lab_04_trace_capture.py`](lab_04_trace_capture.py) | `python solutions/lab_04_trace_capture.py` |

## How to use these

Write your own version first. Then read the solution and compare on these questions rather than on line count.

**Lab 1.** Does your loop have exactly one place where it decides to stop? Does it stop on a step budget as well as on a final answer? Lab 1's solution is standalone by design — no imports from the harness — because the point is that an agent loop is about forty lines and no framework.

**Lab 2.** When the model sends bad arguments, does your tool run anyway? Does the model see the specific error, or a generic "tool failed"? The solution asserts that ten distinct bad calls are all rejected *before* execution, and shows a trace where the model recovers on the next turn.

**Lab 3.** Can every policy claim in your final answer be traced to a `source_id` that exists in the corpus? The solution ends with a written list of the search's limitations — write your own before reading it. If your list is shorter than five items, you have not stress-tested your retrieval.

**Lab 4.** Can a second script load all of your traces with plain `json.loads`, with no special cases? Run `python -m acme_agent.check_traces traces/level-1.jsonl` against your own bundle. It fails with the trace id and the field name, not just "invalid".

## What "reference" does not mean

These are worked examples, not the only correct answers. Two things about them are deliberately imperfect, and finding more is a legitimate Level 3 exercise:

- The offline `ScriptedModel` is not an LLM. It is a deterministic planner that makes the tool calls an LLM *should* make, so the harness can be tested without an API key. It is the floor, not the target.
- Item extraction from free text is shallow, so descriptions read like `Stay` rather than `Hotel Teatro, one night`. Its mistakes are real failure material for Level 3.

Run the whole thing against a real model to see the difference:

```bash
export ANTHROPIC_API_KEY=...
python run_agent.py --all --model claude-sonnet-5
```
