# Lesson 4: RLHF and RLVR

## Core Idea

Both acronyms describe the same loop — sample behaviour, score it, update toward
higher scores — and differ in one place: **where the score comes from.**

**RLHF** (reinforcement learning from human feedback) derives reward from human
preference. People compare outputs, a reward model learns to predict those
comparisons, and the policy optimises against the reward model. It is how you
train for qualities nobody can write a checker for: helpfulness, tone,
appropriate hedging.

**RLVR** (reinforcement learning from verifiable rewards) derives reward from a
program. A checker looks at the outcome and returns a score with no judgment in
the loop. It applies wherever correctness is decidable: a test suite passes, a
total matches, an approval was requested when policy required it.

The engineering question is not which is better. It is **which parts of your task
are verifiable**, because those parts should never be handed to a preference
model. A verifiable outcome scored by human preference is more expensive, slower,
noisier, and less auditable than the check you could have written.

## Sort Your Outcomes First

Take the eight reward components from Level 6 and ask, of each, whether a program
can decide it:

| Component | Decidable by program? |
| --- | --- |
| `task_success` | yes — all checks pass |
| `correct_policy_basis` | yes — cited ⊆ retrieved, and covers required |
| `required_records_checked` | yes — successful lookups in the audit log |
| `correct_approval_behavior` | yes — approval presence vs policy requirement |
| `valid_final_answer_contract` | yes — schema plus total matches draft |
| `invalid_tool_call` | yes — count failed calls |
| `unauthorized_submission` | yes — actor vs employee, report vs authority |
| `model_based_answer_quality` | **no** — whether the answer explains itself |

Seven of eight are verifiable. That ratio is not an accident of this domain —
finance operations is rule-governed, and so is code repair, and so is most of
what agents are deployed to do in production.

**Push everything you can into RLVR and reserve judgment for the residue.** The
residue here is one component out of eight, weighted ±0.15, which is
proportionate to how much of the outcome it represents.

## The Judge In This Repo Is A Stand-In

`verifier_types` reports `model_based`, and the bias note is precise about what
that means:

```text
The model-based verifier is an offline reference judge, not a live LLM call.
```

Deterministic code standing in for a judge, so the course runs free and
identically everywhere. A reader seeing `model_based` would otherwise assume an
LLM with its cost, latency and variance.

This is worth understanding as a pattern rather than a limitation. The *seam* is
real: `model_answer_quality` is a named check consumed by a named reward
component, so swapping in a real judge changes one function and nothing else.
The architecture is RLVR-plus-one-judged-component either way.

Design the seam even if you never use a real judge. Reward components should not
know whether the check behind them is a program or a model.

## Verifiable Does Not Mean Unhackable

RLVR removes judgment from the loop; it does not remove exploits. Level 6's
reward hacker produces the correct total on 120 of 120 rollouts and passes
`deterministic_total` every time — a verifiable check, correctly implemented,
satisfied by memorisation.

What catches it is the *process* checks: it cited policies it never retrieved
and looked up zero receipts. Those are also verifiable, and they are the ones
that hold.

The generalisation: **a verifiable check on an outcome can be satisfied by any
route to that outcome.** If you care how the answer was reached, verify the
route. RLVR gives you cheap, auditable, stable reward — and none of that protects
a badly chosen check.

## Where Human Feedback Is Actually Required

Three places, and it is worth being able to name them:

**Qualities with no decision procedure.** Whether an explanation is clear enough
for the person reading it. `model_based_answer_quality` is the placeholder here.

**Calibrating the checks.** The Level 2 rubric grader is measured against a
human-labelled sample — an agreement rate on five rows, which Lesson 5 of Level 2
shows is far too small. Human labels are how you find out whether an automated
judge is trustworthy at all.

**Deciding what the rules should be.** No verifier tells you that room service
counts against the meal limit. A human wrote that policy, and every deterministic
check downstream inherits its authority from that decision.

The third is easy to forget. Verifiable rewards do not eliminate human judgment;
they relocate it from scoring individual outputs to writing the rules once.

## Cost, Speed, Auditability

| | RLVR | RLHF |
| --- | --- | --- |
| Marginal cost per score | ~zero | human time, or a reward-model call |
| Speed | as fast as your checker | slower by orders of magnitude |
| Stability | changes only when you change it | drifts with raters and models |
| Auditability | read the check | inspect a learned reward model |
| Covers subjective quality | no | yes |

The stability row is the one that matters most for evaluation. A verifiable
reward gives you comparisons that hold across months, because nothing moves
underneath. A learned reward model updated between two runs makes those runs
incomparable, silently.

## Common Failure Modes

- **Using preference data for verifiable outcomes.** Slower, noisier, less
  auditable than the check you skipped.
- **Assuming verifiable means unhackable.** The hacker passes every
  deterministic total check.
- **Verifying outcomes but not process.** Any route to the answer scores the
  same.
- **An unlabelled judged component.** Readers assume the whole reward is
  verifiable.
- **No seam for the judge.** Swapping a stand-in for a real model becomes a
  rewrite.
- **Comparing runs across reward-model versions.** The measuring instrument
  moved.
- **Forgetting that rules are human judgments.** The policy corpus is where the
  human input went.

## Exercise

Open [`reward-design.md`](../../../environments/strongbench_finance/reward-design.md)
and [`simulator-bias-note.md`](../../../environments/strongbench_finance/simulator-bias-note.md).

1. Seven of the eight reward components are program-decidable and one is not.
   Name the exception, and say what would have to be true for it to become
   verifiable.
2. The reward hacker passes `deterministic_total` on every rollout. Explain why
   that is not an argument against RLVR, and name the checks that catch it.
3. The model-based verifier is an offline stand-in. Give the argument for
   labelling that in the bias note rather than only in the code.

Check your answer:

```text
1. model_based_answer_quality — whether the final answer clearly explains the
   draft, submission, total and policy evidence. To become verifiable you would
   need a decision procedure for "clear enough", which means either reducing it
   to structural proxies (mentions the total, names the approval, cites a
   policy) — which is what the offline stand-in does — or accepting that the
   remainder is genuinely a judgment and keeping a model or a human in that one
   slot.

2. Because the failing check was badly chosen, not badly implemented.
   deterministic_total verifies an outcome, and any route to the right outcome
   satisfies it, including memorisation. The fix is more RLVR, not less: verify
   the process. constraint_required_records_checked catches it — zero
   lookup_receipt calls — and constraint_policy_basis_cited catches it, because
   it cited policies search_policy never returned. Both are verifiable checks.

3. Because verifier_types advertises "model_based", and a reader will price that
   as an LLM call with real cost, latency and variance — and will assume the
   reward has been tested against a real judge's noise. It has not. The bias
   note is where a reader learns that the model-based slot is deterministic code
   standing in, so simulator results do not carry evidence about how the reward
   behaves under a genuine judge.
```

Then take a task from your own work and sort its outcomes into verifiable and
judged. If everything lands in the judged column, look again — usually two or
three are decidable and were never written down as rules.

## Checkpoint

You are ready to move on when you can sort your reward components into
verifiable and judged, justify each judged one, and explain why a verifiable
reward still needs process checks rather than outcome checks alone.

## Reading

- [`environments/strongbench_finance/model-verifier-rubric.md`](../../../environments/strongbench_finance/model-verifier-rubric.md)
  — the rubric the offline judge stands in for. Read it as the specification a
  real judge would be given.
- [`rl_reliability/strongbench/reward-hacking-review.md`](../../../rl_reliability/strongbench/reward-hacking-review.md)
  — every exploit paired with the check that catches it. The table is a worked
  argument for verifying process rather than outcome.
