from pathlib import Path

import scripts.check_lesson_depth as checker


def test_audit_recognizes_complete_lesson(tmp_path, monkeypatch):
    lesson = tmp_path / "levels" / "01-build" / "lessons" / "01-complete.md"
    lesson.parent.mkdir(parents=True)
    lesson.write_text(
        "# Lesson 1: Complete\n\n"
        "## Core Idea\n\n"
        "Text.\n\n"
        "## Common Failure Modes\n\n"
        "- Failing silently.\n\n"
        "## Exercise\n\n"
        "Answer: run the checker.\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(checker, "ROOT", tmp_path)

    audit = checker.audit_lesson(lesson)

    assert audit.complete is True
    assert audit.valid is True
    assert audit.needs_outline_status is False


def test_audit_requires_outline_status_for_incomplete_lesson(tmp_path, monkeypatch):
    lesson = tmp_path / "levels" / "01-build" / "lessons" / "02-outline.md"
    lesson.parent.mkdir(parents=True)
    lesson.write_text("# Lesson 2: Outline\n\n## Core Idea\n\nText.\n", encoding="utf-8")
    monkeypatch.setattr(checker, "ROOT", tmp_path)

    audit = checker.audit_lesson(lesson)

    assert audit.complete is False
    assert audit.valid is False
    assert audit.missing == ["failure-mode section", "exercise"]


def test_write_outline_status_inserts_marker_under_title(tmp_path):
    lesson = tmp_path / "lesson.md"
    lesson.write_text("# Lesson\n\n## Core Idea\n\nText.\n", encoding="utf-8")

    checker.add_outline_status(lesson)

    assert lesson.read_text(encoding="utf-8").splitlines()[:3] == [
        "# Lesson",
        "",
        "Status: outline",
    ]


def test_outline_status_makes_incomplete_lesson_valid(tmp_path):
    lesson = tmp_path / "lesson.md"
    lesson.write_text("# Lesson\n\nStatus: outline\n\n## Core Idea\n\nText.\n", encoding="utf-8")

    audit = checker.audit_lesson(lesson)

    assert audit.complete is False
    assert audit.has_outline_status is True
    assert audit.valid is True
