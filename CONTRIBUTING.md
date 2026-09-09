# Contributing

Thanks for considering a contribution. This repository is a curriculum *and* an
executable lab environment, so a change is usually one of two kinds — course
content or code — and each has a different bar.

## Before you start

For anything larger than a typo or a broken link, **open an issue first** and
describe what you want to change and why. The levels build on each other, so a
change in one level often has to be reflected in the artifacts a later level
consumes.

## Ground rules for code

Two constraints keep this repo usable by every learner, and CI enforces both:

1. **Standard library only** for agents and builders. If a change needs a third-
   party package to *run*, it almost certainly belongs somewhere else. `pytest`
   is the one dependency, and only the test suites use it.
2. **No API key, no network** on the default path. The default model adapter is
   a deterministic offline planner, so CI never spends money and never flakes on
   a provider outage. Anything requiring a key or a GPU must be opt-in and
   explicitly marked as such.

Python 3.10 and 3.12 are both tested.

## Ground rules for course content

Numbered lessons are held to the depth bar in
[`levels/LESSON-TEMPLATE.md`](levels/LESSON-TEMPLATE.md). A lesson is either
complete against that bar, or honestly marked `Status: outline` — a
half-finished lesson presented as finished is worse than an outline.

`scripts/check_lesson_depth.py` mechanically enforces two of the five criteria
(a named failure-mode section and an exercise section). The other three need a
human reviewer, which is what the template is for.

Worked examples should be **taken from a file in this repo** and walked through,
rather than invented for the lesson. If the example drifts from the code, the
lesson is wrong.

## Running the checks locally

Run these from the repository root before opening a pull request:

```bash
# tests
python3 -m pip install -r examples/strongbench-expense-agent/requirements.txt
python3 -m pytest

# the Level 1 system still solves every task and writes a valid trace bundle
cd examples/strongbench-expense-agent
python3 run_agent.py --all --quiet
python3 -m strongbench_agent.check_traces traces/level-1.jsonl
cd ../..

# content gates
python3 scripts/check_lesson_depth.py
python3 scripts/check_portfolio_surface.py
```

If you touched a level's pipeline, run that level's builder too — the commands
are listed under **Run Every Level** in the [README](README.md).

## Pull requests

- Keep the change focused; one concern per pull request.
- Say what you ran to verify it, and paste the relevant output.
- If a check fails and you believe the check is wrong, say so in the pull
  request rather than working around it.

## Licensing of contributions

By contributing you agree that your contributions are licensed under the same
terms as the repository: **MIT** for code, **CC BY 4.0** for course content.
See [LICENSE](LICENSE) and [LICENSE-CONTENT](LICENSE-CONTENT).
