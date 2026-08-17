# Syllabus

## Course Overview

Applied Agent Engineering teaches engineers how to build AI systems that can use tools, complete realistic tasks, improve through systematic measurement, and make productive use of proprietary data.

The course uses agents as the hands-on vehicle, but the broader goal is applied AI stack ownership: evals, traces, data pipelines, local model adaptation, workflow integration, simulation, and reinforcement learning.

The course has a four-level core and three advanced specializations.

The conceptual backbone for the course is documented in [mental-models.md](mental-models.md). Learners should revisit those mental models before each level.

## Recommended Pace

| Path | Duration | Audience |
| --- | --- | --- |
| Intensive | 4-6 weeks | Experienced engineers studying full-time. |
| Standard | 10-12 weeks | Working engineers studying part-time. |
| Extended | 16+ weeks | Teams using the course as an internal training program. |

## Prerequisites

Learners should be comfortable with:

- Python basics
- APIs and JSON
- command-line workflows
- Git and GitHub
- basic software testing

Helpful but not required at the start:

- statistics
- machine learning fundamentals
- PyTorch
- information retrieval

## Level 0: Foundations

### Purpose

Give learners the minimum foundation needed to build and evaluate applied AI systems without turning the beginning of the course into a math or ML bootcamp.

### Topics

- LLMs, tokens, context windows, and sampling
- prompts, messages, and structured outputs
- APIs, tools, and function calling
- JSON schemas and validation
- Python project structure
- basic statistics for evals
- data formats: JSONL, CSV, Parquet
- proprietary data, privacy, and governance basics
- local vs hosted model tradeoffs
- safety, permissions, and human approval

### Exit Criteria

Learners can call a model, validate structured output, run a small Python project, and explain why probabilistic systems need evaluation.

## Level 1: Build

### Purpose

Build a reliable tool-using agent that interacts with realistic systems.

### Topics

- LLM vs agent
- agent harnesses
- system prompts and instructions
- structured outputs
- tool calling
- state and context
- retrieval basics
- agent loops
- routing
- human-in-the-loop approval
- model selection

### Project

Build the Acme Expense Agent v1.

### Exit Criteria

The learner can build an agent that completes a multi-step expense task using at least three tools and produces a structured final answer.

## Level 2: Evaluate

### Purpose

Teach learners how to know whether an agent is good.

### Topics

- deterministic vs probabilistic systems
- eval datasets
- golden test cases
- rubrics
- deterministic graders
- LLM-as-judge
- human review
- precision, recall, F1, pass rate, pass@k
- cost, latency, and reliability
- contamination and leakage
- statistical significance
- CI-based regression evals

### Project

Create a benchmark for Acme Expense Agent v1 with at least 100 tasks, multiple grader types, and a reproducible eval report.

### Exit Criteria

The learner can compare two agent versions and explain why they trust the measurement.

## Level 3: Diagnose

### Purpose

Teach learners to explain why agents fail using evidence from trajectories.

### Topics

- traces and trajectories
- failure taxonomies
- tool selection errors
- tool argument errors
- retrieval failures
- hallucination
- state and memory bugs
- ambiguous tasks
- grader failures
- intervention design
- experiment tracking

### Project

Create an Agent Failure Report for the Level 1 agent using the Level 2 benchmark.

### Exit Criteria

The learner can classify failures, identify dominant failure modes, propose interventions, and test whether those interventions work.

## Level 4: Data and Feedback

### Purpose

Turn failures, traces, and human corrections into high-quality datasets.

### Topics

- JSONL and Parquet
- dataset schemas
- ingestion and cleaning
- deduplication
- train/test splitting
- data contamination
- synthetic data
- preference pairs
- trajectories
- rejection sampling
- quality scoring
- dataset cards
- dataset versioning

### Project

Create Agent Training Dataset v1 from traces, failures, human examples, and synthetic examples.

### Exit Criteria

The learner can convert messy agent behavior into a defensible dataset with provenance, schema, quality metrics, and limitations.

## Level 5: Post-training

### Purpose

Teach learners when and how to improve a model directly.

### Topics

- PyTorch fundamentals
- tokenization and chat templates
- supervised fine-tuning
- LoRA and QLoRA
- PEFT
- quantization
- learning rates and batch sizes
- checkpoints
- DPO
- reward models
- model comparison

### Project

Fine-tune an open model using the Level 4 dataset and compare it against the prompted baseline and a frontier model.

### Exit Criteria

The learner can explain whether fine-tuning improved the agent, whether the improvement is worth the cost, and what tradeoffs remain.

## Level 6: Environments

### Purpose

Teach learners to build simulated worlds where agents can practice safely.

### Topics

- environment state
- actions and observations
- deterministic simulation
- stochastic simulation
- task generation
- tool simulation
- state transitions
- rewards
- reproducibility
- sandboxing

### Project

Build Acme Corp Simulator, a simulated company environment with expense policies, employee records, receipts, approvals, and task outcomes.

### Exit Criteria

The learner can create a reproducible environment with tasks, state transitions, and automatic success checks.

## Level 7: Reinforcement Learning

### Purpose

Teach learners how agents can improve through experience.

### Topics

- Markov decision processes
- state and action spaces
- policies
- reward functions
- exploration and exploitation
- policy gradients
- reward hacking
- RLHF
- RLVR
- PPO
- GRPO
- process vs outcome rewards
- online vs offline RL
- rollout analysis

### Project

Train an agent through experience in the Acme Corp Simulator.

### Exit Criteria

The learner can run rollouts, train with verifiable rewards, publish learning curves, and evaluate the trained agent against the original benchmark.

## Final Portfolio

By the end of the curriculum, learners should have a public portfolio containing:

- a working tool-using agent
- an eval harness
- a benchmark dataset
- grader implementations
- an agent failure report
- a curated training dataset
- an optional fine-tuned adapter
- an optional simulated environment
- an optional RL training report
