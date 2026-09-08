# Lesson 3: Search and Grounding

## Core Idea

Grounding is not "the model read a document". It is a checkable property: **the
answer names the source that supports it, and that source was actually
retrieved.**

Both halves matter and they fail differently. An answer with no citation cannot
be audited — a reviewer has to re-derive the reasoning to know whether it is
right. An answer citing a source the agent never retrieved is worse, because it
looks auditable and is not.

This is why grounding is a Level 1 concern rather than a retrieval-quality
concern. The design decision is not which search algorithm to use; it is
returning **stable source identifiers** that survive into the final answer and
can be checked against what came back. Get that right and any search
implementation can be swapped underneath. Get it wrong and no retrieval quality
saves you.

## Sources Need Ids, Not Just Text

Each of the nine policy sections in
[`fixtures.py`](../../../examples/strongbench-expense-agent/strongbench_agent/fixtures.py)
carries five fields:

```text
source_id   policy-meals-001
title       Meals During Travel
category    meals
keywords    [...]
text        Meals purchased while travelling for business are reimbursable up to
            a daily limit of USD 75 per employee. ...
```

`source_id` is the field the whole level turns on. It is stable, it is short
enough to appear in an answer, and it is what
`final_answer.cited_policy_source_ids` holds.

Because ids exist, the deterministic grader can do two independent checks:

```python
unknown = cited - known_ids          # fabricated citations
missing = expected - cited           # required citations omitted
```

Neither is possible if sources are quoted as text. Quotations get paraphrased,
truncated and reformatted; ids do not. **The identifier is what makes grounding
gradeable.**

Note the direction of the first check. `known_ids` comes from the fixture
catalogue, not from the task's expected answer — so an agent inventing
`policy-meals-999` fails even on a task where it also cited everything required.
Grade against the world, not only against the answer key.

## The Search Is Deliberately Simple

```python
def search_policy(query, category=None, top_k=3):
    """Keyword search over the policy corpus.

    Scoring is deliberately simple: keyword hits are worth more than title hits,
    which are worth more than body hits. Lab 3's stretch goal replaces this with
    embeddings; the return shape stays the same either way.
    """
```

Three tiers — keyword 3.0, title 2.0, body 1.0 — summed per section, with
zero-scoring sections dropped and ties broken by `source_id` for determinism.

The docstring makes the architectural point: **the return shape stays the same
either way.** Swap keyword matching for embeddings and nothing downstream
changes, because the contract is "a list of sections with ids and scores", not
"the output of a particular algorithm".

That is the seam worth building early. Retrieval implementations get replaced;
retrieval *interfaces* should not have to be.

The tie-break on `source_id` is a small detail with a large consequence. Without
it, two equally-scored sections could come back in arbitrary order, the agent
could cite either, and the trace would not be reproducible. Determinism in
search is what makes a deterministic benchmark possible.

## Retrieval Success Is Not Grounding

The most instructive failure in this repo is a grounding failure that is *not* a
retrieval failure.

In `bench-029`, `search_policy` returns `policy-lodging-001`, whose text says
"Room service is treated as a meal expense and counts against the daily meal
limit." The right document came back. The agent then categorised room service as
lodging anyway, and cited `policy-lodging-001` in support of the wrong
categorisation.

So: retrieved correctly, cited a real id, still wrong. The citation check passes
and the total check fails.

**Grounding gets you auditability, not correctness.** It guarantees a reviewer
can see what the agent relied on — which is exactly how this bug was diagnosed
in one step rather than by re-deriving the policy from scratch.

## Citations Live In Two Places

The final answer carries `cited_policy_source_ids`, and individual line items
carry their own `policy_source_ids`. The grader unions them:

```python
cited = set(answer.get("cited_policy_source_ids", []))
for group in ("reimbursable_items", "non_reimbursable_items"):
    for line in answer.get(group, []):
        cited.update(line.get("policy_source_ids", []))
for approval in answer.get("approvals_required", []):
    cited.update(approval.get("policy_source_ids", []))
```

Per-item citation is the more useful form. "This dinner was capped at 75.00
under `policy-meals-001`" attaches the justification to the decision it
justifies, so a reviewer checking one line does not have to work out which of
four top-level citations applies.

Collect from everywhere; require the union to cover what the task needs.

## Common Failure Modes

- **Returning text without ids.** Grounding stops being checkable.
- **Checking only that citations are required ones.** Fabricated ids pass
  whenever the real ones are also present.
- **Non-deterministic tie-breaking.** The same query returns different orders
  and the benchmark stops being reproducible.
- **A retrieval interface that leaks the implementation.** Swapping search
  becomes a downstream migration.
- **Treating retrieval success as grounding.** `bench-029` retrieved the right
  policy and got the wrong answer.
- **Only top-level citations.** The reviewer cannot tell which source justified
  which line.
- **Silently returning everything on no match.** The agent is handed the corpus
  and its search strategy is never tested.

## Exercise

Open [`tools.py`](../../../examples/strongbench-expense-agent/strongbench_agent/tools.py)
and [`deterministic.py`](../../../evals/strongbench_benchmark/graders/deterministic.py).

1. `_policy_citations_ok` computes `unknown = cited - known_ids` using the
   fixture catalogue rather than the task's expected ids. Give the agent
   behaviour this catches that an expected-ids-only check would miss.
2. `search_policy` breaks score ties on `source_id`. Name the property of the
   benchmark that would be lost without it.
3. In `bench-029` the agent retrieved `policy-lodging-001` and cited it, and the
   answer was wrong. Which grader check passed, which failed, and what does that
   say about what grounding buys you?

Check your answer:

```text
1. Fabrication. An agent that cites policy-meals-001 (required) alongside an
   invented policy-meals-999 satisfies an expected-ids check completely — every
   required id is present. Only comparing against the catalogue of ids that
   actually exist catches the invented one. This is the difference between
   "did it cite what we wanted" and "is everything it cited real".

2. Reproducibility. With equal scores and no tie-break, two sections can be
   returned in arbitrary order; the agent may cite either, so the same task can
   produce different traces across runs. That breaks byte-reproducible reports
   and makes any diff between runs uninterpretable — you can no longer tell an
   agent change from search ordering noise.

3. The citation check passed — policy-lodging-001 is a real id and the required
   ids were present. The total check failed: expected 75.00, got 108.00.
   Grounding bought auditability, not correctness. The citation is exactly what
   made the diagnosis quick: a reviewer could see which policy the agent
   believed it was applying and immediately spot that it contradicted its own
   categorisation.
```

Then call `search_policy("room service")` and read what comes back. Ask whether
an agent seeing that result has enough to categorise correctly — and if so, what
that tells you about where the failure actually is.

## Checkpoint

You are ready to move on when your sources have stable ids, your answers cite
them per decision, your grader checks citations against the catalogue as well as
the expected set, and your retrieval is deterministic.

## Reading

- [`examples/strongbench-expense-agent/fixtures/policies.json`](../../../examples/strongbench-expense-agent/fixtures/policies.json)
  — the corpus. Note that each section is small and single-topic, which is what
  makes a citation precise enough to check.
- [`evals/strongbench_benchmark/graders/deterministic.py`](../../../evals/strongbench_benchmark/graders/deterministic.py)
  — `_policy_citations_ok` in full. It is the shortest complete example in the
  repo of grading a property rather than a string.
