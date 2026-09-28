from app.services.embedding_service import generate_embedding
from app.services.jd_parser import parse_job_description
from app.services.matching_engine import run_matching

JOB_DESCRIPTION = """Backend Developer

Required Skills:
Java, Spring Boot, REST API, PostgreSQL

Preferred Skills:
Docker, AWS

Minimum 2 years of experience required.
Bachelor's degree in Computer Science or related field.
"""

STRONG_CANDIDATE_PROFILE = {
    "skills": {
        "programming_languages": ["Java"],
        "frameworks": ["Spring Boot"],
        "databases": ["PostgreSQL"],
        "cloud": [],
        "tools": ["Docker"],
        "other": ["REST API"],
    },
    "education": [{"degree": "B.Tech Computer Science", "institution": "XYZ University", "graduation_year": "2020"}],
    "experience": [{"company": "TechCorp", "role": "Backend Developer", "duration": "2021 - 2024", "responsibilities": [], "technologies": ["Java", "Spring Boot"]}],
    "projects": [{"name": "Payment API", "description": "Spring Boot payment service", "technologies": ["Java", "Spring Boot", "PostgreSQL"]}],
    "certifications": ["AWS Certified Developer"],
}

WEAK_CANDIDATE_PROFILE = {
    "skills": {
        "programming_languages": ["Python"],
        "frameworks": ["Django"],
        "databases": ["MySQL"],
        "cloud": [],
        "tools": [],
        "other": [],
    },
    "education": [],
    "experience": [],
    "projects": [],
    "certifications": [],
}


def _match(profile):
    job_requirements = parse_job_description(JOB_DESCRIPTION)
    resume_text = " ".join(
        [s for cat in profile["skills"].values() for s in cat]
        + [p.get("description", "") or "" for p in profile["projects"]]
    )
    resume_embedding = generate_embedding(resume_text)
    job_embedding = generate_embedding(JOB_DESCRIPTION)
    return run_matching(job_requirements, profile, resume_embedding, job_embedding)


def test_jd_parser_extracts_required_and_preferred_skills():
    parsed = parse_job_description(JOB_DESCRIPTION)
    assert "Java" in parsed["required_skills"]
    assert "Spring Boot" in parsed["required_skills"]
    assert "AWS" in parsed["preferred_skills"] or "AWS" in parsed["required_skills"]
    assert parsed["experience"]["min_years"] == 2


def test_strong_candidate_scores_higher_than_weak_candidate():
    strong_result = _match(STRONG_CANDIDATE_PROFILE)
    weak_result = _match(WEAK_CANDIDATE_PROFILE)

    assert strong_result["overall_score"] > weak_result["overall_score"]
    assert strong_result["overall_score"] > 60
    assert weak_result["overall_score"] < 40


def test_strong_candidate_has_no_missing_required_skills():
    result = _match(STRONG_CANDIDATE_PROFILE)
    assert result["missing_skills"] == []


def test_weak_candidate_missing_all_required_skills():
    result = _match(WEAK_CANDIDATE_PROFILE)
    assert set(result["missing_skills"]) == {"Java", "PostgreSQL", "REST API", "Spring Boot"}


def test_scores_are_normalized_between_0_and_100():
    for profile in (STRONG_CANDIDATE_PROFILE, WEAK_CANDIDATE_PROFILE):
        result = _match(profile)
        for key in ("overall_score", "skill_score", "semantic_score", "experience_score", "education_score", "project_score", "certification_score"):
            assert 0 <= result[key] <= 100
