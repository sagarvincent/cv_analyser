"""
Fixture tests for the segmentation/cleaning fixes driven by the
ENGINEERING.jsonl parsing-inefficiency report.

Fixture #1 mirrors the dominant real-world resume layout from the dataset:
top-of-CV job-title banner, fuzzy section headers ("Professional Profile",
"Education and Training"), title+date on the same line, education years
inline, and mojibake artifacts. Every triage-discovered failure pattern
should be added here as a new fixture.
"""

import pytest

from BES01_cv_parser.parser import parse_cv

# ---------------------------------------------------------------------------
# Fixture #1 — real-world layout (title + date inline, fuzzy headers, banner)
# ---------------------------------------------------------------------------

_FIXTURE_1 = """
ENGINEERING MANAGER
Professional Profile
Dedicated engineer with excellent technical and communication skills
demonstrated by 9 years of experience.

Experience
Engineering Manager 05/2014 to Current
Company Name - City , State
Responsible for designing robotic systems and running simulations.
Supervised a team of twelve engineers.

Senior Engineer 03/2010 to 04/2014
Other Company - City , State
Designed mechanical assemblies and managed vendor relationships.

Engineering Technician
First Company Inc
01/2006 to 02/2010
Maintained production equipment and improved line throughput.

Engineering Intern 06/2005 to 12/2005
Intern Corp - City , State
Assisted senior staff with CAD drawings.

Education and Training
M.S : Mechanical Engineering , 2009 State University - City , State
B.S : Mechanical Engineering , 2005 Tech College - City , State

Skill Highlights
Python, AutoCAD, SolidWorks · MATLAB
Proficient in the use of advanced thermal simulation suites across teams
Lean Manufacturing, Six Sigma
""".strip()

# mojibake variant: replacement char + zero-width space injected, as seen
# in 61/118 of the ENGINEERING set
_FIXTURE_1_MOJIBAKE = _FIXTURE_1.replace(
    "Company Name - City , State", "Company Name �​ City , State"
)


@pytest.fixture(scope="module")
def parsed():
    return parse_cv(_FIXTURE_1.encode(), "resume.txt")


# ---------------------------------------------------------------------------
# 1. date-anchored experience splitting
# ---------------------------------------------------------------------------

def test_four_experience_entries(parsed):
    assert len(parsed.sections.experience) == 4


def test_titles_have_dates_stripped(parsed):
    titles = [e.title for e in parsed.sections.experience]
    assert titles[0] == "Engineering Manager"
    assert titles[1] == "Senior Engineer"
    assert titles[2] == "Engineering Technician"
    assert titles[3] == "Engineering Intern"


def test_orgs_populated(parsed):
    orgs = [e.org for e in parsed.sections.experience]
    assert orgs[0] == "Company Name - City , State"
    assert orgs[2] == "First Company Inc"


def test_entry_dates_populated(parsed):
    dates = [e.dates for e in parsed.sections.experience]
    assert dates[0] == "05/2014 to Current"
    assert dates[2] == "01/2006 to 02/2010"


def test_no_boundary_failures(parsed):
    assert parsed.ats_redflags.experience_boundary_failures == 0


# ---------------------------------------------------------------------------
# 2. fuzzy header recovery + strict redflags pinned
# ---------------------------------------------------------------------------

def test_fuzzy_headers_route_sections(parsed):
    # "Professional Profile" → summary, "Education and Training" → education,
    # "Skill Highlights" → skills: none are strict aliases
    assert "Dedicated engineer" in parsed.sections.summary
    assert len(parsed.sections.education) == 2
    assert parsed.sections.skills.text != ""


def test_sections_recovered_by_fuzzy_only(parsed):
    # summary, education, skills recovered only via fuzzy aliases
    assert parsed.ats_redflags.sections_recovered_by_fuzzy_only == 3


def test_heading_detection_rate_stays_strict(parsed):
    # strict pass finds only: experience + other → 2/7. The fuzzy
    # improvements must never move this ATS signal.
    assert parsed.ats_redflags.heading_detection_rate == pytest.approx(2 / 7)


# ---------------------------------------------------------------------------
# 3. headline banner routed deliberately
# ---------------------------------------------------------------------------

def test_headline_captured(parsed):
    assert parsed.sections.headline == "ENGINEERING MANAGER"


def test_headline_not_in_other(parsed):
    assert "ENGINEERING MANAGER" not in parsed.sections.other


# ---------------------------------------------------------------------------
# 4. education years parsed inline
# ---------------------------------------------------------------------------

def test_education_dates_populated(parsed):
    assert parsed.sections.education[0].dates == "2009"
    assert parsed.sections.education[1].dates == "2005"


def test_education_degree_has_year_stripped(parsed):
    assert "2009" not in parsed.sections.education[0].degree
    assert "Mechanical Engineering" in parsed.sections.education[0].degree


# ---------------------------------------------------------------------------
# 5. mojibake cleanup
# ---------------------------------------------------------------------------

def test_mojibake_removed_from_raw_text():
    result = parse_cv(_FIXTURE_1_MOJIBAKE.encode(), "resume.txt")
    assert "�" not in result.raw_text
    assert "​" not in result.raw_text


def test_mojibake_removed_from_org_field():
    result = parse_cv(_FIXTURE_1_MOJIBAKE.encode(), "resume.txt")
    org = result.sections.experience[0].org or ""
    assert "�" not in org and "​" not in org


# ---------------------------------------------------------------------------
# 6. skills noise filters
# ---------------------------------------------------------------------------

def test_skills_sentences_dropped(parsed):
    # the 10-word "Proficient in ..." line is a sentence, not a skill
    assert all(len(item.split()) <= 4 for item in parsed.sections.skills.items)


def test_skills_clean_items_kept(parsed):
    items = parsed.sections.skills.items
    assert "Python" in items
    assert "MATLAB" in items
    assert "Lean Manufacturing" in items


def test_skills_no_bullet_residue(parsed):
    assert all("·" not in item and "•" not in item for item in parsed.sections.skills.items)
