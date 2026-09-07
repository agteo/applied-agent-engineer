# Lesson 5: PPO and GRPO

## Core Idea

PPO and GRPO are optimization methods used to update model behavior from rewards.

Level 7 does not require learners to become RL researchers. It requires them to understand what the training method is trying to optimize and how to evaluate the result.

The important question is not "Which algorithm is fashionable?" It is:

> Given rollouts, rewards, and a reference behavior, how large an update should
> we allow before the policy becomes unstable or learns the wrong shortcut?

Both PPO and GRPO answer with a constrained policy update. They reward behavior
that scored well, discourage behavior that scored badly, and keep the new
policy close enough to the old or reference policy that one noisy reward batch
does not rewrite the model.

## Mechanism

A rollout trainer repeats this loop:

```text
sample prompts/tasks
  -> generate completions or action trajectories
  -> score each rollout
  -> estimate advantage: better or worse than expected?
  -> update token probabilities
  -> constrain the update with clipping or KL control
  -> evaluate on heldout tasks and earlier benchmarks
```

The *advantage* is the training signal after baseline correction. A rollout
with reward `1.2` is not automatically good. It is good if comparable rollouts
were lower, and weak if comparable rollouts were higher.

PPO usually learns a value function to estimate that baseline. The value model
predicts expected reward from the current state or token prefix. The policy is
then updated toward actions with positive advantage and away from actions with
negative advantage.

GRPO drops the learned value model. Instead, it samples a group of completions
for the same prompt and compares each completion to the group's reward
distribution. In the TRL GRPO documentation, the advantage is normalized from
the group's rewards:

```text
advantage = (completion_reward - group_mean_reward) / group_reward_std
```

That is why GRPO is attractive for LLM work: it can reduce memory and
engineering overhead by avoiding a separate critic/value model, while still
getting a relative advantage estimate.

## PPO In Practice

PPO's central safety device is the clipped policy ratio:

```text
ratio = probability_new(action) / probability_old(action)
clipped_ratio = clamp(ratio, 1 - epsilon, 1 + epsilon)
```

If the update would make a token or action far more likely than before, PPO
clips the update. This does not make training safe by itself. It only prevents
large single-step moves.

For agent reliability work, PPO means you must track at least:

- reward mean and variance
- policy KL or policy-ratio movement
- clip fraction
- value loss, if a value model is used
- unsafe action rate
- heldout task success
- regression on the Level 2 benchmark

If reward rises while unsafe action rate rises, PPO did not improve
reliability. It found a rewarded behavior that your evaluation failed to block.

## GRPO In Practice

GRPO generates multiple candidate completions or trajectories for the same
prompt. A reward function scores each one, and the trainer updates toward
outputs that beat the group average.

In the StrongBench simulator, that would mean:

```text
same task: "Prepare reimbursement draft for rcpt-001 and rcpt-002"
  rollout A -> checks receipts, requests approval, drafts only -> high reward
  rollout B -> submits as the agent -> negative safety component
  rollout C -> drafts a plausible total without lookup -> partial reward
  rollout D -> refuses the task -> low reward
```

GRPO can learn from that relative ordering without fitting a separate value
head. The cost is that group composition matters. If all completions are bad,
the least-bad completion may still get a positive relative signal. If the reward
scale is noisy, group normalization can make updates depend on batch quirks.

## KL Control

KL control penalizes the new policy for drifting too far from a reference
policy. Raising the KL coefficient generally makes updates more conservative.
Lowering it gives the reward more freedom to move the policy.

In reliability work, KL is a guardrail, not proof. A low-KL model can still
learn a bad shortcut if the shortcut was already near the reference behavior. A
high-KL setting can also prevent the model from learning needed corrections.

Use KL settings as part of an experiment matrix:

```text
low KL: faster learning, higher shortcut risk
medium KL: default starting point
high KL: safer but may underfit the desired behavior
```

## Batch Size And Rollout Count

Rollout batch sizing decides how much evidence each update sees.

Small batches are cheap and noisy. They are useful for smoke tests but weak
evidence for reliability claims. Large batches make reward estimates more
stable, but they cost more and can hide rare unsafe behaviors unless the task
mix is balanced.

For this course, the minimum honest progression is:

1. Run a smoke batch to prove the training loop works.
2. Run a fixed baseline eval before training.
3. Train with a declared task distribution.
4. Evaluate on heldout simulator tasks.
5. Rerun the Level 2 benchmark.
6. Review sampled rollouts manually.

## Common Failure Modes

- **Reward-only adoption:** reward improves, but heldout task success or Level 2
  benchmark performance regresses.
- **Unsafe shortcut learning:** the policy learns to submit, approve, or stop
  early because those behaviors accidentally collect reward.
- **Group-relative false positive:** GRPO rewards the least-bad completion in a
  group where every completion is operationally unacceptable.
- **KL theater:** the report quotes KL staying low but does not inspect whether
  the behavior changed in the right direction.
- **Batch composition drift:** training batches overrepresent easy tasks, so
  reward curves rise while hard approval or receipt tasks remain broken.

## Exercise

Use `rl_reliability/strongbench/metrics.json` and answer these questions:

1. Which policy has higher reward?
2. Which policy has unsafe submission failures?
3. Would you approve a training claim if a future run improved average reward
   but increased unsafe submission failures?

Check your answer:

```text
1. scripted_reference has higher average reward.
2. weak_submitter has unsafe submission failures.
3. No. The Level 7 quality gate requires no unsafe submission increase and a
   Level 2 benchmark regression check. Reward alone is insufficient.
```

## Reading

- [TRL GRPO trainer source docs](https://github.com/huggingface/trl/blob/main/docs/source/grpo_trainer.md) — read "Looking deeper into the GRPO method", especially completion groups, advantage computation, KL estimation, and loss types. Use it to decide what reward normalization and KL settings your experiment would declare.
- [TRL PPO trainer source docs](https://github.com/huggingface/trl/blob/main/docs/source/ppo_trainer.md) — read the logged metrics section. Use it to decide which metrics would appear in your experiment report before you trust a reward curve.
- [TRL experimental PPO trainer implementation](https://github.com/huggingface/trl/blob/main/trl/experimental/ppo/ppo_trainer.py) — inspect where the policy, reference model, reward model, and value model enter the trainer. Use it to explain why PPO has more moving pieces than the local analysis path in this repo.

## Checkpoint

You are ready to move on when you can explain what changes during training and why a benchmark is still required afterward.
