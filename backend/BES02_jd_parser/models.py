from pydantic import BaseModel


class SalaryRange(BaseModel):
    min: float | None
    max: float | None
    currency: str | None
    raw: str


class JDSections(BaseModel):
    overview: str
    responsibilities: str
    requirements: str
    preferred: str
    skills: str
    about_company: str
    benefits: str
    other: str


class ParsedJD(BaseModel):
    # Header fields (pre-section metadata)
    title: str | None
    company: str | None
    location: str | None
    employment_type: str | None
    seniority: str | None

    salary_range: SalaryRange | None

    # Raw section text
    sections: JDSections

    # Structured bullet lists derived from sections
    responsibilities: list[str]
    required_qualifications: list[str]
    preferred_qualifications: list[str]
    required_skills: list[str]
    benefits: list[str]

    # Meta
    raw_text: str
    parse_warnings: list[str]
    parser_version: str
