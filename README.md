<div align="center">

# Applied AI Systems Engineering

**Build AI systems whose behavior can be measured, diagnosed, improved, and owned.**

An open curriculum and executable lab environment that takes one real agent from
a tool-using assistant to a measurable, diagnosable, data-producing, locally
improvable system.

[![Level 1 checks](https://github.com/agteo/applied-ai-systems-engineering/actions/workflows/level-1.yml/badge.svg)](https://github.com/agteo/applied-ai-systems-engineering/actions/workflows/level-1.yml)
[![Level 2 benchmark](https://github.com/agteo/applied-ai-systems-engineering/actions/workflows/level-2.yml/badge.svg)](https://github.com/agteo/applied-ai-systems-engineering/actions/workflows/level-2.yml)
[![Level 6 environments](https://github.com/agteo/applied-ai-systems-engineering/actions/workflows/level-6.yml/badge.svg)](https://github.com/agteo/applied-ai-systems-engineering/actions/workflows/level-6.yml)

![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue)
![Standard library only](https://img.shields.io/badge/dependencies-stdlib%20only-brightgreen)
![No API key required](https://img.shields.io/badge/API%20key-not%20required-brightgreen)
![Levels 1--7](https://img.shields.io/badge/levels-1--7%20executable-orange)
![Code MIT](https://img.shields.io/badge/code-MIT-blue)
![Content CC BY 4.0](https://img.shields.io/badge/content-CC%20BY%204.0-blue)

[Quickstart](#-quickstart-60-seconds) ·
[Curriculum](#-curriculum) ·
[Learning model](#-how-each-level-works) ·
[Tracks](#-specialization-tracks) ·
[Repository map](#-repository-map)

</div>

---

## ⚡ Quickstart (60 seconds)

No signup, no API key, no network, no package install.

```bash
git clone https://github.com/agteo/applied-ai-systems-engineering.git
cd applied-ai-systems-engineering/examples/strongbench-expense-agent
python3 run_agent.py --all --quiet
```

That runs the **StrongBench Expense Agent** over 22 tasks, writes a trace bundle,
and exits non-zero if any task fails to produce a contract-valid answer.

Then check the traces it just wrote:

```bash
python3 -m strongbench_agent.check_traces traces/level-1.jsonl
```

> [!NOTE]
> **On Windows?** `python3` does not exist on a standard Windows install.
> Read **[docs/windows.md](docs/windows.md)** first — it is three commands and a
> substitution rule, then everything here works.

<details>
<summary><b>Running the test suites</b> (the only part that needs a dependency)</summary>

<br>

Every agent and builder in this repo runs on the Python standard library alone.
`pytest` is needed only for the tests:

```bash
python3 -m pip install -r examples/strongbench-expense-agent/requirements.txt
python3 -m pytest
```

</details>

---

## 🎯 What This Is

**Applied AI Systems Engineering** is the discipline of building AI systems whose
behavior can be measured, diagnosed, improved, and owned.

This repository is an open-source curriculum and lab environment for developing
that talent. The goal is not just to teach people how to build agents. The goal
is to train engineers who can help organizations evaluate AI behavior rigorously,
use proprietary data responsibly, decide when local or open model improvement is
justified, and own more of their AI stack.

Agents are the course's practical vehicle because they expose the full applied AI
loop: tool use, workflow integration, evals, failure diagnosis, data generation,
model adaptation, simulated environments, and reinforcement learning.

```text
Build → Evaluate → Diagnose → Data → Post-train → Environments → RL
```

<details>
<summary><i>Formerly "Applied Agent Engineering" — why the rename?</i></summary>

<br>

The course was renamed because its scope now covers evals, data, model
improvement, environments, verifiers, and AI stack ownership — not only agent
construction.

</details>

### Learners are trained to become engineers who can

| | |
| --- | --- |
| 🏗️ | build AI systems around real business workflows |
| 📊 | evaluate model and agent behavior with reproducible benchmarks |
| 🔍 | diagnose failures from traces instead of guessing |
| 🗂️ | convert proprietary workflow data into defensible datasets |
| ⚖️ | decide when local or open model improvement is justified |
| 🔬 | compare local models, frontier APIs, retrieval, prompting, and tooling honestly |
| 🧪 | design simulated environments where agents can practice safely |
| 🔓 | help companies reduce dependency on black-box AI systems where appropriate |

Levels 1–4 train agentic systems engineering, evaluation, diagnosis, and data
curation. Actual model training is an advanced optional track that requires
additional prerequisites, compute, and executable training infrastructure.

---

## 📚 Curriculum

The **core curriculum is Levels 1–4**. Levels 5–7 are advanced specialization
tracks.

| Level | Module | Outcome |
| :---: | --- | --- |
| **0** | Foundations | Learn the engineering, LLM, data, and measurement basics needed for the course. |
| **1** | [Build](levels/01-build/README.md) | Build a tool-using agent that completes a multi-step business task. |
| **2** | [Evaluate](levels/02-evaluate/README.md) | Create reproducible evals, graders, and benchmark reports. |
| **3** | [Diagnose & Eval Ops](levels/03-diagnose/README.md) | Turn traces into failure datasets, regression checks, release gates, and evidence-backed failure analysis. |
| **4** | [Data and Feedback](levels/04-data/README.md) | Turn traces, failures, and human corrections into defensible datasets. |
| **5A** | [Model Improvement Decisions](levels/05-post-training/README.md) | Decide whether prompting, retrieval, tooling, frontier APIs, or local model adaptation is the right intervention. |
| **5B** | [Post-training Implementation](levels/05-post-training/README.md) | Run GPU-backed SFT/LoRA experiments and compare adapted local models. |
| **5C** | [Local Inference Operations](levels/05-post-training/README.md) | Deploy local or open models behind a gateway with routing, fallback, and observability. |
| **6** | [Environments and Verifiers](levels/06-environments/README.md) | Build simulated domains, state checks, constraints, and reward functions where agents can practice safely. |
| **7** | [RL Literacy](levels/07-reinforcement-learning/README.md) | Analyze rollouts, rewards, RLHF/RLVR, PPO/GRPO, and reward hacking. |

### Maturity and honest limits

| Status | Scope |
| --- | --- |
| ✅ **Executable** | Levels 1–6 — runnable locally, covered by CI |
| 📖 **Analysis only** | Level 7 — runs locally, but **does not train anything**, and does not prepare you for an RL engineering role |
| 🖥️ **Optional GPU** | Track 5B and hosted RL training |

**Next build priority:** finance simulator scope expansion — keep the first slice
expense-first, then add reporting, reconciliation, and related finance operations
workflows.

### Capstones

- **[Core Practical Capstone](capstones/core-practical/README.md)** — required, no GPU.
- **[Advanced GPU Model Adaptation Capstone](capstones/advanced-gpu-model-adaptation/README.md)** — optional, GPU required.

---

## 🚀 Run Every Level

Each level ships a runnable pipeline. Run them in order from the repository root
(after the [Quickstart](#-quickstart-60-seconds)) to build the full artifact chain.

<details open>
<summary><b>Levels 2–4 — evals, diagnosis, and data</b></summary>

<br>

**Level 2** — a deterministic 100-task benchmark, graders, a Markdown eval
report, and a CI release gate:

```bash
python3 -m evals.runner --model scripted
```

**Level 3** — the failure-analysis and regression bundle:

```bash
python3 -m evals.operations
```

**Level 4** — the cleaned StrongBench training dataset and dataset card:

```bash
python3 -m datasets.strongbench
```

</details>

<details>
<summary><b>Levels 5–7 — model improvement, environments, and RL literacy</b></summary>

<br>

**Level 5A** — the model-improvement decision bundle and SFT export, then
validate the optional LoRA config in dry-run mode:

```bash
python3 -m model_improvement.strongbench
python3 -m model_improvement.strongbench.train_lora --dry-run
```

**Level 6** — the StrongBench Finance Operations Simulator, verifiers, rollout
logs, and verifier-derived rewards:

```bash
python3 -m environments.strongbench_finance
```

**Workstream D** — a second code-repair environment built against the same
verifier and reward contract:

```bash
python3 -m environments.code_repair
python3 -m environments.runner environments.code_repair --out /tmp/code-repair-contract --tasks 12
```

**Level 7** — RL literacy over the local simulator: rollout comparison, reward
decomposition, and reward-hacking review. No training run happens, and hosted
training is kept optional and explicit:

```bash
python3 -m rl_reliability.strongbench
python3 integrations/prime-intellect/environments/strongbench_finance_reliability/strongbench_finance_reliability.py
```

</details>

---

## 🧭 How Each Level Works

Every level follows the same pattern:

```text
Concepts → Tools → Lab → Project → Evaluation
```

Every level also **consumes artifacts produced by earlier levels**. Learners do
not build seven unrelated demos. They evolve one canonical AI system from a basic
tool-using assistant into a measurable, diagnosable, data-producing, locally
improvable system.

### The canonical course system

The current executable course project is the **StrongBench Expense Agent**.

At first, it answers expense-policy questions and uses simple tools. Later,
learners evaluate it, diagnose its failures, convert traces into training data,
fine-tune or adapt a smaller local model, place it inside a simulated company
environment, and eventually train it through experience.

The agent is not the final point. It is the scaffold for learning how proprietary
data, evals, local models, verifiers, environments, and workflow ownership fit
together.

> The domain may expand from expense reimbursement into a broader finance
> operations agent if that better reflects deployed enterprise agent work:
> accounts payable, procure-to-pay, order-to-cash, reconciliation, audit support,
> approval routing, exception handling, and policy-governed workflow automation.
> See [curriculum/canonical-system-strategy.md](curriculum/canonical-system-strategy.md).

---

## 🛤️ Specialization Tracks

After Level 4, learners can choose one or more tracks:

| Track | Focus |
| --- | --- |
| **[Agent Quality Engineering](tracks/agent-quality-engineering.md)** | Evals, observability, reliability, red teaming, and production feedback loops. |
| **[Model Improvement](tracks/model-improvement.md)** | Proprietary data pipelines, SFT, LoRA, DPO, and model comparison. |
| **Local AI Stack Ownership** | Open model selection, local serving, gateway routing, fallback, observability, eval gates, data governance, and cost control. |
| **[Environment and Verifier Engineering](tracks/environment-verifier-engineering.md)** | Simulated workflows, deterministic checks, state verifiers, constraint scoring, sandboxes, and rewards. |
| **[RL Literacy for Agent Engineers](tracks/rl-literacy-for-agent-engineers.md)** | Rollouts, verifier-derived rewards, hosted training adapters, reward hacking analysis, and post-training regression evaluation. Analysis only — no training run. |

---

## 🗺️ Suggested Path

1. **Understand the shape.** Read [curriculum/framework.md](curriculum/framework.md)
   for what this course is and why it is built this way.
2. **Run the agent.** Follow the [Quickstart](#-quickstart-60-seconds), then read
   [the agent's README](examples/strongbench-expense-agent/README.md) —
   particularly the design decisions and the known limitations.
3. **Build your own.** Start [Level 1](levels/01-build/README.md) and build your
   own version *before* reading the
   [reference solutions](examples/strongbench-expense-agent/solutions/README.md).
4. **Keep going.** Work through the level pipelines in
   [Run Every Level](#-run-every-level), one level at a time.

### Reference material

Read these as you need them, not before.

| Document | What it gives you |
| --- | --- |
| [mental-models.md](curriculum/mental-models.md) | The reasoning patterns the levels assume. |
| [syllabus.md](curriculum/syllabus.md) | The full level-by-level sequence and pacing options. |
| [glossary.md](curriculum/glossary.md) | Key terms and acronyms. |
| [references.md](curriculum/references.md) | Prior art, indexed to the lesson where each one matters. |
| [feedback-and-assessment.md](curriculum/feedback-and-assessment.md) | How work is assessed. |

---

## 📁 Repository Map

<details>
<summary><b>Expand the full tree</b></summary>

<br>

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
  strongbench-expense-agent/   # the implemented Level 1 system
    strongbench_agent/         # harness, tools, schemas, validation, traces
    fixtures/                  # policy, receipt, employee, and task data
    solutions/                 # reference solutions for the Level 1 labs
    tests/
    run_agent.py

evals/
  strongbench_benchmark/       # Level 2 tasks, schema, graders, calibration, threshold
  operations/                  # Level 3 failure bundle and regression pack
  runner.py                    # benchmark runner
  report.py                    # deterministic Markdown report writer

datasets/
  strongbench/                 # Level 4 dataset builder and generated dataset card

model_improvement/
  strongbench/                 # Level 5A decision bundle, SFT export, LoRA dry-run config

environments/
  strongbench_finance/         # Level 6 simulator, tasks, rollouts, verifiers, rewards
  code_repair/                 # Workstream D transfer environment using the same contract
  contract.py                  # shared environment contract checks
  runner.py                    # domain-agnostic environment runner

rl_reliability/
  strongbench/                 # Level 7 rollouts, reward-hacking review, experiment templates

resources/
capstones/
templates/
tracks/
```

</details>

---

## 📄 License

This repository is licensed in two parts, split by file type:

| What | Files | License |
| --- | --- | --- |
| **Course content** — prose, lessons, labs, exercises, explanations | `.md` | [CC BY 4.0](LICENSE-CONTENT) |
| **Software** — source, config, and the fixtures the code operates on | everything else | [MIT](LICENSE) |

Code samples embedded inside Markdown files count as software, so you can lift
them into your own work under MIT without an attribution obligation. Reuse the
written curriculum under CC BY 4.0 with credit to this repository.

## 🤝 Contributing

Issues and pull requests are welcome — see [CONTRIBUTING.md](CONTRIBUTING.md)
for the content and code bars, and the checks to run locally before opening one.
