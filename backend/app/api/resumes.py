import os

from fastapi import APIRouter, Depends, HTTPException, UploadFile, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.config import settings
from app.db.database import get_db
from app.db.models.resume import CandidateProfile, Resume
from app.db.models.user import User
from app.schemas.resume import ResumeListItem, ResumeOut
from app.services.embedding_service import generate_embedding
from app.services.resume_parser import (
    EmptyDocumentError,
    UnsupportedFileTypeError,
    parse_resume,
)
from app.utils.file_validation import InvalidFileError, safe_filename, validate_extension, validate_size

router = APIRouter(prefix="/api/resumes", tags=["resumes"])


@router.post("/upload", response_model=ResumeOut, status_code=status.HTTP_201_CREATED)
def upload_resume(
    file: UploadFile,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    content = file.file.read()
    try:
        ext = validate_extension(file.filename or "")
        validate_size(content)
        parsed = parse_resume(file.filename or f"upload{ext}", content)
    except (InvalidFileError, UnsupportedFileTypeError, EmptyDocumentError) as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    stored_name = safe_filename(file.filename or "resume", ext)
    stored_path = os.path.join(settings.UPLOAD_DIR, stored_name)
    with open(stored_path, "wb") as f:
        f.write(content)

    embedding_source = " ".join(
        filter(
            None,
            [
                parsed.get("summary"),
                " ".join(e.get("role", "") or "" for e in parsed.get("experience", [])),
                " ".join(p.get("description", "") or "" for p in parsed.get("projects", [])),
            ],
        )
    ) or parsed["raw_text"][:2000]
    embedding = generate_embedding(embedding_source)

    resume = Resume(
        user_id=current_user.id,
        file_name=file.filename or stored_name,
        file_path=stored_path,
        raw_text=parsed["raw_text"],
        parsed_data={
            "contact": parsed["contact"],
            "summary": parsed["summary"],
        },
        embedding=embedding,
    )
    db.add(resume)
    db.flush()

    profile = CandidateProfile(
        resume_id=resume.id,
        summary=parsed["summary"],
        skills=parsed["skills"],
        education=parsed["education"],
        experience=parsed["experience"],
        projects=parsed["projects"],
        certifications=parsed["certifications"],
    )
    db.add(profile)
    db.commit()
    db.refresh(resume)
    return resume


@router.get("", response_model=list[ResumeListItem])
def list_resumes(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    query = db.query(Resume)
    if current_user.role.value == "candidate":
        query = query.filter(Resume.user_id == current_user.id)
    return query.order_by(Resume.created_at.desc()).all()


@router.get("/{resume_id}", response_model=ResumeOut)
def get_resume(resume_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    resume = db.get(Resume, resume_id)
    if not resume:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resume not found")
    if current_user.role.value == "candidate" and resume.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to view this resume")
    return resume


@router.get("/{resume_id}/file")
def view_resume_file(
    resume_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    resume = db.get(Resume, resume_id)
    if not resume:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resume not found")
    if current_user.role.value == "candidate" and resume.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to view this resume")
    if not os.path.isfile(resume.file_path):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resume file not found")

    ext = os.path.splitext(resume.file_name)[1].lower()
    media_types = {
        ".pdf": "application/pdf",
        ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        ".doc": "application/msword",
    }
    return FileResponse(
        resume.file_path,
        media_type=media_types.get(ext, "application/octet-stream"),
        filename=resume.file_name,
        content_disposition_type="inline",
    )


@router.delete("/{resume_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_resume(resume_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    resume = db.get(Resume, resume_id)
    if not resume:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resume not found")
    if current_user.role.value == "candidate" and resume.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this resume")
    if os.path.exists(resume.file_path):
        os.remove(resume.file_path)
    db.delete(resume)
    db.commit()
    return None
