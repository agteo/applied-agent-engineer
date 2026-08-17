# Curriculum Framework

## Thesis

Applied Agent Engineering is the discipline of building AI systems whose behavior can be measured, diagnosed, improved, and owned.

The curriculum is designed around one belief: building an agent is only the beginning. Serious engineering starts when you can explain whether the system works, why it fails, what data would improve it, and whether the organization should rely on a frontier API, retrieval system, workflow automation, local model, fine-tuned adapter, or reinforcement learning loop.

Agents are used as the practical course vehicle because they expose the whole applied AI stack: orchestration, tools, business data, evals, traces, feedback, post-training, environments, and deployment tradeoffs.

## Curriculum Shape

```text
                         APPLIED AGENT ENGINEERING

                                Foundations
                                     |
                                     v
                                  L1 Build
                                     |
                                     v
                                L2 Evaluate
                                     |
                                     v
                                L3 Diagnose
                                     |
                                     v
                              L4 Data and Feedback
                                     |
                +--------------------+--------------------+
                |                    |                    |
                v                    v                    v
        Agent Quality          Model Improvement     Agent Learning
        Engineering            and Local AI Stack    L6 Environments
        Production evals       L5 Post-training             |
        Observability                 |                     v
        Red teaming                   +---------------> L7 RL
```

Levels 1-4 are the core. They are mandatory because every applied AI engineer needs to know how to build a workflow-connected AI system, evaluate it, diagnose it, and convert behavior into usable data.

Levels 5-7 are specializations. They matter deeply, but not every practitioner needs to become a model training or RL engineer. Learners who continue into these levels learn how to adapt open models, build proprietary improvement loops, and reason about owning more of the AI stack.

## Level Pattern

Each level uses the same teaching pattern:

```text
Concepts -> Tools -> Lab -> Project -> Evaluation
```

### Concepts

The mental models learners need before they touch code.

### Tools

The practical libraries, APIs, schemas, scripts, and workflows used in the level.

### Lab

A focused exercise that teaches one skill under constrained conditions.

### Project

A cumulative build that advances the canonical course system.

### Evaluation

The exit test for the level. Learners must demonstrate that their work behaves as intended.

## Artifact Chain

Each level produces artifacts that become inputs to later levels.

| Level | Produces | Consumed By |
| --- | --- | --- |
| L1 Build | Agent harness, tool schemas, traces | L2 eval cases and graders |
| L2 Evaluate | Benchmark dataset, grader outputs, eval report | L3 failure analysis |
| L3 Diagnose | Failure taxonomy, annotated trajectories, interventions | L4 data generation |
| L4 Data | Curated proprietary-style dataset, dataset card, quality metrics | L5 post-training |
| L5 Post-training | Local model adapter, model comparison report | L2 regression benchmark |
| L6 Environments | Simulated domain, tasks, reward functions | L7 rollouts |
| L7 RL | Training runs, learning curves, trained adapter | L2/L3 final evaluation |

## Canonical Agent

The default project is the Acme Expense Agent.

The agent helps employees answer expense-policy questions, search receipts and approvals, prepare reimbursement drafts, and route edge cases to a human reviewer.

This domain is useful because it is realistic without requiring real private data. It includes policies, structured records, proprietary-style business data, tool use, ambiguity, permissions, compliance, and measurable task outcomes.

The agent is a scaffold, not the ceiling. By the end of the curriculum, the learner has built the surrounding improvement system: evals, traces, datasets, adapted local models, simulator, and training loop.

## Design Principles

### Build One System Repeatedly

Learners should experience improvement over time. The same agent should become more reliable because the learner learned how to measure and repair it.

### Evaluation Is Not Optional

Every project must include a reproducible way to decide whether the system improved.

### Diagnosis Comes Before Optimization

The curriculum should train learners to avoid vague claims like "the model is bad" and instead say, "most failures come from incorrect tool arguments after ambiguous entity resolution."

### Data Must Have Provenance

Datasets should include source, schema, filtering criteria, limitations, and separation between training and evaluation data.

### Proprietary Data Is An Engineering Asset

Companies do not get durable AI advantage merely by prompting frontier models. They need systems for collecting, cleaning, governing, evaluating, and using their own workflow data.

### Local Models Must Earn Their Place

Owning more of the AI stack can improve cost, latency, privacy, customization, and independence. But local models must be compared honestly against frontier APIs, retrieval, prompting, and deterministic software.

### Advanced Training Must Justify Itself

Fine-tuning and RL are not assumed to be correct. Learners must compare them against prompting, better tooling, better retrieval, and stronger frontier models.

## Mental Models

The curriculum is supported by a shared set of mental models in [mental-models.md](mental-models.md).

These concepts are revisited throughout the course:

- agents are systems, not prompts
- behavior must be measured, not assumed
- failures must be diagnosed, not hand-waved
- proprietary data must be curated, not dumped into training
- local models must be evaluated, not romanticized
- improvements must be tested, not trusted
- data is the bridge between failure and learning

## Competency Targets

By the end of the core curriculum, a learner can:

1. Build a tool-using agent that performs a multi-step task.
2. Create a benchmark that measures task success, quality, cost, and latency.
3. Diagnose failures from traces using a structured taxonomy.
4. Convert failures and human feedback into a clean dataset.
5. Explain which intervention is most likely to improve the system and why.

By the end of the advanced curriculum, a learner can:

1. Fine-tune or adapt an open model using a curated dataset.
2. Compare prompted, frontier, and fine-tuned systems on the same benchmark.
3. Build a simulated environment with tasks, state transitions, and rewards.
4. Run rollouts and analyze whether experience improves agent behavior.
5. Advise when a company should use a frontier API, local model, retrieval system, workflow automation, or hybrid stack.
