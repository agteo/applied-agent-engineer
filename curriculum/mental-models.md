# Mental Models

Hands-on building teaches learners how to make an agent run. Mental models teach them how to decide whether the agent should exist, whether it works, why it fails, and what to improve next.

These concepts should be revisited throughout the curriculum. They are not a separate theory track. They are the thinking tools behind every lab, project, eval, and diagnosis.

## Essential Spine

```text
Agents are systems, not prompts.
Behavior must be measured, not assumed.
Failures must be diagnosed, not hand-waved.
Proprietary data must be curated, not dumped into training.
Local models must be evaluated, not romanticized.
Improvements must be tested, not trusted.
Data is the bridge between failure and learning.
```

## 1. Agent System Fundamentals

Learners should understand:

- what an agent is, and what it is not
- LLM call vs workflow vs agent loop
- tool use and action selection
- state, memory, context, and persistence
- planning vs routing vs reflection
- human-in-the-loop control
- deterministic code vs probabilistic behavior
- why agents fail differently from normal software

These concepts are introduced in Level 1 and become concrete through tool use, trace capture, and harness design.

## 2. LLM Foundations

Learners should understand:

- tokens, context windows, and sampling
- temperature and decoding behavior
- system, user, assistant, developer, and tool messages
- structured outputs and schemas
- function calling and tool calling
- prompt design as interface design
- model capability differences
- latency, cost, and reliability tradeoffs
- hallucination, uncertainty, and calibration

These concepts belong in Foundations and Level 1, then return in Level 2 when learners measure output quality.

## 3. Software Engineering for Agents

Learners should understand:

- harness design
- tool contracts
- input and output validation
- error handling and recovery
- timeouts, retries, and idempotency
- logging and tracing
- versioning prompts, tools, datasets, and evals
- CI/CD for agent behavior
- testing probabilistic systems

These concepts start in Level 1 and become production-oriented in Level 2 and Level 3.

## 4. Evaluation and Measurement

Learners should understand:

- why "it worked once" is not evidence
- eval datasets
- golden tasks
- rubrics
- deterministic graders
- LLM-as-judge
- human evaluation
- pairwise comparisons
- precision, recall, F1, pass rate, and pass@k
- cost, latency, and quality tradeoffs
- statistical confidence
- eval leakage and contamination
- regression testing

This is the conceptual center of Level 2.

## 5. Failure Diagnosis

Learners should understand:

- agent trajectories
- tool selection failures
- tool argument failures
- retrieval failures
- reasoning failures
- instruction-following failures
- state and memory failures
- ambiguity and underspecification
- environment failures
- grader failures
- root cause analysis
- designing interventions and experiments

This is the conceptual center of Level 3.

## 6. Data and Feedback

Learners should understand:

- what counts as useful agent data
- traces, demonstrations, corrections, and preferences
- JSONL, Parquet, and dataset schemas
- data cleaning and deduplication
- train/test splits
- synthetic data generation
- rejection sampling
- preference pairs
- dataset quality metrics
- dataset cards
- provenance and licensing

This is the conceptual center of Level 4.

## 7. Retrieval and Knowledge Systems

Learners should understand:

- RAG basics
- chunking
- embeddings
- vector search
- hybrid search
- reranking
- citation and grounding
- freshness
- retrieval evaluation
- knowledge vs reasoning failures
- when RAG is better than fine-tuning

These concepts begin in Level 1, deepen in Level 2 and Level 3, and become part of the improvement decision in Level 4 and Level 5.

## 8. Safety, Security, and Permissions

Learners should understand:

- prompt injection
- tool abuse
- data exfiltration
- permission boundaries
- secrets handling
- sandboxing
- human approval gates
- privacy and compliance
- audit logs
- safe failure modes
- red teaming

These concepts should appear throughout the course, starting with Level 1 approval gates and becoming more explicit in production-quality evals.

## 9. Product and Workflow Judgment

Learners should understand:

- when an agent is appropriate
- when a workflow, script, search UI, or form is better
- designing around human review
- user trust and explainability
- UX for uncertainty
- escalation paths
- operational ownership
- cost-benefit analysis
- what "good enough" means in production

These concepts help learners avoid building impressive demos that do not solve real problems.

## 10. Model Improvement

Learners should understand:

- prompting vs retrieval vs tools vs fine-tuning
- supervised fine-tuning
- LoRA and QLoRA
- DPO
- reward models
- model distillation
- quantization
- model serving constraints
- benchmarking fine-tuned models
- knowing when not to train
- proprietary data as a model improvement asset
- local model ownership tradeoffs

These concepts become central in Level 5.

## 10a. Local AI Stack Ownership

Learners should understand:

- frontier API vs local model tradeoffs
- open model selection
- adapter ownership
- data governance
- privacy and compliance constraints
- inference cost and latency
- deployment and serving constraints
- eval gates for local model adoption
- hybrid architectures
- organizational dependency risk

These concepts become explicit in Level 5 and should influence project decisions in Levels 6 and 7.

## 11. Environments and Simulation

Learners should understand:

- simulated tools
- state transitions
- task generation
- reproducibility
- sandboxed practice environments
- automatic success checks
- reward design
- environment realism
- simulator bias
- domain modeling

These concepts become central in Level 6.

## 12. Reinforcement Learning Concepts

Learners should understand:

- Markov decision processes
- policies
- rewards
- rollouts
- exploration vs exploitation
- reward hacking
- RLHF
- RLVR
- PPO and GRPO at a conceptual level
- process vs outcome rewards
- offline vs online RL
- learning curves and failure analysis

These concepts belong after learners already understand evaluation, diagnosis, and environments.

## 13. Operations and Production Readiness

Learners should understand:

- observability
- monitoring
- drift
- incident response
- rate limits
- caching
- fallback models
- cost budgets
- latency budgets
- deployment patterns
- rollbacks
- continuous evals
- feedback loops

These concepts turn course projects into production engineering practice.

## Where These Fit

| Concept Area | Primary Location | Reinforced In |
| --- | --- | --- |
| Agent system fundamentals | Foundations, Level 1 | All levels |
| LLM foundations | Foundations, Level 1 | Level 2, Level 5 |
| Software engineering for agents | Level 1 | Level 2, Level 3 |
| Evaluation and measurement | Level 2 | All later levels |
| Failure diagnosis | Level 3 | Level 4, Level 5, Level 7 |
| Data and feedback | Level 4 | Level 5, Level 7 |
| Retrieval and knowledge systems | Level 1 | Level 2, Level 3, Level 5 |
| Safety, security, and permissions | Level 1 | All levels |
| Product and workflow judgment | Foundations | All projects |
| Model improvement | Level 5 | Level 2 regression evals |
| Local AI stack ownership | Level 5 | Level 6, Level 7 |
| Environments and simulation | Level 6 | Level 7 |
| Reinforcement learning | Level 7 | Advanced specialization |
| Production readiness | Level 2 | Level 3, Level 4, track projects |
