from typing import List
from pydantic import BaseModel

class JobRecommendation(BaseModel):
    job_id: str
    title: str
    status: str
    overall_score: float
    skill_score: float
    semantic_score: float
    matched_skills: List[str]
    missing_skills: List[str]
