"""Autograder tests for Part 7 (REPORT.md completeness). DO NOT EDIT.

These tests only check that the report is complete. Your instructor grades
the quality of the writing by hand.
"""
import re

import pytest

from assignment.paths import ROOT

REPORT = ROOT / "REPORT.md"
ANSWER_MARKER = "**Your answer:**"

SECTIONS = {
    "1. Sales Insights": 80,
    "2. Data Cleaning Decisions": 80,
    "3. Titanic EDA Findings": 100,
    "4. Model Results": 100,
    "5. Reflection": 50,
}


def _sections():
    text = REPORT.read_text(encoding="utf-8")
    parts = re.split(r"^## ", text, flags=re.MULTILINE)
    return {p.splitlines()[0]: "\n".join(p.splitlines()[1:]) for p in parts[1:]}


def _words(text):
    return re.findall(r"[A-Za-z0-9%.]+", text)


def test_student_details_filled():
    assert REPORT.exists(), "REPORT.md is missing"
    text = REPORT.read_text(encoding="utf-8")
    assert not re.search(r"\*\*Student name:\*\*\s*TODO", text), "fill in your name"
    assert not re.search(r"\*\*GitHub username:\*\*\s*TODO", text), "fill in your GitHub username"


@pytest.mark.parametrize("title,min_words", SECTIONS.items())
def test_section_completed(title, min_words):
    sections = _sections()
    match = next((body for heading, body in sections.items() if heading.startswith(title)), None)
    assert match is not None, f"section '{title}' is missing; do not rename the headings"
    assert ANSWER_MARKER in match, f"keep the '{ANSWER_MARKER}' line in '{title}' and write below it"
    answer = match.split(ANSWER_MARKER, 1)[1]
    assert not re.search(r"^\s*TODO\s*$", answer, flags=re.MULTILINE), f"replace the TODO in '{title}'"
    count = len(_words(answer))
    assert count >= min_words, f"your answer to '{title}' has ~{count} words; it needs at least {min_words}"
