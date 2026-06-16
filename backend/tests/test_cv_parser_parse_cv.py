"""
Integration tests for cv_parser.parser.parse_cv.

Unit-level cases use an in-memory synthetic CV to keep tests fast and
deterministic.  The @pytest.mark.integration tests read real fixture files
from test/real_data/ and are skipped automatically when the file is absent.
"""

import pathlib

import pytest

from BES01_cv_parser.parser import parse_cv

# ---------------------------------------------------------------------------
# Synthetic fixture — a well-structured CV as plain text
# ---------------------------------------------------------------------------

_SYNTHETIC_CV = """
John Smith
Software Engineer | john@example.com | github.com/jsmith

SUMMARY
Experienced software engineer with 5 years of Python and backend development background.

EXPERIENCE

Software Engineer
Tech Company Inc.
Jan 2020 - Present
Led development of microservices using Python, Docker, and Kubernetes.
Managed a team of 4 developers across two sprints per month.

Junior Developer
Startup Ltd.
2018 - 2020
Built REST APIs and implemented CI/CD pipelines.
Worked alongside the engineering team to ship features.

EDUCATION

Bachelor of Computer Science
State University
2014 - 2018
GPA 3.8

SKILLS
Python, JavaScript, React, Docker, AWS, SQL, Kubernetes, Agile

CERTIFICATIONS
AWS Certified Developer - certified 2021
Google Cloud Professional Certificate - 2022
""".strip()

_REPO_ROOT = pathlib.Path(__file__).parents[2]  # cv_analyser/


# ---------------------------------------------------------------------------
# Extraction method and raw text
# ---------------------------------------------------------------------------

def test_parse_txt_extraction_method():
    result = parse_cv(_SYNTHETIC_CV.encode(), "resume.txt")
    assert result.extraction_method == "text"


def test_parse_txt_raw_text_populated():
    result = parse_cv(_SYNTHETIC_CV.encode(), "resume.txt")
    assert len(result.raw_text) > 50
    assert "SUMMARY" in result.raw_text or "summary" in result.raw_text.lower()


# ---------------------------------------------------------------------------
# Section structure
# ---------------------------------------------------------------------------

def test_parse_txt_summary_populated():
    result = parse_cv(_SYNTHETIC_CV.encode(), "resume.txt")
    assert result.sections.summary != ""
    assert "engineer" in result.sections.summary.lower()


def test_parse_txt_experience_has_entries():
    result = parse_cv(_SYNTHETIC_CV.encode(), "resume.txt")
    assert len(result.sections.experience) >= 1


def test_parse_txt_experience_entry_fields():
    result = parse_cv(_SYNTHETIC_CV.encode(), "resume.txt")
    first = result.sections.experience[0]
    assert first.title is not None
    assert first.dates is not None
    assert "2020" in first.dates or "2018" in first.dates


def test_parse_txt_education_has_entries():
    result = parse_cv(_SYNTHETIC_CV.encode(), "resume.txt")
    assert len(result.sections.education) >= 1


def test_parse_txt_education_entry_fields():
    result = parse_cv(_SYNTHETIC_CV.encode(), "resume.txt")
    edu = result.sections.education[0]
    assert edu.degree is not None
    assert "2014" in (edu.dates or "") or "2018" in (edu.dates or "")


def test_parse_txt_skills_populated():
    result = parse_cv(_SYNTHETIC_CV.encode(), "resume.txt")
    assert result.sections.skills.text != ""
    assert len(result.sections.skills.items) >= 3
    skill_names = [s.lower() for s in result.sections.skills.items]
    assert any("python" in s for s in skill_names)


def test_parse_txt_certifications_populated():
    result = parse_cv(_SYNTHETIC_CV.encode(), "resume.txt")
    assert len(result.sections.certifications) >= 1


# ---------------------------------------------------------------------------
# ATS red flags — all metrics must be in valid ranges
# ---------------------------------------------------------------------------

def test_parse_txt_redflags_numeric_ranges():
    result = parse_cv(_SYNTHETIC_CV.encode(), "resume.txt")
    f = result.ats_redflags
    assert 0.0 <= f.stream_order_anomaly <= 1.0
    assert 0.0 <= f.encoding_anomaly_rate <= 1.0
    assert 0.0 <= f.line_length_bimodality <= 1.0
    assert 0.0 <= f.hyphenation_break_rate <= 1.0
    assert 0.0 <= f.heading_detection_rate <= 1.0
    assert 0.0 <= f.section_coherence <= 1.0
    assert 0.0 <= f.unclassified_ratio <= 1.0
    assert f.distinct_bullet_chars >= 0
    assert f.text_density >= 0.0


def test_parse_txt_redflags_extraction_method_matches():
    result = parse_cv(_SYNTHETIC_CV.encode(), "resume.txt")
    assert result.ats_redflags.extraction_method == "text"


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------

def test_parse_empty_txt_does_not_raise():
    result = parse_cv(b"", "empty.txt")
    assert result.extraction_method == "text"
    assert result.raw_text == ""


def test_parse_empty_txt_sections_are_default():
    result = parse_cv(b"", "empty.txt")
    s = result.sections
    assert s.summary == ""
    assert s.experience == []
    assert s.education == []
    assert s.skills.text == ""
    assert s.certifications == []


def test_parse_unsupported_extension_returns_failed():
    result = parse_cv(b"some content", "resume.xyz")
    assert result.extraction_method == "failed"
    assert result.raw_text == ""


def test_parse_unsupported_extension_sections_empty():
    result = parse_cv(b"some content", "resume.xyz")
    s = result.sections
    assert s.experience == []
    assert s.education == []


def test_parse_whitespace_only_txt():
    result = parse_cv(b"   \n\n\n   ", "blank.txt")
    assert result.raw_text == ""
    assert result.extraction_method == "text"


# ---------------------------------------------------------------------------
# Real fixture files — skipped automatically if absent
# ---------------------------------------------------------------------------

@pytest.mark.integration
def test_parse_real_pdf():
    pdf_path = _REPO_ROOT / "test" / "real_data" / "SagarResume-2.pdf"
    if not pdf_path.exists():
        pytest.skip(f"fixture not found: {pdf_path}")
    result = parse_cv(pdf_path.read_bytes(), pdf_path.name)
    assert result.extraction_method in ("digital_pdf", "ocr_pdf")
    assert len(result.raw_text) > 100
    # A real CV should have at least one parseable section
    s = result.sections
    has_content = (
        s.summary != ""
        or len(s.experience) > 0
        or len(s.education) > 0
        or s.skills.text != ""
    )
    assert has_content


@pytest.mark.integration
def test_parse_real_pdf_redflags_in_range():
    pdf_path = _REPO_ROOT / "test" / "real_data" / "SagarResume-2.pdf"
    if not pdf_path.exists():
        pytest.skip(f"fixture not found: {pdf_path}")
    result = parse_cv(pdf_path.read_bytes(), pdf_path.name)
    f = result.ats_redflags
    assert 0.0 <= f.stream_order_anomaly <= 1.0
    assert 0.0 <= f.encoding_anomaly_rate <= 1.0
    assert f.text_density >= 0.0


@pytest.mark.integration
def test_parse_real_docx():
    docx_path = _REPO_ROOT / "test" / "real_data" / "Arya_Sivaraj.docx"
    if not docx_path.exists():
        pytest.skip(f"fixture not found: {docx_path}")
    result = parse_cv(docx_path.read_bytes(), docx_path.name)
    assert result.extraction_method == "docx"
    assert len(result.raw_text) > 100


@pytest.mark.integration
def test_parse_integration_pdf():
    pdf_path = _REPO_ROOT / "test" / "integration" / "data" / "testcase2_cv.pdf"
    if not pdf_path.exists():
        pytest.skip(f"fixture not found: {pdf_path}")
    result = parse_cv(pdf_path.read_bytes(), pdf_path.name)
    assert result.extraction_method in ("digital_pdf", "ocr_pdf")
    assert len(result.raw_text) > 50
