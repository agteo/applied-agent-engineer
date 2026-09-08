# Lesson 7: Hardening the Harness

## Core Idea

The harness owns everything the model does not. Validation, tool execution,
error handling, step limits, trace capture — none of it is the model's job, and
all of it decides whether a model failure becomes a recoverable observation or a
crash.

The organising principle is stated in the harness docstring:

```text
A model failure should never become a harness crash — invalid tool arguments
come back to the model as an observation, because recovery is the behaviour
Level 2 measures.
```

Two categories, two treatments. **Model mistakes are data**: record them, hand
them back, let the run continue. **Harness bugs are bugs**: let them surface,
loudly, because swallowing them hides the thing you need to fix.

Getting that boundary wrong in either direction is expensive. Crash on model
mistakes and you throw away the recovery behaviour your evaluation exists to
measure. Swallow harness bugs and your traces record failures the agent never
had.

## Every Run Terminates, And Says Why

```python
DEFAULT_MAX_STEPS = 8

stop_reason = "max_steps_exceeded"
for step_number in range(1, max_steps + 1):
    ...
```

`stop_reason` is initialised to the pessimistic value and overwritten only when
something better happens. That ordering is deliberate: if the loop exits without
setting it, the reason is already correct. There is no path out of this function
that leaves the outcome unexplained.

The reasons that can appear:

| `stop_reason` | Meaning |
| --- | --- |
| `final_answer` | the model produced a valid answer |
| `max_steps_exceeded` | the budget ran out |
| `model_error` | the model call itself failed |

`AgentResult.ok` is defined as `stop_reason == "final_answer"` — so success is a
single explicit condition rather than the absence of an exception.

A step budget is not just a cost control. An agent without one can loop forever
on a task it cannot solve, and the loop looks like slowness rather than failure.
Eight steps is small enough that a stuck agent fails fast and legibly.

## Model Outages End The Run Cleanly

```python
try:
    response = model(messages)
except Exception as error:  # a model outage ends the run, cleanly
    step.error = f"model_error: {error}"
    step.latency_ms = _elapsed_ms(started)
    trace.error = step.error
    stop_reason = "model_error"
    break
```

A bare `except Exception` is usually a smell, and here it is correct: a provider
outage, a timeout, a rate limit — none of these are conditions the harness can
fix, and all of them should produce a trace rather than a stack trace.

Notice what happens before the `break`. The error is written to the step *and*
to the trace, and the latency is recorded. The run ends with a complete artifact
saying what happened and when, which is the difference between an incident you
can analyse and one you have to reproduce.

The failure is recorded in two places on purpose: `step.error` locates it in the
run, `trace.error` makes it visible without walking the steps.

## Latency Is Recorded Per Step

`_elapsed_ms(started)` is called on both paths — success and error — so a step
that failed still carries how long it took before failing.

This matters more than it looks. Timeouts and slow steps are invisible in
aggregate latency: a run that took twelve seconds could be six fast steps or one
that hung. Per-step timing turns that into a fact, and it is what makes the p50
and p95 in the Level 2 report meaningful rather than decorative.

## The Trace Is Written Whatever Happens

The trace object is constructed before the first step and appended to as the run
proceeds. Every exit path — answer, budget, outage — leaves a complete trace
behind.

That is what makes the harness usable as an instrument. Level 2 grades traces,
Level 3 annotates them, Level 4 converts them into data. A harness that only
produces a trace on success produces nothing on exactly the runs those levels
care about.

Version fields go in at construction: `agent_version`, `model`,
`prompt_version`, `trace_schema_version`. A trace that cannot say which build
produced it is an interesting story about the past.

## Defaults Are Injectable

```python
def run_agent(task, model, task_id="manual-001",
              tools=None, max_steps=DEFAULT_MAX_STEPS, writer=None):
    tools = tools or TOOL_FUNCTIONS
```

Tools, the step budget and the trace writer are all parameters with sensible
defaults. That is what lets the same harness run the real toolset, a
deliberately broken one, or a test double — which is precisely how
`weak-no-tool` is built.

The `weak-no-tool` baseline exists because the harness accepts a different tool
mapping. Without that seam there would be no control configuration, and without
a control there would be no evidence the benchmark can detect failure.

**Build the seam that lets you construct a deliberately broken version of your
agent.** You will need it in Level 2 and you cannot retrofit it cheaply.

## Common Failure Modes

- **Crashing on invalid tool arguments.** Destroys the recovery behaviour the
  benchmark measures.
- **Swallowing harness exceptions.** Your bugs get recorded as agent failures.
- **No step budget.** A stuck agent looks slow rather than failed.
- **A default `stop_reason` of success.** An unexplained exit reads as a pass.
- **No trace on failure.** The runs you most need to study produce nothing.
- **Aggregate latency only.** One hung step and six fast ones look identical.
- **Hardcoded tools.** No control configuration, so no evidence the benchmark
  discriminates.
- **No version fields.** The trace cannot say which build it describes.

## Exercise

Open [`agent.py`](../../../examples/strongbench-expense-agent/strongbench_agent/agent.py).

1. `stop_reason` is initialised to `"max_steps_exceeded"` before the loop.
   Explain why that particular default is safer than `"unknown"` or
   `"final_answer"`.
2. The model call is wrapped in a bare `except Exception`, which is usually poor
   practice. Justify it here, and name the class of error that should *not* be
   caught this way.
3. `tools` is a parameter rather than a hardcoded import. Name the Level 2
   artifact that exists only because of that seam, and what its absence would
   cost.

Check your answer:

```text
1. Because the loop can exit by falling off the end, and the pessimistic default
   is then already correct with no extra code. "unknown" would require every
   exit path to remember to set it, and a missed path produces a trace nobody
   can interpret. "final_answer" would be actively dangerous: a run that
   silently exhausted its budget would be recorded as a success, and the
   benchmark would score it as one.

2. A model call fails for reasons entirely outside the harness — outages,
   timeouts, rate limits, malformed provider responses — and none of them are
   recoverable here. Catching broadly converts all of them into a trace with
   stop_reason "model_error" instead of a stack trace, which is the artifact
   Level 3 needs. What should not be caught this way is a bug in the harness
   itself: a KeyError in trace construction or a broken tool mapping is not a
   model failure, and swallowing it would record your bug as the agent's.

3. The weak-no-tool baseline, which is the same harness run with a different
   tool mapping. Without the seam there is no control configuration, so 89/100
   would stand alone — and a benchmark that has never been shown to fail cannot
   distinguish "the agent works" from "the tasks are passable without doing the
   work". The seam is what makes the 0/30 comparison possible.
```

Then set `max_steps=1` and run a task that needs two tool calls. Read the trace:
`stop_reason` should be `max_steps_exceeded`, the trace should be complete, and
nothing should have raised.

## Checkpoint

You are ready to complete Level 1 when your harness records a stop reason on
every path, returns model mistakes as observations while letting harness bugs
surface, writes a trace whatever happens, and accepts an injected toolset you can
deliberately break.

## Reading

- [`examples/strongbench-expense-agent/strongbench_agent/trace.py`](../../../examples/strongbench-expense-agent/strongbench_agent/trace.py)
  — what the harness is accumulating as it runs. Read the two files together;
  the harness is mostly a machine for producing this artifact.
- [`evals/operations/strongbench/intervention-experiment.md`](../../../evals/operations/strongbench/intervention-experiment.md)
  — the experiment the injectable-tools seam makes possible, and the clearest
  argument for building it before you need it.
