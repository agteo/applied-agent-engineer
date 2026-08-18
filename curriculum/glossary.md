# Glossary

Key terms and acronyms used throughout the Applied Agent Engineering curriculum.

## Agent

An AI system that can use a model to decide actions, call tools, observe results, maintain state, and continue until a task is complete or a stopping condition is reached.

## Agent Harness

The software layer that manages the agent loop, messages, tool calls, validation, state, traces, errors, and stopping conditions.

## Agent Loop

The repeated cycle of model call, action selection, tool execution, observation, and next decision.

## Agent Trajectory

The full sequence of steps an agent took during a task, including prompts, model responses, tool calls, observations, errors, and final answer.

## API

Application Programming Interface. A software interface that allows one program to call another system or service.

## Benchmark

A reproducible set of tasks and graders used to measure system behavior.

## CI

Continuous Integration. Automated checks that run when code changes, often used to catch regressions.

## Context Window

The amount of text, tokens, tool outputs, and conversation history a model can consider in a single request.

## Contamination

Leakage between training, development, or evaluation data that makes results look better than they really are.

## Dataset Card

A document describing a dataset's purpose, sources, schema, collection process, cleaning steps, splits, limitations, and appropriate uses.

## Deterministic Grader

A grader implemented with code that produces repeatable results for objective checks such as valid JSON, correct totals, required fields, or expected citations.

## DPO

Direct Preference Optimization. A preference optimization method that trains a model using preferred and rejected responses.

## Embedding

A numeric representation of text, images, or other data that can be compared for similarity.

## Eval

Short for evaluation. A structured process for measuring whether an AI system behaves as intended.

## Eval Dataset

A set of tasks used to evaluate model or agent behavior.

## Frontier Model

A high-capability hosted model from a leading AI provider. Frontier models are often strong but may have higher cost, latency, privacy, or dependency tradeoffs.

## Function Calling

A model capability where the model returns a structured request to call a function or tool instead of only producing prose.

## Golden Dataset

A carefully authored and reviewed evaluation dataset with trusted expected outputs.

## Golden Task

A high-quality evaluation task with a trusted expected answer or grading criteria.

## GRPO

Group Relative Policy Optimization. A reinforcement learning method used in some LLM post-training workflows that compares groups of sampled outputs.

## Hallucination

When a model produces unsupported or false information while presenting it as true.

## HITL

Human-in-the-loop. A system design pattern where a person reviews, approves, corrects, or overrides an AI system at important points.

## Inference

Running a trained model to produce outputs from inputs.

## JSONL

JSON Lines. A file format where each line is a separate JSON object. Commonly used for traces, eval tasks, and training examples.

## KL

Kullback-Leibler divergence. A measure of difference between probability distributions, often used in RL and post-training to keep a trained policy from drifting too far from a reference model.

## LLM

Large Language Model. A model trained to process and generate text or text-like tokens.

## LoRA

Low-Rank Adaptation. A parameter-efficient fine-tuning method that trains small adapter weights instead of updating all model weights.

## MCP

Model Context Protocol. A protocol for connecting AI systems to tools, data sources, and external capabilities through a common interface.

## MDP

Markov Decision Process. A formal reinforcement learning framework involving states, actions, transitions, rewards, and policies.

## Model Adapter

A small set of trained parameters used with a base model to alter behavior without replacing the entire model.

## Observability

The ability to inspect what a system is doing through traces, logs, metrics, and events.

## Parquet

A columnar data file format commonly used for larger structured datasets.

## Pass Rate

The percentage of tasks that pass a grader or benchmark.

## pass@k

A metric that measures whether at least one of k sampled attempts succeeds.

## PEFT

Parameter-Efficient Fine-Tuning. A family of methods for adapting models by training a small number of additional or selected parameters.

## Policy

In business workflows, a rule or guideline the agent should follow. In reinforcement learning, a policy is the strategy a model or agent uses to choose actions.

## PPO

Proximal Policy Optimization. A reinforcement learning algorithm commonly used to update policies while limiting unstable changes.

## Prompt

Instructions and context given to a model.

## Prompt Injection

An attack or failure mode where untrusted input attempts to override system instructions, reveal secrets, or misuse tools.

## QLoRA

Quantized Low-Rank Adaptation. A memory-efficient fine-tuning approach that combines quantization with LoRA.

## Quantization

Reducing the precision of model weights or activations to lower memory use and often improve inference efficiency.

## RAG

Retrieval-Augmented Generation. A pattern where a system retrieves relevant external information and provides it to the model before generation.

## Regression

A behavior that used to work but gets worse after a change.

## Reinforcement Learning

A training approach where an agent learns from actions, observations, and rewards.

## Reward

A signal used to score behavior in an environment or reinforcement learning setup.

## Reward Hacking

When an agent optimizes the reward signal in a way that does not match the real goal.

## RL

Reinforcement Learning.

## RLHF

Reinforcement Learning from Human Feedback. A training approach that uses human judgments or preferences to shape model behavior.

## RLVR

Reinforcement Learning from Verifiable Rewards. A training approach that uses automatically checkable outcomes as reward signals.

## Rollout

A full or partial trajectory generated by an agent interacting with an environment.

## Rubric Grader

A grader that uses a defined scoring rubric to assess qualities that may be difficult to check deterministically, such as clarity or usefulness.

## SFT

Supervised Fine-Tuning. Training a model on examples of desired input-output behavior.

## Structured Output

Model output that follows a defined schema, such as JSON with required fields.

## Synthetic Data

Data generated artificially, often by a model or script, rather than collected directly from real users or production systems.

## Tool Calling

The process where a model requests that the agent harness execute a specific tool with structured arguments.

## Tool Schema

A formal definition of a tool's inputs, outputs, purpose, and constraints.

## Trace

A structured record of a model or agent run, usually including inputs, outputs, tool calls, observations, errors, costs, and latency.

## Train/Development/Test Split

A separation of data into training data, development data for iteration, and test or held-out data for final evaluation.

## Verifier

A program or process that checks whether an output or action satisfies a condition, such as passing tests or reaching a correct environment state.

