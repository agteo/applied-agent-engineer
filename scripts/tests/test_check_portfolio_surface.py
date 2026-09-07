from pathlib import Path

import scripts.check_portfolio_surface as checker


def test_check_sections_reports_missing_sections(tmp_path):
    path = tmp_path / "example.md"
    path.write_text("# Example\n\n## Problem\n\nText.\n", encoding="utf-8")

    failures = checker.check_sections(path, ["## Problem", "## Evidence"])

    assert failures == [f"{path}: missing ## Evidence"]


def test_check_sections_accepts_required_sections(tmp_path):
    path = tmp_path / "example.md"
    path.write_text("# Example\n\n## Problem\n\nText.\n\n## Evidence\n\nText.\n", encoding="utf-8")

    failures = checker.check_sections(path, ["## Problem", "## Evidence"])

    assert failures == []
