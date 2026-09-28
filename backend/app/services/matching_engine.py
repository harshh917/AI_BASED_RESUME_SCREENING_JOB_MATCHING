"""
Core scoring engine. Combines multiple independent signals into one
explainable, weighted overall score (0-100). Weights come from
Settings.scoring_weights so they are configurable (not hardcoded) and are
NOT presented as scientifically optimal — they are a reasonable starting
point per the assignment brief.

    overall = 40% skill + 25% semantic + 15% experience
              + 10% project + 5% education + 5% certification

Every sub-score function is pure (no I/O, no randomness) so the whole
engine is unit-testable and its output reproducible for a given input,
per the "keep scoring logic deterministic and inspectable" rule.
"""
import re
from typing import Any, Dict, List, Optional

from app.core.config import settings
from app.services.embedding_service import cosine_similarity

_DURATION_YEAR_RE = re.compile(r"(19|20)\d{2}")


def score_skills(
    required_skills: List[str], preferred_skills: List[str], candidate_skills: List[str]
) -> Dict[str, Any]:
    candidate_set = {s.lower() for s in candidate_skills}
    required_set = {s.lower(): s for s in required_skills}
    preferred_set = {s.lower(): s for s in preferred_skills}

    matched_required = [orig for low, orig in required_set.items() if low in candidate_set]
    missing_required = [orig for low, orig in required_set.items() if low not in candidate_set]
    matched_preferred = [orig for low, orig in preferred_set.items() if low in candidate_set]

    if not required_set:
        required_ratio = 1.0 if candidate_set else 0.0
    else:
        required_ratio = len(matched_required) / len(required_set)

    preferred_ratio = (len(matched_preferred) / len(preferred_set)) if preferred_set else 0.0

    # Required skills dominate; preferred skills can add up to +10 bonus points.
    score = (required_ratio * 90) + (preferred_ratio * 10)
    score = min(100.0, score)

    return {
        "score": round(score, 2),
        "matched_required_skills": sorted(matched_required),
        "missing_required_skills": sorted(missing_required),
        "matched_preferred_skills": sorted(matched_preferred),
    }


def score_semantic(resume_embedding: Optional[List[float]], job_embedding: Optional[List[float]]) -> float:
    if not resume_embedding or not job_embedding:
        return 0.0
    return round(cosine_similarity(resume_embedding, job_embedding) * 100, 2)


def _estimate_candidate_years(experience: List[Dict[str, Any]]) -> float:
    """Best-effort total years of experience from free-text 'duration'
    fields. Returns 0.0 (not an assumption of missing = many years) when it
    cannot confidently parse anything."""
    total_years = 0.0
    for entry in experience or []:
        duration = (entry or {}).get("duration") or ""
        matches = re.findall(r"((?:19|20)\d{2})", duration)
        if len(matches) >= 2:
            start_year, end_year = int(matches[0]), int(matches[1])
            total_years += max(0.0, end_year - start_year)
        elif len(matches) == 1 and re.search(r"present|current", duration, re.IGNORECASE):
            # started in matches[0], ongoing — count conservatively as 1 year minimum
            total_years += 1.0
    return total_years


def score_experience(job_experience_requirement: Dict[str, Any], candidate_experience: List[Dict[str, Any]]) -> Dict[str, Any]:
    min_years = (job_experience_requirement or {}).get("min_years")
    candidate_years = _estimate_candidate_years(candidate_experience)

    if min_years is None:
        # Nothing to compare against — score based on presence of any relevant experience.
        score = 70.0 if candidate_experience else 30.0
    elif min_years == 0:
        score = 100.0
    elif candidate_years >= min_years:
        score = 100.0
    else:
        score = max(0.0, (candidate_years / min_years) * 100)

    return {"score": round(score, 2), "estimated_candidate_years": round(candidate_years, 1)}


def score_education(education_requirement: Optional[str], candidate_education: List[Dict[str, Any]]) -> float:
    if not education_requirement:
        return 70.0 if candidate_education else 40.0
    if not candidate_education:
        return 0.0

    req_lower = education_requirement.lower()
    for entry in candidate_education:
        degree = (entry.get("degree") or "").lower()
        if any(tok in degree for tok in ["b.tech", "be", "bachelor", "b.e", "bsc"]) and any(
            tok in req_lower for tok in ["b.tech", "bachelor", "b.e", "bsc"]
        ):
            return 100.0
        if any(tok in degree for tok in ["m.tech", "master", "m.e", "msc", "mba"]) and any(
            tok in req_lower for tok in ["m.tech", "master", "m.e", "msc", "mba"]
        ):
            return 100.0
    return 50.0  # candidate has *some* education info, just not a confirmed match


def score_projects(required_skills: List[str], preferred_skills: List[str], projects: List[Dict[str, Any]]) -> float:
    relevant_skills = {s.lower() for s in (required_skills + preferred_skills)}
    if not relevant_skills:
        return 50.0 if projects else 0.0
    if not projects:
        return 0.0

    project_skills = set()
    for project in projects:
        for tech in project.get("technologies", []) or []:
            project_skills.add(tech.lower())

    overlap = relevant_skills & project_skills
    ratio = len(overlap) / len(relevant_skills)
    return round(min(100.0, ratio * 100), 2)


def score_certifications(certifications: List[str]) -> float:
    if not certifications:
        return 0.0
    return min(100.0, len(certifications) * 25.0)


def compute_overall_score(sub_scores: Dict[str, float]) -> float:
    weights = settings.scoring_weights
    overall = (
        sub_scores["skill"] * weights["skill"]
        + sub_scores["semantic"] * weights["semantic"]
        + sub_scores["experience"] * weights["experience"]
        + sub_scores["project"] * weights["project"]
        + sub_scores["education"] * weights["education"]
        + sub_scores["certification"] * weights["certification"]
    )
    return round(overall, 2)


def run_matching(
    job_requirements: Dict[str, Any],
    candidate_profile: Dict[str, Any],
    resume_embedding: Optional[List[float]],
    job_embedding: Optional[List[float]],
) -> Dict[str, Any]:
    """Full scoring pass for one (resume, job) pair. Returns everything
    needed to persist a MatchResult row and render the explanation."""
    required_skills = job_requirements.get("required_skills", [])
    preferred_skills = job_requirements.get("preferred_skills", [])

    from app.services.skill_extractor import flatten_skills

    candidate_skill_buckets = candidate_profile.get("skills") or {}
    candidate_skills = flatten_skills(candidate_skill_buckets) if isinstance(candidate_skill_buckets, dict) else []

    skill_result = score_skills(required_skills, preferred_skills, candidate_skills)
    semantic_score = score_semantic(resume_embedding, job_embedding)
    experience_result = score_experience(job_requirements.get("experience", {}), candidate_profile.get("experience", []))
    education_score = score_education(job_requirements.get("education_requirement"), candidate_profile.get("education", []))
    project_score = score_projects(required_skills, preferred_skills, candidate_profile.get("projects", []))
    certification_score = score_certifications(candidate_profile.get("certifications", []))

    sub_scores = {
        "skill": skill_result["score"],
        "semantic": semantic_score,
        "experience": experience_result["score"],
        "project": project_score,
        "education": education_score,
        "certification": certification_score,
    }
    overall_score = compute_overall_score(sub_scores)

    return {
        "overall_score": overall_score,
        "skill_score": skill_result["score"],
        "semantic_score": semantic_score,
        "experience_score": experience_result["score"],
        "education_score": education_score,
        "project_score": project_score,
        "certification_score": certification_score,
        "matched_skills": skill_result["matched_required_skills"] + skill_result["matched_preferred_skills"],
        "missing_skills": skill_result["missing_required_skills"],
        "matched_preferred_skills": skill_result["matched_preferred_skills"],
        "estimated_candidate_years": experience_result["estimated_candidate_years"],
    }
