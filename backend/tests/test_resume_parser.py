import pytest

from app.services.resume_parser import (
    EmptyDocumentError,
    UnsupportedFileTypeError,
    parse_resume,
)
from tests.helpers import make_docx_bytes, make_pdf_bytes

SAMPLE_RESUME_TEXT = """John Doe
john.doe@example.com | 9876543210

Summary
Backend engineer with experience building APIs.

Education
B.Tech Computer Science
ABC Institute of Technology
2020

Experience
Backend Developer
TechCorp Pvt Ltd
Jan 2021 - Present
Built REST APIs using FastAPI and PostgreSQL
Deployed services with Docker

Projects
Payment Processing API
A Java Spring Boot service for processing payments with PostgreSQL

Certifications
AWS Certified Developer Associate
"""


def test_parse_valid_pdf_resume():
    pdf_bytes = make_pdf_bytes(SAMPLE_RESUME_TEXT)
    result = parse_resume("resume.pdf", pdf_bytes)

    assert result["raw_text"].strip() != ""
    assert result["contact"]["email"] == "john.doe@example.com"
    assert "PostgreSQL" in result["skills"]["databases"] + result["skills"]["frameworks"]
    assert len(result["experience"]) >= 1
    assert len(result["certifications"]) >= 1


def test_parse_valid_docx_resume():
    paragraphs = SAMPLE_RESUME_TEXT.split("\n")
    docx_bytes = make_docx_bytes(paragraphs)
    result = parse_resume("resume.docx", docx_bytes)

    assert result["raw_text"].strip() != ""
    assert result["contact"]["email"] == "john.doe@example.com"


def test_parse_rejects_unsupported_file_type():
    with pytest.raises(UnsupportedFileTypeError):
        parse_resume("resume.txt", b"hello world")


def test_parse_rejects_empty_document():
    empty_pdf = make_pdf_bytes("")
    with pytest.raises(EmptyDocumentError):
        parse_resume("empty.pdf", empty_pdf)


def test_parser_is_robust_to_missing_sections():
    minimal_text = "Jane Smith\njane@example.com\n\nSkills\nPython, Django, PostgreSQL"
    pdf_bytes = make_pdf_bytes(minimal_text)
    result = parse_resume("minimal.pdf", pdf_bytes)

    # Missing sections should default to empty, not raise
    assert result["education"] == []
    assert result["certifications"] == []
    assert "Python" in result["skills"]["programming_languages"]
