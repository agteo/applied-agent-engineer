# Canonical System Strategy

## Purpose

The course should use one recurring system so learners experience the full improvement loop:

```text
build -> evaluate -> diagnose -> collect data -> improve -> simulate -> verify -> train
```

The current executable seed is the Acme Expense Agent. It is useful because it is bounded, offline, policy-driven, tool-heavy, and easy to grade. It should not be treated as the guaranteed final domain.

The final canonical system should be chosen by the kinds of agents companies are actually deploying and need capability in evaluating.

## Current Hypothesis

The strongest candidate direction is a broader finance operations agent, not a narrow expense reimbursement assistant.

Finance operations is attractive because it is:

- common across companies
- high-volume and workflow-oriented
- policy-governed
- data-rich without requiring real customer data in the course
- naturally suited to deterministic and state-based verification
- relevant to observability, evals, approvals, auditability, and human review
- close to current enterprise agent deployment patterns

Possible scope:

```text
expense reimbursement
accounts payable
purchase order matching
invoice review
approval routing
order-to-cash follow-up
reconciliation
audit support
policy Q&A
exception handling
```

## Selection Criteria

The canonical system should score well on these criteria:

| Criterion | Why It Matters |
| --- | --- |
| Deployed in industry | Learners should practice on work companies actually need. |
| Tool and workflow heavy | The course is about agents as systems, not chat-only assistants. |
| Verifiable outcomes | Deterministic, state, and constraint verifiers should be possible. |
| Safe synthetic data | The repo must remain usable without private data. |
| Progressive complexity | The same domain must support Levels 1-7. |
| Production eval relevance | Traces, failures, regression packs, release gates, and monitoring should be natural. |
| Data flywheel | Failures should convert into datasets, synthetic examples, preference data, and trajectories. |
| Environment/RL fit | The domain should support simulated state transitions, rollouts, rewards, and reward-hacking examples. |
| Open-source implementation | Learners should be able to run the core locally and cheaply. |

## Candidate Domains

### Finance Operations Agent

Best current candidate.

Strengths:

- maps to deployed back-office automation
- supports approvals, exceptions, reconciliation, compliance, and audit trails
- has clear state changes and verifiable task outcomes
- can start with expenses and expand gradually

Risks:

- can become too domain-specific if accounting complexity dominates the agent engineering lessons
- requires careful synthetic fixture design to stay realistic

### Customer Support Operations Agent

Strong alternative.

Strengths:

- widely deployed
- easy to understand
- strong fit for tracing, evals, rubric grading, and human review

Risks:

- many outcomes are subjective
- harder to build deterministic state verifiers unless the support workflow includes account actions, refunds, ticket routing, or CRM updates

### Software Engineering Agent

Strong advanced or parallel domain.

Strengths:

- highly relevant to current agent usage
- strong deterministic verification through tests
- natural fit for sandboxes and CI

Risks:

- may distract from business workflow agents
- learners can mistake coding-agent evals for the whole field

### Sales / CRM Agent

Useful for state-verifier lessons.

Strengths:

- clear state changes in CRM records
- realistic enterprise workflow
- good for constraint verification

Risks:

- synthetic data can feel artificial
- subjective sales quality may require noisier model-based judging

## Recommended Direction

Keep the current Acme Expense Agent as Level 1's executable seed.

Expand the canonical system toward:

```text
Acme Finance Operations Agent
```

This lets the repo preserve existing work while broadening the domain enough to support production eval operations, verifier engineering, and RL environments.

Proposed evolution:

```text
Level 1:
  Expense-policy assistant with receipt lookup and approval escalation.

Level 2:
  100-task benchmark across expense tasks, invoice checks, approvals, and policy questions.

Level 3:
  Production-style trace review, failure datasets, regression packs, and release gates.

Level 4:
  Trace-to-dataset conversion for corrections, synthetic examples, preference pairs, and trajectories.

Level 5:
  Model improvement decisions and optional post-training on curated finance workflow data.

Level 6:
  Acme Finance Simulator with expenses, invoices, approvals, vendors, employees, audit logs, and state verifiers.

Level 7:
  RL reliability experiment using verifier-derived rewards and held-out regression evaluation.
```

## Evidence To Recheck Periodically

This decision should be revisited as the market changes. Review signals from:

- enterprise AI deployment reports
- AI agent job descriptions
- evaluation and post-training job descriptions
- finance, customer support, software engineering, and operations agent case studies
- platform examples from observability, eval, environment, and RL vendors

The course should prefer domains where companies are deploying agents and where agent reliability can be measured with more than subjective judgment.

