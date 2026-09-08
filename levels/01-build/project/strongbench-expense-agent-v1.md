# Project: StrongBench Expense Agent v1

## Objective

Build the first version of the canonical course agent.

The agent helps employees reason about expense reimbursement using policy
search, receipt lookup, calculation, and approval gating.

## Required Capabilities

The agent must:

1. Answer expense-policy questions using retrieved policy snippets.
2. Look up simulated receipt records.
3. Calculate reimbursable totals.
4. Identify missing information.
5. Identify expenses that require manager approval.
6. Ask for human approval before preparing an action with external or financial
   consequences.
7. Return a structured final answer.
8. Save traces for every run.

## Required Tools

Four tools, and one of them is different from the others.

| Tool | Permission | Purpose |
| --- | --- | --- |
| `search_policy` | read | find relevant policy sections |
| `lookup_receipt` | read | retrieve simulated receipt records |
| `calculate_reimbursement` | read | totals, limits, non-reimbursable amounts |
| `request_human_approval` | **write** | ask before preparing or submitting |

**Classify your tools by effect before writing the loop.** Three of these answer
questions and touch nothing; one can have a consequence a person would care
about. That split is what lets a harness enforce "no write-permission tool
before an approval step" mechanically, across every tool you add later, instead
of maintaining a hardcoded list of dangerous names.

Reference:
[`strongbench_agent/schemas.py`](../../../examples/strongbench-expense-agent/strongbench_agent/schemas.py)
defines all four with a `permission` field on each.

## Final Answer Contract

```json
{
  "summary": "Short human-readable answer.",
  "reimbursable_items": [
    {
      "description": "Airport parking",
      "amount": 47.0,
      "policy_source_ids": ["policy-travel-002"]
    }
  ],
  "non_reimbursable_items": [],
  "missing_information": [],
  "approvals_required": [
    {
      "approval_type": "manager",
      "reason": "Missing hotel receipt"
    }
  ],
  "total_reimbursable": 47.0,
  "cited_policy_source_ids": ["policy-travel-002"],
  "confidence": "medium",
  "next_action": "Ask manager to approve exception for missing hotel receipt."
}
```

Eight fields are required; `cited_policy_source_ids` is optional but strongly
recommended, because a pure policy answer has no line items and nowhere else to
show its grounding. `additionalProperties` is `false` — an invented field is
rejected rather than silently dropped, so the model finds out it did not
communicate what it thought it did.

The committed contract is
[`FINAL_ANSWER_SCHEMA`](../../../examples/strongbench-expense-agent/strongbench_agent/schemas.py).
Level 2's contract grader imports it rather than re-describing the shape — one
definition, two consumers. Do the same, or the two will drift and the drift will
report as agent failure.

## Reference Implementation

A working implementation with fixtures and tests is in
[`examples/strongbench-expense-agent/`](../../../examples/strongbench-expense-agent/).
**Build your own first**, then read it and disagree with it in your
implementation note.

The four pieces worth reading in this order:

| Read | For |
| --- | --- |
| [`validation.py`](../../../examples/strongbench-expense-agent/strongbench_agent/validation.py) | what "validating a tool call" actually means — ten JSON Schema keywords, hand-written |
| [`agent.py`](../../../examples/strongbench-expense-agent/strongbench_agent/agent.py) | the loop, and why an invalid tool call is an observation rather than an exception |
| [`docs/trace-schema.md`](../../../examples/strongbench-expense-agent/docs/trace-schema.md) | the contract three later levels consume |
| [`solutions/`](../../../examples/strongbench-expense-agent/solutions/) | one runnable reference per Level 1 lab |

Fixtures — policies, receipts, employees, tasks — are in
[`fixtures/`](../../../examples/strongbench-expense-agent/fixtures/). Your policy
ids must come from that catalogue: Level 2's grader checks cited ids against it,
so an invented id fails even when the required ones are also present.

## Example Tasks

Use these while developing:

1. "I spent $47 on airport parking and $68 on dinner during a customer trip.
   What can I reimburse?"
2. "I lost my hotel receipt for a $214 stay. Can I still submit it?"
3. "Find the receipt for my Denver dinner last Thursday and tell me whether it
   is within policy."
4. "Prepare a reimbursement recommendation for my trip with parking, dinner, and
   hotel expenses."
5. "Can you submit this reimbursement for me?"

The fifth is the one that matters. `policy-submission-001` reserves submission
for the employee, so the correct behaviour is to prepare the draft, record an
`approvals_required` entry with `approval_type` of `"employee"`, and stop. A
refusal that returns nothing is a worse product and a worse trace.

## Constraints

- Do not connect to real financial systems.
- Do not use real employee data.
- Do not submit real reimbursements.
- Do not let the model execute arbitrary code.
- Do not continue beyond the maximum step count.

## Evaluation Preview

Level 2 will evaluate this project on task success, policy citation accuracy,
tool-call correctness, structured output validity, cost, latency, and failure
rate.

Two consequences for how you build now:

- **Keep the toolset injectable.** Level 2's control configuration is this same
  harness with its tools removed. Without that seam there is no negative
  control, and a benchmark that has never been shown to fail is not evidence.
- **Write a trace on every exit path**, including failures. Level 2 grades
  traces, Level 3 annotates them, Level 4 converts them into data. A harness that
  only produces a trace on success produces nothing on the runs those levels
  care about.

See what downstream evidence should look like in
[`examples/reference-artifacts/eval-report/`](../../../examples/reference-artifacts/eval-report/).

## Submission Checklist

- [ ] Agent runs locally.
- [ ] At least three tools are implemented.
- [ ] Tool arguments are validated.
- [ ] Final answers follow the contract.
- [ ] Policy citations are included, and every id exists in the fixtures.
- [ ] Human approval is used for risky actions.
- [ ] At least 20 traces are saved.
- [ ] Every run records a `stop_reason`, including failures.
- [ ] Known limitations are documented.

## Exit Standard

Verify mechanically rather than by inspection:

```bash
cd examples/strongbench-expense-agent
python3 -m strongbench_agent.check_traces path/to/your/traces.jsonl
```

That checks the bundle against the trace contract with per-field messages. Then
confirm the two properties a checker cannot see:

```bash
# 1. Invalid arguments must not end the run.
#    Send a malformed tool call and confirm the trace continues, with the
#    rejected arguments still recorded in tool_arguments.

# 2. The toolset must be injectable.
#    Run your agent with an empty tool mapping. It should complete and produce
#    traces, not crash - that is Level 2's control configuration.
```

The project is complete when `check_traces` passes on 20+ traces, a malformed
tool call produces an observation rather than a stack trace, and your agent runs
with a substituted toolset.
