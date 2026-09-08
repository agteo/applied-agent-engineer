# Lesson 7: Local Inference Operations

## Core Idea

Choosing to serve a model yourself is an operations decision, not a modelling
one. The model is the easy part; what you are taking on is availability,
capacity, failover, and the quality difference between whatever you can run and
whatever you were calling before.

The reasons to do it are real — cost at volume, data residency, latency,
independence from a vendor's roadmap and pricing. So are the costs, and they
arrive as a pager rather than an invoice.

The mistake this lesson is built to prevent: treating a local model as a drop-in
substitution. A hosted API is a *managed service* — capacity planning, failover
and upgrades are someone's full-time job. Running the weights is the smallest
part of replacing it.

## Design The Gateway, Not The Model

[`gateway-plan.json`](../../../model_improvement/strongbench/gateway-plan.json)
plans the serving layer rather than the model:

```json
{"aliases": {"agent":    "strongbench-agent-model",
             "primary":  "strongbench-local-primary",
             "fallback": "strongbench-hosted-fallback"},
 "drills": ["normal local serving",
            "local worker unavailable before benchmark slice",
            "local worker interrupted during benchmark slice"],
 "measurements": ["task_success", "latency_ms", "error_rate",
                  "fallback_rate", "quality_delta"]}
```

The **alias indirection** is the load-bearing idea. The agent is configured with
`strongbench-agent-model` and never names a backend. Routing decisions —
primary, fallback, canary, rollback — happen in the gateway, and the agent needs
no deploy to change them.

Without it, "fall back to hosted" is a code change under incident conditions.
With it, it is a routing change. **The seam is the whole design**, and it costs
one indirection to have.

## Rehearse The Failures You Expect

Three drills, and the second and third are not the same:

| Drill | What it exercises |
| --- | --- |
| normal local serving | the happy path and its baseline numbers |
| worker unavailable **before** a slice | failover on connect — clean, easy |
| worker interrupted **during** a slice | failover mid-run — the hard one |

Failing before a run is a connection error at a natural boundary; you route to
fallback and start. Failing *during* one leaves an agent mid-episode with a
partial trace and some tools already executed. Does the run resume on the
fallback with a different model's behaviour halfway through? Restart, and
duplicate any side effects? Fail cleanly and record why?

There is no universally right answer, and the wrong move is to find out during
an incident. For this agent the tools are read-only except approval requests, so
restarting is cheap — a property worth knowing *before* you need it.

**Write your drills as the failures you actually expect**, and rehearse the
messy one rather than only the clean one.

## Five Measurements, And The Two People Forget

```text
task_success   latency_ms   error_rate   fallback_rate   quality_delta
```

The first three are standard. The last two are what make this plan a
capability-and-operations plan rather than a monitoring dashboard.

**`fallback_rate`** — the proportion of traffic served by the fallback. If it
sits at 30%, you are not running locally; you are running a hosted service with
an expensive cache in front of it, and the cost model you justified this with is
wrong. Nothing else surfaces that: success and latency can both look fine while
the fallback quietly does most of the work.

**`quality_delta`** — the difference in task success between primary and
fallback on the same tasks. Serving two models means serving two behaviours, and
your users experience a mixture whose composition changes with your uptime. If
the delta is large, availability incidents are also quality incidents, and your
benchmark number is a weighted average of two different systems.

Measure both from day one. They are the two numbers that tell you whether the
architecture is doing what you claimed.

## Local Serving Does Not Change The Adoption Gate

Track 5C is a serving change, not a capability change, and the same gate applies:

```text
Adopt a trained or local model only if heldout benchmark success improves
without increasing unsafe submission failures.
```

A locally served model must clear the Level 2 benchmark and the
`unsafe_submission` slice like any other candidate. The temptation is to treat
serving as infrastructure and skip evaluation — but a smaller local model with
a different tokenizer and a different instruction-following profile is a
different agent, and "it is the same model, just self-hosted" is rarely true
once quantisation and a different serving stack are involved.

Run the benchmark against the local endpoint. It is one command, and it is the
difference between a deployment and a hope.

## What This Repo Does And Does Not Give You

The gateway plan is a **drill plan**, not a running gateway — `purpose` says
"Track 5C local inference gateway drill plan", and there is no serving code in
the repo.

That is the honest scope. The course teaches the decisions: what to alias, what
to rehearse, what to measure. It does not ship an inference server, and the
comparison table in the model-improvement report lists frontier and hybrid APIs
as "not measured in offline course path" for the same reason.

Treat the plan as the checklist you take into a real deployment, and expect the
serving stack itself to be the part you build.

## Common Failure Modes

- **Naming backends in the agent.** Failover becomes a deploy under incident
  conditions.
- **Only rehearsing clean failures.** Mid-run failover is the one that surprises
  you.
- **Not measuring `fallback_rate`.** You cannot tell local serving from an
  expensive proxy.
- **Not measuring `quality_delta`.** Availability incidents become silent
  quality incidents.
- **Skipping the benchmark because it is "the same model".** Quantisation and
  serving stacks change behaviour.
- **Treating serving as exempt from the adoption gate.** A different agent
  needs the same evidence.
- **Costing the GPU and not the operations.** Availability is the expensive
  part.

## Exercise

Open [`gateway-plan.json`](../../../model_improvement/strongbench/gateway-plan.json)
and [`decision.json`](../../../model_improvement/strongbench/decision.json).

1. The plan defines three aliases when one backend would run. Describe the
   incident where the indirection saves you, and what the alternative looks like
   at 2am.
2. Two drills cover a worker failing before and during a benchmark slice.
   Explain why they are different problems, and say which property of this
   agent's tools makes the harder one cheaper to handle here.
3. `fallback_rate` and `quality_delta` are measured alongside success and
   latency. Give the specific wrong conclusion each one prevents.

Check your answer:

```text
1. The local worker degrades — slow, or failing a fraction of requests. With
   aliases you repoint strongbench-agent-model at the hosted fallback in the
   gateway: a routing change, reversible, no deploy. Without them the backend is
   named in agent configuration, so recovery means editing config, redeploying
   and hoping the change is correct, at 2am, under pressure, with no easy
   rollback. Same incident, minutes versus hours.

2. Failing before a slice is a connection error at a clean boundary: no work is
   in flight, so you route to fallback and start. Failing during one leaves a
   partial trace with some tool calls already executed, so you must decide
   between resuming on a different model mid-episode, restarting and possibly
   duplicating side effects, or failing cleanly. Here restarting is cheap
   because all tools are read-only except request_human_approval — there is
   almost nothing to duplicate. An agent with write-heavy tools would not have
   that luxury.

3. fallback_rate prevents concluding that local serving is working when most
   traffic is actually being served by the hosted fallback — success and latency
   would both look healthy while the cost model you justified the project with
   is wrong. quality_delta prevents reading a single aggregate benchmark number
   as the agent's quality when users are actually experiencing a mixture of two
   models whose composition changes with your uptime.
```

Then write the fourth drill this plan is missing, for a failure mode you have
seen in production. Say what it exercises and which of the five measurements
would move.

## Checkpoint

You are ready to complete Level 5 when your agent addresses a model alias rather
than a backend, you have rehearsed a mid-run failover, you measure fallback rate
and quality delta, and your locally served model has cleared the same adoption
gate as any other candidate.

## Reading

- [`model_improvement/strongbench/comparison-report.md`](../../../model_improvement/strongbench/comparison-report.md)
  — where hosted, local and hybrid options sit side by side with their evidence
  status. Serving is a candidate in that table, not an exemption from it.
- [`model_improvement/strongbench/decision.json`](../../../model_improvement/strongbench/decision.json)
  — the adoption gate that applies to a locally served model exactly as it
  applies to a trained one.
