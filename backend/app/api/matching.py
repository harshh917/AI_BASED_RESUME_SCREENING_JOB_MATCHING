from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import require_role
from app.db.database import get_db
from app.db.models.job import Job
from app.db.models.match_result import MatchResult
from app.db.models.resume import Resume
from app.db.models.user import User, UserRole
from app.schemas.match import MatchResultOut, RankedCandidate
from app.services.explanation_service import build_explanation
from app.services.matching_engine import run_matching

router = APIRouter(prefix="/api/matching", tags=["matching"])


def _run_and_store(job: Job, resume: Resume, db: Session) -> MatchResult:
    if not resume.profile:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Resume has no parsed candidate profile yet",
        )

    candidate_profile = {
        "skills": resume.profile.skills,
        "education": resume.profile.education,
        "experience": resume.profile.experience,
        "projects": resume.profile.projects,
        "certifications": resume.profile.certifications,
    }

    result = run_matching(
        job_requirements=job.parsed_requirements or {},
        candidate_profile=candidate_profile,
        resume_embedding=resume.embedding,
        job_embedding=job.embedding,
    )
    explanation = build_explanation(result, job_title=job.title)

    existing = (
        db.query(MatchResult)
        .filter(MatchResult.resume_id == resume.id, MatchResult.job_id == job.id)
        .first()
    )
    match = existing or MatchResult(resume_id=resume.id, job_id=job.id)
    match.overall_score = result["overall_score"]
    match.semantic_score = result["semantic_score"]
    match.skill_score = result["skill_score"]
    match.experience_score = result["experience_score"]
    match.education_score = result["education_score"]
    match.project_score = result["project_score"]
    match.certification_score = result["certification_score"]
    match.matched_skills = result["matched_skills"]
    match.missing_skills = result["missing_skills"]
    match.explanation = explanation

    if not existing:
        db.add(match)
    db.commit()
    db.refresh(match)
    return match


@router.post("/{job_id}/{resume_id}", response_model=MatchResultOut)
def match_single(
    job_id: str,
    resume_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.recruiter, UserRole.admin)),
):
    job = db.get(Job, job_id)
    resume = db.get(Resume, resume_id)
    if not job or not resume:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job or resume not found")
    if job.recruiter_id != current_user.id and current_user.role != UserRole.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized for this job")
    return _run_and_store(job, resume, db)


@router.post("/job/{job_id}/run", response_model=list[MatchResultOut])
def run_matching_for_job(
    job_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.recruiter, UserRole.admin)),
):
    job = db.get(Job, job_id)
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")
    if job.recruiter_id != current_user.id and current_user.role != UserRole.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized for this job")

    resumes = db.query(Resume).join(User, Resume.user_id == User.id).filter(User.role == UserRole.candidate).all()
    results = []
    for resume in resumes:
        if not resume.profile:
            continue
        results.append(_run_and_store(job, resume, db))
    return results


@router.get("/{job_id}/results", response_model=list[RankedCandidate])
def get_ranked_results(
    job_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.recruiter, UserRole.admin)),
):
    job = db.get(Job, job_id)
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")
    if job.recruiter_id != current_user.id and current_user.role != UserRole.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized for this job")

    matches = (
        db.query(MatchResult)
        .filter(MatchResult.job_id == job_id)
        .order_by(MatchResult.overall_score.desc())
        .all()
    )
    ranked = []
    for idx, match in enumerate(matches, start=1):
        resume = db.get(Resume, match.resume_id)
        candidate_name = "Candidate"
        if resume and resume.parsed_data:
            candidate_name = (resume.parsed_data.get("contact") or {}).get("name") or resume.file_name
        ranked.append(
            RankedCandidate(
                rank=idx,
                resume_id=match.resume_id,
                candidate_name=candidate_name,
                overall_score=match.overall_score,
                skill_score=match.skill_score,
                experience_score=match.experience_score,
                missing_skills=match.missing_skills or [],
                match_id=match.id,
            )
        )
    return ranked


@router.get("/{job_id}/{resume_id}", response_model=MatchResultOut)
def get_match_detail(
    job_id: str,
    resume_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.recruiter, UserRole.admin)),
):
    job = db.get(Job, job_id)
    if job and job.recruiter_id != current_user.id and current_user.role != UserRole.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized for this job")
    match = (
        db.query(MatchResult)
        .filter(MatchResult.job_id == job_id, MatchResult.resume_id == resume_id)
        .first()
    )
    if not match:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Match result not found. Run matching first.")
    return match
