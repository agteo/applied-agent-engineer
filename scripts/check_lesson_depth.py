"""Check Workstream A lesson-depth markers.

A numbered lesson is either complete against the mechanical depth gate or it is
honestly marked `Status: outline`.

The mechanical gate intentionally checks only two things:

- a named failure-mode section
- an exercise section

The other Workstream A criteria need human review.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
LESSON_GLOB = "levels/*/lessons/[0-9][0-9]-*.md"
OUTLINE_STATUS = "Status: outline"

FAILURE_HEADINGS = {
    "## Common Failure Modes",
    "## Failure Modes",
    "## Common Mistakes",
}


@dataclass(frozen=True)
class LessonAudit:
    path: Path
    has_outline_status: bool
    has_failure_mode: bool
    has_exercise: bool

    @property
    def complete(self) -> bool:
        return self.has_failure_mode and self.has_exercise

    @property
    def needs_outline_status(self) -> bool:
        return not self.complete

    @property
    def valid(self) -> bool:
        return self.complete or self.has_outline_status

    @property
    def missing(self) -> list[str]:
        missing = []
        if not self.has_failure_mode:
            missing.append("failure-mode section")
        if not self.has_exercise:
            missing.append("exercise")
        return missing


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Check lesson-depth outline markers.")
    parser.add_argument(
        "--write-outline-status",
        action="store_true",
        help="Insert `Status: outline` under lesson titles that do not meet the mechanical depth gate.",
    )
    args = parser.parse_args(argv)

    lesson_paths = sorted(ROOT.glob(LESSON_GLOB))
    audits = [audit_lesson(path) for path in lesson_paths]

    if args.write_outline_status:
        for audit in audits:
            if audit.needs_outline_status and not audit.has_outline_status:
                add_outline_status(audit.path)
        audits = [audit_lesson(path) for path in lesson_paths]

    print_report(audits)
    invalid = [audit for audit in audits if not audit.valid]
    return 1 if invalid else 0


def audit_lesson(path: Path) -> LessonAudit:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    headings = {line.strip() for line in lines if line.startswith("## ")}
    return LessonAudit(
        path=path,
        has_outline_status=has_outline_status(lines),
        has_failure_mode=bool(FAILURE_HEADINGS & headings),
        has_exercise="## Exercise" in headings,
    )


def has_outline_status(lines: list[str]) -> bool:
    for line in lines[:5]:
        if line.strip() == OUTLINE_STATUS:
            return True
    return False


def add_outline_status(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or not lines[0].startswith("# "):
        raise ValueError(f"{path}: expected first line to be a lesson title")
    updated = [lines[0], "", OUTLINE_STATUS, *lines[1:]]
    path.write_text("\n".join(collapse_blank_after_status(updated)).rstrip() + "\n", encoding="utf-8")


def collapse_blank_after_status(lines: list[str]) -> list[str]:
    text = "\n".join(lines)
    text = re.sub(rf"({re.escape(OUTLINE_STATUS)})\n{{2,}}", rf"\1\n\n", text)
    return text.splitlines()


def print_report(audits: list[LessonAudit]) -> None:
    complete = sum(audit.complete for audit in audits)
    outline = sum(audit.has_outline_status for audit in audits)
    missing_failure = sum(not audit.has_failure_mode for audit in audits)
    missing_exercise = sum(not audit.has_exercise for audit in audits)
    print("# Lesson Depth Audit")
    print()
    print(f"- lessons: {len(audits)}")
    print(f"- mechanically complete: {complete}")
    print(f"- marked outline: {outline}")
    print(f"- missing failure-mode section: {missing_failure}")
    print(f"- missing exercise: {missing_exercise}")
    print()
    for audit in audits:
        if audit.valid:
            continue
        relative = audit.path.relative_to(ROOT)
        print(f"FAIL {relative}: missing {', '.join(audit.missing)} and no `{OUTLINE_STATUS}` marker.")


if __name__ == "__main__":
    raise SystemExit(main())
