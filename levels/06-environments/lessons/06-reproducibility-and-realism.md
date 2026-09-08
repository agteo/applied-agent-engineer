# Lesson 6: Reproducibility and Realism

## Core Idea

These two properties pull against each other, and most environment designs get
into trouble by refusing to choose.

**Reproducibility** means the same inputs give the same outputs, forever. It is
what lets you attribute a change in results to a change in the agent, which is
the entire basis of evaluation. Without it, every comparison is confounded by
noise you cannot separate from signal.

**Realism** means the environment resembles the world the agent will actually
face — messy inputs, ambiguous cases, other actors, delay. It is what makes
success in the environment predict success outside it.

You can have a lot of both, but not by accident, and the resolution is not a
compromise in the middle. It is: **build the reproducible environment, then
write down exactly how it differs from the world.** The gap becomes a documented
artifact rather than an unexamined assumption, and results get read with the
right amount of trust.

## What Reproducibility Costs, Concretely

This environment buys determinism with four decisions:

**A seed in state.** `initial_state(seed)` produces the same six employees,
thirty-two receipts and eight trips every time, and the seed is recorded *in the
state itself* so a rollout carries the world it ran in.

**No randomness in task generation.** Families enumerate candidates in a fixed
order and are drawn round-robin. The seed rotates the starting family; it does
not sample. Same seed, same 120 tasks, byte for byte.

**Content-hashed assignment wherever a bucket is needed.** The Level 4 splitter
uses a hash of the example id rather than a random draw, which removes the
option of re-running until the numbers look better.

**Byte-reproducible artifacts.** Every builder writes sorted JSON with a stable
key order, and CI runs `git diff --exit-code` after rebuilding. If a rebuild
changes a file, either the code changed or something is non-deterministic, and
both are things you want to be told.

The cost is real: no randomised task sampling, no timestamps in artifacts, no
"just re-run it and see". What you get is that any diff is a signal.

## Determinism Is Not The Same As A Fixed Answer

A common misreading: determinism means the environment always produces the same
result, so it cannot be sensitive to agent behaviour.

It means the opposite. The *environment* is fixed so that the only thing varying
is the agent. Three policies over the same 120 tasks produce three sharply
different outcomes:

```text
scripted_reference   1.000 success   avg  1.90
weak_submitter       0.000 success   avg -1.63   120 unsafe submissions
reward_hacker        0.000 success   avg -0.82    19 unsafe submissions
```

Nothing here is noise. Every difference is attributable to policy behaviour,
which is exactly what a deterministic environment is for.

## Realism Is A Debt, So Write It Down

[`simulator-bias-note.md`](../../../environments/strongbench_finance/simulator-bias-note.md)
is short and is the most useful document in the bundle:

```text
This simulator is deterministic and fixture-sized. It is useful for teaching
state transitions, verifier design, reward decomposition, and rollout logging,
but it is easier than a real finance operations environment.

Scope: expense reimbursement only. ... invoices, purchase orders, vendors,
reconciliation records, and the exception queue are not implemented and should
not be described as if they were.

Known omissions: messy OCR, partial receipts, changing policies, multi-actor
delays, adversarial vendors, real payment rails, and ambiguous human approvals.
The model-based verifier is an offline reference judge, not a live LLM call.

Treat high simulator reward as readiness for harder evaluation, not proof of
production reliability.
```

Three things it does that are worth copying exactly.

**It states scope against the name.** The environment is called a Finance
Operations Simulator and implements expense reimbursement only. Rather than
quietly hoping nobody notices, the note says the unimplemented parts "should not
be described as if they were". A name that oversells is a debt; disclosing it is
the interest payment.

**It lists omissions concretely.** Not "simplified" but *messy OCR, partial
receipts, changing policies, multi-actor delays*. Each is a specific thing a real
deployment has that this does not, so a reader can judge whether their case
lands in the gap.

**It bounds the claim.** High reward is "readiness for harder evaluation, not
proof of production reliability." That sentence is what stops a good number
becoming a bad decision.

## Every Omission Is A Capability You Are Not Measuring

Read the omissions as a list of things your agent has never been tested on:

| Omission | What goes untested |
| --- | --- |
| messy OCR | recovery from bad input |
| partial receipts | reasoning under incomplete evidence |
| changing policies | whether it re-reads or caches stale rules |
| multi-actor delays | behaviour when an approval does not return |
| adversarial vendors | robustness to inputs designed to mislead |
| ambiguous human approvals | escalation when the answer is genuinely unclear |

An agent scoring 1.000 here has demonstrated none of those. That is not a flaw
in the environment — it is what "fixture-sized" means — but it must be stated,
because the number invites the opposite conclusion.

Write your omissions list *before* you publish results. Afterwards it reads as
excuse-making, and you will be under pressure to shorten it.

## Where To Spend Realism

Not all realism is worth the same. Add it where a *verifier* would become
sharper, not where the world would look more convincing.

Adding vendor names to the fixtures makes the environment feel richer and
changes no check. Adding partial receipts creates a genuine decision — reason
from incomplete evidence or ask — which is a behaviour worth grading and cannot
currently be measured at all.

The question for any proposed realism: **which check gets better, or which new
check becomes possible?** If neither, it is set dressing.

## Common Failure Modes

- **Randomised task sampling.** Comparisons stop being attributable, and
  re-running until the number improves becomes available.
- **Timestamps or ids in artifacts.** Every rebuild diffs, so no diff means
  anything.
- **No bias note.** The gap between simulator and world becomes an unexamined
  assumption.
- **A vague bias note.** "Simplified" tells a reader nothing they can act on.
- **Realism that no check reads.** Consistency cost, no verification value.
- **Reading simulator success as production readiness.** The note exists to stop
  exactly this.
- **Writing the omissions after the results.** It becomes negotiable.

## Exercise

Open [`simulator-bias-note.md`](../../../environments/strongbench_finance/simulator-bias-note.md)
and [`metrics.json`](../../../environments/strongbench_finance/metrics.json).

1. The reference policy scores 1.000. Using the omissions list, name three
   capabilities that score does not evidence, and say what each would need.
2. The note says the model-based verifier is "an offline reference judge, not a
   live LLM call." Why does that belong in a bias note rather than only in the
   code, and what could a reader wrongly conclude without it?
3. You are given budget for one addition to the environment. Choose between
   vendor names on receipts and partial receipts, and justify it in terms of
   checks.

Check your answer:

```text
1. Recovery from malformed input — needs messy OCR or corrupted receipt
   fixtures. Reasoning under incomplete evidence — needs partial receipts,
   where the correct behaviour may be to ask rather than answer. Behaviour when
   an approval does not return — needs multi-actor delay, so a pending approval
   can stay pending. None of the three is exercised by any of the 120 tasks, so
   1.000 is silent on all of them.

2. Because a reader seeing "model_based" in verifier_types will assume an LLM
   judge with its associated cost, latency and variance. Here it is
   deterministic offline code standing in for one, which is why the environment
   runs free and identically everywhere — and why its judgments are simpler
   than a real judge's. Without the note they would over-read the model-based
   check as evidence the reward survives contact with a real judge, which it
   has never been tested against.

3. Partial receipts. Vendor names make the fixtures look realistic and change no
   check — every verifier reads amounts, categories, has_receipt and ids.
   Partial receipts create a genuine decision under uncertainty, which makes a
   new check possible: did the agent flag missing information rather than
   guessing? That is a behaviour the environment currently cannot grade at all,
   and it is on the omissions list.
```

Then rebuild the environment twice and diff the artifacts. Byte-identical output
is what makes the CI drift gate meaningful; if you cannot get that property,
find out which field is moving before trusting any comparison.

## Checkpoint

You are ready to move on when your environment rebuilds byte-identically, its
seed is recorded in the artifacts it produces, and you have written the
omissions list a reader would need to size your results correctly.

## Reading

- [`environments/strongbench_finance/manifest.json`](../../../environments/strongbench_finance/manifest.json)
  — note the `scope` field beside the metrics. Putting the limitation next to the
  numbers is what stops the numbers travelling without it.
- [`rl_reliability/strongbench/experiment-plan.md`](../../../rl_reliability/strongbench/experiment-plan.md)
  — the downstream consumer of these results. Its decision rule requires a
  held-out seed precisely because a deterministic environment can be memorised.
