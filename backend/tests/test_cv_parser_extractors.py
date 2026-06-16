"""
Tests for cv_parser.extractors — file routing and text extraction.
Corrupt/empty PDF tests document a known gap: the extractor propagates
pdfplumber exceptions rather than returning a graceful failed result.
"""

import pytest

from BES01_cv_parser.extractors import (
    RawExtraction,
    _extension_of,
    dispatch_by_extension,
    extract_text,
    supported_extensions,
)


# ---------------------------------------------------------------------------
# _extension_of helper
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("filename,expected", [
    ("resume.pdf", "pdf"),
    ("cv.DOCX", "docx"),
    ("my.resume.TXT", "txt"),
    ("no_extension", ""),
    (".hidden", "hidden"),
    ("file.", ""),
])
def test_extension_of(filename, expected):
    assert _extension_of(filename) == expected


# ---------------------------------------------------------------------------
# extract_text
# ---------------------------------------------------------------------------

def test_extract_text_utf8():
    result = extract_text(b"Hello World")
    assert result.text == "Hello World"
    assert result.method == "text"


def test_extract_text_empty_bytes():
    result = extract_text(b"")
    assert result.text == ""
    assert result.method == "text"


def test_extract_text_latin1_fallback():
    # "Résumé" encoded as latin-1 is not valid UTF-8
    latin1_bytes = "Résumé".encode("latin-1")
    result = extract_text(latin1_bytes)
    assert result.method == "text"
    assert len(result.text) > 0  # decoded without raising


def test_extract_text_strips_leading_trailing_whitespace():
    result = extract_text(b"  hello  \n")
    assert result.text == "hello"


# ---------------------------------------------------------------------------
# dispatch_by_extension — routing
# ---------------------------------------------------------------------------

def test_dispatch_txt_routes_correctly():
    result = dispatch_by_extension(b"plain text content", "cv.txt")
    assert result.method == "text"
    assert result.text == "plain text content"


def test_dispatch_txt_case_insensitive():
    result = dispatch_by_extension(b"content", "cv.TXT")
    assert result.method == "text"


def test_dispatch_unsupported_extension_returns_failed():
    result = dispatch_by_extension(b"anything", "file.xyz")
    assert result.method == "failed"
    assert result.text == ""


def test_dispatch_no_extension_returns_failed():
    result = dispatch_by_extension(b"data", "resume")
    assert result.method == "failed"
    assert result.text == ""


def test_dispatch_failed_result_has_empty_chars_and_zero_area():
    result = dispatch_by_extension(b"data", "file.xyz")
    assert result.chars == []
    assert result.total_page_area == 0.0


# ---------------------------------------------------------------------------
# dispatch_by_extension — corrupt / empty PDF
# GAP: extract_pdf has no try/except; pdfplumber raises on invalid bytes.
# These tests document that behavior so it's visible before production hits it.
# ---------------------------------------------------------------------------

def test_dispatch_corrupt_pdf_raises():
    with pytest.raises(Exception):
        dispatch_by_extension(b"not a real pdf", "resume.pdf")


def test_dispatch_empty_pdf_raises():
    with pytest.raises(Exception):
        dispatch_by_extension(b"", "empty.pdf")


# ---------------------------------------------------------------------------
# supported_extensions
# ---------------------------------------------------------------------------

def test_supported_extensions_contains_expected():
    exts = supported_extensions()
    assert "pdf" in exts
    assert "docx" in exts
    assert "txt" in exts
