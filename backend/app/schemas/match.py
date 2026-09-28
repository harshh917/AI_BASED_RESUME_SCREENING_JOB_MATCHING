from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict


class MatchResultOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    resume_id: str
    job_id: str
    overall_score: float
    semantic_score: float
    skill_score: float
    experience_score: float
    education_score: float
    project_score: float
    certification_score: float
    matched_skills: Optional[List[str]] = None
    missing_skills: Optional[List[str]] = None
    explanation: Optional[str] = None
    created_at: datetime


class RankedCandidate(BaseModel):
    rank: int
    resume_id: str
    candidate_name: str
    overall_score: float
    skill_score: float
    experience_score: float
    missing_skills: List[str]
    match_id: str
