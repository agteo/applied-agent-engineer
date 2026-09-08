# Lab 5: Gateway Failover Drill

## Objective

Design the serving layer for a locally hosted model, and rehearse the failure
you have not thought about.

**No GPU required.** This lab is about the gateway and the drills, not about
running weights. The measurements can be exercised against any two backends,
including two configurations of the scripted adapter.

## Build

**Design the gateway, not the model.** The agent should address an alias —
`your-agent-model` — and never name a backend. Routing, failover, canary and
rollback then happen in the gateway, and "fall back to hosted" is a routing
change rather than a code change made under incident conditions.

Define three aliases: what the agent asks for, the primary, and the fallback.

Then write your drills. At minimum:

| Drill | Exercises |
| --- | --- |
| normal serving | the happy path, and its baseline numbers |
| primary unavailable **before** a run | failover at a clean boundary |
| primary interrupted **during** a run | failover mid-episode — the hard one |

The third is the one that matters. An agent interrupted mid-episode has a
partial trace and some tools already executed. Resume on a different model
halfway through? Restart and risk duplicating side effects? Fail cleanly and
record why? **There is no universally right answer, and the wrong move is to
decide during an incident.**

Check your own tools first: if they are read-only except for one approval
request, restarting is cheap. A write-heavy toolset does not have that luxury.

## Measurements

Five, and the last two are the ones people omit:

```text
task_success   latency_ms   error_rate   fallback_rate   quality_delta
```

- **`fallback_rate`** — if it sits at 30%, you are running a hosted service with
  an expensive cache in front of it, and the cost model you justified this with
  is wrong. Success and latency can both look healthy while this is true.
- **`quality_delta`** — the success difference between primary and fallback on
  the same tasks. Serving two models means users experience a mixture whose
  composition changes with your uptime.

## Deliverable

Submit:

- a gateway plan: aliases, drills, measurements
- drill results for all three scenarios, including what the agent did mid-run
- a stated policy for mid-episode failover
- the benchmark run against your primary backend

## Checks

The drills are judged by rehearsal, not by a command. Score each **high /
medium / low**:

| Criterion | High |
| --- | --- |
| Indirection | the agent names an alias; no backend appears in agent config |
| Mid-run drill | actually executed, with the resulting trace inspected |
| Failover policy | stated, and justified by your tools' write behaviour |
| `fallback_rate` | measured, with a threshold at which you would reconsider |
| `quality_delta` | measured on the same tasks across both backends |
| Adoption gate | primary backend cleared the Level 2 benchmark and the safety slice |

One thing is a command, and it is not optional:

```bash
# A locally served model is a different agent. Benchmark it.
python3 -m evals.runner --model <your-primary> --report /tmp/local.md
diff <(grep '^- ' /tmp/local.md) <(grep '^- ' evals/reports/sample-report.md)
```

The lab passes at high on Indirection, Mid-run drill and Adoption gate. Serving
is a candidate in the comparison table, not an exemption from it — quantisation
and a different serving stack change behaviour, so "it is the same model, just
self-hosted" is rarely true.

## Reference

Compare against
[`gateway-plan.json`](../../../model_improvement/strongbench/gateway-plan.json).

```bash
python3 -c "
import json; print(json.dumps(json.load(open('model_improvement/strongbench/gateway-plan.json')), indent=1))
"
```

Note it is a **drill plan**, not a running gateway — there is no serving code in
this repo. It gives you the decisions to take into a real deployment: what to
alias, what to rehearse, what to measure. Expect the serving stack itself to be
the part you build.
