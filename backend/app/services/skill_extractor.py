"""
Extracts, normalizes, and categorizes skills from free text (resumes or job
descriptions). Uses a curated taxonomy (app/utils/skills_taxonomy.py) rather
than a generic NER model, which keeps results deterministic and inspectable
per the project's engineering rules ("keep scoring logic deterministic").
"""
import re
from typing import Dict, List

from app.utils.skills_taxonomy import ALIASES, category_of, normalize_skill

# Build once: longest aliases first so "spring boot" matches before "spring"
_SORTED_ALIASES = sorted(ALIASES.keys(), key=len, reverse=True)


def _compile_patterns():
    patterns = []
    for alias in _SORTED_ALIASES:
        escaped = re.escape(alias)
        # word-boundary aware, but tolerant of '.', '+', '#' inside skill names
        pattern = re.compile(rf"(?<![A-Za-z0-9]){escaped}(?![A-Za-z0-9])", re.IGNORECASE)
        patterns.append((alias, pattern))
    return patterns


_PATTERNS = _compile_patterns()


def extract_skills(text: str) -> Dict[str, List[str]]:
    """
    Scan `text` for known skills and return them bucketed by category, e.g.:
    {"programming_languages": ["Python"], "frameworks": ["FastAPI"], ...}
    Each list contains de-duplicated canonical skill names.
    """
    if not text:
        return _empty_buckets()

    found_canonical = set()
    for alias, pattern in _PATTERNS:
        if pattern.search(text):
            found_canonical.add(normalize_skill(alias))

    buckets = _empty_buckets()
    for skill in sorted(found_canonical):
        buckets[category_of(skill)].append(skill)
    return buckets


def flatten_skills(skill_buckets: Dict[str, List[str]]) -> List[str]:
    flat: List[str] = []
    for values in skill_buckets.values():
        flat.extend(values)
    return sorted(set(flat))


def _empty_buckets() -> Dict[str, List[str]]:
    return {
        "programming_languages": [],
        "frameworks": [],
        "databases": [],
        "cloud": [],
        "tools": [],
        "other": [],
    }
