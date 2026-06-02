"""
Tests for the pure leaf functions — no I/O, no external dependencies, fast.
"""

import pytest

from cv_parser.leaves.cleaning_leaves import (
    distinct_bullet_chars,
    hyphenation_break_rate,
    line_length_bimodality,
    normalise_whitespace,
)
from cv_parser.leaves.extraction_leaves import (
    encoding_anomaly_rate,
    page_area,
    stream_order_anomaly,
    text_density,
)
from cv_parser.leaves.segmentation_leaves import (
    find_date_range,
    is_heading,
    label_for_heading,
    section_coherence_score,
    split_blocks_by_blank_line,
)


# ---------------------------------------------------------------------------
# is_heading
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("line", [
    "EXPERIENCE",
    "experience",
    "Work Experience",
    "EDUCATION",
    "education",
    "SKILLS",
    "Technical Skills",
    "skills",
    "CERTIFICATIONS",
    "certifications",
    "Projects",
    "Summary",
    "About Me",
    "profile",
    "OBJECTIVE",
    "Employment",
    "Core Competencies",
    "Portfolio",
    "Courses",
    # with trailing colon
    "EXPERIENCE:",
    "education:",
])
def test_is_heading_known_sections(line):
    assert is_heading(line) is True


@pytest.mark.parametrize("line", [
    "",
    "John Smith currently works at a company handling many responsibilities",
    "Python JavaScript React Node.js Docker AWS Kubernetes GCP Azure",
    "Led a cross-functional team of 8 engineers across three product lines",
])
def test_is_heading_non_headings(line):
    assert is_heading(line) is False


def test_is_heading_all_caps_unknown_section():
    # ALL-CAPS passes the isupper() check even for unknown sections
    assert is_heading("FOOBAR") is True


# ---------------------------------------------------------------------------
# label_for_heading
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("line,expected", [
    ("experience", "experience"),
    ("EXPERIENCE", "experience"),
    ("Work Experience", "experience"),
    ("employment", "experience"),
    ("Professional Experience", "experience"),
    ("Work History", "experience"),
    ("education", "education"),
    ("EDUCATION", "education"),
    ("Academic Background", "education"),
    ("qualifications", "education"),
    ("skills", "skills"),
    ("Technical Skills", "skills"),
    ("Core Competencies", "skills"),
    ("key skills", "skills"),
    ("summary", "summary"),
    ("profile", "summary"),
    ("About Me", "summary"),
    ("objective", "summary"),
    ("Professional Summary", "summary"),
    ("projects", "projects"),
    ("Personal Projects", "projects"),
    ("portfolio", "projects"),
    ("certifications", "certifications"),
    ("certificates", "certifications"),
    ("courses", "certifications"),
    ("licenses", "certifications"),
])
def test_label_for_heading_known(line, expected):
    assert label_for_heading(line) == expected


@pytest.mark.parametrize("line", [
    "FOOBAR",          # all-caps but not a known section
    "gibberish",
    "Random Heading",
    "",
])
def test_label_for_heading_unknown_returns_none(line):
    assert label_for_heading(line) is None


def test_label_for_heading_strips_trailing_colon():
    assert label_for_heading("experience:") == "experience"
    assert label_for_heading("SKILLS:") == "skills"


# ---------------------------------------------------------------------------
# find_date_range
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("text,expected_nonempty", [
    ("Jan 2020 - Present", True),
    ("January 2019 - December 2022", True),
    ("2018 - 2022", True),
    ("2020 to present", True),
    ("06/2019 - 08/2021", True),
    ("Sep. 2017 - Mar. 2020", True),
])
def test_find_date_range_detects_dates(text, expected_nonempty):
    result = find_date_range(text)
    assert (result is not None) == expected_nonempty


@pytest.mark.parametrize("text", [
    "no dates here",
    "John Smith",
    "",
    "Python JavaScript React",
])
def test_find_date_range_returns_none_when_absent(text):
    assert find_date_range(text) is None


def test_find_date_range_returns_matched_substring():
    text = "Software Engineer | Tech Corp | Jan 2020 - Present"
    result = find_date_range(text)
    assert result is not None
    assert "2020" in result
    assert "resent" in result.lower()


# ---------------------------------------------------------------------------
# section_coherence_score
# ---------------------------------------------------------------------------

def test_section_coherence_skills_high():
    content = "Python\nJavaScript\nReact\nDocker\nAWS\nSQL"
    score = section_coherence_score("skills", content)
    assert score > 0.0


def test_section_coherence_experience_high():
    content = "Led a team of engineers\nManaged the project delivery\nDeveloped APIs"
    score = section_coherence_score("experience", content)
    assert score > 0.0


def test_section_coherence_education_high():
    content = "Bachelor of Computer Science\nState University\nGPA 3.8"
    score = section_coherence_score("education", content)
    assert score > 0.0


def test_section_coherence_empty_content_returns_zero():
    assert section_coherence_score("skills", "") == 0.0


def test_section_coherence_unknown_section_returns_zero():
    assert section_coherence_score("other", "anything goes here") == 0.0


def test_section_coherence_score_in_range():
    score = section_coherence_score("skills", "Python AWS Docker React Kubernetes")
    assert 0.0 <= score <= 1.0


# ---------------------------------------------------------------------------
# split_blocks_by_blank_line
# ---------------------------------------------------------------------------

def test_split_blocks_two_entries():
    text = "Title A\nOrg A\n\nTitle B\nOrg B"
    blocks = split_blocks_by_blank_line(text)
    assert len(blocks) == 2
    assert "Title A" in blocks[0]
    assert "Title B" in blocks[1]


def test_split_blocks_single_block_no_blank():
    text = "Title\nDescription line"
    blocks = split_blocks_by_blank_line(text)
    assert len(blocks) == 1


def test_split_blocks_empty_string():
    assert split_blocks_by_blank_line("") == []


def test_split_blocks_only_blank_lines():
    assert split_blocks_by_blank_line("\n\n\n") == []


# ---------------------------------------------------------------------------
# normalise_whitespace
# ---------------------------------------------------------------------------

def test_normalise_crlf_to_lf():
    assert normalise_whitespace("hello\r\nworld") == "hello\nworld"


def test_normalise_collapses_spaces_and_tabs():
    assert normalise_whitespace("hello   \t  world") == "hello world"


def test_normalise_collapses_excess_newlines():
    result = normalise_whitespace("a\n\n\n\nb")
    assert result == "a\n\nb"


def test_normalise_strips_edges():
    assert normalise_whitespace("  hello  ") == "hello"


def test_normalise_empty_string():
    assert normalise_whitespace("") == ""


# ---------------------------------------------------------------------------
# distinct_bullet_chars
# ---------------------------------------------------------------------------

def test_distinct_bullet_chars_none():
    assert distinct_bullet_chars("plain text no bullets") == 0


def test_distinct_bullet_chars_one_type():
    assert distinct_bullet_chars("• item one\n• item two\n• item three") == 1


def test_distinct_bullet_chars_multiple_types():
    count = distinct_bullet_chars("• item ▪ other ● third – fourth")
    assert count == 4


# ---------------------------------------------------------------------------
# hyphenation_break_rate
# ---------------------------------------------------------------------------

def test_hyphenation_break_rate_detects_break():
    lines = ["re-", "sponsible for delivery", "other line"]
    rate = hyphenation_break_rate(lines)
    assert rate > 0.0


def test_hyphenation_break_rate_no_breaks():
    lines = ["clean line one", "clean line two", "clean line three"]
    assert hyphenation_break_rate(lines) == 0.0


def test_hyphenation_break_rate_empty():
    assert hyphenation_break_rate([]) == 0.0


def test_hyphenation_break_rate_single_line():
    assert hyphenation_break_rate(["only one line"]) == 0.0


# ---------------------------------------------------------------------------
# line_length_bimodality
# ---------------------------------------------------------------------------

def test_line_length_bimodality_in_range():
    lines = ["short", "a longer line here", "tiny", "another longer line with more words"]
    score = line_length_bimodality(lines)
    assert 0.0 <= score <= 1.0


def test_line_length_bimodality_too_few_lines_returns_zero():
    assert line_length_bimodality(["a", "bb", "ccc"]) == 0.0


def test_line_length_bimodality_ignores_blank_lines():
    lines = ["word", "", "another", "", "more", "last"]
    score = line_length_bimodality(lines)
    assert 0.0 <= score <= 1.0


# ---------------------------------------------------------------------------
# stream_order_anomaly
# ---------------------------------------------------------------------------

def test_stream_order_anomaly_empty():
    assert stream_order_anomaly([]) == 0.0


def test_stream_order_anomaly_single_char():
    chars = [{"text": "a", "x0": 10.0, "top": 5.0, "page_number": 1}]
    assert stream_order_anomaly(chars) == 0.0


def test_stream_order_anomaly_clean_left_to_right():
    chars = [
        {"text": "a", "x0": 10.0, "top": 5.0, "page_number": 1},
        {"text": "b", "x0": 20.0, "top": 5.0, "page_number": 1},
        {"text": "c", "x0": 30.0, "top": 5.0, "page_number": 1},
    ]
    assert stream_order_anomaly(chars) == 0.0


def test_stream_order_anomaly_backwards_chars():
    chars = [
        {"text": "c", "x0": 30.0, "top": 5.0, "page_number": 1},
        {"text": "b", "x0": 20.0, "top": 5.0, "page_number": 1},
        {"text": "a", "x0": 10.0, "top": 5.0, "page_number": 1},
    ]
    assert stream_order_anomaly(chars) == 1.0


def test_stream_order_anomaly_cross_page_ignored():
    # Page boundary — cross-page pairs are skipped
    chars = [
        {"text": "a", "x0": 30.0, "top": 5.0, "page_number": 1},
        {"text": "b", "x0": 10.0, "top": 5.0, "page_number": 2},
    ]
    assert stream_order_anomaly(chars) == 0.0


# ---------------------------------------------------------------------------
# text_density
# ---------------------------------------------------------------------------

def test_text_density_zero_area():
    assert text_density(1000, 0.0) == 0.0


def test_text_density_normal():
    result = text_density(100, 1000.0)
    assert abs(result - 0.1) < 1e-9


# ---------------------------------------------------------------------------
# encoding_anomaly_rate
# ---------------------------------------------------------------------------

def test_encoding_anomaly_rate_empty():
    assert encoding_anomaly_rate("") == 0.0


def test_encoding_anomaly_rate_clean_ascii():
    assert encoding_anomaly_rate("Hello World 123!") == 0.0


def test_encoding_anomaly_rate_mojibake_detected():
    rate = encoding_anomaly_rate("caf�")
    assert rate > 0.0


# ---------------------------------------------------------------------------
# page_area
# ---------------------------------------------------------------------------

def test_page_area_normal():
    assert page_area(100.0, 200.0) == 20000.0


def test_page_area_zero_dimension():
    assert page_area(0.0, 200.0) == 0.0


def test_page_area_negative_clamped_to_zero():
    assert page_area(-10.0, 200.0) == 0.0
