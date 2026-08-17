# Applied Agent Engineering

Applied Agent Engineering is the discipline of building AI systems whose behavior can be measured, diagnosed, and improved.

This repository is an open-source curriculum and lab environment for engineers who want to build reliable agents that interact with real tools, data, and environments. The course is organized around a simple progression:

```text
Build -> Evaluate -> Diagnose -> Data -> Post-train -> Environments -> RL
```

The core curriculum is Levels 1-4. Levels 5-7 are advanced specialization tracks for model improvement, simulated environments, and reinforcement learning.

## Learning Model

Every level follows the same pattern:

```text
Concepts -> Tools -> Lab -> Project -> Evaluation
```

Every level also consumes artifacts produced by earlier levels. Learners do not build seven unrelated demos. They evolve one canonical agent from a basic tool-using assistant into a measurable, diagnosable, improvable system.

## Canonical Course Agent

The default course project is the Acme Expense Agent.

At first, it answers expense-policy questions and uses simple tools. Later, learners evaluate it, diagnose its failures, convert traces into training data, fine-tune a smaller model, place it inside a simulated company environment, and eventually train it through experience.

## Curriculum

| Level | Module | Outcome |
| --- | --- | --- |
| 0 | Foundations | Learn the engineering, LLM, data, and measurement basics needed for the course. |
| 1 | Build | Build a tool-using agent that completes a multi-step business task. |
| 2 | Evaluate | Create reproducible evals, graders, and benchmark reports. |
| 3 | Diagnose | Analyze trajectories and classify agent failures with evidence. |
| 4 | Data and Feedback | Turn traces, failures, and human corrections into defensible datasets. |
| 5 | Post-training | Compare prompting, frontier models, and fine-tuned open models. |
| 6 | Environments | Build simulated domains where agents can practice safely. |
| 7 | Reinforcement Learning | Train agents through rollouts, rewards, and experience. |

## Repository Map

```text
curriculum/
  framework.md
  syllabus.md

levels/
  01-build/
    README.md
    lessons/
    labs/
    project/

examples/
  acme-expense-agent/

evals/
datasets/
environments/
templates/
```

## Tracks

After Level 4, learners can choose one or more tracks:

| Track | Focus |
| --- | --- |
| Agent Quality Engineering | Evals, observability, reliability, red teaming, and production feedback loops. |
| Model Improvement | Data generation, SFT, LoRA, DPO, and model comparison. |
| Agent Learning | Simulated environments, rewards, rollouts, and RL. |

## Start Here

1. Read [curriculum/framework.md](curriculum/framework.md).
2. Read [curriculum/syllabus.md](curriculum/syllabus.md).
3. Start Level 1 in [levels/01-build/README.md](levels/01-build/README.md).

