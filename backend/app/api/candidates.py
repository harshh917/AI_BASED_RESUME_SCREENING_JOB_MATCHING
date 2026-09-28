from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import require_role
from app.db.database import get_db
from app.db.models.resume import Resume
from app.db.models.user import User, UserRole
from app.schemas.resume import ResumeOut

router = APIRouter(prefix="/api/candidates", tags=["candidates"])


@router.get("", response_model=list[ResumeOut])
def list_candidates(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.recruiter, UserRole.admin)),
):
    """Recruiter-facing view of all uploaded candidate resumes/profiles.
    Never returns sensitive/protected attributes (gender, religion, age,
    photo, etc.) — none of those fields exist anywhere in the schema."""
    return db.query(Resume).order_by(Resume.created_at.desc()).all()
