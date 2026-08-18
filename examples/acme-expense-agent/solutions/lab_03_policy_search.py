#!/usr/bin/env python3
"""Reference solution: Lab 3, Policy Search.

    python solutions/lab_03_policy_search.py

Grounding is the difference between an agent that answers and an agent you can
audit. Every claim the agent makes about policy has to trace back to a
source_id that exists in fixtures/policies.json.

The corpus is fixtures/policies.json (nine sections across meals, travel,
lodging, receipts, approval, and submission). The search tool is
`acme_agent.tools.search_policy`.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from acme_agent import fixtures
from acme_agent.agent import run_agent
from acme_agent.models import ScriptedModel
from acme_agent.trace import TraceWriter

TRACE_PATH = Path(__file__).resolve().parent.parent / "traces" / "lab-03.jsonl"

TASKS = [
    ("lab-03-001", "Can I reimburse dinner during business travel?"),
    ("lab-03-002", "What happens if I lost a hotel receipt?"),
    ("lab-03-003", "Which expenses need manager approval?"),
]


def main() -> int:
    from acme_agent.tools import search_policy

    known = {section["source_id"] for section in fixtures.policy_sections()}
    print(f"Corpus: {len(known)} sections across "
          f"{len({s['category'] for s in fixtures.policy_sections()})} categories\n")

    print("--- Retrieval ---")
    for _, task in TASKS:
        results = search_policy(task, top_k=3)["results"]
        top = ", ".join(f"{r['source_id']} ({r['score']})" for r in results)
        print(f"  {task}\n    -> {top}")

    print("\n--- Grounded answers ---")
    writer = TraceWriter(TRACE_PATH)
    for task_id, task in TASKS:
        result = run_agent(task, ScriptedModel(), task_id=task_id, writer=writer)
        cited = sorted(
            {
                source_id
                for group in ("reimbursable_items", "non_reimbursable_items")
                for line in result.final_answer[group]
                for source_id in line["policy_source_ids"]
            }
            | {
                source_id
                for entry in result.final_answer["approvals_required"]
                for source_id in entry.get("policy_source_ids", [])
            }
            | set(result.final_answer.get("cited_policy_source_ids", []))
        )
        invented = [source_id for source_id in cited if source_id not in known]
        assert cited, "a grounded answer must cite at least one policy section"
        print(f"  {task_id}: cited={cited} invented={invented}")
        assert not invented, "the agent cited a policy id that does not exist"

    print(f"\nThree traces written to {TRACE_PATH}")
    print(
        "\nKnown limitations of this search — write your own version of this list:\n"
        "  1. Keyword matching, so it misses paraphrase. 'Can I expense booze?' does not\n"
        "     retrieve policy-meals-002, because 'booze' is in no keyword list.\n"
        "  2. Whole sections are returned, so a long section dilutes the relevant\n"
        "     sentence and eats context.\n"
        "  3. Scores are normalised against the top hit, so a bad best match still\n"
        "     scores 1.0. The score says 'most relevant of these', never 'relevant'.\n"
        "  4. No recency or version awareness: two policy versions would both match.\n"
        "  5. There is no 'nothing found' path. An empty result set is what should\n"
        "     force the agent to say it does not know, and Level 2 measures how often\n"
        "     it says that instead of guessing."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
