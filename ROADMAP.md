# Build Roadmap

This roadmap turns the curriculum specification into an executable course.

A phase is done when its code runs in CI. A phase whose spec reads well and
whose code does not exist is not started.

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

## Phase 2: Ship The Production Eval Foundation — NEXT

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
