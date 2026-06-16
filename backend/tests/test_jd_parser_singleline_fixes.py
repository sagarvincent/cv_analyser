"""
Tests for BES03_jd_parser 1.1.0 single-line / scraped-JD fixes.

Coverage:
  - reflow_inline_headings: gate on newline-sparse input; colon + ALL-CAPS
    cue splitting; no-op on multi-line text (regression guard).
  - Full parse_jd on a single-line (Built In style) JD: populated sections,
    short title, no warnings.
  - Salary digit guard: bare-comma currency tokens no longer crash.
  - split_bullets sentence fallback on a long single-line section.
"""
from BES02_jd_parser.leaves.extraction_leaves import extract_salary
from BES02_jd_parser.leaves.segmentation_leaves import (
    reflow_inline_headings,
    split_bullets,
)
from BES02_jd_parser.parser import parse_jd


# ── Single-line JD fixture (condensed Built In shape) ─────────────────────────

SINGLE_LINE_JD = (
    "About Acme Corp is a leading global provider of cloud commerce solutions "
    "headquartered in Atlanta with thousands of employees serving retail and "
    "banking customers around the world every single day of the year. "
    "Title: Senior Backend Engineer Grade: 11 Location: Midtown Atlanta "
    "YOU ARE Passionate about technology and love solving hard distributed "
    "systems problems at a massive scale for millions of users worldwide. "
    "IN THIS ROLE, YOU CAN EXPECT TO Build and operate high-throughput APIs. "
    "Craft clean, well-tested code using continuous delivery. Mentor newer "
    "engineers across several scrum teams in the platform organization. "
    "YOU HAVE 5+ years of software development experience with Java and "
    "TypeScript. Experience designing and testing RESTful APIs at scale. "
    "EVEN BETTER IF YOU HAVE Background with Spring, Kafka, and Kubernetes. "
    "Familiarity with GCP, Azure, or AWS cloud native data stores."
)


# ── reflow_inline_headings ────────────────────────────────────────────────────

def test_reflow_is_noop_on_multiline_text():
    multiline = "Responsibilities\nBuild APIs\nRequirements\n5 years Java"
    assert reflow_inline_headings(multiline) == multiline


def test_reflow_is_noop_on_short_text():
    short = "Title: Engineer YOU HAVE 5 years experience"
    assert reflow_inline_headings(short) == short


def test_reflow_splits_colon_labels_and_caps_cues():
    out = reflow_inline_headings(SINGLE_LINE_JD)
    assert out.count("\n") > 5
    lines = [ln.strip() for ln in out.split("\n")]
    assert "Title: Senior Backend Engineer" in lines
    assert "YOU HAVE" in lines
    assert "EVEN BETTER IF YOU HAVE" in lines


# ── Full parse on the single-line JD ──────────────────────────────────────────

def test_singleline_jd_populates_sections():
    p = parse_jd(SINGLE_LINE_JD)
    assert p.responsibilities, "responsibilities should not be empty"
    assert p.required_qualifications, "requirements should not be empty"
    assert p.preferred_qualifications, "preferred should not be empty"


def test_singleline_jd_has_short_title():
    p = parse_jd(SINGLE_LINE_JD)
    assert p.title == "Senior Backend Engineer"


def test_singleline_jd_requirements_not_polluted_by_persona():
    # "YOU ARE Passionate..." is persona fluff and must not land in requirements.
    p = parse_jd(SINGLE_LINE_JD)
    joined = " ".join(p.required_qualifications).lower()
    assert "5+ years" in joined
    assert "passionate about technology" not in joined


def test_singleline_jd_clears_section_warnings():
    # The reflow fix targets responsibilities/requirements/preferred detection.
    p = parse_jd(SINGLE_LINE_JD)
    assert "no responsibilities section found" not in p.parse_warnings
    assert "no requirements section found" not in p.parse_warnings
    assert "no preferred qualifications section found" not in p.parse_warnings


# ── Salary digit guard ────────────────────────────────────────────────────────

def test_salary_bare_comma_does_not_crash():
    assert extract_salary("compensation USD, competitive") is None
    assert extract_salary("pay $, negotiable") is None


def test_salary_valid_range_still_parses():
    out = extract_salary("salary $120,000 to $150k")
    assert out is not None
    assert out["min"] == 120000.0
    assert out["max"] == 150000.0
    assert out["currency"] == "USD"


# ── split_bullets sentence fallback ───────────────────────────────────────────

def test_split_bullets_sentence_fallback_on_long_line():
    long_line = (
        "Build and operate high-throughput APIs across teams. "
        "Craft clean well-tested code using continuous delivery pipelines. "
        "Mentor newer engineers in the wider platform organization daily."
    ) * 2
    items = split_bullets(long_line)
    assert len(items) >= 3


def test_split_bullets_keeps_short_lines_intact():
    text = "Build APIs\n5 years Java\nMentor engineers"
    assert split_bullets(text) == ["Build APIs", "5 years Java", "Mentor engineers"]
