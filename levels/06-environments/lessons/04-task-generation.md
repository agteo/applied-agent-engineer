# Lesson 4: Task Generation

## Core Idea

A generator's job is not to produce many tasks. It is to produce many *distinct*
tasks, and the difference is the whole subject.

The failure is easy to fall into and hard to see afterwards. Cycle a list of
eight templates 15 times and you have 120 task ids, 120 rows in a JSONL file,
and a metrics block reporting `task_count: 120`. Everything reads as coverage.
What you actually have is eight tasks and a benchmark that cannot distinguish an
agent which solved eight problems from one which solved 120.

This environment made exactly that mistake and had it corrected, which is why
the metrics now report two numbers instead of one:

```json
{"task_count": 120, "distinct_task_count": 120}
```

**Report both. If they differ, the second is the real one.**

## Distinctness Needs A Definition

You cannot count distinct tasks without deciding what makes two tasks the same.
Here the signature is the tuple that determines the whole task:

```python
signature = (actor, employee_id, tuple(receipt_ids))
```

Everything else — the prompt text, the expected total, the required policies,
the difficulty — is *derived* from those three. Two tasks with the same signature
are the same task wearing different ids.

That is the design principle worth taking: derive as much of a task as possible
from a small tuple, then dedup on the tuple. It makes distinctness checkable
rather than aspirational, and it stops the expected answer from being authored
separately from the inputs, which is how oracle bugs get in.

## Families Are Predicates, Not Templates

Eight families, each a function over the fixtures rather than a fixed string:

```text
straightforward_reimbursement   receipt present, no cap reduces the amount
meal_limit                      a meal over the 75.00 daily cap
lodging_limit                   lodging over the 250.00 nightly cap
missing_receipt                 no receipt, amount at or above 25.00
edge_case_under_receipt_threshold  no receipt, amount below 25.00
ambiguous_receipt_lookup        involves a client-entertainment line
multi_step_trip                 three or four receipts from one trip
unsafe_submission               the requester is the employee's manager
```

A family is a *predicate over the fixture set*, so it yields as many distinct
tasks as the fixtures support. Add a receipt and every family that matches it
gains candidates. A template, by contrast, yields exactly one task no matter how
rich the world becomes.

This is why the fixture set matters: 32 receipts across 8 trips and 6 employees
is what makes 120 distinct tasks reachable. The generator did not get more
creative; the world got big enough to ask more questions about.

## Enumerate, Then Draw Round-Robin

No randomness anywhere:

```python
pools  = {name: builder(receipts, employees) for name, builder in FAMILY_BUILDERS}
offset = seed % len(names)
order  = names[offset:] + names[:offset]
# draw one from each pool in turn, skipping exhausted pools, deduping by signature
```

Each family enumerates its full candidate list in a deterministic order. The
generator then rotates through the families taking one at a time, which keeps
the mix balanced while pools last:

| Family | Tasks |
| --- | ---: |
| multi_step_trip | 22 |
| unsafe_submission | 19 |
| edge_case_under_receipt_threshold | 17 |
| ambiguous_receipt_lookup | 16 |
| missing_receipt | 14 |
| lodging_limit | 12 |
| meal_limit | 11 |
| straightforward_reimbursement | 9 |

The distribution is uneven because pools exhaust at different points —
`straightforward_reimbursement` runs out first, since few receipts are both
present and uncapped. Round-robin fills from the families that still have
candidates rather than repeating from the ones that do not.

**The seed rotates the starting family; it does not randomise selection.** Same
seed, same 120 tasks, byte for byte. A different seed gives a genuinely
different set drawn from the same pools — which is what makes a held-out task
set possible, and it is exactly what Level 7 asks for before any reliability
claim.

## Expected Answers Are Computed From The Rules

The oracle is not authored. It is derived from the same policy functions the
verifier uses:

```python
"total_reimbursable": round(sum(reimbursable_amount(row) for row in rows), 2),
"approval_required":  approval_required_for(rows),
"may_submit":         actor == employee_id,
"required_policy_ids": policy_ids_for(rows, actor, employee_id),
```

This is the property that makes 120 tasks maintainable. Change the meal cap from
75 to 80 and every expected total updates on the next build. Hand-authored
oracles would need 120 edits, and the ones nobody remembered would become silent
task bugs.

The tradeoff is real and worth stating: an error in `reimbursable_amount` appears
in both the tasks and the verifier, so they agree with each other and are both
wrong. Derived oracles trade many small independent errors for one large
correlated one. That is usually the better trade — a correlated error is at
least findable in one place — but it means the policy functions deserve their own
tests rather than being checked only through the benchmark.

## Difficulty Is Derived Too

```python
if not may_submit or len(rows) > 2:  return "hard"
if approval_required or len(rows) > 1: return "medium"
return "easy"
```

Giving 23 easy, 56 medium, 41 hard. Derived difficulty means the label cannot
drift from the task: add a receipt and the task becomes harder in the metadata
as well as in fact. Hand-labelled difficulty is a guess that ages.

## Common Failure Modes

- **Counting rows instead of distinct tasks.** 120 ids, 8 problems.
- **No signature.** Distinctness cannot be measured, so nobody notices.
- **Templates instead of predicates.** Coverage stops growing when the fixture
  set does.
- **Random selection.** Re-running until the numbers look better becomes
  available, and eventually taken.
- **Hand-authored oracles.** A rule change means N edits and some are missed.
- **Never generating a second seed.** No held-out set, so memorisation and
  capability stay indistinguishable.
- **Uniform family sizes forced.** Padding an exhausted family means repeating
  its tasks, which is the original bug in a new place.

## Exercise

Open `generate_tasks` and `FAMILY_BUILDERS` in
[`environments/strongbench_finance/__init__.py`](../../../environments/strongbench_finance/__init__.py)
and [`tasks.jsonl`](../../../environments/strongbench_finance/tasks.jsonl).

1. `straightforward_reimbursement` yields 9 tasks while `multi_step_trip` yields
   22. Explain the difference from the predicates, and say why forcing them
   equal would be a mistake.
2. `metrics.json` reports `task_count` and `distinct_task_count` separately.
   Construct the generator bug that would make them differ, and say what a
   reader should conclude if they ever do.
3. Expected totals are computed by `reimbursable_amount`, the same function the
   verifier uses. Name the class of bug this makes impossible and the class it
   makes harder to detect.

Check your answer:

```text
1. straightforward requires a receipt present AND no cap reducing the amount,
   which few of the 32 receipts satisfy; multi_step_trip draws 3- and 4-receipt
   combinations from 8 trips, which combinatorially yields far more candidates.
   Forcing them equal would mean either truncating multi_step_trip — discarding
   distinct tasks for symmetry — or padding straightforward by repeating, which
   reintroduces duplicate tasks under different ids. Let pool sizes reflect what
   the fixtures actually support.

2. Any path that appends a task without checking the signature set — for
   example a family builder emitting the same (actor, employee, receipts) tuple
   twice, or a dedup check that runs before the tuple is fully constructed. If
   the two numbers ever differ, the benchmark contains duplicate tasks under
   distinct ids, so its coverage is smaller than its size and every per-family
   rate is weighted by accidental repetition.

3. Impossible: a task whose expected answer disagrees with the policy rules —
   drift between the oracle and the implementation cannot occur, because there
   is one implementation. Harder to detect: an error in reimbursable_amount
   itself, which now appears identically in the tasks and the verifier, so they
   agree and are both wrong. The benchmark cannot catch it; only unit tests on
   the policy functions can.
```

Then run `generate_tasks(seed=7, count=120)` and compare its signatures with
`seed=42`. The overlap is what tells you whether you have a usable held-out set.

## Checkpoint

You are ready to move on when your generator reports distinct task count beside
task count, defines tasks by a signature it dedups on, derives expected answers
from the same rules the verifier uses, and produces a genuinely different set
under a different seed.

## Reading

- [`environments/strongbench_finance/tasks.jsonl`](../../../environments/strongbench_finance/tasks.jsonl)
  — scan the `expected` blocks. Every field is derived; check that you could
  regenerate each from the receipt ids and the actor alone.
- [`evals/strongbench_benchmark/build_tasks.py`](../../../evals/strongbench_benchmark/build_tasks.py)
  — the Level 2 equivalent for a static benchmark. Comparing the two shows which
  properties come from generation and which from authoring.
