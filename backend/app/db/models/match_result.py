import uuid
from datetime import datetime, timezone

from sqlalchemy import JSON, Column, DateTime, Float, ForeignKey, String, Text, UniqueConstraint
from sqlalchemy.orm import relationship

from app.db.database import Base


class MatchResult(Base):
    __tablename__ = "match_results"
    __table_args__ = (UniqueConstraint("resume_id", "job_id", name="uq_resume_job"),)

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    resume_id = Column(String(36), ForeignKey("resumes.id"), nullable=False)
    job_id = Column(String(36), ForeignKey("jobs.id"), nullable=False)

    overall_score = Column(Float, nullable=False)
    semantic_score = Column(Float, nullable=False)
    skill_score = Column(Float, nullable=False)
    experience_score = Column(Float, nullable=False)
    education_score = Column(Float, nullable=False)
    project_score = Column(Float, nullable=False)
    certification_score = Column(Float, nullable=False, default=0.0)

    matched_skills = Column(JSON, nullable=True)
    missing_skills = Column(JSON, nullable=True)
    explanation = Column(Text, nullable=True)

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    resume = relationship("Resume", back_populates="match_results")
    job = relationship("Job", back_populates="match_results")
