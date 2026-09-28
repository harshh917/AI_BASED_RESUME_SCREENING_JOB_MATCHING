from app.services.matching_engine import score_skills
from app.services.skill_extractor import extract_skills, flatten_skills
from app.utils.skills_taxonomy import normalize_skill


def test_exact_skill_match():
    skills = extract_skills("Proficient in Python and PostgreSQL")
    flat = flatten_skills(skills)
    assert "Python" in flat
    assert "PostgreSQL" in flat


def test_normalized_skill_aliases():
    assert normalize_skill("JS") == "JavaScript"
    assert normalize_skill("ReactJS") == "React"
    assert normalize_skill("Postgres") == "PostgreSQL"
    assert normalize_skill("Node") == "Node.js"


def test_missing_skill_detected():
    result = score_skills(
        required_skills=["Java", "Spring Boot", "AWS"],
        preferred_skills=["Docker"],
        candidate_skills=["Java", "Spring Boot"],
    )
    assert "AWS" in result["missing_required_skills"]
    assert "Java" in result["matched_required_skills"]
    assert result["score"] < 100


def test_preferred_skill_bonus():
    base = score_skills(
        required_skills=["Java", "Spring Boot"],
        preferred_skills=["Docker"],
        candidate_skills=["Java", "Spring Boot"],
    )
    with_preferred = score_skills(
        required_skills=["Java", "Spring Boot"],
        preferred_skills=["Docker"],
        candidate_skills=["Java", "Spring Boot", "Docker"],
    )
    assert with_preferred["score"] > base["score"]
    assert "Docker" in with_preferred["matched_preferred_skills"]


def test_full_required_skill_match_scores_high():
    result = score_skills(
        required_skills=["Python", "FastAPI"],
        preferred_skills=[],
        candidate_skills=["Python", "FastAPI", "Docker"],
    )
    assert result["score"] == 90.0  # 100% required ratio * 90, no preferred defined
    assert result["missing_required_skills"] == []
