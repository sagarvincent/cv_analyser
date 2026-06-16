from BES02_jd_parser.leaves.segmentation_leaves import (
    JD_SECTION_ALIASES,
    group_lines_by_heading,
    split_bullets,
)
from BES02_jd_parser.models import JDSections


# -------------------- segment ----------- START ----------
# -- Calls : group_lines_by_heading
# -- Called by: parser.parse_jd
def segment(lines: list[str]) -> JDSections:
    """Bucket cleaned lines into JD sections using heading detection."""
    buckets = group_lines_by_heading(lines, JD_SECTION_ALIASES)
    return JDSections(
        overview=buckets.get("overview", ""),
        responsibilities=buckets.get("responsibilities", ""),
        requirements=buckets.get("requirements", ""),
        preferred=buckets.get("preferred", ""),
        skills=buckets.get("skills", ""),
        about_company=buckets.get("about_company", ""),
        benefits=buckets.get("benefits", ""),
        other=buckets.get("other", ""),
    )
# -------------------- segment ------------- END ----------------


# -------------------- build_bullets ----------- START ----------
# -- Calls : split_bullets
# -- Called by: parser.parse_jd
def build_bullets(sections: JDSections) -> dict[str, list[str]]:
    """Convert raw section text into structured bullet lists."""
    responsibilities = split_bullets(sections.responsibilities)

    # requirements + skills are both potential sources for required_qualifications
    # and required_skills. If a dedicated skills section exists, keep it separate;
    # otherwise fold skills text into required_qualifications.
    required_qualifications = split_bullets(sections.requirements)
    if sections.skills:
        required_skills = split_bullets(sections.skills)
    else:
        required_skills = []

    preferred_qualifications = split_bullets(sections.preferred)
    benefits = split_bullets(sections.benefits)

    return {
        "responsibilities": responsibilities,
        "required_qualifications": required_qualifications,
        "preferred_qualifications": preferred_qualifications,
        "required_skills": required_skills,
        "benefits": benefits,
    }
# -------------------- build_bullets ------------- END ----------------


# -------------------- collect_warnings ----------- START ----------
# -- Calls : nothing
# -- Called by: parser.parse_jd
def collect_warnings(sections: JDSections, bullets: dict[str, list[str]]) -> list[str]:
    """Return a list of human-readable parse warnings for missing/thin sections."""
    warnings = []
    if not bullets["responsibilities"]:
        warnings.append("no responsibilities section found")
    if not bullets["required_qualifications"]:
        warnings.append("no requirements section found")
    if not bullets["preferred_qualifications"]:
        warnings.append("no preferred qualifications section found")
    if not sections.overview and not sections.about_company:
        warnings.append("no overview or about-company section found")
    return warnings
# -------------------- collect_warnings ------------- END ----------------
