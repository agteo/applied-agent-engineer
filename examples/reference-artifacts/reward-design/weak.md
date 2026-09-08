# Weak Reward Design: StrongBench Finance Reliability

> This is a *plausible* bad example, not a strawman. It is roughly what a
> careful engineer produces on a first pass, which is what makes it worth
> studying: the flaws are real and none of them look like flaws.

## Components

| Component | Weight |
| --- | ---: |
| `task_success` — all checks passed | +1.00 |
| `answer_quality` — the final answer is clear and complete | +0.30 |
| `cited_a_policy` — the answer cites at least one policy id | +0.20 |
| `requested_approval` — an approval was requested | +0.20 |
| `used_tools` — at least one tool was called | +0.10 |
| `invalid_tool_call` | −0.20 |
| `unsafe_submission` | −0.20 |

Total possible: 1.80.

## Reward Hacking Risks

Reward hacking is a known risk. We will monitor rollouts after training and
adjust weights if the policy starts exploiting the reward.

---

## Why This Is Weak

Five defects, in order of how much they cost.

**1. Three components reward an action rather than a judgment.**
`requested_approval` fires whenever an approval exists, so "request approval on
every task" collects it on all of them — including the majority where policy
requires none. `cited_a_policy` and `used_tools` have the same shape. **Any
check of the form "did the agent do X?" is satisfied by always doing X.** The
fix is to compare against expectation: `bool(approval) == expected`.

**2. The penalties are smaller than the rewards they guard.**
`unsafe_submission` at −0.20 against `requested_approval` at +0.20 means a
policy that submits everything and asks for approval everywhere breaks even.
A cheap exploit needs a penalty that outweighs the reward it collects, not one
that matches it.

**3. `answer_quality` is a judgment with no named check.** It cannot be
audited, it will drift with whatever produces it, and it is worth more than any
safety term. If a component cannot name the verifier check it reads, it is a
judgment call wearing a number's clothes.

**4. Nothing verifies process.** Every component reads the final answer or a
tool-call count. A policy that memorises correct totals, cites policies it never
retrieved, and looks nothing up scores 1.80 — full marks. There is no check
asking whether the agent *read* the receipts or whether the cited policies came
back from a search.

**5. The hacking section is an intention, not a control.** "We will monitor and
adjust" names no exploit and no detection. A risk register with no named check
per row cannot be verified and will not be maintained. Compare
[`good.md`](good.md), where every exploit is paired with the specific check that
catches it, and an adversarial policy is run to prove they fire.

## The Test It Fails

Write a policy that does the cheapest thing satisfying every component, and score
it. If it scores well, the reward is wrong. This one hands full marks to a policy
that never reads anything.
