# Lesson 1: RL Framing

## Core Idea

Reinforcement learning has a specific shape, and the useful skill for an agent
engineer is recognising whether your problem has that shape — not implementing
the algorithms.

The shape is five parts: **state**, **actions**, **observations**, **reward**,
**termination**. Framing a problem means saying what each one is for your system,
concretely enough that someone could implement a runner from your description.

Doing that exercise is worth more than it sounds, because most agent problems
fail the test in an informative way. If your reward can only be computed by a
human, you do not have an RL problem; you have an evaluation problem with a
human in it. If your episodes never terminate, you have a service, not a task.
Writing the framing down is how you find out cheaply.

This repo's framing is committed as
[`mdp-framing.md`](../../../rl_reliability/strongbench/mdp-framing.md), and it is
worth reading as a template.

## The Five Parts, Filled In

**State.** The Level 6 simulator state: employees, managers, policies, receipts,
trips, drafts, approval requests, submitted reports, audit log. Twelve keys,
four of which start empty and record what the agent did.

The critical property is that state is *inspectable*. An RL framing where state
is "whatever the model has in context" cannot support verification, because
nothing outside the model can look at it.

**Actions.** Seven: `search_policy`, `lookup_receipt`, `get_employee_profile`,
`create_reimbursement_draft`, `request_manager_approval`,
`submit_reimbursement`, `final_answer`.

A discrete, enumerated action space with typed arguments. Not "the model emits
text" — the action space is closed, which is what makes an invalid action a
detectable event rather than an interpretation problem.

**Observations.** Each action returns an audit event: the action, a success
flag, and a structured payload. Note that observations include *failures* —
`ok: false` with an error — so the policy can react to being refused. An
observation channel that only reports success cannot teach recovery.

**Reward.** The sum of the verifier-derived components from Level 6. Not a
judgment, not a model call: eight named components, each derived from a named
check.

**Termination.** `final_answer`, or the runner truncates a rollout that cannot
produce one. Two reasons, both recorded in the rollout's `termination_reason`.

## Reward From Verifiers Is The Load-Bearing Choice

The framing says reward "is the sum of verifier-derived components from the
Level 6 environment", and everything downstream depends on it.

An RL setup whose reward is a separate judgment — a model call, a heuristic, a
human rating — has a reward nobody can audit and a policy that will find its
gaps. Deriving reward from checks that already have names means every point of
reward is traceable to a specific verifier, and a suspicious policy can be
diagnosed by reading which components it earned.

This is why Levels 6 and 7 are ordered as they are. **You cannot frame a
sensible RL problem until you have verifiers**, because the reward is the
verifiers. A team that reaches for RL before it can verify anything is choosing
its reward from whatever it can compute, which is how reward hacking gets
designed in from the start.

## What The Framing Refuses To Claim

The last section is the most important:

```text
This Phase 7 bundle compares a scripted reference policy to a deliberately weak
submitter policy; it does not claim trained-policy improvement.
```

A framing document is where overclaiming starts, because writing an MDP down
makes a project feel like an RL project. Stating what has *not* been done, in
the same file, is what keeps the framing a design artifact rather than an
implied result.

## Framing Is Not Permission To Train

Having a valid MDP does not mean RL is the right intervention — and here it is
not, for a reason visible in the framing itself.

The reference policy scores one distinct reward across all 120 rollouts. A
policy with no variance in its returns provides no gradient signal: advantage
estimation compares outcomes within a batch, and identical outcomes compare to
nothing. The framing is sound and the data is unusable for learning, which are
independent facts.

**A correct framing tells you what a training run would optimise. It does not
tell you that one would work.** The Level 5 decision — 49 tools-and-retrieval
labels against 13 model labels — is a separate argument, and it comes first.

## Where Agent Problems Usually Fail The Framing

Run the five parts against your own system and watch for these:

| Symptom | What it means |
| --- | --- |
| Reward needs a human | evaluation problem, not an RL problem |
| Episodes never end | a service, not a task |
| State lives only in the model's context | nothing can verify it |
| Actions are free-form text | invalid actions are uncountable |
| Reward is a single opaque score | no way to diagnose what a policy learned |

Each is a reason to stop and fix the environment rather than reach for a
trainer.

## Common Failure Modes

- **Framing before verifiers exist.** The reward becomes whatever is computable.
- **State the runner cannot inspect.** No verification, so no trustworthy reward.
- **Observations that omit failures.** Recovery cannot be learned or measured.
- **Unbounded episodes.** No terminal state means no return to attribute.
- **A single scalar reward.** Nothing to diagnose when a policy games it.
- **Treating a valid framing as a decision to train.** They are separate
  arguments.
- **A framing document with no "does not claim" section.** Reads as a result.

## Exercise

Open [`mdp-framing.md`](../../../rl_reliability/strongbench/mdp-framing.md) and
[`metrics.json`](../../../rl_reliability/strongbench/metrics.json).

1. The framing says observations carry a success flag. Name the policy behaviour
   that becomes learnable because failures are observable, and what an
   observation channel reporting only successes would cost.
2. Reward is defined as the sum of Level 6's verifier components rather than as
   a separate judgment. Give two properties this buys that a model-judged reward
   would not have.
3. `scripted_reference` has `distinct_rewards: 1` across 120 rollouts. Explain
   why the framing can be entirely correct while this dataset is unusable for
   training.

Check your answer:

```text
1. Recovery — retrying with corrected arguments after a refusal, or choosing a
   different route when a tool says no. With failures visible the policy can
   condition on them; if observations reported only successes, a refused
   submission would be indistinguishable from one that never happened, so the
   policy could neither learn to respond to refusal nor be measured on it. The
   invalid_tool_call penalty would also have nothing to count.

2. Auditability: every point of reward traces to a named verifier check, so a
   suspicious policy can be diagnosed by reading its components rather than
   guessing. And stability: verifier-derived reward does not drift when a
   provider updates a model, so a reward comparison across months is still a
   comparison. A model-judged reward has neither — it is opaque per-point and
   moves under you.

3. The framing describes the problem correctly: state, actions, observations,
   reward and termination are all well defined, and a policy operating in this
   environment is doing genuine RL-shaped work. The dataset is a separate
   matter. Advantage estimation compares returns within a group, and 120
   identical returns give nothing to compare, so there is no gradient signal
   regardless of how good the framing is. Correct framing, unusable data.
```

Then write the same five parts for a system you work on. The part you cannot
fill in is the finding.

## Checkpoint

You are ready to move on when you can state state, actions, observations, reward
and termination for your own system, say which of them your current tooling
cannot inspect, and separate "this is RL-shaped" from "we should train".

## Reading

- [`environments/strongbench_finance/reward-design.md`](../../../environments/strongbench_finance/reward-design.md)
  — the reward this framing points at, component by component. The framing is
  only as good as the verifiers underneath it.
- [`rl_reliability/strongbench/experiment-plan.md`](../../../rl_reliability/strongbench/experiment-plan.md)
  — what a framing becomes once it has a decision rule attached. Read it next;
  framing without a decision rule is a description.
