import uuid
from datetime import datetime, timezone

from sqlalchemy import JSON, Column, DateTime, ForeignKey, String, Text
from sqlalchemy.orm import relationship

from app.core.config import settings
from app.db.database import Base
from app.db.vector_type import Vector


class Resume(Base):
    __tablename__ = "resumes"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    file_name = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    raw_text = Column(Text, nullable=True)
    parsed_data = Column(JSON, nullable=True)  # structured extraction (skills/edu/exp/projects/certs)
    embedding = Column(Vector(settings.EMBEDDING_DIM), nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    owner = relationship("User", back_populates="resumes")
    profile = relationship(
        "CandidateProfile", back_populates="resume", uselist=False, cascade="all, delete-orphan"
    )
    match_results = relationship("MatchResult", back_populates="resume", cascade="all, delete-orphan")


class CandidateProfile(Base):
    __tablename__ = "candidate_profiles"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    resume_id = Column(String(36), ForeignKey("resumes.id"), nullable=False, unique=True)
    summary = Column(Text, nullable=True)
    skills = Column(JSON, nullable=True)          # {"languages": [...], "frameworks": [...], ...}
    education = Column(JSON, nullable=True)        # list[{degree, institution, field, year}]
    experience = Column(JSON, nullable=True)       # list[{company, role, duration, responsibilities, technologies}]
    projects = Column(JSON, nullable=True)         # list[{name, description, technologies}]
    certifications = Column(JSON, nullable=True)   # list[str]

    resume = relationship("Resume", back_populates="profile")
