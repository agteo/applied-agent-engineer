# RL for Agent Reliability

## Focus

RL for Agent Reliability is the advanced path that turns verifier-derived rewards into rollout analysis and optional training experiments.

The goal is not to teach RL as an abstract math topic. The goal is to test whether experience improves agent behavior in a measurable workflow environment.

## Core Skills

- RL framing for agent tasks
- rollout generation
- verifier-derived reward design
- reward hacking review
- held-out evaluation
- regression evaluation
- learning curve interpretation
- pre-training and post-training failure comparison

## Reference Stack

The course should keep the local environment and verifier contracts independent, then expose Prime Intellect as the hosted RL path:

```text
local simulator
local verifiers
local eval reports
Prime Intellect / Verifiers adapter
optional TRL path for local or self-managed training
```

Prime Intellect is useful because it gives learners a concrete path from environment and verifier work to hosted RL training. It should not be required for learners who only complete the analysis path.

## Portfolio Evidence

A learner completing this track should have:

- an RL framing of the environment
- rollout data with reward components
- reward hacking risk analysis
- a training experiment design
- learning curves if training is run
- held-out eval results
- regression eval results
- a recommendation about whether the trained agent is more reliable

