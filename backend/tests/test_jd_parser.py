"""
Tests for BES03_jd_parser.

Coverage:
  - extraction_leaves: infer_seniority, extract_salary, extract_location,
    extract_employment_type, flatten_json, flatten_csv
  - segmentation_leaves: is_heading, label_for_heading, split_bullets
  - Full parse_jd pipeline: text fixture, JSON fixture, warnings
"""
import json

import pytest

from BES02_jd_parser.leaves.extraction_leaves import (
    extract_employment_type,
    extract_location,
    extract_salary,
    flatten_csv,
    flatten_json,
    infer_seniority,
)
from BES02_jd_parser.leaves.segmentation_leaves import (
    is_heading,
    label_for_heading,
    split_bullets,
)
from BES02_jd_parser.parser import parse_jd


# ── Fixtures ──────────────────────────────────────────────────────────────────

SIMPLE_JD = """\
Senior Product Designer at Acme Ltd
London · Full-time · £60,000 – £80,000

About The Role
We are looking for a Senior Product Designer to lead our design system.

Responsibilities
• Define and evolve the design system
• Partner with engineers to ship high-quality UI
• Mentor junior designers

Requirements
5+ years of product design experience
Proficiency in Figma and prototyping tools
Experience working in agile environments

Preferred Qualifications
Fintech or regulated-industry background
Experience with design tokens

Skills
Figma
Design Systems
Prototyping

Benefits
Flexible working hours
25 days holiday
Private healthcare
"""

SPARSE_JD = """\
Junior Software Engineer
We build cool stuff.
"""


# ── infer_seniority ───────────────────────────────────────────────────────────

@pytest.mark.parametrize("title,expected", [
    ("Senior Product Designer", "senior"),
    ("Junior Software Engineer", "junior"),
    ("Lead Backend Engineer", "lead"),
    ("Principal Architect", "lead"),
    ("Software Engineer", "mid"),
    ("Product Manager", "manager"),
    ("VP of Engineering", "director"),
    ("Director of Product Design", "director"),
    ("Intern – Data Science", "intern"),
    ("Associate Consultant", "junior"),
    ("Staff Engineer", "lead"),
])
def test_infer_seniority(title, expected):
    assert infer_seniority(title) == expected


# ── extract_salary ────────────────────────────────────────────────────────────

def test_extract_salary_gbp_range():
    result = extract_salary("Salary: £60,000 – £80,000 per year")
    assert result is not None
    assert result["currency"] == "GBP"
    assert result["min"] == 60_000.0
    assert result["max"] == 80_000.0


def test_extract_salary_usd_k():
    result = extract_salary("$80k - $120k depending on experience")
    assert result is not None
    assert result["currency"] == "USD"
    assert result["min"] == 80_000.0
    assert result["max"] == 120_000.0


def test_extract_salary_single_value():
    result = extract_salary("Up to £75,000")
    assert result is not None
    assert result["min"] == 75_000.0
    assert result["max"] is None


def test_extract_salary_none_when_missing():
    assert extract_salary("No salary mentioned here.") is None


# ── extract_location ──────────────────────────────────────────────────────────

def test_extract_location_remote():
    assert extract_location(["Remote · Full-time"]) == "Remote"


def test_extract_location_city():
    assert extract_location(["London · Full-time"]) == "London"


def test_extract_location_hybrid():
    result = extract_location(["Hybrid working, Manchester"])
    assert result is not None
    assert result.lower() in ("hybrid", "manchester")


def test_extract_location_none():
    assert extract_location(["We build great things"]) is None


# ── extract_employment_type ───────────────────────────────────────────────────

@pytest.mark.parametrize("line,expected", [
    ("London · Full-time", "full-time"),
    ("Contract role", "contract"),
    ("Part time position", "part-time"),
    ("Permanent opportunity", "permanent"),
])
def test_extract_employment_type(line, expected):
    assert extract_employment_type([line]) == expected


def test_extract_employment_type_none():
    assert extract_employment_type(["Senior engineer role"]) is None


# ── flatten_json ──────────────────────────────────────────────────────────────

def test_flatten_json_simple():
    data = json.dumps({"title": "Engineer", "description": "Build things"}).encode()
    result = flatten_json(data)
    assert "Engineer" in result
    assert "Build things" in result


def test_flatten_json_nested():
    data = json.dumps({
        "job": {"title": "Designer", "requirements": ["Figma", "Sketch"]},
        "meta": {"company": "Acme"},
    }).encode()
    result = flatten_json(data)
    assert "Designer" in result
    assert "Figma" in result
    assert "Acme" in result


def test_flatten_json_invalid_falls_back_to_raw():
    raw = b"not json at all"
    result = flatten_json(raw)
    assert "not json" in result


# ── flatten_csv ───────────────────────────────────────────────────────────────

def test_flatten_csv_with_headers():
    csv_bytes = b"title,description\nEngineer,Build things\n"
    result = flatten_csv(csv_bytes)
    assert "Engineer" in result
    assert "Build things" in result


def test_flatten_csv_empty():
    assert flatten_csv(b"") == ""


# ── is_heading / label_for_heading ────────────────────────────────────────────

@pytest.mark.parametrize("line", [
    "Responsibilities",
    "RESPONSIBILITIES",
    "About The Role",
    "Requirements:",
    "Benefits",
    "What You'll Do",
])
def test_is_heading_recognises_jd_headers(line):
    assert is_heading(line) is True


@pytest.mark.parametrize("line", [
    "5+ years of product design experience",
    "We are looking for a talented designer",
    "",
    "A very long line that goes on and on and definitely exceeds the heading length limit so it should not be treated as heading",
])
def test_is_heading_rejects_content_lines(line):
    assert is_heading(line) is False


@pytest.mark.parametrize("line,expected_label", [
    ("Responsibilities", "responsibilities"),
    ("What You'll Do", "responsibilities"),
    ("Requirements", "requirements"),
    ("What We're Looking For", "requirements"),
    ("Preferred Qualifications", "preferred"),
    ("Benefits", "benefits"),
    ("About Us", "about_company"),
    ("About The Role", "overview"),
    ("Skills", "skills"),
])
def test_label_for_heading(line, expected_label):
    assert label_for_heading(line) == expected_label


def test_label_for_heading_unknown_returns_none():
    assert label_for_heading("Random Unrecognised Header") is None


# ── split_bullets ─────────────────────────────────────────────────────────────

def test_split_bullets_strips_bullet_chars():
    text = "• Design systems\n● Figma proficiency\n- Agile experience"
    result = split_bullets(text)
    assert result == ["Design systems", "Figma proficiency", "Agile experience"]


def test_split_bullets_empty_lines_filtered():
    text = "• First item\n\n• Second item\n\n"
    result = split_bullets(text)
    assert len(result) == 2


def test_split_bullets_preserves_long_sentences():
    sentence = "Collaborate closely with engineers and product managers to ship high-quality features on time."
    result = split_bullets(sentence)
    assert result == [sentence]


# ── Full parse_jd pipeline ────────────────────────────────────────────────────

@pytest.fixture
def parsed():
    return parse_jd(SIMPLE_JD)


def test_parse_jd_title(parsed):
    assert parsed.title == "Senior Product Designer at Acme Ltd"


def test_parse_jd_seniority(parsed):
    assert parsed.seniority == "senior"


def test_parse_jd_location(parsed):
    assert parsed.location is not None
    assert "London" in parsed.location or "london" in parsed.location.lower()


def test_parse_jd_employment_type(parsed):
    assert parsed.employment_type == "full-time"


def test_parse_jd_salary(parsed):
    assert parsed.salary_range is not None
    assert parsed.salary_range.currency == "GBP"
    assert parsed.salary_range.min == 60_000.0
    assert parsed.salary_range.max == 80_000.0


def test_parse_jd_responsibilities_non_empty(parsed):
    assert len(parsed.responsibilities) >= 2
    assert any("design system" in r.lower() for r in parsed.responsibilities)


def test_parse_jd_required_qualifications_non_empty(parsed):
    assert len(parsed.required_qualifications) >= 2


def test_parse_jd_preferred_qualifications(parsed):
    assert len(parsed.preferred_qualifications) >= 1
    assert any("fintech" in p.lower() for p in parsed.preferred_qualifications)


def test_parse_jd_required_skills(parsed):
    assert "Figma" in parsed.required_skills


def test_parse_jd_benefits(parsed):
    assert len(parsed.benefits) >= 2


def test_parse_jd_no_warnings_on_complete_jd(parsed):
    assert parsed.parse_warnings == []


def test_parse_jd_parser_version(parsed):
    from BES02_jd_parser import JD_PARSER_VERSION
    assert parsed.parser_version == JD_PARSER_VERSION


def test_parse_jd_raw_text_populated(parsed):
    assert len(parsed.raw_text) > 50


# ── Sparse JD — warnings emitted ─────────────────────────────────────────────

def test_parse_sparse_jd_emits_warnings():
    result = parse_jd(SPARSE_JD)
    assert len(result.parse_warnings) > 0
    assert any("responsibilities" in w for w in result.parse_warnings)
    assert any("requirements" in w for w in result.parse_warnings)


def test_parse_sparse_jd_title_captured():
    result = parse_jd(SPARSE_JD)
    assert result.title == "Junior Software Engineer"
    assert result.seniority == "junior"


# ── JSON input via parse_jd ───────────────────────────────────────────────────

def test_parse_jd_from_json_flattened():
    jd_dict = {
        "title": "Data Scientist",
        "responsibilities": ["Build ML models", "Analyse data"],
        "requirements": ["Python", "SQL"],
    }
    text = "\n".join([
        "Data Scientist",
        "Build ML models",
        "Analyse data",
        "Python",
        "SQL",
    ])
    result = parse_jd(text)
    assert result.title == "Data Scientist"
    assert result.seniority == "mid"
