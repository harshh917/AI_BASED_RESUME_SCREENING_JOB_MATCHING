from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.api.deps import require_role
from app.api.matching import _run_and_store
from app.db.database import get_db
from app.db.models.application import Application, ApplicationStatus
from app.db.models.job import Job
from app.db.models.resume import Resume
from app.db.models.user import User, UserRole
from app.schemas.application import ApplicationCreate, ApplicationOut, ApplicationStatusUpdate

router = APIRouter(prefix="/api/applications", tags=["applications"])


def _out(app: Application) -> ApplicationOut:
    return ApplicationOut(
        id=app.id,
        job_id=app.job_id,
        candidate_id=app.candidate_id,
        resume_id=app.resume_id,
        cover_note=app.cover_note,
        status=app.status,
        match_score=app.match_score,
        applied_at=app.applied_at,
        job_title=app.job.title,
        candidate_name=app.candidate.name,
        candidate_email=app.candidate.email,
        resume_file_name=app.resume.file_name,
    )


@router.post("/jobs/{job_id}", response_model=ApplicationOut, status_code=status.HTTP_201_CREATED)
def apply_to_job(
    job_id: str,
    payload: ApplicationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.candidate, UserRole.admin)),
):
    job = db.get(Job, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    if job.status != "active":
        raise HTTPException(status_code=400, detail="Applications are closed for this job")

    resume = db.get(Resume, payload.resume_id)
    if not resume or resume.user_id != current_user.id:
        raise HTTPException(status_code=400, detail="Please select one of your resumes")
    if not resume.profile:
        raise HTTPException(status_code=400, detail="This resume is not parsed yet. Upload or re-upload a valid resume.")

    existing = (
        db.query(Application)
        .filter(Application.job_id == job_id, Application.candidate_id == current_user.id)
        .first()
    )
    if existing:
        raise HTTPException(status_code=409, detail="You have already applied to this job")

    match = _run_and_store(job, resume, db)
    application = Application(
        job_id=job.id,
        candidate_id=current_user.id,
        resume_id=resume.id,
        cover_note=payload.cover_note,
        status=ApplicationStatus.applied,
        match_score=match.overall_score,
    )
    db.add(application)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="You have already applied to this job")
    db.refresh(application)
    return _out(application)


@router.get("/mine", response_model=list[ApplicationOut])
def my_applications(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.candidate, UserRole.admin)),
):
    rows = (
        db.query(Application)
        .filter(Application.candidate_id == current_user.id)
        .order_by(Application.applied_at.desc())
        .all()
    )
    return [_out(row) for row in rows]


@router.get("/jobs/{job_id}", response_model=list[ApplicationOut])
def job_applications(
    job_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.recruiter, UserRole.admin)),
):
    job = db.get(Job, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    if job.recruiter_id != current_user.id and current_user.role != UserRole.admin:
        raise HTTPException(status_code=403, detail="Not authorized for this job")

    rows = (
        db.query(Application)
        .filter(Application.job_id == job_id)
        .order_by(Application.match_score.desc().nullslast(), Application.applied_at.desc())
        .all()
    )
    return [_out(row) for row in rows]


@router.patch("/{application_id}/status", response_model=ApplicationOut)
def update_application_status(
    application_id: str,
    payload: ApplicationStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.recruiter, UserRole.admin)),
):
    application = db.get(Application, application_id)
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    if application.job.recruiter_id != current_user.id and current_user.role != UserRole.admin:
        raise HTTPException(status_code=403, detail="Not authorized for this application")

    application.status = payload.status
    db.commit()
    db.refresh(application)
    return _out(application)
