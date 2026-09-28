from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import require_role
from app.db.database import get_db
from app.db.models.job import Job
from app.db.models.resume import Resume
from app.db.models.user import User, UserRole
from app.schemas.recommendation import JobRecommendation
from app.services.matching_engine import run_matching

router = APIRouter(prefix="/api/recommendations", tags=["recommendations"])

@router.get("/jobs", response_model=list[JobRecommendation])
def recommended_jobs(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.candidate, UserRole.admin)),
):
    resumes = db.query(Resume).filter(Resume.user_id == current_user.id).all()
    jobs = db.query(Job).filter(Job.status == "active").order_by(Job.created_at.desc()).all()
    recommendations = []
    for job in jobs:
        best = None
        for resume in resumes:
            if not resume.profile:
                continue
            profile = {
                "skills": resume.profile.skills,
                "education": resume.profile.education,
                "experience": resume.profile.experience,
                "projects": resume.profile.projects,
                "certifications": resume.profile.certifications,
            }
            result = run_matching(job.parsed_requirements or {}, profile, resume.embedding, job.embedding)
            if best is None or result["overall_score"] > best["overall_score"]:
                best = result
        if best is not None:
            recommendations.append(JobRecommendation(
                job_id=job.id,
                title=job.title,
                status=job.status,
                overall_score=best["overall_score"],
                skill_score=best["skill_score"],
                semantic_score=best["semantic_score"],
                matched_skills=best.get("matched_skills", []),
                missing_skills=best.get("missing_skills", []),
            ))
    return sorted(recommendations, key=lambda x: x.overall_score, reverse=True)
