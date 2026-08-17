# Build Roadmap

This roadmap turns the curriculum specification into an executable course.

## Phase 1: Make Level 1 Executable

Goal: a learner can build and run the Acme Expense Agent locally.

Deliverables:

- Python project scaffold
- dependency file
- local model/API adapter interface
- Acme policy fixtures
- receipt and employee fixtures
- calculator, policy search, receipt lookup, and approval tools
- trace schema
- trace writer
- reference solution for Level 1 labs
- basic tests
- CI workflow for Level 1 checks

## Phase 2: Ship The Golden Eval Set

Goal: a learner can evaluate agent behavior against a real benchmark.

Deliverables:

- 100-task Acme benchmark
- task schema
- expected outputs
- deterministic graders
- rubric grader
- human-reviewed calibration examples
- benchmark runner
- sample benchmark report
- CI checks for Level 1 and Level 2 submissions

## Phase 3: Add Feedback Mechanisms

Goal: learners get meaningful feedback without needing the course author in the loop.

Deliverables:

- reference solutions for Levels 1-2 labs
- bad submission examples
- annotated failed traces
- grading rubrics with worked examples
- automated checks with clear failure messages
- instructor review guide

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

## Phase 6: Environment And RL Prototype

Goal: make environment learning honest and bounded.

Deliverables:

- Acme Corp Simulator minimal implementation
- deterministic success checks
- rollout logger
- reward hacking examples
- Level 7 reading-and-analysis path
- optional training path only after environment and compute requirements are real
