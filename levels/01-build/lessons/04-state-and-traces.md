# Lesson 4: State and Traces

## Core Idea

A trace is not a log. A log is written for a human debugging today; a trace is a
**data contract** that three later levels consume — Level 2 grades it, Level 3
annotates it, Level 4 converts it into training data.

That changes how you design it. The question stops being "what would be useful
to print" and becomes "what will be impossible to recover if I do not record it
now?" A trace is written once and read for the life of the project, on runs you
cannot reproduce, by people who were not there.

The rule that follows, stated at the top of
[`trace-schema.md`](../../../examples/strongbench-expense-agent/docs/trace-schema.md):

```text
Adding a field is a safe change. Changing what a field means is not — bump
trace_schema_version when you do.
```

Additive changes are cheap because old consumers ignore new fields. Semantic
changes are expensive because every consumer is silently wrong until someone
notices.

## Keep The Arguments That Failed

The single most consequential field in the schema, with the reason attached:

```text
tool_arguments   What the model asked for, BEFORE validation. Keep it even when
                 validation fails: this is the raw material for Level 3's
                 failure taxonomy.
```

There are two argument fields, not one:

| Field | Holds | Null when |
| --- | --- | --- |
| `tool_arguments` | what the model asked for | never |
| `validated_arguments` | what the harness accepted | validation rejected the call |

Recording only the validated form would mean every rejected call vanishes. You
would see that a step failed and never what the model actually tried — and the
difference between `{"category": "dinner"}` and `{"category": 42}` is the
difference between two entirely different bugs.

**Record intent and outcome separately.** This is the general form: whenever
your system transforms or rejects an input, keep both sides.

## Errors Are Prefixed By Kind

```text
invalid_arguments   unknown_tool   tool_error
model_error         final_answer_invalid   no_action
```

Six kinds, and the prefix is on the string rather than in a separate field so it
survives any consumer that treats the error as text.

The value is aggregation. "How often does the model call a tool that does not
exist?" is a prefix count over a bundle. Without prefixes it is a regex over
free-form messages that breaks the first time someone rewords one — which is the
same brittleness the Level 2 grader was carrying until it was fixed.

The distinctions also matter individually. `invalid_arguments` is a model
mistake and recoverable. `tool_error` is your bug. `model_error` is a provider
outage. Collapsing them into "error" throws away the triage.

## Metadata Is Derived, Not Maintained

```text
stop_reason, step_count, tool_calls, total_tokens, latency_ms, max_steps
```

All computed from `steps` when the trace is serialised. Nothing here is
maintained alongside the run, so nothing can drift out of sync with it.

`tool_calls` — "tool names in call order" — is described in the schema doc as
*the trajectory shape Level 3 reads first*, and that is exactly how it is used.
Nineteen of the thirty annotated failures are identified by one property: the
list is empty. An agent that answered without gathering evidence is a one-field
query rather than a trace-by-trace investigation.

Derived summaries earn their place when they turn a common question into a
lookup. They stop earning it the moment they are hand-maintained.

## Version Fields Or The Trace Is Anonymous

Four of them: `agent_version`, `model`, `prompt_version`,
`trace_schema_version`. The doc is blunt about why `prompt_version` is there:

```text
Which system prompt produced this run. Without it, an eval result cannot be
reproduced.
```

A benchmark result from an unknown prompt version cannot be compared to
anything. This is the field teams add after their first unreproducible
regression, and the traces from before that point stay unusable forever.

## Reproducibility Is A Trace Concern

Two fields are volatile by nature — `run_id` and `started_at` — and the schema
addresses them directly:

```text
run_id      Committed scripted bundles use a stable id so rebuilds are
            byte-reproducible.
started_at  Committed scripted bundles use a fixed timestamp.
latency_ms  Committed scripted bundles set this to 0; real-model runs may
            record wall-clock timing.
```

The tension is real. Timestamps and unique ids are genuinely useful on live
runs, and they make committed artifacts diff on every rebuild — which destroys
the `git diff --exit-code` gate the other levels rely on.

The resolution is to make determinism a property of the *writer* rather than
removing the fields: a deterministic mode derives `run_id` from stable content
and fixes the timestamps, so committed bundles are byte-reproducible while live
runs keep real values.

Decide this before you commit a trace bundle. Retrofitting it means rewriting
every artifact downstream of it.

## The Bundle Is Checked, Not Assumed

```bash
python3 -m strongbench_agent.check_traces traces/level-1.jsonl
```

A trace format nothing validates is a format that drifts. The checker enforces
the contract with per-field messages in the same style as the Level 2 graders —
naming the task, the field and the problem — so a broken bundle is a five-second
fix rather than an investigation.

Run it in CI. Level 1's workflow does, immediately after generating the traces.

## Common Failure Modes

- **Discarding rejected arguments.** Level 3 loses the raw material for tool
  failure analysis.
- **One error field with no kind.** Aggregation becomes regex over prose.
- **Hand-maintained metadata.** Drifts from the steps it summarises.
- **No `prompt_version`.** Results cannot be reproduced or compared.
- **Volatile fields in committed bundles.** Every rebuild diffs and the gate
  becomes noise.
- **Changing a field's meaning without bumping the version.** Every consumer is
  silently wrong.
- **No validator.** The format drifts and nobody finds out until a grader
  breaks.

## Exercise

Open [`trace-schema.md`](../../../examples/strongbench-expense-agent/docs/trace-schema.md)
and a trace from `traces/level-1.jsonl`.

1. `tool_arguments` and `validated_arguments` are separate fields. Construct the
   Level 3 question that can be answered with both and cannot with only the
   second.
2. `metadata.tool_calls` is derived rather than stored. Name the Level 3 finding
   it makes a one-field query, and say how many annotated failures it identifies.
3. Committed bundles use a fixed `started_at` and a stable `run_id`. Explain what
   breaks if they use live values, and why removing the fields entirely would be
   the wrong fix.

Check your answer:

```text
1. "What did the model get wrong about this tool's arguments?" With both, you
   can see the rejected call — {"category": "dinner"} against an enum of
   ["meals", ...] — and classify it as TOOLS.arguments with a specific cause.
   With only validated_arguments the field is null and all you know is that
   something failed, so the taxonomy label has nothing behind it and the
   intervention cannot be specific.

2. That the agent answered without calling any tool: metadata.tool_calls is
   empty. It identifies the 19 weak-no-tool failures, which share one
   hypothesis and one intervention. Without the derived field you would inspect
   each trace's steps individually to establish the same thing.

3. Live values make every rebuild produce a different file, so `git diff
   --exit-code` reports a change on every run and the drift gate can no longer
   distinguish an agent change from a rebuild. Removing the fields is wrong
   because they are genuinely useful on live runs — run_id distinguishes two
   runs of the same task, started_at orders them. The fix is a deterministic
   writer mode: stable values in committed bundles, real values in production.
```

Then run the agent twice and diff the two trace files. Everything that differs
is either non-determinism you should understand or a field that needs a
deterministic mode.

## Checkpoint

You are ready to move on when your trace records intent as well as outcome,
errors carry a kind, metadata is derived, version fields are present, and a
checker validates the bundle in CI.

## Reading

- [`examples/strongbench-expense-agent/strongbench_agent/trace.py`](../../../examples/strongbench-expense-agent/strongbench_agent/trace.py)
  — the writer. Short enough to read whole, and the dataclass is the schema in
  executable form.
- [`evals/operations/strongbench/annotated-failures.jsonl`](../../../evals/operations/strongbench/annotated-failures.jsonl)
  — a trace two levels downstream, with diagnosis attached. It is the clearest
  argument for recording fields whose value is not obvious today.
