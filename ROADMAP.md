# Build Roadmap

This roadmap turns the curriculum specification into an executable course.

A phase is done when its code runs in CI. A phase whose spec reads well and
whose code does not exist is not started.

## How To Use This Roadmap

If you are picking up this work, read in this order:

1. [STATUS.md](STATUS.md) — what runs today and what does not.
2. **The Promise** and **Gap Ledger** below — what the repo owes a learner, and
   what is missing.
3. **Phase 2** — the only thing to build right now, with acceptance criteria.
4. **Release Milestones** — how phases and workstreams combine into something
   worth announcing.

Two rules govern the order of work, both inherited from
[STATUS.md](STATUS.md):

- Nothing new starts while an unshipped phase is the next priority. The failure
  mode this project watches for is specification work crowding out executable
  work.
- Writing a curriculum document is not progress. A phase ships when its code
  runs in CI.

Read the rest of this file as reference for the phase you are on, not
front to back.

## The Promise

The claim this repo makes to a learner is:

> Finish this and you can build an AI system, prove whether it works, explain
> why it fails, turn that into data, decide which intervention is justified,
> and defend the decision with evidence.

Level 1 is executable, which delivers *build*. Everything after *build* is
specification. The promise is currently one-sixth kept.

This section exists because the phase list can be fully checked off while the
promise stays unkept. Some of what the promise needs is not a phase. It is
teaching depth, worked examples, and evidence a learner can show someone else.

## Gap Ledger

What stands between this repo and the promise, ordered by leverage rather than
by level number.

| # | Gap | Why it blocks the promise | Lands in |
| --- | --- | --- | --- |
| 1 | No runnable benchmark or graders | Without Level 2 a learner can only claim "I built an agent", which is the commodity claim this course exists to beat. Every downstream artifact — failure taxonomy, regression pack, training comparison, reward design — is unfalsifiable until a benchmark can disagree with it. | Phase 2 |
| 2 | No finished example artifacts | A solo learner cannot tell a good eval report from a plausible one. A rubric with no anchored examples grades nothing. | Phase 3, Workstream B |
| 3 | Teaching depth inverts with difficulty | Level 1 lessons teach: loop diagrams, named failure modes, exercises. Levels 5-7 lessons list nouns and link out. Support is thinnest exactly where the learner is weakest. | Workstream A |
| 4 | No portfolio surface | Tracks list "portfolio evidence" but nothing in the repo shows what a hiring-legible deliverable looks like, and every graduate would ship an identical Acme repo. | Workstream C |
| 5 | One domain, and the easy end of it | Text-only finance operations is the gentle end of environment engineering. Hiring demand is code repair, browser and computer use, and multi-turn support. Verifier skill has to survive one transfer to prove it generalises. | Workstream D |
| 6 | The RL track terminates in prose | Phase 7 assumes hosted training. Without a funded run there is no honest completion bar, and the track name promises more than analysis delivers. | Phase 7 |

Gaps 1 and 2 are the release blockers. Gaps 3 through 6 are what separate a
course a learner can finish from a course that changes what they can be hired
to do.

## Build Architecture

The repo should own the portable improvement loop:

```text
traces -> evals -> failures -> data -> system/model changes -> environments -> verifiers -> rewards
```

External products are adapters. The core artifacts must remain runnable locally
and cheaply:

- agent tasks
- trace schema
- eval datasets
- deterministic graders
- simulated environment state
- deterministic, state, constraint, and model-based verifiers
- reward components
- rollout logs
- benchmark and regression reports

The current executable seed is the Acme Expense Agent. The likely canonical
direction is broader: an Acme Finance Operations Agent that can cover expenses,
invoices, purchase orders, approval routing, reconciliation, audit support, and
exception handling.

## Reference Stack

Use an open-source-first stack when quality and industry relevance are strong:

```text
Python + pytest
Docker
Langfuse
Inspect AI
GitHub Actions
Prime Intellect / Verifiers
```

Selection rule:

- prefer open-source, self-hostable, cost-effective tools when the quality bar
  is high and industry usage is credible
- use hosted platforms as optional accelerators, production variants, or
  advanced adapters
- keep course-owned abstractions portable across vendors

Current stack posture:

| Tool | Core Role | Posture |
| --- | --- | --- |
| Python + pytest | Deterministic verification | Open source, free, foundational. |
| Docker | Reproducible environments | Local-first and broadly used. |
| Langfuse | Tracing and observability | Open-source core, self-hostable, cloud optional. |
| Inspect AI | Evals-as-code and agent evals | Open source, local/CI friendly. |
| GitHub Actions | CI release gates | Free tier is enough for course workflows; concepts are portable. |
| Prime Intellect / Verifiers | Hosted RL path | Advanced adapter; local simulator and verifiers stay independent. |

Optional comparison labs can cover DeepEval, Braintrust, LangSmith, Weights &
Biases, MLflow, E2B, BrowserGym, Browserbase, METR Task Standard, and TRL.

Inspect AI is the primary evals-as-code framework for now because it maps well
to datasets, solvers/agents, tools, scorers, sandboxed tasks, eval logs,
external agents, and CI-friendly eval runs. DeepEval remains a useful optional
comparison framework for pytest-style LLM app evaluation.

## Verifier Engineering

A verifier answers: did the agent actually accomplish the task?

Teach four verifier types:

| Verifier Type | Use |
| --- | --- |
| Deterministic verifier | Check objective answers such as totals, dates, IDs, and policy citations. |
| State verifier | Check whether simulated databases, approvals, drafts, invoices, or records changed correctly. |
| Constraint verifier | Score partial completion across multiple required conditions. |
| Model-based verifier | Use an LLM judge or human rubric for subjective outcomes. |

Real agent evaluation should combine hard and soft verification:

```text
agent trajectory
      |
      +--> hard verifiers: state, database, API calls, calculations, constraints
      |
      +--> soft verifiers: LLM judge, rubric, human rating
      |
      v
task score
      |
      +--> evaluation
      |
      +--> reward for post-training / RL
```

Rewards must be compositional and log their components. Example components:

```text
+1.00 task_success
+0.25 correct_policy_basis
+0.20 required_records_checked
+0.20 correct_approval_behavior
+0.10 valid_final_answer_contract
-0.20 unnecessary_tool_call
-0.40 invalid_tool_call
-0.50 skipped_required_approval
-0.75 unauthorized_submission
-1.00 fabricated_policy_or_record
```

Reward-hacking traps should be explicit: asking for approval on everything,
refusing to act, calling every tool every time, optimizing final-answer format
while skipping state-changing work, learning fixture-specific shortcuts, and
submitting work without required evidence.

## Production Eval Operations

Learners should build this loop, not merely inspect a hosted dashboard:

```text
production traces
  -> failure review
  -> eval dataset
  -> regression pack
  -> eval harness
  -> release gate
  -> deploy or diagnose
  -> new test case
```

Reference implementation:

```text
Langfuse + Inspect AI + GitHub Actions + Python
```

Langfuse Cloud, Braintrust, LangSmith, and other hosted services are production
variants, not prerequisites.

## Phase 1: Make Level 1 Executable — SHIPPED

Goal: a learner can build and run the Acme Expense Agent locally.

All of it lives in [examples/acme-expense-agent/](examples/acme-expense-agent/).

- [x] Python project scaffold
- [x] dependency file
- [x] local model/API adapter interface (`acme_agent/models.py`)
- [x] Acme policy fixtures (`fixtures/policies.json`)
- [x] receipt and employee fixtures
- [x] calculator, policy search, receipt lookup, and approval tools (`acme_agent/tools.py`)
- [x] trace schema ([`docs/trace-schema.md`](examples/acme-expense-agent/docs/trace-schema.md))
- [x] trace writer (`acme_agent/trace.py`)
- [x] reference solution for Level 1 labs (`solutions/`)
- [x] basic tests (50, in `tests/`)
- [x] CI workflow for Level 1 checks ([`.github/workflows/level-1.yml`](.github/workflows/level-1.yml))

## Phase 2: Ship The Production Eval Foundation — SHIPPED

Goal: a learner can evaluate agent behavior against a real benchmark and use the result as a production-style release gate.

This is the only thing that matters until it ships. The Level 1 harness gives
Phase 2 what it needs to build against: a trace format, a final-answer
contract, fixtures with known-correct answers, and a zero-cost model adapter
that makes a 100-task run free and deterministic.

The current executable seed remains the Acme Expense Agent. The benchmark should be designed so it can expand into a broader Acme Finance Operations Agent if finance operations proves to be the right canonical domain.

Deliverables:

- 100-task Acme benchmark
- task schema
- expected outputs
- deterministic graders
- rubric grader
- human-reviewed calibration examples
- benchmark runner
- sample benchmark report
- production eval report format
- CI checks for Level 1 and Level 2 submissions
- release-gate thresholds and failure messages

Implemented in [evals/](evals/). The scripted baseline currently passes 89/100
tasks; the remaining failures are preserved as concrete Level 3 diagnosis
material rather than hidden.

Target layout:

```text
evals/
  acme_benchmark/
    tasks.jsonl              # 100 tasks: id, prompt, expected, tags, difficulty
    schema.json              # task schema, versioned
    graders/
      deterministic.py       # totals, dates, ids, citation existence
      contract.py            # final-answer contract conformance
      rubric.py              # model-based grader, rubric held separately
      rubric.md              # the rubric itself, human-reviewable without code
    calibration/
      human_reviewed.jsonl   # judge-vs-human agreement sample
  runner.py                  # runs a model adapter over the benchmark
  report.py                  # emits the eval report
  reports/sample-report.md   # the reference report Workstream B annotates
```

Acceptance criteria, in order:

1. `python3 -m evals.runner --model scripted` runs 100 tasks offline, with no
   API key, in under two minutes.
2. Task pass/fail is reproducible: same commit and same seed give the same
   report, byte for byte.
3. Every grader failure message names the task id and the field, matching the
   standard `acme_agent/check_traces.py` already set.
4. The rubric grader reports agreement rate against `human_reviewed.jsonl`, and
   the report states that number rather than hiding it.
5. `report.py` emits task success, cost, latency, and per-tag breakdown.
6. CI runs the benchmark and fails the build when success rate drops below a
   threshold committed in the workflow.
7. The task schema supports a domain field, so finance operations tasks can be
   added later without a migration.

Deliberate non-goals for Phase 2: real-model benchmark runs as a CI
requirement, a hosted dashboard, and any Level 3+ artifact.

## Phase 3: Add Production Eval Operations And Feedback Mechanisms

Goal: learners can turn traces into failure datasets, regression packs, release decisions, and meaningful feedback without needing the course author in the loop.

Deliverables:

- reference solutions for Levels 1-2 labs
- bad submission examples
- annotated failed traces
- failure analysis bundle
- trace-to-eval-dataset workflow
- regression pack generation
- grading rubrics with worked examples
- automated checks with clear failure messages
- instructor review guide
- optional Langfuse + Inspect AI integration notes

## Phase 4: Make Levels 3-4 Concrete

Goal: diagnosis and data work operate on real traces and failures.

Deliverables:

- failed trace bundle
- failure taxonomy examples
- annotated diagnosis examples
- trace-to-dataset converter
- cleaned dataset sample
- dataset card template and reference dataset card

## Phase 5: Split Model Training Into A Real Optional Track

Goal: distinguish model-improvement judgment from actual GPU-backed training.

Deliverables:

- Level 5A: model improvement decision track
- Level 5B: optional post-training implementation track
- compute requirements
- cost estimates
- small-model training script
- LoRA/QLoRA config
- model comparison report
- advanced GPU capstone bundle

## Phase 6: Environment And Verifier Prototype

Goal: make environment learning honest, bounded, and useful for both evaluation and later training.

Deliverables:

- Acme Finance Operations Simulator minimal implementation
- deterministic success checks
- state verifiers
- constraint verifiers
- model-based verifier examples
- rollout logger
- reward functions derived from verifier components
- reward hacking examples
- Level 7 RL reliability analysis path
- optional Prime Intellect adapter only after local environment and verifier contracts are real
- optional training path only after environment, verifier, and compute requirements are real

The simulator should be deterministic under a seed and emit rollout records
with task ID, seed, initial state hash, step list, terminal state, reward, and
component metrics.

Initial simulator state should cover:

- employees
- managers
- policies
- receipts
- trips
- draft reports
- approval requests
- audit log
- vendors
- invoices
- purchase orders
- reconciliation records
- exception queue

Initial actions should cover:

- search policy
- lookup receipt
- calculate reimbursement
- create expense draft
- attach receipt
- request manager approval
- submit report
- review invoice
- match purchase order
- route exception
- reconcile record
- ask clarifying question
- final answer

## Phase 7: Prime Adapter And RL Reliability Experiment

Goal: prove that verifier-derived rewards can support a serious RL reliability
experiment without making hosted training a prerequisite for the course.

Prime Intellect / Verifiers should be an adapter over the local simulator, not
the source of truth. The expected boundary is:

```text
local simulator + local verifiers
        |
        v
integrations/prime-intellect/environments/acme_finance_reliability/
        |
        v
hosted eval and optional hosted RL training
```

Deliverables:

- Prime-compatible Verifiers environment adapter
- eval config for a baseline run
- tiny RL smoke config
- small RL experiment config
- result report template
- validation note for Prime CLI/account differences
- optional TRL path for local or self-managed training comparison

### The Honest Bar Decision

Phase 7 currently assumes hosted training. If no run is funded, the track
delivers analysis documents while its title promises reliability engineering.
Resolve this before R3 by picking one:

- **Fund one reference run.** A single small GRPO or SFT run whose logs,
  learning curves, reward-component breakdown, and sampled rollouts are
  committed to `integrations/prime-intellect/reports/`. Learners who cannot
  afford compute still study a real run, and the track keeps its name. This is
  the preferred option: one funded run serves every future learner.
- **Rename the track.** Call it RL literacy for agent engineers, state in
  [README.md](README.md) and
  [tracks/rl-for-agent-reliability.md](tracks/rl-for-agent-reliability.md)
  that it does not prepare a learner for an RL engineering role, and define a
  completion bar the analysis path can actually meet.

Until one of the two lands, the README should not list this track alongside
tracks a learner can finish.

Example target files:

```text
integrations/prime-intellect/
  README.md
  environments/
    acme_finance_reliability/
      acme_finance_reliability.py
      pyproject.toml
      README.md
  configs/
    eval/acme-finance-reliability-baseline.toml
    rl/acme-finance-reliability-smoke.toml
    rl/acme-finance-reliability-small.toml
  reports/template.md
```

Every RL run should require:

1. Baseline eval before training.
2. Training run with a fixed task distribution.
3. Held-out eval after training.
4. Regression eval on the Level 2 benchmark.
5. Reward-component analysis.
6. Manual review of sampled rollouts.
7. Failure comparison before and after training.

Passing means more than "reward went up":

- held-out task success improves
- invalid or unsafe actions do not increase
- approval correctness improves or remains stable
- Level 2 benchmark does not materially regress
- sampled rollouts show real behavioral improvement

## Workstreams

Phases build the machine. Workstreams make it teachable. They run *behind*
Phase 2 — the Rule Of Construction in [STATUS.md](STATUS.md) applies to them
too, and no workstream opens while an unshipped phase is the next priority.

### Workstream A: Teaching Depth Parity

Goal: a lesson is done when a learner who has read nothing else can do the
thing. Today Level 1 lessons clear that bar and Levels 5-7 lessons do not.

Depth bar. Every lesson needs all five:

1. Core idea in prose, not a noun list.
2. A diagram or worked example of the actual mechanism.
3. At least one named, concrete failure mode.
4. An exercise with a checkable answer.
5. Reading tied to a specific decision the learner is about to make.

Immediate task: audit every lesson against the bar and add
`Status: outline` to the top of each one that fails, so the repo stops reading
as more finished than it is. That audit is one commit and it is worth doing
before any rewriting.

Rewrite priority:

| Lesson | Missing |
| --- | --- |
| `levels/07-reinforcement-learning/lessons/05-ppo-and-grpo.md` | Everything past the noun list: the clipped objective, advantage estimation, why GRPO drops the value model, the KL term and what raising it does, rollout batch sizing. Needs a read-along against a specific TRL trainer file, not the docs index. |
| `levels/07-reinforcement-learning/lessons/01-04, 06-07` | Same pattern, less severe. |
| `levels/06-environments/lessons/05-rewards-and-success-checks.md`, `07-rollout-analysis.md` | The reward table in this roadmap is more concrete than the lessons that teach it. Move it into the lessons. |
| `levels/02-evaluate/lessons/04-rubrics-and-llm-judges.md` | Names the calibration metrics but ships no copyable rubric. |
| `levels/04-data/lessons/06-splits-and-contamination.md` | Needs a worked contamination check against the Level 2 benchmark. |

Done when: no lesson in `levels/` carries `Status: outline`, and a
`scripts/check_lesson_depth.py` run in CI fails on any lesson missing an
exercise or a failure-mode section.

### Workstream B: Assessment Without An Instructor

Goal: a solo learner can tell whether their own work is good. This is the
cheapest fix for the risk named in
[curriculum/feedback-and-assessment.md](curriculum/feedback-and-assessment.md):
that the course "can create confidence without skill".

For each major deliverable — eval report, failure analysis, dataset card,
model improvement decision memo, reward design — ship three files:

```text
examples/reference-artifacts/<deliverable>/
  good.md          # the standard, annotated with why each part earns its place
  weak.md          # a plausible-but-bad version, same task, same data
  rubric.md        # high/medium/low anchors that quote good.md and weak.md
```

`weak.md` is the load-bearing one. The failure modes to dramatise are already
listed in `feedback-and-assessment.md`: brittle string matching, missing trace
data, vague failure labels, contaminated datasets, uncalibrated judges, and
training claims with no benchmark evidence.

Start with the eval report, because Phase 2 produces the data for it and
nothing downstream is gradeable without it.

Done when: every project spec in `levels/*/project/` links a rubric with
anchored examples, and no rubric cites an example file that does not exist.

### Workstream C: Portfolio Surface

Goal: the course produces something a hiring manager can read in ten minutes.
Tracks currently list portfolio evidence as bullet points; no example exists.

Deliverables:

- `templates/portfolio-writeup.md` — the public-facing writeup format: the
  problem, the measurement, the diagnosis, the intervention, the evidence it
  worked, and what the learner would do next.
- one filled-in example per track, built from the reference artifacts in
  Workstream B.
- a differentiation requirement added to
  [capstones/core-practical/README.md](capstones/core-practical/README.md):
  the capstone must contain at least one element the learner chose — their own
  failure mode, their own task family, or their own domain port. Identical
  submissions are a portfolio liability, and right now the capstone guarantees
  them.

Done when: a learner following the capstone produces a writeup that does not
match any other learner's on the chosen element.

### Workstream D: Domain Transfer

Goal: prove the verifier and reward contracts are skills rather than Acme
trivia. Text-only finance operations is the easy end of environment
engineering; the roles this curriculum targets are code repair,
browser/computer use, and multi-turn support.

The Level 6 contract should be domain-agnostic first, then ported once:

```text
levels/06-environments/           # teaches the contract
environments/acme_finance/        # domain 1 (Phase 6)
environments/<second_domain>/     # domain 2, same interface, different shape
```

Candidates, easiest first: a code-repair environment with test-suite
verification (SWE-bench-shaped); a multi-turn support environment with policy
and state checks (tau2-bench-shaped); a browser task environment
(WebArena-shaped, most expensive).

Deliverables:

- one alternate environment implementing the same verifier and reward
  interface as the Acme simulator
- a transfer note: what carried over, what did not, and what the second domain
  forced the interface to change

Done when: the same runner and the same verifier base classes execute both
environments in CI with no domain-specific branches in shared code.

## Release Milestones

Phases and workstreams interleave. These are the only four states worth
announcing.

| Release | Contents | A learner can then |
| --- | --- | --- |
| R1 | Phase 2 + Workstream B for the eval report | Complete Levels 1-2 alone and know whether their agent works. |
| R2 | Phases 3-4 + remaining Workstream B artifacts | Complete the core Levels 1-4 and the core capstone alone. |
| R3 | Workstream A depth pass + Phase 5 + the Phase 7 decision | Trust that a track's title matches what it delivers. |
| R4 | Phase 6 + Workstream D + Phase 7 | Show transferable environment and verifier work. |

R1 is the first release worth telling anyone about. Until it ships, the honest
description of this repo is "a well-built Level 1 and a detailed plan".

## Small Debts

Not phases. Fix in passing.

- [README.md](README.md) Start Here says `python run_agent.py`. Stock macOS has
  only `python3`, so step 2 of onboarding fails on a clean machine. Use
  `python3` throughout, or add a one-line note.
- README describes the run as having no dependencies while the test suite
  needs `pytest` from `requirements.txt`. Both are true of different commands;
  say which is which.
- The README track table implies parity across tracks whose completeness
  differs by an order of magnitude. Mark each track's state until R3.
