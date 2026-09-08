# Lab 2: Simulated Tools

## Objective

Specify tools by the state they change, and move policy rules out of the agent's
judgment into the tools.

## Build

**A simulated tool is not a mock.** A mock returns a canned value. A simulated
tool owns a piece of state and defines how it changes — which is what lets a
verifier ask "did a report get filed, by whom, and was that allowed?"

Specify each tool as a row:

```text
name | required arguments | state transition
```

The third column is the contract. Two rules:

- **Read tools still write an audit event.** A read that leaves no trace cannot
  be verified, and the check degrades into searching the agent's own output for
  an id — which a reward hacker walks straight through.
- **Write tools name the exact key**, derived from the task id, so verification
  is a lookup rather than a search and a repeat overwrites rather than
  duplicating.

**Put policy in the tool, not the prompt.** An agent that can decide when to ask
permission can decide not to. If a rule says only the employee may submit, the
tool must refuse a different actor — then "did it respect the gate?" becomes a
state query instead of a question about intent.

**Refusals return `ok: false`, they do not raise.** An exception ends the episode
and erases how the agent responds to being told no, which is behaviour worth
measuring.

## Deliverable

Submit:

- a tool schema list with a state transition per tool
- the simulator implementing them
- at least one tool that refuses an action on policy grounds

## Checks

```bash
python3 - <<'PY'
import json
tools = json.load(open("path/to/your/tool-schemas.json"))
for t in tools:
    ok = bool(t.get("state_transition"))
    print(f"  {'OK ' if ok else 'MISSING'} {t['name']}: {t.get('state_transition','-')}")
conditional = [t for t in tools if "only when" in t.get("state_transition", "").lower()]
print("OK: at least one tool enforces policy" if conditional
      else "FAIL: no tool refuses anything - policy is left to the agent")
PY
```

Then prove the refusal path returns rather than raises:

```bash
python3 -c "
import sys; sys.path.insert(0,'.')
# call your write tool with an unauthorised actor; it must return ok=False
"
```

The lab passes when every tool declares a state transition, at least one refuses
on policy grounds, and a refused call returns an observation the agent can react
to.

## Reference

Compare against
[`tool-schemas.json`](../../../environments/strongbench_finance/tool-schemas.json)
and the `Simulator` class in
[`environments/strongbench_finance/__init__.py`](../../../environments/strongbench_finance/__init__.py).

```bash
python3 -c "
import json
for t in json.load(open('environments/strongbench_finance/tool-schemas.json')):
    print(f\"  {t['name']:28} {t['state_transition']}\")
"
```

Two rows carry a condition — `submit_reimbursement` writes "only when actor is
employee", and `final_answer` requires that cited policy ids came back from
`search_policy`. Those two conditions are what make the unsafe-submission and
fabricated-citation checks possible.
