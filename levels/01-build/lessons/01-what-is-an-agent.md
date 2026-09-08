# Lesson 1: What Is an Agent?

## Core Idea

An agent is not a model. An agent is a **system that uses a model to decide what
to do next**, and almost every interesting engineering question lives in the
system rather than in the model.

A plain model call maps text to text. An agent adds a loop: the model proposes
an action, something else validates it, something else executes it, the result
comes back as an observation, and the loop runs again until a stopping
condition. The model contributes judgment at each step. Everything else —
validation, execution, error handling, budgets, the record of what happened — is
yours.

That split is the reason this course exists. When an agent fails, the useful
question is rarely "was the model good enough?" It is: did the harness validate
that call, did the tool answer the question it was asked, was the observation
readable, did anything record it. Those are engineering questions with
engineering answers, and they are where most agent failures actually live.

## Five Parts

| Part | In this repo |
| --- | --- |
| a task | a string from a user or a benchmark row |
| a model | `ScriptedModel` or `AnthropicModel`, behind one interface |
| tools | four, each with a schema and a permission |
| state | the trace: steps, arguments, observations, errors |
| a stopping condition | `final_answer`, `max_steps_exceeded`, or `model_error` |

Two of these are commonly missed.

**State is not the conversation.** The trace records intent (`tool_arguments`),
outcome (`observation`), and what was rejected in between. A message list is what
the model sees; the trace is what you can grade, diagnose, and later turn into
training data.

**The stopping condition is explicit and named.** Every run ends with a reason
recorded, including the boring ones. An agent that stops without saying why has
produced a result nobody can interpret.

## The Loop

```text
Task
  |
  v
Model  --> final answer? --> validate against the contract --> Stop
  |
  +-> tool call --> validate arguments --> execute --> observe --> Model
                          |
                          +-> invalid --> observation: error --> Model
```

The branch that matters is the bottom one. **An invalid tool call is an
observation, not an exception.** The harness writes the error into the step,
hands it back, and the loop continues — because recovery is behaviour worth
measuring, and a crash erases it.

That single decision shapes the rest of Level 1. It is why arguments are kept
even when rejected, why error strings are prefixed by kind, and why a run that
went badly still produces a complete trace.

## The Model Is Behind An Interface

```python
class Model(Protocol):
    def __call__(self, messages: list[dict[str, Any]]) -> ModelResponse: ...
```

Two implementations satisfy it: `ScriptedModel` (`name =
"scripted-reference-v1"`), a deterministic offline planner, and
`AnthropicModel`, which calls a real provider.

The default is the scripted one, which is why every command in this course runs
offline, free, and identically on every machine. That is not a limitation of the
teaching setup — it is what makes a hundred-task benchmark a thing you run
casually rather than budget for.

The seam matters beyond cost. Because the model is injectable, so is a
deliberately broken one, which is how the `weak-no-tool` control in Level 2
exists. **Build the interface before you need the second implementation.**

## What Makes This An Agent Rather Than A Script

A fair objection to the scripted model: if the planner is deterministic code, is
this an agent at all?

The agent is the *system*, and the system is unchanged when you swap the
planner. Same loop, same validation, same tools, same trace, same graders. The
model decides; the harness constrains. Substituting a model for a decision
procedure changes the quality of the decisions and nothing about the
architecture.

This is a useful test for your own designs. If replacing your model with a
scripted stand-in requires rewriting the harness, the harness has model-specific
logic in it that probably belongs elsewhere.

## Where Agents Fail

Named early because the rest of the course is organised around them:

| Failure | Level 3 label |
| --- | --- |
| answered without calling a required tool | `TOOLS.selection` |
| called the right tool with wrong arguments | `TOOLS.arguments` |
| read the tool result and drew the wrong conclusion | `TOOLS.interpretation` |
| omitted the policy source that supports the answer | `RETRIEVAL.citation` |
| got the arithmetic or the rule application wrong | `MODEL.reasoning` |
| ignored a boundary such as employee-only submission | `MODEL.instruction_following` |

Only two of the six are the model reasoning badly. The rest are about tool use
and retrieval — and in this repo's annotated failures they outnumber the model
labels **49 to 13**. Build accordingly.

## Common Failure Modes

- **Treating the model as the agent.** Most failures are harness and tool
  failures.
- **Crashing on invalid tool arguments.** Destroys the recovery you wanted to
  measure.
- **Stopping without a reason.** The run cannot be interpreted.
- **State as the message list.** Nothing to grade, diagnose, or convert.
- **A hardcoded model.** No control configuration, so no evidence your benchmark
  discriminates.
- **No step budget.** A stuck agent looks slow rather than failed.
- **Assuming a better model fixes it.** 49 of 62 failure labels here are not
  about the model.

## Exercise

Take three tasks and label whether each requires a direct answer, a tool call,
retrieval, or human approval:

```text
"Can I reimburse dinner during business travel?"
"What is 48.50 plus 91.00 against a USD 75 daily cap?"
"Submit Noah's expense report for him."
```

Check your answer:

```text
"Can I reimburse dinner during business travel?"  -> retrieval
    The answer lives in policy text, not in the model.

"What is 48.50 plus 91.00 against a USD 75 daily cap?"  -> tool call
    Arithmetic against a policy limit is a calculator job, not a guess.

"Submit Noah's expense report for him."  -> human approval
    policy-submission-001 reserves submission for the employee. The agent
    prepares the draft and stops.
```

A task can need more than one. The useful question is which capability the task
*starts* with, because that decides the agent's first action.

Then run `python3 run_agent.py --all --quiet` and open
`traces/level-1.jsonl`. Find one trace where the first tool call is not the one
you would have made, and say what the model saw that led it there.

## Checkpoint

You are ready to move on when you can name the five parts in a system you have
seen, say which failures belong to the harness rather than the model, and
explain why an invalid tool call should not end a run.

## Reading

- [`examples/strongbench-expense-agent/strongbench_agent/agent.py`](../../../examples/strongbench-expense-agent/strongbench_agent/agent.py)
  — the loop in about a hundred lines. Read it once now and again after Lesson 7;
  most of it is the error handling this lesson describes.
- [`evals/operations/strongbench/taxonomy.md`](../../../evals/operations/strongbench/taxonomy.md)
  — the failure labels, three levels ahead. Reading them early tells you what
  the harness will be asked to make visible.
