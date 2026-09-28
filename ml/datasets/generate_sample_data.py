"""
Generates real files from the sample dataset definitions so they can be
exercised through the actual upload/parse/match pipeline (not just used as
inline test fixtures):

    ml/datasets/resumes/*.pdf
    ml/datasets/job_descriptions/*.json

Run from the ml/datasets/ directory:
    python generate_sample_data.py
"""
import json
import os

import fitz  # PyMuPDF

from sample_job_descriptions import JOB_DESCRIPTIONS
from sample_resume_texts import RESUMES

RESUME_DIR = os.path.join(os.path.dirname(__file__), "resumes")
JD_DIR = os.path.join(os.path.dirname(__file__), "job_descriptions")


def write_pdf(filename: str, text: str) -> None:
    doc = fitz.open()
    page = doc.new_page()
    y = 72
    for line in text.split("\n"):
        if y > 780:
            page = doc.new_page()
            y = 72
        page.insert_text((72, y), line, fontsize=11)
        y += 14
    doc.save(os.path.join(RESUME_DIR, filename))
    doc.close()


def main():
    os.makedirs(RESUME_DIR, exist_ok=True)
    os.makedirs(JD_DIR, exist_ok=True)

    for filename, text in RESUMES.items():
        write_pdf(filename, text)
        print(f"Wrote {os.path.join('resumes', filename)}")

    for filename, jd in JOB_DESCRIPTIONS.items():
        path = os.path.join(JD_DIR, filename)
        with open(path, "w") as f:
            json.dump(jd, f, indent=2)
        print(f"Wrote {os.path.join('job_descriptions', filename)}")


if __name__ == "__main__":
    main()
