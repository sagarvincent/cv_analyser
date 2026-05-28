from datetime import date
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel


class QualificationOut(BaseModel):
    type: Literal["degree", "certification", "training"]
    institution_name: str
    degree_name: str | None
    course_name: str | None
    start_date: date
    end_date: date | None
    marks: Decimal | None


class ExperienceOut(BaseModel):
    job_title: str
    company: str
    salary: Decimal | None
    joining_date: date
    leaving_date: date | None


class AspirationOut(BaseModel):
    desired_role: str
    desired_salary: Decimal | None
    active: bool


class ProjectOut(BaseModel):
    name: str
    domain: str
    fun_description: str | None
    techstack_description: str | None
    start_date: date | None
    end_date: date | None
    deployed: bool
    source_type: Literal["qualification", "experience", "portfolio"]


class ProfileResponse(BaseModel):
    username: str
    full_name: str
    email: str
    age: int
    location: str | None
    qualifications: list[QualificationOut]
    experience: list[ExperienceOut]
    aspirations: list[AspirationOut]
    projects: list[ProjectOut]
