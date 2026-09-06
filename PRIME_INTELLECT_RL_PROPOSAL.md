# Environment, Verifier, and RL Integration Proposal

Date: 2026-09-06

## Recommendation

Adapt this repository around a vendor-neutral environment and verifier architecture, then use Prime Intellect as the advanced hosted RL path.

Do not create a separate Prime Intellect project, and do not make Prime the organizing center of the curriculum. The repository should own the agent tasks, traces, eval datasets, deterministic verifiers, rewards, rollouts, and reports. External systems should be adapters.

The target shape is:

```text
Production traces
        |
        v
Eval datasets + regression packs
        |
        v
Local eval harness + deterministic graders
        |
        v
Acme Finance Operations simulated environment
        |
        v
Verifiers and reward functions
        |
        +--> Production eval operations
        |
        +--> Prime-compatible hosted RL training
```

## Curriculum Thesis

Applied Agent Engineering should train people to operate the full agent improvement loop:

```text
traces -> evals -> failures -> data -> system/model changes -> environments -> verifiers -> rewards
```

Levels 1-4 should be presented as a common core. Levels 5-7 should become specialization tracks:

```text
Common Core
  L1 Agent & Harness Engineering
  L2 Evaluation
  L3 Production Eval Operations and Failure Analysis
  L4 Data & Feedback

Specializations
  Agent Quality Engineering
  Model Improvement
  Environment and Verifier Engineering
  RL for Agent Reliability
```

Prime Intellect fits as the advanced endpoint where environment/verifier work becomes hosted RL training.

The current executable seed is the Acme Expense Agent, but the likely canonical direction is broader: an Acme Finance Operations Agent. The environment and verifier design should support expansion from expenses into invoices, purchase orders, approval routing, reconciliation, audit support, and exception handling.

## Reference Stack

The core school should standardize around a small, open-source-first stack:

```text
Python + pytest
Docker
Langfuse
Inspect AI
GitHub Actions
Prime Intellect / Verifiers
```

Selection rule:

```text
Prefer open-source, self-hostable, cost-effective tools when the quality bar is high and industry usage is credible.
Use hosted platforms as optional accelerators, production variants, or advanced adapters.
Keep course-owned abstractions portable across vendors.
```

Current fit:

| Tool | Core Role | Open-Source / Cost Posture |
| --- | --- | --- |
| Python + pytest | Deterministic verification | Open source, free, foundational. |
| Docker | Reproducible environments | Open ecosystem, local-first. |
| Langfuse | Tracing and observability | Open-source core, self-hostable, cloud optional. |
| Inspect AI | Evals-as-code and agent evals | Open source, local/CI friendly. |
| GitHub Actions | CI release gates | Free tier is enough for course workflows; portable concepts. |
| Prime Intellect / Verifiers | Hosted RL path | Use as advanced hosted adapter; keep local simulator/verifiers independent. |

Optional comparison labs can expose learners to:

```text
DeepEval
Braintrust
LangSmith
Weights & Biases
MLflow
E2B
BrowserGym
Browserbase
METR Task Standard
TRL
```

The educational objective is not vendor fluency. A graduate should be able to walk into a company using Braintrust instead of Langfuse, LangSmith instead of Inspect, or Scale environments instead of Prime and still understand the architecture.

## Why Inspect AI Over DeepEval As The Primary Framework

Inspect AI is the better primary evals-as-code framework for this repo because it is open source and maps more cleanly to the full course arc:

```text
datasets
solvers / agents
tools
scorers
sandboxed tasks
eval logs
external agent integration
CI-friendly eval runs
```

That makes it a stronger fit for agent evaluation, production regression packs, sandboxed workflows, and the later bridge into environment/verifier engineering.

DeepEval is still useful. It is approachable, pytest-like, and strong for teaching simple LLM assertions, RAG metrics, conversational metrics, and CI integration. It should appear as an optional comparison exercise, especially for learners coming from application testing.

The curriculum position should be:

```text
Inspect AI = primary framework for general agent evals and eval operations.
DeepEval = optional comparison framework for pytest-style LLM app evaluation.
```

This should remain a pragmatic choice rather than a permanent bet. If DeepEval's open-source framework becomes the better fit for agent trajectories, tools, and stateful verification, the adapter layer should make it easy to swap.

## Production Eval Operations

Production Eval Operations teaches this loop:

```text
PRODUCTION
    |
    v
TRACE
    |
    +----------------+
    |                |
    v                v
Observability    Failures
                     |
                     v
                Eval dataset
                     |
                     v
                Eval harness
                     |
          +----------+----------+
          |                     |
          v                     v
        PASS                  FAIL
          |                     |
          v                     v
       Deploy              Diagnose
                                |
                                v
                          New test case
                                |
                                v
                              repeat
```

Learners should be able to build this loop, not merely click around an observability UI.

Platform categories:

| Platform Type | Examples | What Students Learn |
| --- | --- | --- |
| Agent observability / tracing | Langfuse, LangSmith, Arize Phoenix | Inspect traces, tool calls, latency, token cost, and failure points. |
| Eval platforms | Braintrust, LangSmith, Langfuse | Datasets, experiments, graders, comparisons, and release evidence. |
| Eval frameworks | Inspect AI, DeepEval, Ragas | Evals-as-code, automated testing, and reproducible scoring. |
| Experiment tracking | Weights & Biases, MLflow | Compare models, runs, prompts, configs, and datasets. |
| CI/CD | GitHub Actions | Prevent bad agent versions from shipping. |

Core repo deliverables:

```text
evals/acme-expense-benchmark/
  tasks.jsonl
  expected_outputs.jsonl
  graders.py
  runner.py
  report.py

integrations/langfuse/
  README.md
  trace-export.md
  dataset-import.md

integrations/inspect-ai/
  README.md
  acme_eval.py
  scorers.py

.github/workflows/
  acme-evals.yml
```

## Verifier Engineering

A verifier answers:

> Did the agent actually accomplish the task?

This is stronger than asking an LLM whether the final response looks plausible.

Example:

```text
Task:
Cancel my 3pm meeting with Sarah and reschedule it for Friday at 11am.

State verifier:
  Thursday 3pm event deleted       pass
  Friday 11am event created        pass
  Sarah invited                    pass
  Other meetings unchanged         pass

Reward:
  1.0
```

Verifier Engineering should teach four verifier types:

### A. Deterministic Verifier

Use when there is an objectively correct answer.

```python
assert invoice.total == 183.42
```

This is the best case because the reward is unambiguous.

### B. State Verifier

Use when the agent must change an environment correctly.

```python
assert crm.customer["status"] == "qualified"
assert crm.deals["123"].value == 50_000
```

This is critical for workflow agents.

### C. Constraint Verifier

Use when a task has multiple requirements.

```text
email sent              pass
correct recipient       pass
attachment included     pass
amount correct          pass
subject line correct    fail

reward = 0.8
```

### D. Model-Based Verifier

Use for subjective outcomes:

```text
Was this support response empathetic, accurate, and actionable?
```

This can use an LLM judge and rubric, but it is inherently noisier than hard verification.

Real agent evaluation should combine hard and soft verification:

```text
AGENT TASK
    |
    v
Agent trajectory
    |
    +---------------------+
    |                     |
    v                     v
Hard verifiers       Soft verifiers
  state                LLM judge
  database             rubric
  API calls            human rating
  calculations
  constraints
    |                     |
    +----------+----------+
               |
               v
          Task score
               |
        +------+------+
        |             |
        v             v
    Evaluation      Reward
                      |
                      v
                Post-training
```

## Core Goal

The goal should be narrower than "train an agent with RL."

The proposed goal is:

> Improve the reliability of the Acme Finance Operations Agent in simulated finance workflows, measured by deterministic task success, tool discipline, policy compliance, approval correctness, state integrity, and regression resistance.

Concrete reliability dimensions:

```text
Task completion
Policy correctness
Tool-call validity
State consistency
Approval safety
Recovery from missing or ambiguous data
No unauthorized actions
No reward-hacking shortcuts
Stable behavior across task variants
```

## Proposed Repository Structure

```text
environments/
  acme-finance-simulator/
    acme_sim/
      state.py
      actions.py
      tools.py
      tasks.py
      rewards.py
      rollout.py
      fixtures/
    tests/
    README.md
    pyproject.toml

integrations/
  langfuse/
    README.md
    trace-export.md
    dataset-import.md

  inspect-ai/
    README.md
    acme_eval.py
    scorers.py

  deepeval/
    README.md
    comparison-lab.md

  prime-intellect/
    README.md
    environments/
      acme_finance_reliability/
        acme_finance_reliability.py
        pyproject.toml
        README.md
    configs/
      eval/
        acme-finance-reliability-baseline.toml
      rl/
        acme-finance-reliability-smoke.toml
        acme-finance-reliability-small.toml
        acme-finance-reliability-ablation.toml
    reports/
      template.md

  browsergym/
    README.md
    acme-browser-task-sketch.md

  metr-task-standard/
    README.md
    acme-task-family-sketch/

levels/07-rl/
  README.md
  lessons/
    01-rl-for-agent-reliability.md
    02-environments-as-evals.md
    03-reward-design.md
    04-rollouts-and-credit-assignment.md
    05-prime-intellect-hosted-training.md
    06-reward-hacking-and-regression.md
    07-rl-result-review.md
  labs/
    lab-01-baseline-rollouts.md
    lab-02-reward-function.md
    lab-03-prime-env-adapter.md
    lab-04-hosted-rl-smoke-run.md
    lab-05-reliability-regression-report.md
  project/
    acme-agent-reliability-rl.md
```

## Phase 1: Build The Production Eval Foundation

Prioritize the existing Phase 2 roadmap: the 100-task golden benchmark and deterministic graders.

RL without a stable benchmark is hard to interpret. We need to know whether a trained model became more reliable or merely better at exploiting a narrow reward.

Deliverables:

```text
evals/acme-expense-benchmark/
  tasks.jsonl
  expected_outputs.jsonl
  graders.py
  runner.py
  report.py
```

Metrics:

```text
exact_success_rate
policy_citation_accuracy
required_tool_use_rate
invalid_tool_call_rate
approval_escalation_accuracy
final_answer_contract_pass_rate
latency_or_step_count
```

## Phase 2: Add Production Eval Operations

Add the production quality loop around the benchmark:

```text
trace export
failure tagging
dataset curation
regression pack generation
eval report
release gate
CI workflow
```

Reference implementation:

```text
Langfuse + Inspect AI + GitHub Actions + Python
```

This reference implementation is intentionally open-source-first and local/CI friendly. Langfuse Cloud, Braintrust, LangSmith, and other hosted services should be framed as production variants, not prerequisites for learning the loop.

The later comparison lab can replace one component:

```text
Langfuse -> LangSmith or Braintrust
Inspect AI -> DeepEval
GitHub Actions -> another CI system
```

## Phase 3: Build The Acme Finance Operations Simulator

Prime can host training, but the repository needs to own the environment.

Implement the simulator locally first.

Start with the existing expense workflow, but design the simulator as Acme Finance Operations rather than as a reimbursement-only domain.

State:

```text
employees
managers
policies
receipts
trips
draft_reports
approval_requests
audit_log
vendors
invoices
purchase_orders
reconciliation_records
exception_queue
```

Actions:

```text
search_policy
lookup_receipt
calculate_reimbursement
create_expense_draft
attach_receipt
request_manager_approval
submit_report
review_invoice
match_purchase_order
route_exception
reconcile_record
ask_clarifying_question
final_answer
```

Observations:

```text
tool result
validation error
policy snippet
missing data notice
approval status
terminal success/failure
```

The simulator should be deterministic under a seed. Every rollout should emit JSONL traces compatible with the existing trace philosophy.

Example rollout record:

```json
{
  "task_id": "acme_finance_sim_042",
  "seed": 42,
  "initial_state_hash": "...",
  "steps": [
    {
      "role": "assistant",
      "action": "lookup_receipt",
      "args": {"receipt_id": "r_182"}
    },
    {
      "role": "environment",
      "observation": {"merchant": "Hotel Atlas", "amount": 248.12}
    }
  ],
  "terminal_state": "success",
  "reward": 0.83,
  "metrics": {
    "policy_correct": true,
    "approval_required": true,
    "approval_requested": true,
    "invalid_actions": 0
  }
}
```

## Phase 4: Add Reliability Verifiers And Rewards

Rewards should be compositional, not one opaque scalar.

Example reward components:

```text
+1.00 task_success
+0.25 correct_policy_basis
+0.20 required_receipts_checked
+0.20 correct_approval_behavior
+0.10 valid_final_answer_contract
-0.20 unnecessary_tool_call
-0.40 invalid_tool_call
-0.50 skipped_required_approval
-0.75 unauthorized_submission
-1.00 fabricated_policy_or_receipt
```

Each component should also be logged as a metric. This is critical because a scalar reward curve alone will hide regressions.

Include specific reward-hacking traps:

```text
Agent asks for approval on everything.
Agent refuses to act to avoid mistakes.
Agent calls every tool every time.
Agent optimizes final answer format but skips state-changing work.
Agent learns fixture-specific shortcuts.
Agent submits drafts without required evidence.
```

## Phase 5: Create A Prime-Compatible Verifiers Environment

Prime/Verifiers environments package the task dataset, harness, and rubric. Keep this as an adapter over the local simulator.

That boundary matters. The simulator remains ours; Prime is one runner.

Prime adapter shape:

```python
# integrations/prime-intellect/environments/acme_finance_reliability/acme_finance_reliability.py

import verifiers as vf

def load_environment(config):
    dataset = load_acme_finance_tasks(config.taskset)
    rubric = vf.Rubric(
        funcs=[
            task_success_reward,
            policy_correctness_reward,
            approval_safety_reward,
            tool_validity_reward,
            format_reward,
        ],
        weights=[1.0, 0.3, 0.4, 0.2, 0.1],
    )

    return AcmeFinanceReliabilityEnv(
        dataset=dataset,
        rubric=rubric,
        simulator_config=config.simulator,
    )
```

Start with a multi-turn tool environment where the model must interact with simulated tools and eventually produce a final answer.

Target workflow:

```bash
prime env install integrations/prime-intellect/environments/acme_finance_reliability
prime eval run acme-finance-reliability -m <baseline-model> -n 20
```

## Phase 6: Add Prime Configs For Evaluation And RL

Add checked-in config templates, but do not commit credentials or account-specific state.

Example files:

```text
integrations/prime-intellect/configs/eval/acme-finance-reliability-baseline.toml
integrations/prime-intellect/configs/rl/acme-finance-reliability-smoke.toml
integrations/prime-intellect/configs/rl/acme-finance-reliability-small.toml
```

The first RL config should be deliberately tiny: a smoke run that proves packaging, rollouts, reward logging, and result review work.

Example config intent:

```toml
model = "Qwen/Qwen3-4B-Instruct-2507"
max_steps = 50
batch_size = 64
rollouts_per_example = 4

[sampling]
max_tokens = 1024

[[env]]
id = "acme-finance-reliability"
```

Expected user workflow:

```bash
prime login
prime env install integrations/prime-intellect/environments/acme_finance_reliability
prime eval run acme-finance-reliability -n 20
prime train run integrations/prime-intellect/configs/rl/acme-finance-reliability-smoke.toml
prime train logs <run-id> -f
```

Exact commands may need adjustment against the installed Prime CLI and user account state. The repository should include a validation note instead of assuming all learners have identical Prime setup.

## Phase 7: Define The Reliability Experiment Protocol

Every RL run should require:

```text
1. Baseline eval before training.
2. Training run with fixed task distribution.
3. Held-out eval after training.
4. Regression eval on the Level 2 benchmark.
5. Reward-component analysis.
6. Manual review of sampled rollouts.
7. Failure comparison before and after training.
```

Minimum report:

```text
Model:
Environment version:
Taskset version:
Reward version:
Training config:
Baseline score:
Post-training score:
Held-out score:
Regression benchmark score:
Biggest improvement:
Biggest regression:
Reward hacking observed:
Recommendation:
```

Pass condition should not be "reward went up." It should be:

```text
Held-out task success improves.
Invalid or unsafe actions do not increase.
Approval correctness improves or remains stable.
Level 2 benchmark does not regress materially.
Sampled rollouts show real behavioral improvement.
```

## Phase 8: Add Curriculum Content After The Code Exists

`STATUS.md` explicitly warns against spec work crowding out executable work. Keep Level 7 docs thin until the simulator and Prime adapter run.

Order of implementation:

```text
1. 100-task benchmark and deterministic graders.
2. Production eval report format.
3. Failure analysis bundle.
4. Trace-to-dataset path.
5. Acme Finance Operations Simulator.
6. Verifier/reward design.
7. Prime Intellect adapter.
8. RL reliability experiment.
9. Full Level 7 lessons/labs.
```

## Why This Improves Agent Reliability

The current agent can be checked for final-answer validity and basic tool use. The environment/verifier stack would let us train and evaluate more operational behaviors:

```text
Does the agent recover when a receipt is missing?
Does it ask for approval only when required?
Does it avoid submitting invalid drafts?
Does it use tools in the right order?
Does it preserve state across multiple steps?
Does it avoid inventing policy?
Does it complete workflows under realistic constraints?
```

This is where environment-based RL is useful: not teaching facts, but shaping repeated decision behavior under measurable feedback.

## Risks

Main risks:

```text
Reward hacking
Simulator overfitting
Vendor coupling
Premature complexity
Cloud cost
Misleading gains
Platform churn
```

Mitigations:

```text
Use reward-component metrics, held-out evals, and adversarial tasks.
Use seeded task generation and hidden test splits.
Keep Prime-specific files under integrations/prime-intellect/.
Start with eval-only Prime integration before training.
Use smoke configs and local evals first.
Compare against prompting, retrieval/tool fixes, and SFT baselines.
Teach architecture first and vendor mechanics second.
```

## Concrete Recommendation

Add the environment, verifier, and RL path in three layers:

```text
Layer 1: Local Acme benchmark, simulator, verifiers, rewards, and reports.
Layer 2: Production eval operations with Langfuse, Inspect AI, and GitHub Actions.
Layer 3: Hosted RL training through a Prime-compatible Verifiers adapter.
```

Do not restructure the whole repo around Prime. Make Prime the advanced backend for Level 7: the place learners go after they can already explain the environment, reward, benchmark, and failure modes locally.
