# Lab 4: RL Experiment Report

## Objective

Write the report and the decision rule **before** any run, so a disappointing
result can be published.

## Build

By the time results arrive you have spent a budget and told people it was
happening. A decision rule written at that moment will be shaped by the result
it is about to judge. So write it first.

Five sections:

1. **Question** — answerable, and containing the failure it guards against. Not
   "does it improve?" but "can experience improve reliability *without
   increasing unsafe actions*?"
2. **Baselines** — at least two, both runnable, one a deliberate negative
   control.
3. **Artifacts a run must save** — training logs, reward curves, sampled
   rollouts, post-training benchmark results. Listed before the run, so a
   missing one is a known omission rather than a discovery.
4. **Decision rule** — a conjunction, phrased as *only if*.
5. **Current status** — what has and has not been run.

Your decision rule needs at least three conditions:

- **held-out** improvement, not seen-task improvement
- **safety slice flat or better**, checked separately, never netted into an
  aggregate
- **the original benchmark does not regress**

Phrase it as "better only if". A rule listing what would make you *reject*
invites arguing about whether this particular result is one of those cases.

## Deliverable

Submit:

- the experiment plan, committed before any run
- a report template with the evidence table already laid out
- your rollout set's variance, and whether it can train anything

## Checks

```bash
python3 - <<'PY'
import re
plan = open("path/to/your/experiment-plan.md").read().lower()
for name, pat in [("question", r"##\s*question"),
                  ("baselines", r"##\s*baselines"),
                  ("decision rule", r"##\s*decision rule"),
                  ("status", r"status|current")]:
    print(f"  {'OK ' if re.search(pat, plan) else 'MISSING'} {name}")
conj = sum(w in plan for w in (" and ", "without increasing", "does not regress"))
print("OK: rule is a conjunction" if conj >= 2
      else "FAIL: single-condition rule - optimisation will satisfy it the wrong way")
print("OK: states what has not been run" if "not been performed" in plan
      or "no trained" in plan or "not_run" in plan else "FAIL: no status")
PY
```

The lab passes when the plan predates any run, its rule is a conjunction phrased
as *only if*, and it states plainly what has not been done.

## Reference

Compare against
[`experiment-plan.md`](../../../rl_reliability/strongbench/experiment-plan.md)
and
[`experiment-report.md`](../../../rl_reliability/strongbench/experiment-report.md).

```bash
cat rl_reliability/strongbench/experiment-plan.md
```

Both are committed with no run behind them, which is the right order. The report
opens "Do not claim RL improvement yet" and carries a section titled *What this
rollout set cannot do* — stating that with near-constant reward per policy the
data is a regression suite, not training data.

Writing that section before the run is what makes it possible to publish a
disappointing result. A report drafted afterwards will find a way to keep a good
number.
