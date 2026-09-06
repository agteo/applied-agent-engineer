"""Build Acme Agent Training Dataset v1.

    python3 -m datasets.acme
"""

from __future__ import annotations

from collections import Counter
import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUT = ROOT / "datasets" / "acme"
LEVEL1_TRACES = ROOT / "examples" / "acme-expense-agent" / "traces" / "level-1.jsonl"
FAILURE_ANNOTATIONS = ROOT / "evals" / "operations" / "acme" / "annotated-failures.jsonl"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build Acme Agent Training Dataset v1.")
    parser.add_argument("--out", default=str(DEFAULT_OUT))
    args = parser.parse_args(argv)

    bundle = build_dataset()
    write_dataset(bundle, Path(args.out))
    print(bundle["card"].rstrip())
    return 0


def build_dataset() -> dict[str, Any]:
    raw = []
    raw.extend(examples_from_level1_traces(load_jsonl(LEVEL1_TRACES)))
    raw.extend(examples_from_failure_annotations(load_jsonl(FAILURE_ANNOTATIONS)))
    raw.extend(synthetic_examples())
    raw.extend(dirty_examples(raw))
    cleaned, rejected = clean_examples(raw)
    split_rows = apply_splits(cleaned)
    metrics = build_metrics(raw, cleaned, rejected, split_rows)
    card = render_dataset_card(metrics)
    return {
        "raw": raw,
        "cleaned": split_rows,
        "rejected": rejected,
        "metrics": metrics,
        "card": card,
    }


def examples_from_level1_traces(traces: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for trace in traces:
        answer = trace.get("final_answer")
        if not answer:
            continue
        rows.append(
            make_example(
                example_id=f"trace-{trace['task_id']}",
                source_type="level1_trace",
                task_id=trace["task_id"],
                prompt=trace["task"],
                target=answer,
                labels=["demonstration"],
                provenance={
                    "path": str(LEVEL1_TRACES.relative_to(ROOT)),
                    "trace_schema_version": trace.get("trace_schema_version"),
                    "model": trace.get("model"),
                },
            )
        )
    return rows


def examples_from_failure_annotations(annotations: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for annotation in annotations:
        corrected = corrected_answer(annotation)
        rows.append(
            make_example(
                example_id=f"correction-{annotation['annotation_id'].replace(':', '-')}",
                source_type="failure_correction",
                task_id=annotation["task_id"],
                prompt=annotation["prompt"],
                target=corrected,
                rejected_target=annotation["trace"].get("final_answer"),
                labels=["correction"] + annotation["taxonomy_labels"],
                provenance={
                    "path": str(FAILURE_ANNOTATIONS.relative_to(ROOT)),
                    "annotation_id": annotation["annotation_id"],
                    "config": annotation["config"],
                },
            )
        )
    return rows


def synthetic_examples() -> list[dict[str, Any]]:
    rows = []
    for index in range(1, 101):
        family = SYNTHETIC_FAMILIES[(index - 1) % len(SYNTHETIC_FAMILIES)]
        amount = family["amounts"][(index - 1) % len(family["amounts"])]
        prompt = family["prompt"].format(amount=amount, index=index)
        rows.append(
            make_example(
                example_id=f"synthetic-{index:03d}",
                source_type="synthetic_gap_target",
                task_id=f"synthetic-{index:03d}",
                prompt=prompt,
                target=family["target"](amount),
                labels=["synthetic", family["label"]],
                provenance={
                    "generator": "datasets.acme.synthetic_examples",
                    "target_failure_mode": family["label"],
                },
            )
        )
    return rows


def dirty_examples(existing_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    duplicate = dict(existing_rows[0])
    duplicate["example_id"] = "cleaning-fixture-duplicate"

    missing_provenance = make_example(
        example_id="cleaning-fixture-missing-provenance",
        source_type="cleaning_fixture",
        task_id="cleaning-fixture-missing-provenance",
        prompt="Cleaning fixture: reimburse a valid lunch with missing provenance.",
        target=_answer(18.0, "policy-meals-001", "A normal same-day lunch is reimbursable when provenance is present."),
        labels=["cleaning_fixture"],
        provenance={},
    )

    invalid_target = make_example(
        example_id="cleaning-fixture-invalid-target",
        source_type="cleaning_fixture",
        task_id="cleaning-fixture-invalid-target",
        prompt="Cleaning fixture: this row has an intentionally incomplete target.",
        target={"summary": "Incomplete target used to test dataset cleaning."},
        labels=["cleaning_fixture"],
        provenance={"generator": "datasets.acme.dirty_examples"},
    )

    return [duplicate, missing_provenance, invalid_target]


def clean_examples(raw: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    seen: set[str] = set()
    cleaned = []
    rejected = []
    for row in raw:
        reason = rejection_reason(row)
        fingerprint = stable_fingerprint(row)
        if not reason and fingerprint in seen:
            reason = "duplicate_prompt_target"
        if reason:
            rejected.append({"example_id": row["example_id"], "reason": reason, "source_type": row["source_type"]})
            continue
        seen.add(fingerprint)
        cleaned.append(row)
    return cleaned, rejected


def apply_splits(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    split_rows = []
    for index, row in enumerate(rows):
        row = dict(row)
        row["split"] = choose_split(row, index)
        split_rows.append(row)
    return split_rows


def corrected_answer(annotation: dict[str, Any]) -> dict[str, Any]:
    total = round(float(annotation["expected_total"]), 2)
    policy_ids = sorted(
        {
            source_id
            for failure in annotation["failures"]
            for source_id in extract_policy_ids(failure)
        }
    )
    labels = set(annotation["taxonomy_labels"])
    approvals = []
    missing = []
    if "MODEL.instruction_following" in labels:
        approvals.append(
            {
                "approval_type": "manager",
                "reason": "The task requires approval handling before reimbursement can be treated as payable.",
                "policy_source_ids": policy_ids or ["policy-approval-001"],
            }
        )
    if "TOOLS.interpretation" in labels:
        missing.append("Resolve the missing approval or receipt requirement before payment.")
    return {
        "summary": f"Corrected target: USD {total:.2f} is the expected reimbursable amount for this task.",
        "reimbursable_items": (
            [
                {
                    "description": "Expected reimbursable amount",
                    "amount": total,
                    "policy_source_ids": policy_ids or ["policy-meals-001"],
                    "reason": "Matches the benchmark oracle.",
                }
            ]
            if total
            else []
        ),
        "non_reimbursable_items": [],
        "missing_information": missing,
        "approvals_required": approvals,
        "total_reimbursable": total,
        "confidence": "medium",
        "next_action": "Use this correction as supervised data, then rerun the benchmark.",
        "cited_policy_source_ids": policy_ids,
    }


def extract_policy_ids(text: str) -> list[str]:
    return [part.strip("[]'.,") for part in text.split() if part.startswith("policy-")]


def make_example(
    *,
    example_id: str,
    source_type: str,
    task_id: str,
    prompt: str,
    target: dict[str, Any],
    labels: list[str],
    provenance: dict[str, Any],
    rejected_target: dict[str, Any] | None = None,
) -> dict[str, Any]:
    row = {
        "schema_version": "1.0.0",
        "example_id": example_id,
        "source_type": source_type,
        "task_id": task_id,
        "prompt": prompt,
        "messages": [{"role": "user", "content": prompt}],
        "target_final_answer": target,
        "labels": sorted(set(labels)),
        "provenance": provenance,
        "quality": {
            "contract_valid": has_required_answer_fields(target),
            "has_provenance": bool(provenance),
            "safe_for_training": True,
        },
    }
    if rejected_target is not None:
        row["rejected_final_answer"] = rejected_target
    return row


def rejection_reason(row: dict[str, Any]) -> str | None:
    if not row.get("prompt"):
        return "missing_prompt"
    if not row.get("provenance"):
        return "missing_provenance"
    if not has_required_answer_fields(row.get("target_final_answer", {})):
        return "invalid_target_contract"
    if row["source_type"] == "failure_correction" and not row.get("rejected_final_answer"):
        return "missing_rejected_answer"
    return None


def has_required_answer_fields(answer: dict[str, Any]) -> bool:
    required = {
        "summary",
        "reimbursable_items",
        "non_reimbursable_items",
        "missing_information",
        "approvals_required",
        "total_reimbursable",
        "confidence",
        "next_action",
    }
    return required <= set(answer)


def stable_fingerprint(row: dict[str, Any]) -> str:
    payload = json.dumps(
        {
            "prompt": row.get("prompt"),
            "target": row.get("target_final_answer"),
            "source_type": row.get("source_type"),
        },
        sort_keys=True,
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]


def choose_split(row: dict[str, Any], index: int) -> str:
    if row["source_type"] == "failure_correction":
        return "dev" if index % 2 else "heldout"
    if row["source_type"] == "level1_trace":
        return "dev" if index % 5 == 0 else "train"
    bucket = int(hashlib.sha256(row["example_id"].encode("utf-8")).hexdigest(), 16) % 10
    if bucket < 7:
        return "train"
    if bucket < 9:
        return "dev"
    return "heldout"


def build_metrics(
    raw: list[dict[str, Any]],
    cleaned: list[dict[str, Any]],
    rejected: list[dict[str, Any]],
    split_rows: list[dict[str, Any]],
) -> dict[str, Any]:
    return {
        "raw_count": len(raw),
        "cleaned_count": len(cleaned),
        "rejected_count": len(rejected),
        "by_source_type": dict(sorted(Counter(row["source_type"] for row in split_rows).items())),
        "by_split": dict(sorted(Counter(row["split"] for row in split_rows).items())),
        "by_label": dict(sorted(Counter(label for row in split_rows for label in row["labels"]).items())),
        "rejection_reasons": dict(sorted(Counter(row["reason"] for row in rejected).items())),
        "heldout_protection": "Benchmark-derived failure corrections are assigned only to dev or heldout splits.",
    }


def render_dataset_card(metrics: dict[str, Any]) -> str:
    return (
        "# Acme Agent Training Dataset v1\n\n"
        "## Intended Use\n\n"
        "Use this dataset to prototype supervised correction, preference, and regression-data workflows for the Acme Expense Agent. It is a teaching dataset, not production financial data.\n\n"
        "## Sources\n\n"
        "- Level 1 trace demonstrations from `examples/acme-expense-agent/traces/level-1.jsonl`.\n"
        "- Level 3 annotated benchmark failures from `evals/operations/acme/annotated-failures.jsonl`.\n"
        "- Synthetic gap-targeted examples generated by `python3 -m datasets.acme`.\n\n"
        "## Schema\n\n"
        "Rows follow `datasets/acme/schema.json` and include `example_id`, `source_type`, `messages`, `target_final_answer`, labels, provenance, quality flags, and split.\n\n"
        "## Cleaning\n\n"
        "Rows without prompts, provenance, or contract-shaped targets are rejected. Duplicate prompt/target/source triples are removed.\n\n"
        "## Metrics\n\n"
        f"- raw rows: {metrics['raw_count']}\n"
        f"- cleaned rows: {metrics['cleaned_count']}\n"
        f"- rejected rows: {metrics['rejected_count']}\n"
        f"- splits: {json.dumps(metrics['by_split'], sort_keys=True)}\n"
        f"- sources: {json.dumps(metrics['by_source_type'], sort_keys=True)}\n\n"
        "## Limitations\n\n"
        "Synthetic examples are template-generated and should not be used to claim real model improvement without held-out benchmark evaluation. Correction targets are compact oracle summaries, not full human-authored ideal answers.\n\n"
        "## Privacy\n\n"
        "All examples use fictional Acme fixtures. No personal, customer, or production data is included.\n\n"
        "## Level 5 Use Case\n\n"
        "Use the train split for small SFT experiments, the dev split for prompt or adapter iteration, and the heldout split plus the Level 2 benchmark for regression checks.\n"
    )


def write_dataset(bundle: dict[str, Any], out: Path) -> None:
    out.mkdir(parents=True, exist_ok=True)
    write_jsonl(out / "raw.jsonl", bundle["raw"])
    write_jsonl(out / "cleaned.jsonl", bundle["cleaned"])
    write_jsonl(out / "rejected.jsonl", bundle["rejected"])
    for split in ("train", "dev", "heldout"):
        write_jsonl(out / f"{split}.jsonl", [row for row in bundle["cleaned"] if row["split"] == split])
    (out / "metrics.json").write_text(json.dumps(bundle["metrics"], indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (out / "dataset-card.md").write_text(bundle["card"], encoding="utf-8")
    (out / "schema.json").write_text(json.dumps(DATASET_SCHEMA, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (out / "synthetic-generation.md").write_text(SYNTHETIC_GENERATION_NOTE, encoding="utf-8")


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows = []
    with open(path, encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    with open(path, "w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, sort_keys=True) + "\n")


def _answer(total: float, policy_id: str, summary: str) -> dict[str, Any]:
    return {
        "summary": summary,
        "reimbursable_items": (
            [{"description": "Expense", "amount": round(total, 2), "policy_source_ids": [policy_id], "reason": "Within policy."}]
            if total
            else []
        ),
        "non_reimbursable_items": [],
        "missing_information": [],
        "approvals_required": [],
        "total_reimbursable": round(total, 2),
        "confidence": "medium",
        "next_action": "Use the cited policy source and rerun the benchmark after any change.",
        "cited_policy_source_ids": [policy_id],
    }


SYNTHETIC_FAMILIES = [
    {
        "label": "receipt_threshold",
        "prompt": "Synthetic {index}: I lost a receipt for a ${amount} lunch. What should happen?",
        "amounts": [24.0, 24.99, 25.0, 26.0, 40.0],
        "target": lambda amount: {
            **_answer(amount, "policy-receipts-001", f"USD {amount:.2f} can be considered, but receipts at or above USD 25 need documentation."),
            "missing_information": ["Missing receipt declaration required."] if amount >= 25 else [],
            "approvals_required": (
                [{"approval_type": "manager", "reason": "Missing receipt at or above threshold.", "policy_source_ids": ["policy-receipts-001"]}]
                if amount >= 25
                else []
            ),
        },
    },
    {
        "label": "meal_limit",
        "prompt": "Synthetic {index}: I spent ${amount} on same-day travel meals. What is reimbursable?",
        "amounts": [60.0, 75.0, 76.0, 90.0, 120.0],
        "target": lambda amount: _answer(min(amount, 75.0), "policy-meals-001", "Meals are capped at USD 75 per employee per day."),
    },
    {
        "label": "lodging_limit",
        "prompt": "Synthetic {index}: My hotel was ${amount} for one night. What comes back?",
        "amounts": [200.0, 250.0, 251.0, 289.0, 400.0],
        "target": lambda amount: {
            **_answer(min(amount, 250.0), "policy-lodging-001", "Hotel lodging is reimbursable up to USD 250 per night."),
            "approvals_required": (
                [{"approval_type": "manager", "reason": "Lodging exceeds the nightly limit.", "policy_source_ids": ["policy-lodging-001"]}]
                if amount > 250
                else []
            ),
        },
    },
    {
        "label": "submission_gate",
        "prompt": "Synthetic {index}: Please submit my ${amount} reimbursement report for me.",
        "amounts": [47.0, 115.0, 214.0, 329.0, 500.0],
        "target": lambda amount: {
            **_answer(amount, "policy-submission-001", "The agent may prepare a draft but must not submit on the employee's behalf."),
            "approvals_required": [{"approval_type": "employee", "reason": "Only the employee may submit.", "policy_source_ids": ["policy-submission-001"]}],
            "next_action": "Prepare a draft if requested; the employee must submit it.",
        },
    },
]

SYNTHETIC_GENERATION_NOTE = """# Synthetic Generation

Synthetic examples are generated by `datasets.acme.synthetic_examples`.

The generator targets four Level 3 failure modes:

- receipt threshold handling
- daily meal limits
- lodging limits
- employee-only submission gates

Accepted rows must have provenance, a contract-shaped target final answer, and
a non-empty prompt. Rejected rows are written to `rejected.jsonl`.
"""

DATASET_SCHEMA: dict[str, Any] = {
    "type": "object",
    "required": [
        "schema_version",
        "example_id",
        "source_type",
        "task_id",
        "prompt",
        "messages",
        "target_final_answer",
        "labels",
        "provenance",
        "quality",
        "split",
    ],
    "properties": {
        "schema_version": {"type": "string"},
        "example_id": {"type": "string"},
        "source_type": {"type": "string"},
        "task_id": {"type": "string"},
        "prompt": {"type": "string"},
        "messages": {"type": "array"},
        "target_final_answer": {"type": "object"},
        "rejected_final_answer": {"type": "object"},
        "labels": {"type": "array", "items": {"type": "string"}},
        "provenance": {"type": "object"},
        "quality": {"type": "object"},
        "split": {"type": "string", "enum": ["train", "dev", "heldout"]},
    },
}


if __name__ == "__main__":
    raise SystemExit(main())
