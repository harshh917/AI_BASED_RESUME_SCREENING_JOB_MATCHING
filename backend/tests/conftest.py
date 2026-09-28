import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault("DATABASE_URL", "sqlite:///./test.db")
os.environ.setdefault("EMBEDDING_BACKEND", "hashing")

import pytest
from fastapi.testclient import TestClient

from app.db import models  # noqa: F401 ensure models registered
from app.db.database import Base, engine
from app.main import app


@pytest.fixture(scope="session", autouse=True)
def _setup_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)
    db_file = "./test.db"
    if os.path.exists(db_file):
        os.remove(db_file)


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def recruiter_token(client):
    import uuid

    resp = client.post(
        "/api/auth/register",
        json={
            "name": "Rita Recruiter",
            "email": f"rita.recruiter.{uuid.uuid4().hex[:8]}@example.com",
            "password": "supersecret1",
            "role": "recruiter",
        },
    )
    assert resp.status_code == 201, resp.text
    return resp.json()["access_token"]


@pytest.fixture
def candidate_token(client):
    import uuid

    resp = client.post(
        "/api/auth/register",
        json={
            "name": "Charlie Candidate",
            "email": f"charlie.candidate.{uuid.uuid4().hex[:8]}@example.com",
            "password": "supersecret1",
            "role": "candidate",
        },
    )
    assert resp.status_code == 201, resp.text
    return resp.json()["access_token"]
