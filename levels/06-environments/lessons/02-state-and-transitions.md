# Lesson 2: State and Transitions

## Core Idea

An environment is a state model plus the rules for changing it. Everything else
— tools, tasks, rewards — is an interface onto those two things.

The design question is narrower than it first appears: **what must be in state
for the checks you intend to run?** State is not a model of the world. It is the
minimum record that makes agent behaviour verifiable, and every key you add is a
key you must keep consistent across every transition forever.

The failure mode at each end is real. Too little state and behaviour becomes
unobservable — you cannot check that an approval was requested if approvals are
not recorded. Too much and you are maintaining a simulation of a company, most
of which no verifier reads, all of which can drift out of sync.

The discipline that resolves it: **add a key when a check needs it, not before.**

## Two Kinds Of Key

[`state-schema.json`](../../../environments/strongbench_finance/state-schema.json)
requires twelve keys, and they divide cleanly:

| Fixtures — the world as given | Records — what the agent did |
| --- | --- |
| `employees` (6) | `drafts` (starts empty) |
| `managers` (3) | `approval_requests` (starts empty) |
| `policies` (6) | `submitted_reports` (starts empty) |
| `receipts` (32) | `audit_log` (starts empty) |
| `trips` (8) | |
| plus `schema_version`, `environment`, `seed` | |

Look at
[`initial-state.json`](../../../environments/strongbench_finance/initial-state.json)
and the four record keys are all empty. That is the shape to aim for: **the
initial state contains only the world; everything else is evidence the agent
created.**

This is what makes verification a state query rather than a trace search. "Did
the agent file a draft?" is `drafts["draft-{task_id}"]`, not a scan of the action
list. Records that start empty and are written only by tools mean their contents
*are* the agent's footprint.

## Transitions Are Keyed, Not Appended

Every write in this environment names its key:

```text
create_reimbursement_draft   ->  drafts[draft-{task_id}]
request_manager_approval     ->  approval_requests[approval-{task_id}]
submit_reimbursement         ->  submitted_reports[report-{task_id}]
```

The key is derived from the task id, which buys two properties.

**Verification is a lookup.** `verify_rollout` opens with three of them:

```python
draft     = state["drafts"].get(f"draft-{task['id']}")
approval  = state["approval_requests"].get(f"approval-{task['id']}")
submitted = state["submitted_reports"].get(f"report-{task['id']}")
```

Three dictionary reads, no searching, no ambiguity about which draft belongs to
which task.

**Repeats overwrite rather than accumulate.** An agent that calls
`create_reimbursement_draft` twice ends with one draft, not two. Whether that is
right depends on your domain — here it models "the draft for this task", and it
means a retry does not look like two drafts to a verifier counting them.

Choose the key deliberately. It determines what "doing it twice" means.

## The Audit Log Is Not Bookkeeping

`audit_log` is appended to by *every* tool, including the read-only ones. That
looks redundant next to `actions` in the rollout record, and it is not: the audit
log lives in **state**, so it survives into the terminal state hash and can be
inspected by anything holding the state.

More importantly, it is what makes reads verifiable. Without it, "did the agent
look up the receipt?" has no answer in state, and the check degrades into
searching the agent's own output for an id — which is the substring anti-pattern
a reward hacker walks straight through.

If a tool does something you might later want to check, it must leave a record,
even when it changes nothing else.

## Seeds And Hashes Make State Comparable

`seed` sits in state, and the rollout record carries a hash of the state before
and after:

```json
{"initial_state_hash": "932ca7a7...", "terminal_state_hash": "cb6c02bd..."}
```

The seed makes the world reproducible: same seed, same fixtures, same tasks. The
hashes make episodes comparable without diffing structures — `initial ==
terminal` means the agent changed nothing, checkable across a million rollouts
without parsing an action.

`schema_version` is in the required list for the reason every persisted format
needs one: state written under an old shape must be identifiable when the shape
changes. It is currently `1.1.0`, having moved from `1.0.0` when the fixture set
grew.

## Deep-Copy Or Everything Lies

Each rollout starts from a copy:

```python
state = deepcopy(base_state)
simulator = Simulator(state)
```

Without that, episode two starts inside episode one's drafts. Rollouts stop
being independent, the second task sees a submitted report it did not create,
and the failures are baffling because the code looks correct in isolation.

Any environment reused across episodes needs this, and it is the single most
common bug in hand-rolled simulators. If your rollouts pass individually and
fail in a batch, look here first.

## Common Failure Modes

- **State the checks do not read.** Every key is a consistency obligation; pay
  for the ones that earn it.
- **Behaviour that leaves no state.** If an action is not recorded, it cannot be
  verified.
- **Records that are not empty initially.** You cannot distinguish the agent's
  work from the fixture.
- **Unkeyed appends.** Verification becomes a search, and repeats become
  duplicates.
- **No audit trail for reads.** Forces verifiers back to inspecting the agent's
  own output.
- **Sharing state across episodes.** Rollouts stop being independent and the
  failures make no sense.
- **No schema version.** Old state becomes unidentifiable the day the shape
  changes.

## Exercise

Open [`state-schema.json`](../../../environments/strongbench_finance/state-schema.json)
and [`initial-state.json`](../../../environments/strongbench_finance/initial-state.json).

1. Four of the twelve required keys are empty in the initial state. Name them
   and explain what property that emptiness gives every verifier.
2. `audit_log` is appended to by read-only tools that change nothing else.
   Justify the cost, and name the verifier check that would be impossible
   without it.
3. `submit_reimbursement` writes `submitted_reports[report-{task_id}]`. Describe
   what changes if the key were an auto-incrementing id instead, both for
   verification and for what a repeated call means.

Check your answer:

```text
1. drafts, approval_requests, submitted_reports, audit_log. Because they start
   empty, anything in them at the end of an episode was put there by the agent.
   Verification becomes a direct question about the agent's footprint — "is
   there a draft for this task?" — rather than a diff against a starting
   population, and a no-op episode is detectable because those keys are still
   empty.

2. The cost is a state write on every read call. It buys observability of
   reading, which is otherwise invisible: reads change nothing, so without the
   log there is no trace of them in state at all.
   constraint_required_records_checked depends on it — it asks whether each
   required receipt was retrieved by a successful lookup_receipt. Without the
   audit log the check would have to search the agent's own output for the
   receipt id, which a policy can satisfy by naming an id it never read.

3. Verification stops being a lookup and becomes a search: the verifier must
   scan submitted_reports for an entry matching this task, since it cannot
   construct the key. And a repeated submit would create a second report rather
   than overwriting, so "how many reports exist" changes meaning — a retry now
   looks like two submissions, and any check counting them reports a safety
   violation that did not happen.
```

Then add a key to the state schema and try to justify it by naming the check
that reads it. If no check does, you have found the rule this lesson is about.

## Checkpoint

You are ready to move on when every key in your state is read by some check,
your record keys start empty, every write names its key, and each episode begins
from an independent copy.

## Reading

- [`environments/strongbench_finance/tool-schemas.json`](../../../environments/strongbench_finance/tool-schemas.json)
  — the transition column beside this schema. Every key here should be reachable
  by a tool and read by a check; the two files are one design.
- [`environments/contract.py`](../../../environments/contract.py) — the shared
  interface both environments implement. Read it when deciding which parts of
  your state model are domain-specific and which belong in the contract.
