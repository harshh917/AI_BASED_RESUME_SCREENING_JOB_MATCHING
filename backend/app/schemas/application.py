from datetime import datetime
from pydantic import BaseModel, Field

from app.db.models.application import ApplicationStatus


class ApplicationCreate(BaseModel):
    resume_id: str
    cover_note: str | None = Field(default=None, max_length=3000)


class ApplicationStatusUpdate(BaseModel):
    status: ApplicationStatus


class ApplicationOut(BaseModel):
    id: str
    job_id: str
    candidate_id: str
    resume_id: str
    cover_note: str | None
    status: ApplicationStatus
    match_score: float | None
    applied_at: datetime
    job_title: str
    candidate_name: str
    candidate_email: str
    resume_file_name: str

    class Config:
        from_attributes = True
