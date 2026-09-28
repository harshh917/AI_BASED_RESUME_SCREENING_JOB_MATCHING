from datetime import datetime
from typing import Any, Dict, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


JOB_STATUSES = {"active", "closed", "draft"}


class JobCreate(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    description: str = Field(min_length=1)


class JobUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None

    @field_validator("status")
    @classmethod
    def validate_status(cls, value):
        if value is not None and value not in JOB_STATUSES:
            raise ValueError("status must be active, closed, or draft")
        return self


class JobOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    recruiter_id: str
    title: str
    description: str
    parsed_requirements: Optional[Dict[str, Any]] = None
    created_at: datetime
    updated_at: datetime
    status: str
