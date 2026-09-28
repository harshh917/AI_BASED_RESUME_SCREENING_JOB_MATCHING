"""Utility helpers shared by the test suite: build minimal in-memory
PDF/DOCX files so tests don't depend on fixture binaries."""
import io

import fitz  # PyMuPDF
from docx import Document


def make_pdf_bytes(text: str) -> bytes:
    doc = fitz.open()
    page = doc.new_page()
    y = 72
    for line in text.split("\n"):
        page.insert_text((72, y), line, fontsize=11)
        y += 14
    data = doc.tobytes()
    doc.close()
    return data


def make_docx_bytes(paragraphs: list[str]) -> bytes:
    document = Document()
    for p in paragraphs:
        document.add_paragraph(p)
    buffer = io.BytesIO()
    document.save(buffer)
    return buffer.getvalue()
