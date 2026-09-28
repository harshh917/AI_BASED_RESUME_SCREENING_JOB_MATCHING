"""
Parses a free-text job description into a structured requirements object,
distinguishing "required" vs "preferred" skills and pulling out a minimum
experience range. Same rule-based philosophy as resume_parser: deterministic
and inspectable rather than an opaque model call.
"""
import re
from typing import Any, Dict, Optional

from app.services.skill_extractor import extract_skills, flatten_skills

REQUIRED_MARKERS = re.compile(
    r"(required skills|requirements|must have|mandatory skills)[:\-]?", re.IGNORECASE
)
PREFERRED_MARKERS = re.compile(
    r"(preferred skills|nice to have|good to have|bonus|preferred qualifications)[:\-]?", re.IGNORECASE
)
EXPERIENCE_RE = re.compile(
    r"(\d+)\s*(?:\+|\-)?\s*(?:to|-)?\s*(\d+)?\s*years?", re.IGNORECASE
)


def _split_sections(text: str):
    """Split JD text into (required_block, preferred_block, rest) using
    marker keywords. If no markers are found, the whole text is treated as
    the required block (safer default: nothing is silently dropped)."""
    req_match = REQUIRED_MARKERS.search(text)
    pref_match = PREFERRED_MARKERS.search(text)

    if not req_match and not pref_match:
        return text, ""

    if req_match and pref_match:
        if req_match.start() < pref_match.start():
            return text[req_match.end():pref_match.start()], text[pref_match.end():]
        return text[req_match.end():], text[pref_match.end():req_match.start()]

    if req_match:
        return text[req_match.end():], ""

    return text, text[pref_match.end():]


def extract_experience_range(text: str) -> Dict[str, Optional[int]]:
    match = EXPERIENCE_RE.search(text)
    if not match:
        return {"min_years": None, "max_years": None}
    min_years = int(match.group(1))
    max_years = int(match.group(2)) if match.group(2) else None
    return {"min_years": min_years, "max_years": max_years}


def extract_education_requirement(text: str) -> Optional[str]:
    degree_keywords = ["bachelor", "master", "b.tech", "m.tech", "b.e", "m.e", "bsc", "msc", "phd", "mba"]
    lowered = text.lower()
    for kw in degree_keywords:
        if kw in lowered:
            idx = lowered.find(kw)
            return text[max(0, idx - 10): idx + 40].strip()
    return None


def extract_job_title(text: str) -> Optional[str]:
    first_line = text.strip().split("\n")[0].strip()
    return first_line[:120] if first_line else None


def parse_job_description(text: str) -> Dict[str, Any]:
    if not text or not text.strip():
        raise ValueError("Job description text is empty")

    required_block, preferred_block = _split_sections(text)

    required_skills = flatten_skills(extract_skills(required_block))
    preferred_skills = flatten_skills(extract_skills(preferred_block)) if preferred_block else []
    # A skill mentioned in both blocks is required (stricter category wins)
    preferred_skills = [s for s in preferred_skills if s not in required_skills]

    return {
        "job_title": extract_job_title(text),
        "required_skills": required_skills,
        "preferred_skills": preferred_skills,
        "experience": extract_experience_range(text),
        "education_requirement": extract_education_requirement(text),
        "domain": None,  # left for future ML classification, not fabricated
    }
