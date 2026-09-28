"""
Resume parsing pipeline:
  file bytes -> raw text -> cleaned text -> section detection -> structured profile

Deliberately rule/regex based (not a black-box LLM call) so it is
deterministic, inspectable, and free to run inside tests/CI. Robust to
missing sections: every field defaults to None/[] rather than raising.
"""
import io
import re
from typing import Any, Dict, List, Optional

import fitz  # PyMuPDF
from docx import Document

from app.services.skill_extractor import extract_skills

SUPPORTED_EXTENSIONS = {".pdf", ".docx"}

SECTION_HEADERS = {
    "summary": ["summary", "objective", "profile"],
    "education": ["education", "academic background", "qualifications"],
    "experience": ["experience", "work experience", "employment history", "professional experience"],
    "projects": ["projects", "academic projects", "personal projects"],
    "certifications": ["certifications", "certificates", "licenses"],
    "skills": ["skills", "technical skills", "core competencies"],
}

EMAIL_RE = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")
PHONE_RE = re.compile(r"(\+?\d{1,3}[\s-]?)?(\d{10}|\(\d{3}\)\s?\d{3}[\s-]?\d{4}|\d{3}[\s-]\d{3}[\s-]\d{4})")
YEAR_RE = re.compile(r"(19|20)\d{2}")


class UnsupportedFileTypeError(Exception):
    pass


class EmptyDocumentError(Exception):
    pass


def extract_text(filename: str, content: bytes) -> str:
    """Dispatch to the right extractor based on file extension. Raises on
    unsupported types or unreadable/corrupted files."""
    ext = _get_extension(filename)
    if ext not in SUPPORTED_EXTENSIONS:
        raise UnsupportedFileTypeError(f"Unsupported file type: {ext}")

    if ext == ".pdf":
        text = _extract_pdf_text(content)
    else:
        text = _extract_docx_text(content)

    cleaned = clean_text(text)
    if not cleaned.strip():
        raise EmptyDocumentError("No extractable text found in document")
    return cleaned


def _get_extension(filename: str) -> str:
    idx = filename.rfind(".")
    return filename[idx:].lower() if idx != -1 else ""


def _extract_pdf_text(content: bytes) -> str:
    try:
        doc = fitz.open(stream=content, filetype="pdf")
    except Exception as exc:  # corrupted / unreadable PDF
        raise EmptyDocumentError(f"Could not read PDF: {exc}") from exc
    text_parts = [page.get_text() for page in doc]
    doc.close()
    return "\n".join(text_parts)


def _extract_docx_text(content: bytes) -> str:
    try:
        document = Document(io.BytesIO(content))
    except Exception as exc:
        raise EmptyDocumentError(f"Could not read DOCX: {exc}") from exc
    paragraphs = [p.text for p in document.paragraphs]
    for table in document.tables:
        for row in table.rows:
            for cell in row.cells:
                paragraphs.append(cell.text)
    return "\n".join(paragraphs)


def clean_text(text: str) -> str:
    text = text.replace("\x00", " ")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def detect_sections(text: str) -> Dict[str, str]:
    """Split resume text into named sections using header keyword matching.
    Falls back gracefully: any text before the first recognized header is
    treated as the top ("summary"/contact) block."""
    lines = text.split("\n")
    sections: Dict[str, List[str]] = {"header": []}
    current = "header"

    header_lookup = {}
    for section, keywords in SECTION_HEADERS.items():
        for kw in keywords:
            header_lookup[kw] = section

    for line in lines:
        stripped = line.strip().lower().strip(":")
        matched_section = None
        if 0 < len(stripped) <= 40:
            for kw, section in header_lookup.items():
                if stripped == kw or (stripped.startswith(kw) and len(stripped) <= len(kw) + 3):
                    matched_section = section
                    break
        if matched_section:
            current = matched_section
            sections.setdefault(current, [])
            continue
        sections.setdefault(current, []).append(line)

    return {k: "\n".join(v).strip() for k, v in sections.items()}


def extract_contact_info(text: str) -> Dict[str, Optional[str]]:
    email_match = EMAIL_RE.search(text)
    phone_match = PHONE_RE.search(text)
    # Best-effort name guess: first non-empty line that isn't an email/phone/header
    name = None
    for line in text.split("\n")[:5]:
        candidate = line.strip()
        if candidate and not EMAIL_RE.search(candidate) and not PHONE_RE.search(candidate) and len(candidate) < 60:
            name = candidate
            break
    return {
        "name": name,
        "email": email_match.group(0) if email_match else None,
        "phone": phone_match.group(0) if phone_match else None,
    }


def extract_education(section_text: str) -> List[Dict[str, Any]]:
    if not section_text:
        return []
    entries = []
    for block in re.split(r"\n\s*\n", section_text):
        block = block.strip()
        if not block:
            continue
        year_match = YEAR_RE.search(block)
        entries.append(
            {
                "degree": _first_line(block),
                "institution": _second_line(block),
                "field": None,
                "graduation_year": year_match.group(0) if year_match else None,
            }
        )
    return entries


def extract_experience(section_text: str) -> List[Dict[str, Any]]:
    if not section_text:
        return []
    entries = []
    for block in re.split(r"\n\s*\n", section_text):
        block = block.strip()
        if not block:
            continue
        lines = [l.strip() for l in block.split("\n") if l.strip()]
        if not lines:
            continue
        duration_match = re.search(
            r"(\b\w+\s\d{4}\b|\b\d{4}\b)\s*(-|–|to)\s*(\b\w+\s\d{4}\b|\bpresent\b|\b\d{4}\b)",
            block,
            re.IGNORECASE,
        )
        skills = extract_skills(block)
        from app.services.skill_extractor import flatten_skills

        entries.append(
            {
                "company": lines[1] if len(lines) > 1 else None,
                "role": lines[0],
                "duration": duration_match.group(0) if duration_match else None,
                "responsibilities": lines[2:6],
                "technologies": flatten_skills(skills),
            }
        )
    return entries


def extract_projects(section_text: str) -> List[Dict[str, Any]]:
    if not section_text:
        return []
    entries = []
    for block in re.split(r"\n\s*\n", section_text):
        block = block.strip()
        if not block:
            continue
        lines = [l.strip() for l in block.split("\n") if l.strip()]
        if not lines:
            continue
        from app.services.skill_extractor import flatten_skills

        entries.append(
            {
                "name": lines[0],
                "description": " ".join(lines[1:4]) if len(lines) > 1 else None,
                "technologies": flatten_skills(extract_skills(block)),
            }
        )
    return entries


def extract_certifications(section_text: str) -> List[str]:
    if not section_text:
        return []
    return [l.strip("-• ").strip() for l in section_text.split("\n") if l.strip()]


def _first_line(block: str) -> Optional[str]:
    lines = [l.strip() for l in block.split("\n") if l.strip()]
    return lines[0] if lines else None


def _second_line(block: str) -> Optional[str]:
    lines = [l.strip() for l in block.split("\n") if l.strip()]
    return lines[1] if len(lines) > 1 else None


def parse_resume(filename: str, content: bytes) -> Dict[str, Any]:
    """Full pipeline: bytes -> structured candidate profile dict.
    Raises UnsupportedFileTypeError / EmptyDocumentError on bad input."""
    raw_text = extract_text(filename, content)
    sections = detect_sections(raw_text)

    contact = extract_contact_info(raw_text)
    skills = extract_skills(sections.get("skills", "") or raw_text)
    education = extract_education(sections.get("education", ""))
    experience = extract_experience(sections.get("experience", ""))
    projects = extract_projects(sections.get("projects", ""))
    certifications = extract_certifications(sections.get("certifications", ""))

    return {
        "raw_text": raw_text,
        "contact": contact,  # NOT used for scoring — display/reference only
        "summary": sections.get("summary") or sections.get("header"),
        "skills": skills,
        "education": education,
        "experience": experience,
        "projects": projects,
        "certifications": certifications,
    }
