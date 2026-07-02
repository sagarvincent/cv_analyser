# Self-contained design-centric taxonomy for the Skill Matrix service.
#
# CATEGORIES — skill category → representative keywords. The joined keyword list
#              doubles as the prototype text embedded for semantic matching.
# BUCKETS    — job-profile bucket → space-separated profile keywords, embedded once
#              and compared (cosine) against the CV to pick the resume's bucket.
#
# These are intentionally a standalone copy (not imported from BES03) so this
# service has no cross-package dependency on the scorer.

CATEGORIES: dict[str, list[str]] = {
    "Leadership & Strategy": [
        "leadership", "strategy", "vision", "director", "manager", "executive",
        "roadmap", "stakeholder", "org", "hiring", "mentoring", "team", "budget",
    ],
    "Design & Craft": [
        "design", "ux", "ui", "figma", "sketch", "prototype", "wireframe",
        "visual", "interaction", "accessibility", "typography", "layout", "brand",
    ],
    "Research & Data": [
        "research", "usability", "testing", "interviews", "data", "analytics",
        "insights", "survey", "qualitative", "quantitative", "metrics", "kpi",
    ],
    "Technical & Engineering": [
        "engineering", "react", "python", "sql", "api", "machine learning",
        "frontend", "backend", "architecture", "cloud", "devops", "algorithms",
    ],
    "Communication & Influence": [
        "communication", "presentation", "writing", "storytelling", "alignment",
        "negotiation", "cross-functional", "collaboration", "workshops", "facilitation",
    ],
}

BUCKETS: dict[str, str] = {
    "Product Designer": "ux ui design figma sketch prototyping wireframes user research visual interaction design system",
    "UX Researcher": "research usability testing interviews surveys insights user behaviour qualitative quantitative synthesis",
    "Design Manager": "leadership team management hiring mentoring design process feedback roadmap strategy stakeholder",
    "Product Manager": "product roadmap strategy stakeholders metrics agile sprint backlog prioritisation user stories",
    "Design Engineer": "design engineering react css design system components tokens frontend accessibility implementation",
    "Design Systems Lead": "design system tokens components documentation governance contribution figma engineering collaboration",
    "UX Director": "director strategy leadership org planning executive vision culture hiring budget design operations",
    "Content Designer": "content writing copy ux writing information architecture voice tone documentation microcopy",
    "Service Designer": "service design journey mapping systems thinking operations research facilitation blueprinting",
    "Creative Director": "creative brand art direction visual storytelling campaigns identity photography print digital",
    "Data Analyst": "sql data analysis python tableau reporting dashboards kpi metrics insights stakeholder communication",
    "Engineering Manager": "engineering management team technical roadmap hiring architecture code review process agile",
}
