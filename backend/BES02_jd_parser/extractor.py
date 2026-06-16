import re

from BES01_cv_parser.extractors import extract_docx, extract_pdf
from BES02_jd_parser.leaves.extraction_leaves import (
    extract_company,
    extract_employment_type,
    extract_location,
    extract_salary,
    flatten_csv,
    flatten_json,
    infer_seniority,
)
from BES02_jd_parser.leaves.segmentation_leaves import (
    JD_SECTION_ALIASES,
    first_heading_index,
)
from BES02_jd_parser.models import SalaryRange

# An explicit "Title: ..." label, common in scraped single-line JDs.
_TITLE_LINE_RE = re.compile(r"(?im)^\s*title\s*:\s*(.+)$")
_MAX_TITLE_LEN = 120


# -------------------- dispatch_file ----------- START ----------
# -- Calls : extract_pdf, extract_docx, flatten_json, flatten_csv
# -- Called by: interface.parse_jd_endpoint
def dispatch_file(file_bytes: bytes, filename: str) -> str:
    """Extract plain text from an uploaded JD file.

    Supported: PDF, DOC, DOCX, JSON, CSV.
    Returns an empty string on unsupported format (caller emits a warning)."""
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    if ext == "pdf":
        return extract_pdf(file_bytes).text
    if ext in ("doc", "docx"):
        return extract_docx(file_bytes).text
    if ext == "json":
        return flatten_json(file_bytes)
    if ext == "csv":
        return flatten_csv(file_bytes)
    return ""
# -------------------- dispatch_file ------------- END ----------------


# -------------------- extract_header ----------- START ----------
# -- Calls : first_heading_index, extract_company, extract_location,
#            extract_employment_type, extract_salary, infer_seniority
# -- Called by: parser.parse_jd
def extract_header(
    lines: list[str],
    full_text: str,
) -> dict:
    """Extract pre-section metadata: title, company, location, employment_type,
    seniority, salary_range.

    Operates on the header block — lines before the first detected section
    heading. Salary is searched across the full text because it can appear
    anywhere (benefits section, header, footer)."""
    boundary = first_heading_index(lines, JD_SECTION_ALIASES)
    header_lines = [ln for ln in lines[:boundary] if ln.strip()]

    # Prefer an explicit "Title:" label; else the first short header line.
    # A blob-like first line (newline-sparse JD) is rejected rather than used
    # as the title.
    title: str | None = None
    explicit = _TITLE_LINE_RE.search(full_text)
    if explicit:
        title = explicit.group(1).strip()
    else:
        for line in header_lines:
            stripped = line.strip()
            if stripped and len(stripped) <= _MAX_TITLE_LEN:
                title = stripped
                break

    company = extract_company(header_lines)
    location = extract_location(header_lines)
    employment_type = extract_employment_type(header_lines)
    seniority = infer_seniority(title) if title else None

    salary_dict = extract_salary(full_text)
    salary_range: SalaryRange | None = SalaryRange(**salary_dict) if salary_dict else None

    return {
        "title": title,
        "company": company,
        "location": location,
        "employment_type": employment_type,
        "seniority": seniority,
        "salary_range": salary_range,
    }
# -------------------- extract_header ------------- END ----------------
