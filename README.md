# Applied Agent Engineering

Applied Agent Engineering is the discipline of building AI systems whose behavior can be measured, diagnosed, improved, and owned.

This repository is an open-source curriculum and lab environment for developing applied AI systems talent. The goal is not just to teach people how to build agents. The goal is to train engineers who can help organizations evaluate AI behavior rigorously, use proprietary data responsibly, decide when local or open model improvement is justified, and own more of their AI stack.

Agents are the course's practical vehicle because they expose the full applied AI loop: tool use, workflow integration, evals, failure diagnosis, data generation, model adaptation, simulated environments, and reinforcement learning.

## Maturity

Levels 1-6 are executable. Level 7 is an analysis-only literacy track: it runs
locally, but it does not train anything. Track 5B and hosted RL training remain
optional GPU work.

```bash
cd examples/acme-expense-agent
python3 run_agent.py --all --quiet
```

That runs the Acme Expense Agent over 22 tasks with no API key and no network, writes a trace bundle, and exits non-zero if any task fails to produce a contract-valid answer. Tools, fixtures, tests, reference solutions for all four Level 1 labs, and a CI workflow ship with it: [examples/acme-expense-agent/](examples/acme-expense-agent/).

Level 2 adds a deterministic 100-task benchmark, graders, a Markdown eval
report, and a CI release gate:

```bash
python3 -m evals.runner --model scripted
```

Level 3 builds the failure-analysis and regression bundle:

```bash
python3 -m evals.operations
```

Level 4 builds the cleaned Acme training dataset and dataset card:

```bash
python3 -m datasets.acme
```

Level 5A builds the model-improvement decision bundle and SFT export, then
validates the optional LoRA config in dry-run mode:

```bash
python3 -m model_improvement.acme
python3 -m model_improvement.acme.train_lora --dry-run
```

Level 6 builds the Acme Finance Operations Simulator, verifiers, rollout logs,
and verifier-derived rewards:

```bash
python3 -m environments.acme_finance
```

Level 7 builds RL literacy over the local simulator: rollout comparison, reward
decomposition, and reward-hacking review. No training run happens, and hosted
training is kept optional and explicit:

```bash
python3 -m rl_reliability.acme
```

The next build priority is hardening the course through the teaching-depth,
portfolio, and domain-transfer workstreams. Levels 5-7 lessons are still
outlines, so the code currently runs ahead of the teaching.

The course is organized around a simple progression:

```text
Build -> Evaluate -> Diagnose -> Data -> Post-train -> Environments -> RL
```

The core curriculum is Levels 1-4. Levels 5-7 are advanced specialization tracks for agent quality engineering, model improvement, local AI stack ownership, environment/verifier engineering, and reinforcement learning.

The course has two capstones:

- [Core Practical Capstone](capstones/core-practical/README.md): required, no GPU.
- [Advanced GPU Model Adaptation Capstone](capstones/advanced-gpu-model-adaptation/README.md): optional, GPU required.

## What This Curriculum Trains

Learners are trained to become engineers who can:

- build AI systems around real business workflows
- evaluate model and agent behavior with reproducible benchmarks
- diagnose failures from traces instead of guessing
- convert proprietary workflow data into defensible datasets
- decide when local or open model improvement is justified
- compare local models, frontier APIs, retrieval, prompting, and tooling honestly
- design simulated environments where agents can practice safely
- help companies reduce dependency on black-box AI systems where appropriate

The core Levels 1-4 train agentic systems engineering, evaluation, diagnosis, and data curation. Actual model training is an advanced optional track that requires additional prerequisites, compute, and executable training infrastructure.

## Learning Model

Every level follows the same pattern:

```text
Concepts -> Tools -> Lab -> Project -> Evaluation
```

Every level also consumes artifacts produced by earlier levels. Learners do not build seven unrelated demos. They evolve one canonical AI system from a basic tool-using assistant into a measurable, diagnosable, data-producing, locally improvable system.

The current executable seed is the Acme Expense Agent. The final canonical system should remain contingent on where companies are actually deploying agents and need stronger evaluation capability.

## Canonical Course System

The current executable course project is the Acme Expense Agent.

At first, it answers expense-policy questions and uses simple tools. Later, learners evaluate it, diagnose its failures, convert traces into training data, fine-tune or adapt a smaller local model, place it inside a simulated company environment, and eventually train it through experience.

The agent is not the final point. It is the scaffold for learning how proprietary data, evals, local models, verifiers, environments, and workflow ownership fit together.

The domain may expand from expense reimbursement into a broader finance operations agent if that better reflects deployed enterprise agent work: accounts payable, procure-to-pay, order-to-cash, reconciliation, audit support, approval routing, exception handling, and policy-governed workflow automation. See [curriculum/canonical-system-strategy.md](curriculum/canonical-system-strategy.md).

## Curriculum

| Level | Module | Outcome |
| --- | --- | --- |
| 0 | Foundations | Learn the engineering, LLM, data, and measurement basics needed for the course. |
| 1 | Build | Build a tool-using agent that completes a multi-step business task. |
| 2 | Evaluate | Create reproducible evals, graders, and benchmark reports. |
| 3 | Production Eval Operations and Diagnose | Turn traces into failure datasets, regression checks, release gates, and evidence-backed failure analysis. |
| 4 | Data and Feedback | Turn traces, failures, and human corrections into defensible datasets. |
| 5A | Model Improvement Decisions | Decide whether prompting, retrieval, tooling, frontier APIs, or local model adaptation is the right intervention. |
| 5B | Post-training Implementation | Run GPU-backed SFT/LoRA experiments and compare adapted local models. |
| 5C | Local Inference Operations | Deploy local or open models behind a gateway with routing, fallback, and observability. |
| 6 | Environments and Verifiers | Build simulated domains, state checks, constraints, and reward functions where agents can practice safely. |
| 7 | RL Literacy for Agent Engineers | Analyze rollouts, rewards, RLHF/RLVR, PPO/GRPO, and reward hacking. Analysis only; it does not prepare you for an RL engineering role. Optional training requires real compute and supervision. |

## Repository Map

```text
curriculum/
  framework.md
  references.md
  syllabus.md

levels/
  01-build/
    README.md
    lessons/
    labs/
    project/

examples/
  acme-expense-agent/     # the implemented Level 1 system
    acme_agent/           # harness, tools, schemas, validation, traces
    fixtures/             # policy, receipt, employee, and task data
    solutions/            # reference solutions for the Level 1 labs
    tests/
    run_agent.py

evals/
  acme_benchmark/          # Level 2 tasks, schema, graders, calibration, threshold
  operations/              # Level 3 failure bundle and regression pack
  runner.py                # benchmark runner
  report.py                # deterministic Markdown report writer
datasets/
  acme/                    # Level 4 dataset builder and generated dataset card
model_improvement/
  acme/                    # Level 5A decision bundle, SFT export, LoRA dry-run config
environments/
  acme_finance/            # Level 6 simulator, tasks, rollouts, verifiers, rewards
rl_reliability/
  acme/                    # Level 7 rollouts, reward-hacking review, experiment templates
resources/
capstones/
templates/
tracks/
```

## Tracks

After Level 4, learners can choose one or more tracks:

| Track | Focus |
| --- | --- |
| Agent Quality Engineering | Evals, observability, reliability, red teaming, and production feedback loops. |
| Model Improvement | Proprietary data pipelines, SFT, LoRA, DPO, and model comparison. |
| Local AI Stack Ownership | Open model selection, local serving, gateway routing, fallback, observability, eval gates, data governance, and cost control. |
| Environment and Verifier Engineering | Simulated workflows, deterministic checks, state verifiers, constraint scoring, sandboxes, and rewards. |
| RL Literacy for Agent Engineers | Rollouts, verifier-derived rewards, hosted training adapters, reward hacking analysis, and post-training regression evaluation. Analysis only — no training run. |

## Start Here

1. Read [curriculum/framework.md](curriculum/framework.md) for what this course is and why it is shaped this way.

2. Run the agent. No signup, no API key, no dependencies:

   ```bash
   cd examples/acme-expense-agent
   python3 run_agent.py --all --quiet
   python3 -m acme_agent.check_traces traces/level-1.jsonl
   ```

   Then read [its README](examples/acme-expense-agent/README.md), particularly the design decisions and the known limitations.

3. Start Level 1 in [levels/01-build/README.md](levels/01-build/README.md), and build your own version before reading the [reference solutions](examples/acme-expense-agent/solutions/README.md).

4. Run the Level 2 benchmark from the repository root:

   ```bash
   python3 -m evals.runner --model scripted
   ```

5. Build the Level 3 eval-ops bundle:

   ```bash
   python3 -m evals.operations
   ```

6. Build the Level 4 dataset bundle:

   ```bash
   python3 -m datasets.acme
   ```

7. Build the Level 5A model-improvement bundle:

   ```bash
   python3 -m model_improvement.acme
   python3 -m model_improvement.acme.train_lora --dry-run
   ```

8. Build the Level 6 simulator bundle:

   ```bash
   python3 -m environments.acme_finance
   ```

9. Build the Level 7 RL literacy bundle, and check the adapter loads:

   ```bash
   python3 -m rl_reliability.acme
   python3 integrations/prime-intellect/environments/acme_finance_reliability/acme_finance_reliability.py
   ```

Read these as you need them, not before:

- [curriculum/mental-models.md](curriculum/mental-models.md) — the reasoning patterns the levels assume.
- [curriculum/syllabus.md](curriculum/syllabus.md) — the full level-by-level sequence.
- [curriculum/glossary.md](curriculum/glossary.md) — key terms and acronyms.
- [curriculum/references.md](curriculum/references.md) — prior art, indexed to the lesson where each one matters.
- [curriculum/feedback-and-assessment.md](curriculum/feedback-and-assessment.md) — how work is assessed.
