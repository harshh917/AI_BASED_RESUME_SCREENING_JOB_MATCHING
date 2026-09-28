from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict


class EducationItem(BaseModel):
    degree: Optional[str] = None
    institution: Optional[str] = None
    field: Optional[str] = None
    graduation_year: Optional[str] = None


class ExperienceItem(BaseModel):
    company: Optional[str] = None
    role: Optional[str] = None
    duration: Optional[str] = None
    responsibilities: List[str] = []
    technologies: List[str] = []


class ProjectItem(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    technologies: List[str] = []


class SkillsBlock(BaseModel):
    programming_languages: List[str] = []
    frameworks: List[str] = []
    databases: List[str] = []
    cloud: List[str] = []
    tools: List[str] = []
    other: List[str] = []


class CandidateProfileOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    summary: Optional[str] = None
    skills: Optional[Dict[str, List[str]]] = None
    education: Optional[List[Dict[str, Any]]] = None
    experience: Optional[List[Dict[str, Any]]] = None
    projects: Optional[List[Dict[str, Any]]] = None
    certifications: Optional[List[str]] = None


class ResumeOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    file_name: str
    created_at: datetime
    profile: Optional[CandidateProfileOut] = None


class ResumeListItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    file_name: str
    created_at: datetime
