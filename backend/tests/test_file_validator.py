import pytest

from upload_validation.file_validator import FileValidator, MAX_FILE_SIZE_BYTES


@pytest.fixture
def v():
    return FileValidator()


# ---------------------------------------------------------------------------
# Allowed extensions
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("filename", ["resume.pdf", "cv.docx", "cv.txt"])
def test_allowed_extensions_pass(v, filename):
    ok, err = v.validate(filename, 1024)
    assert ok is True
    assert err is None


@pytest.mark.parametrize("filename", ["resume.PDF", "cv.DOCX", "cv.TXT", "Resume.Pdf"])
def test_allowed_extensions_case_insensitive(v, filename):
    ok, err = v.validate(filename, 1024)
    assert ok is True
    assert err is None


# ---------------------------------------------------------------------------
# Rejected extensions
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("filename", [
    "malware.exe",
    "photo.jpg",
    "scan.png",
    "data.csv",
    "archive.gz",
    "script.py",
    "spreadsheet.xlsx",
])
def test_rejected_extensions_fail(v, filename):
    ok, err = v.validate(filename, 1024)
    assert ok is False
    assert err is not None


def test_rejected_no_extension(v):
    ok, err = v.validate("resume", 1024)
    assert ok is False
    assert err is not None


def test_rejected_extension_in_error_message(v):
    ok, err = v.validate("malware.exe", 1024)
    assert ok is False
    assert ".exe" in err


def test_error_message_lists_allowed_types(v):
    _, err = v.validate("photo.jpg", 1024)
    # Allowed set is DOCX, PDF, TXT — at least one must appear in the message
    assert any(ext in err for ext in ("PDF", "DOCX", "TXT"))


# ---------------------------------------------------------------------------
# File size boundary
# ---------------------------------------------------------------------------

def test_size_exactly_at_limit_passes(v):
    ok, err = v.validate("cv.pdf", MAX_FILE_SIZE_BYTES)
    assert ok is True
    assert err is None


def test_size_one_byte_over_limit_fails(v):
    ok, err = v.validate("cv.pdf", MAX_FILE_SIZE_BYTES + 1)
    assert ok is False
    assert err is not None


def test_size_error_message_contains_mb(v):
    ok, err = v.validate("cv.pdf", MAX_FILE_SIZE_BYTES + 1)
    assert ok is False
    assert "MB" in err


def test_size_zero_passes(v):
    ok, err = v.validate("cv.pdf", 0)
    assert ok is True


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------

def test_dotfile_with_allowed_ext_passes(v):
    # ".pdf" → rsplit(".", 1)[-1] = "pdf" → allowed
    ok, _ = v.validate(".pdf", 1024)
    assert ok is True


def test_dotfile_with_rejected_ext_fails(v):
    ok, _ = v.validate(".exe", 1024)
    assert ok is False


def test_multiple_dots_uses_last_extension(v):
    # "my.resume.pdf" → last ext is "pdf" → allowed
    ok, err = v.validate("my.resume.pdf", 1024)
    assert ok is True
    assert err is None

    # "resume.pdf.exe" → last ext is "exe" → rejected
    ok2, _ = v.validate("resume.pdf.exe", 1024)
    assert ok2 is False
