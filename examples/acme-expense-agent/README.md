# Acme Expense Agent

The canonical course system, implemented. Level 1 scope: a tool-using agent with typed tools, argument validation, a structured final-answer contract, and JSONL trace capture.

The agent helps employees work out what they can reimburse under Acme's expense policy. It is the same system every later level builds on — evaluated in Level 2, diagnosed in Level 3, mined for training data in Level 4.

## Quickstart

No API key required. The default model adapter is a deterministic offline planner.

```bash
cd examples/acme-expense-agent
python run_agent.py --task "I spent \$47 on parking and \$68 on dinner. What can I reimburse?"
```

Run the full Level 1 task set and check the resulting traces:

```bash
python run_agent.py --all --quiet
python -m acme_agent.check_traces traces/level-1.jsonl
```

Run against a real model:

```bash
python -m pip install -r requirements.txt
export ANTHROPIC_API_KEY=...
python run_agent.py --all --model claude-sonnet-5
```

Run the tests:

```bash
python -m pip install pytest
python -m pytest          # or: make check
```

## What you get

```text
acme_agent/
  agent.py          # the harness: loop, validation, tool execution, step budget
  models.py         # model adapters (offline ScriptedModel, AnthropicModel)
  tools.py          # search_policy, lookup_receipt, calculate_reimbursement, request_human_approval
  schemas.py        # tool schemas + the final-answer contract
  validation.py     # a ~90-line JSON-Schema-shaped validator, no dependencies
  trace.py          # trace dataclasses and the JSONL writer
  check_traces.py   # automated Level 1 check with actionable failure messages
  fixtures.py       # fixture loading

fixtures/
  policies.json     # 9 policy sections + the machine-readable rules they encode
  receipts.json     # 12 receipts across 3 employees
  employees.json    # 6 employees and their reporting lines
  tasks.json        # the 22 manual Level 1 tasks

solutions/          # reference solution for each of the four Level 1 labs
tests/              # 50 tests covering validation, tools, harness, and traces
traces/             # generated trace bundle + one hand-annotated example
docs/trace-schema.md
run_agent.py        # CLI
```

## Design decisions worth arguing with

**The core has no dependencies.** `validation.py` is a hand-written validator rather than `jsonschema`, because "validate the tool call" should be ninety readable lines the first time you meet it, not an import.

**The arithmetic lives in a tool, not in the model.** `calculate_reimbursement` owns every threshold and every sum, and returns a policy `source_id` with each decision. That is what makes a total auditable: it is reproducible from the tool arguments alone, without trusting the model.

**The default model is not a model.** `ScriptedModel` is a deterministic planner that produces the tool calls an LLM should produce. It exists so the harness, the tools, the traces, and the tests run offline, in CI, at zero cost. Level 2 compares it against a real model on the same benchmark — you cannot tell how much the model contributes until the harness is measurable without it.

**The agent can prepare but never submit.** `request_human_approval` denies `submit_report` unconditionally, citing `policy-submission-001`. An unattended agent must not be able to talk itself into a financial action.

**Bad tool arguments are observations, not crashes.** The harness validates, then hands the model the exact error and lets it try again. Recovery is a behaviour Level 2 measures, so the harness has to make recovery possible.

## Known limitations

These are real, and several are deliberate teaching material rather than bugs to hide:

- Free-text item extraction is shallow; descriptions read like `Stay` instead of `Hotel Teatro, one night`.
- The agent never reconciles the amounts a user states against the receipts on file, so a user who misremembers an amount gets a confidently wrong total.
- `total_reimbursable` includes items still pending approval, so it means "claimable if approved", not "payable now". Level 2 has to decide which one it grades.
- The 60-day submission window in `policy-submission-001` is retrieved but never enforced in `calculate_reimbursement`.
- Policy search is keyword-based, so it misses paraphrase, and its scores are normalised against the top hit — a bad best match still scores 1.0.

## Curriculum specs

- [Level 1: Build](../../levels/01-build/README.md) — the spec this implements
- [Level 2: Evaluate](../../levels/02-evaluate/README.md)
- [Level 3: Diagnose](../../levels/03-diagnose/README.md)
- [Level 4: Data and Feedback](../../levels/04-data/README.md)
- [Level 5: Post-training](../../levels/05-post-training/README.md)
- [Level 6: Environments](../../levels/06-environments/README.md)
- [Level 7: Reinforcement Learning](../../levels/07-reinforcement-learning/README.md)

| Level | Agent milestone | Status |
| --- | --- | --- |
| 1 | Basic tool-using expense assistant | shipped |
| 2 | Evaluated agent with benchmark reports | next |
| 3 | Diagnosed agent with failure taxonomy | spec only |
| 4 | Data-producing agent with curated traces | spec only |
| 5 | Agent backed by a fine-tuned or adapted model | spec only |
| 6 | Agent operating inside Acme Corp Simulator | spec only |
| 7 | Agent improved through experience and rewards | spec only |
