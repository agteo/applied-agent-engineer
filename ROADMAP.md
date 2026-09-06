# Build Roadmap

This roadmap turns the curriculum specification into an executable course.

A phase is done when its code runs in CI. A phase whose spec reads well and
whose code does not exist is not started.

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
