from tests.helpers import make_pdf_bytes

RESUME_TEXT = """Jane Smith
jane.smith@example.com

Skills
Java, Spring Boot, PostgreSQL, REST API

Experience
Backend Developer
DevCorp
2021 - 2023
Built REST APIs

Education
B.Tech Computer Science
State University
2020
"""

JOB_DESCRIPTION = """Backend Developer

Required Skills:
Java, Spring Boot, PostgreSQL

Preferred Skills:
Docker

Minimum 1 years of experience required.
"""


def test_register_and_login(client):
    resp = client.post(
        "/api/auth/register",
        json={"name": "Test User", "email": "flow.user@example.com", "password": "password123", "role": "candidate"},
    )
    assert resp.status_code == 201
    assert resp.json()["access_token"]

    resp = client.post(
        "/api/auth/login", json={"email": "flow.user@example.com", "password": "password123"}
    )
    assert resp.status_code == 200
    assert resp.json()["user"]["email"] == "flow.user@example.com"


def test_login_rejects_wrong_password(client):
    client.post(
        "/api/auth/register",
        json={"name": "Bad Login", "email": "badlogin@example.com", "password": "password123", "role": "candidate"},
    )
    resp = client.post("/api/auth/login", json={"email": "badlogin@example.com", "password": "wrongpass"})
    assert resp.status_code == 401


def test_resume_upload_requires_auth(client):
    files = {"file": ("resume.pdf", make_pdf_bytes(RESUME_TEXT), "application/pdf")}
    resp = client.post("/api/resumes/upload", files=files)
    assert resp.status_code == 401


def test_resume_upload_rejects_bad_extension(client, candidate_token):
    headers = {"Authorization": f"Bearer {candidate_token}"}
    files = {"file": ("resume.exe", b"not a resume", "application/octet-stream")}
    resp = client.post("/api/resumes/upload", files=files, headers=headers)
    assert resp.status_code == 400


def test_full_matching_flow(client, candidate_token, recruiter_token):
    # Candidate uploads a resume
    headers_candidate = {"Authorization": f"Bearer {candidate_token}"}
    files = {"file": ("resume.pdf", make_pdf_bytes(RESUME_TEXT), "application/pdf")}
    resp = client.post("/api/resumes/upload", files=files, headers=headers_candidate)
    assert resp.status_code == 201, resp.text
    resume_id = resp.json()["id"]
    assert resp.json()["profile"]["skills"]["programming_languages"] == ["Java"] or "Java" in resp.json()["profile"]["skills"].get("programming_languages", [])

    # Recruiter creates a job
    headers_recruiter = {"Authorization": f"Bearer {recruiter_token}"}
    resp = client.post("/api/jobs", json={"title": "Backend Developer", "description": JOB_DESCRIPTION}, headers=headers_recruiter)
    assert resp.status_code == 201, resp.text
    job_id = resp.json()["id"]
    assert "Java" in resp.json()["parsed_requirements"]["required_skills"]

    # Recruiter runs matching for the job
    resp = client.post(f"/api/matching/job/{job_id}/run", headers=headers_recruiter)
    assert resp.status_code == 200, resp.text
    results = resp.json()
    assert len(results) >= 1
    assert results[0]["overall_score"] > 0

    # Ranked results
    resp = client.get(f"/api/matching/{job_id}/results", headers=headers_recruiter)
    assert resp.status_code == 200
    ranked = resp.json()
    assert ranked[0]["rank"] == 1
    assert ranked[0]["resume_id"] == resume_id

    # Match detail
    resp = client.get(f"/api/matching/{job_id}/{resume_id}", headers=headers_recruiter)
    assert resp.status_code == 200
    assert "Overall Match" in resp.json()["explanation"]


def test_candidate_cannot_create_job(client, candidate_token):
    headers = {"Authorization": f"Bearer {candidate_token}"}
    resp = client.post("/api/jobs", json={"title": "X", "description": "Required Skills: Python"}, headers=headers)
    assert resp.status_code == 403


def test_candidate_cannot_access_other_candidates_resume(client, candidate_token):
    # Upload as this candidate
    headers = {"Authorization": f"Bearer {candidate_token}"}
    files = {"file": ("resume.pdf", make_pdf_bytes(RESUME_TEXT), "application/pdf")}
    resp = client.post("/api/resumes/upload", files=files, headers=headers)
    resume_id = resp.json()["id"]

    # A second, unrelated candidate tries to fetch it
    reg = client.post(
        "/api/auth/register",
        json={"name": "Other Candidate", "email": "other.candidate@example.com", "password": "password123", "role": "candidate"},
    )
    other_token = reg.json()["access_token"]
    resp = client.get(f"/api/resumes/{resume_id}", headers={"Authorization": f"Bearer {other_token}"})
    assert resp.status_code == 403


def test_results_require_auth(client, recruiter_token):
    headers = {"Authorization": f"Bearer {recruiter_token}"}
    resp = client.post("/api/jobs", json={"title": "T", "description": "Required Skills: Python"}, headers=headers)
    job_id = resp.json()["id"]
    assert client.get(f"/api/matching/{job_id}/results").status_code == 401
    assert client.get(f"/api/matching/{job_id}/results", headers=headers).status_code == 200
