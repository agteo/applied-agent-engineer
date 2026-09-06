# RL Literacy for Agent Engineers

**What this track does not do:** it does not prepare you for an RL engineering
role. No training run happens here. If you need learning curves on your CV, this
track is the literacy prerequisite, not the qualification.

Renamed from "RL for Agent Reliability" because that title promised reliability
engineering while the track delivered analysis. The completion bar below is one
the analysis path can actually meet. See
[`ROADMAP.md`](../ROADMAP.md) — the Honest Bar Decision.

The executable path is [`rl_reliability/acme/`](../rl_reliability/acme/) and the
hosted adapter is
[`integrations/prime-intellect/`](../integrations/prime-intellect/). Hosted RL
training remains optional and must be backed by real logs and benchmark
comparison before any improvement claim is made.

## Focus

This track turns verifier-derived rewards into rollout analysis, and teaches you
to read a training result someone else produced without being fooled by it.

The goal is not to teach RL as an abstract math topic, and not to make you an RL
engineer. The goal is to make you the person who can say whether a claimed
improvement is real.

## Core Skills

- RL framing for agent tasks
- rollout generation
- verifier-derived reward design
- reward hacking review
- held-out evaluation design
- regression evaluation
- learning curve interpretation
- pre-training and post-training failure comparison

## Reference Stack

The course keeps the local environment and verifier contracts independent, then
exposes Prime Intellect as the hosted RL path:

```text
local simulator
local verifiers
local eval reports
Prime Intellect / Verifiers adapter
optional TRL path for local or self-managed training
```

Prime Intellect gives learners a concrete path from environment and verifier
work to hosted RL training. It is not required, and nothing in this track's
completion bar depends on it.

## Completion Bar

You have finished this track when you can produce all of these from the local
simulator, with no GPU:

- an RL framing of the environment: state, actions, observations, reward, termination
- rollout data with decomposed reward components
- a reward hacking review that names at least one exploit the current verifiers
  do **not** catch, with the check you would add
- a training experiment design: baselines, task distribution, held-out split,
  and the decision rule that would make you reject the trained policy
- a written critique of a training result you did not produce — what evidence is
  missing, and what claim the evidence actually supports

## If You Do Run Training

Optional, and out of scope for completion. A run counts as evidence only with
baseline eval, training logs, reward-component curves, held-out simulator eval,
a Level 2 benchmark regression check, and a sampled rollout review. See
[`integrations/prime-intellect/reports/template.md`](../integrations/prime-intellect/reports/template.md)
and [`VALIDATION.md`](../integrations/prime-intellect/VALIDATION.md).
