from typing import Literal

from pydantic import BaseModel


ExtractionMethod = Literal["digital_pdf", "ocr_pdf", "docx", "text", "failed"]


class ExperienceEntry(BaseModel):
    title: str | None = None
    org: str | None = None
    dates: str | None = None
    description: str = ""


class EducationEntry(BaseModel):
    degree: str | None = None
    institution: str | None = None
    dates: str | None = None


class SkillsBlock(BaseModel):
    text: str = ""
    items: list[str] = []


class Sections(BaseModel):
    summary: str = ""
    experience: list[ExperienceEntry] = []
    education: list[EducationEntry] = []
    skills: SkillsBlock = SkillsBlock()
    projects: str = ""
    certifications: list[str] = []
    other: str = ""


class AtsRedFlags(BaseModel):
    stream_order_anomaly: float
    text_density: float
    encoding_anomaly_rate: float
    extraction_method: ExtractionMethod
    distinct_bullet_chars: int
    line_length_bimodality: float
    hyphenation_break_rate: float
    heading_detection_rate: float
    section_coherence: float
    unclassified_ratio: float


class ParsedCV(BaseModel):
    raw_text: str
    sections: Sections
    extraction_method: ExtractionMethod
    ats_redflags: AtsRedFlags
