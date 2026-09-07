"""Check Workstream C portfolio-surface artifacts."""

from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_TEMPLATE_SECTIONS = [
    "## One-Sentence Claim",
    "## Problem",
    "## Measurement",
    "## Diagnosis",
    "## Intervention Or Decision",
    "## Evidence",
    "## Differentiating Choice",
    "## What I Would Do Next",
    "## Links",
]

REQUIRED_EXAMPLES = [
    ROOT / "examples" / "portfolio" / "agent-quality-engineering.md",
    ROOT / "examples" / "portfolio" / "model-improvement.md",
    ROOT / "examples" / "portfolio" / "environment-verifier-engineering.md",
    ROOT / "examples" / "portfolio" / "rl-literacy.md",
]


def main() -> int:
    failures = []
    template = ROOT / "templates" / "portfolio-writeup.md"
    failures.extend(check_sections(template, REQUIRED_TEMPLATE_SECTIONS))
    for example in REQUIRED_EXAMPLES:
        failures.extend(check_sections(example, REQUIRED_TEMPLATE_SECTIONS[1:]))

    capstone = (ROOT / "capstones" / "core-practical" / "README.md").read_text(encoding="utf-8")
    if "## Differentiation Requirement" not in capstone:
        failures.append("capstones/core-practical/README.md: missing differentiation requirement")
    if "templates/portfolio-writeup.md" not in capstone:
        failures.append("capstones/core-practical/README.md: missing portfolio template link")

    print("# Portfolio Surface Audit")
    print()
    print(f"- examples: {len(REQUIRED_EXAMPLES)}")
    print(f"- failures: {len(failures)}")
    for failure in failures:
        print(f"FAIL {failure}")
    return 1 if failures else 0


def check_sections(path: Path, sections: list[str]) -> list[str]:
    if not path.exists():
        return [f"{display_path(path)}: missing file"]
    text = path.read_text(encoding="utf-8")
    return [f"{display_path(path)}: missing {section}" for section in sections if section not in text]


def display_path(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


if __name__ == "__main__":
    raise SystemExit(main())
