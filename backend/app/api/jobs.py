from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.api.deps import require_role
from app.db.database import get_db
from app.db.models.job import Job
from app.db.models.application import Application, ApplicationStatus
from app.db.models.user import User, UserRole
from app.schemas.job import JobCreate, JobOut, JobUpdate
from app.services.embedding_service import generate_embedding
from app.services.jd_parser import parse_job_description

router = APIRouter(prefix="/api/jobs", tags=["jobs"])


@router.post("", response_model=JobOut, status_code=status.HTTP_201_CREATED)
def create_job(
    payload: JobCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.recruiter, UserRole.admin)),
):
    if not payload.description.strip():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Job description cannot be empty")

    parsed_requirements = parse_job_description(payload.description)
    embedding = generate_embedding(payload.description)

    job = Job(
        recruiter_id=current_user.id,
        title=payload.title,
        description=payload.description,
        parsed_requirements=parsed_requirements,
        embedding=embedding,
    )
    db.add(job)
    db.commit()
    db.refresh(job)
    return job


@router.get("", response_model=list[JobOut])
def list_jobs(db: Session = Depends(get_db), current_user: User = Depends(require_role(UserRole.recruiter, UserRole.admin, UserRole.candidate))):
    query = db.query(Job)
    if current_user.role == UserRole.recruiter:
        query = query.filter(Job.recruiter_id == current_user.id)
    if current_user.role == UserRole.candidate:
        query = query.filter(Job.status == "active")
    return query.order_by(Job.created_at.desc()).all()


@router.get("/{job_id}", response_model=JobOut)
def get_job(job_id: str, db: Session = Depends(get_db)):
    job = db.get(Job, job_id)
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")
    return job


@router.put("/{job_id}", response_model=JobOut)
def update_job(
    job_id: str,
    payload: JobUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.recruiter, UserRole.admin)),
):
    job = db.get(Job, job_id)
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")
    if job.recruiter_id != current_user.id and current_user.role != UserRole.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to edit this job")

    if payload.title is not None:
        job.title = payload.title
    if payload.description is not None:
        job.description = payload.description
        job.parsed_requirements = parse_job_description(payload.description)
        job.embedding = generate_embedding(payload.description)
    if payload.status is not None:
        job.status = payload.status

    db.commit()
    db.refresh(job)
    return job


@router.delete("/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_job(
    job_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.recruiter, UserRole.admin)),
):
    job = db.get(Job, job_id)
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")
    if job.recruiter_id != current_user.id and current_user.role != UserRole.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this job")
    db.delete(job)
    db.commit()
    return None


@router.get("/stats/{job_id}")
def job_stats(
    job_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.recruiter, UserRole.admin)),
):
    job = db.get(Job, job_id)
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")
    if job.recruiter_id != current_user.id and current_user.role != UserRole.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized for this job")
    rows = db.query(Application.status, func.count(Application.id)).filter(Application.job_id == job_id).group_by(Application.status).all()
    counts = {str(status_value.value if hasattr(status_value, "value") else status_value): count for status_value, count in rows}
    return {
        "job_id": job_id,
        "status": job.status,
        "applications": sum(counts.values()),
        "applied": counts.get("applied", 0),
        "shortlisted": counts.get("shortlisted", 0),
        "rejected": counts.get("rejected", 0),
        "hired": counts.get("hired", 0),
    }
