# Applied Agent Engineering

Applied Agent Engineering is the discipline of building AI systems whose behavior can be measured, diagnosed, improved, and owned.

This repository is an open-source curriculum and lab environment for developing applied AI systems talent. The goal is not just to teach people how to build agents. The goal is to train engineers who can help organizations evaluate AI behavior rigorously, use proprietary data responsibly, decide when local or open model improvement is justified, and own more of their AI stack.

Agents are the course's practical vehicle because they expose the full applied AI loop: tool use, workflow integration, evals, failure diagnosis, data generation, model adaptation, simulated environments, and reinforcement learning.

## Maturity

Level 1 is executable. Levels 2-7 are specification.

```bash
cd examples/acme-expense-agent
python run_agent.py --all --quiet
```

That runs the Acme Expense Agent over 22 tasks with no API key and no network, writes a trace bundle, and exits non-zero if any task fails to produce a contract-valid answer. Tools, fixtures, tests, reference solutions for all four Level 1 labs, and a CI workflow ship with it: [examples/acme-expense-agent/](examples/acme-expense-agent/).

The next build priority is the 100-task golden benchmark and its graders, which is what makes Level 2 real. See [STATUS.md](STATUS.md) and [ROADMAP.md](ROADMAP.md).

The course is organized around a simple progression:

```text
Build -> Evaluate -> Diagnose -> Data -> Post-train -> Environments -> RL
```

The core curriculum is Levels 1-4. Levels 5-7 are advanced specialization tracks for model improvement, local AI stack ownership, simulated environments, and reinforcement learning.

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

## Canonical Course System

The default course project is the Acme Expense Agent.

At first, it answers expense-policy questions and uses simple tools. Later, learners evaluate it, diagnose its failures, convert traces into training data, fine-tune or adapt a smaller local model, place it inside a simulated company environment, and eventually train it through experience.

The agent is not the final point. It is the scaffold for learning how proprietary data, evals, local models, and workflow ownership fit together.

## Curriculum

| Level | Module | Outcome |
| --- | --- | --- |
| 0 | Foundations | Learn the engineering, LLM, data, and measurement basics needed for the course. |
| 1 | Build | Build a tool-using agent that completes a multi-step business task. |
| 2 | Evaluate | Create reproducible evals, graders, and benchmark reports. |
| 3 | Diagnose | Analyze trajectories and classify agent failures with evidence. |
| 4 | Data and Feedback | Turn traces, failures, and human corrections into defensible datasets. |
| 5A | Model Improvement Decisions | Decide whether prompting, retrieval, tooling, frontier APIs, or local model adaptation is the right intervention. |
| 5B | Post-training Implementation | Run GPU-backed SFT/LoRA experiments and compare adapted local models. |
| 6 | Environments | Build simulated domains where agents can practice safely. |
| 7 | RL Reading and Analysis | Analyze rollouts, rewards, RLHF/RLVR, PPO/GRPO, and reward hacking. Optional training requires real compute and supervision. |

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
datasets/
environments/
resources/
capstones/
templates/
```

## Tracks

After Level 4, learners can choose one or more tracks:

| Track | Focus |
| --- | --- |
| Agent Quality Engineering | Evals, observability, reliability, red teaming, and production feedback loops. |
| Model Improvement | Proprietary data pipelines, SFT, LoRA, DPO, and model comparison. |
| Local AI Stack Ownership | Open model selection, deployment tradeoffs, eval gates, data governance, and cost control. |
| Agent Learning | Simulated environments, rewards, rollouts, and RL. |

## Start Here

1. Read [curriculum/framework.md](curriculum/framework.md).
2. Read [curriculum/mental-models.md](curriculum/mental-models.md).
3. Use [curriculum/glossary.md](curriculum/glossary.md) for key terms and acronyms.
4. Read [curriculum/references.md](curriculum/references.md).
5. Read [curriculum/feedback-and-assessment.md](curriculum/feedback-and-assessment.md).
6. Read [curriculum/syllabus.md](curriculum/syllabus.md).
7. Check current maturity in [STATUS.md](STATUS.md).
8. Run the agent: [examples/acme-expense-agent/README.md](examples/acme-expense-agent/README.md).
8. Start Level 1 in [levels/01-build/README.md](levels/01-build/README.md).
