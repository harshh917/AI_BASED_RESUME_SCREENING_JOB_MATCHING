# AI-Based Resume Screening and Intelligent Job Matching System

A decision-support system that helps recruiters compare resumes against job descriptions using resume parsing, skill extraction, semantic embeddings, and explainable weighted scoring.

> **This is a decision-support tool, not an automated hiring system.** It ranks and explains; a human makes the decision. Protected attributes (gender, religion, caste, race, age, photograph, marital status, nationality) are never used for scoring or ranking, and no such fields exist in the data model.

---

## Table of Contents

1. [Project Status](#1-project-status)
2. [Features](#2-features)
3. [System Architecture](#3-system-architecture)
4. [Tech Stack](#4-tech-stack)
5. [Repository Structure](#5-repository-structure)
6. [Getting Started](#6-getting-started)
7. [Configuration](#7-configuration)
8. [Database](#8-database)
9. [Running the Application](#9-running-the-application)
10. [Testing](#10-testing)
11. [Docker](#11-docker)
12. [API Reference](#12-api-reference)
13. [AI / ML Methodology](#13-ai--ml-methodology)
14. [Sample Data and Evaluation](#14-sample-data-and-evaluation)
15. [Security and Responsible AI](#15-security-and-responsible-ai)
16. [Known Limitations](#16-known-limitations)
17. [Roadmap](#17-roadmap)
18. [License](#18-license)

---

## 1. Project Status

| Area | Status | Notes |
|---|---|---|
| Backend API (FastAPI) | Working | Exercised end-to-end against a live server |
| Automated tests | 23 passing | Run on SQLite with the offline embedding fallback |
| Alembic migrations | Verified on SQLite | Not yet verified on PostgreSQL + pgvector |
| Frontend (React) | Builds | Production build succeeds; not yet browser-tested |
| Docker Compose | Written | Not yet executed |
| Sentence Transformers embeddings | Implemented | Not run in the authoring environment (no model download access) |
| Evaluation framework | Working | Metrics code only; no validated accuracy figures exist yet |

---

## 2. Features

**Candidates**
- Register, log in, upload a resume (PDF or DOCX)
- View the structured profile extracted from their own resume
- Browse open jobs

**Recruiters**
- Create jobs by pasting a job description; requirements are extracted automatically
- Run matching across all uploaded resumes
- View a ranked candidate table with a minimum-score filter
- Open a per-candidate match page with sub-scores, matched and missing skills, and a written explanation
- Dashboard: total jobs, total candidates, resumes screened, average match score

**Platform**
- JWT authentication with `candidate`, `recruiter`, and `admin` roles
- Resume upload validation: extension allow-list, size limit, random stored filenames
- Explanations report absent data as *"Not identified in the submitted resume"* rather than assuming a gap
- Structured error responses; stack traces are never returned to clients

---

## 3. System Architecture

```mermaid
flowchart LR
    UI[React + Vite + Tailwind] -->|Axios / JWT| API[FastAPI]
    API --> SVC[Services layer]
    SVC --> RP[resume_parser]
    SVC --> JP[jd_parser]
    SVC --> SK[skill_extractor]
    SVC --> EM[embedding_service]
    SVC --> ME[matching_engine]
    SVC --> EX[explanation_service]
    API -->|SQLAlchemy| DB[(PostgreSQL + pgvector)]
```

**Resume pipeline**

```text
Upload -> Validate (type, size) -> Extract text (PDF/DOCX) -> Clean
       -> Detect sections -> Extract entities -> Candidate profile
       -> Generate embedding -> Store
```

**Design rules**
- API routes validate, authorize, and delegate. Business logic lives in `backend/app/services/`.
- The embedding model sits behind an abstraction (`EmbeddingBackend`) and can be replaced without touching callers.
- Scoring is deterministic: the same input always produces the same output.

---

## 4. Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React, Vite, Tailwind CSS v4, Axios, React Router |
| Backend | Python 3.11+, FastAPI, Pydantic, SQLAlchemy, Alembic |
| Database | PostgreSQL with pgvector (SQLite supported for development and tests) |
| NLP / ML | Sentence Transformers (`all-MiniLM-L6-v2`), rule-based extraction with a curated skill taxonomy |
| Document parsing | PyMuPDF (PDF), python-docx (DOCX) |
| Auth | JWT (python-jose), bcrypt (passlib) |
| Testing | pytest, FastAPI TestClient |
| DevOps | Docker, docker-compose |

> spaCy, scikit-learn, and numpy are listed in `requirements.txt` for planned use, but the current extractors do not import them.

---

## 5. Repository Structure

```text
ai-resume-matching/
├── backend/
│   ├── app/
│   │   ├── main.py                 # App entrypoint, CORS, error handlers
│   │   ├── api/                    # auth, resumes, jobs, matching, candidates, deps
│   │   ├── core/                   # config (env settings), security (JWT, hashing)
│   │   ├── db/                     # engine/session, models/, portable Vector type
│   │   ├── schemas/                # Pydantic request/response models
│   │   ├── services/               # parsing, extraction, embeddings, scoring, explanations
│   │   └── utils/                  # skills taxonomy, upload validation
│   ├── alembic/                    # Migrations
│   ├── tests/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── pages/                  # Landing, auth, candidate and recruiter pages
│   │   ├── components/             # ScoreBadge, SkillList, StatCard, ProtectedRoute
│   │   ├── services/               # Axios client and API wrappers
│   │   ├── hooks/                  # useAuth
│   │   └── layouts/
│   ├── Dockerfile
│   └── nginx.conf
├── ml/
│   ├── datasets/                   # Synthetic resumes and job descriptions
│   ├── evaluation/                 # metrics.py, evaluate.py, labels.example.json
│   ├── notebooks/
│   └── experiments/
├── uploads/                        # Local file storage (git-ignored)
├── docker-compose.yml
├── .env.example                    # Docker Compose variables
└── LICENSE
```

---

## 6. Getting Started

### Prerequisites

| Tool | Version | Needed for |
|---|---|---|
| Python | 3.11 or newer | Backend |
| Node.js | 20 or newer | Frontend |
| PostgreSQL with pgvector | 15 or newer | Production-style setup (optional for quick start) |
| Docker and Docker Compose | Recent | Container setup (optional) |

### Quick start (SQLite, no database server)

```bash
# 1. Backend
cd backend
python -m venv .venv
source .venv/bin/activate            # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
```

Edit `backend/.env` and set:

```env
DATABASE_URL=sqlite:///./dev.db
JWT_SECRET_KEY=<output of: openssl rand -hex 32>
```

```bash
uvicorn app.main:app --reload --port 8000
```

```bash
# 2. Frontend (new terminal)
cd frontend
npm install
npm run dev
```

| Service | URL |
|---|---|
| Frontend | http://localhost:5173 |
| API | http://localhost:8000 |
| Interactive API docs | http://localhost:8000/docs |
| Health check | http://localhost:8000/api/health |

On first start the app creates tables automatically (development convenience). For PostgreSQL deployments use Alembic, as described in the next section.

The first run with `EMBEDDING_BACKEND=sentence_transformer` downloads the model from Hugging Face (about 90 MB) and needs internet access. To skip this during development, set `EMBEDDING_BACKEND=hashing` (see [Configuration](#7-configuration) for the caveat).

---

## 7. Configuration

All configuration comes from environment variables, read from `backend/.env`. Nothing is hardcoded.

| Variable | Default | Description |
|---|---|---|
| `DATABASE_URL` | PostgreSQL URL | SQLAlchemy connection string |
| `JWT_SECRET_KEY` | insecure dev value | **Must be changed** for any real deployment |
| `JWT_ALGORITHM` | `HS256` | JWT signing algorithm |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `60` | Token lifetime |
| `UPLOAD_DIR` | `../uploads/resumes` | Where uploaded resumes are stored |
| `MAX_UPLOAD_SIZE_MB` | `5` | Upload size limit |
| `ALLOWED_UPLOAD_EXTENSIONS` | `.pdf,.docx` | Upload allow-list |
| `EMBEDDING_BACKEND` | `sentence_transformer` | `sentence_transformer` or `hashing` |
| `EMBEDDING_MODEL_NAME` | `sentence-transformers/all-MiniLM-L6-v2` | Model to load |
| `EMBEDDING_DIM` | `384` | Must match the model |
| `CORS_ORIGINS` | `http://localhost:5173,http://localhost:3000` | Comma-separated allowed origins |
| `WEIGHT_SKILL` | `0.40` | Scoring weight |
| `WEIGHT_SEMANTIC` | `0.25` | Scoring weight |
| `WEIGHT_EXPERIENCE` | `0.15` | Scoring weight |
| `WEIGHT_PROJECT` | `0.10` | Scoring weight |
| `WEIGHT_EDUCATION` | `0.05` | Scoring weight |
| `WEIGHT_CERTIFICATION` | `0.05` | Scoring weight |

Keep the six weights summing to 1.0. The application does not currently enforce this.

Frontend: set `VITE_API_BASE_URL` (default `http://localhost:8000`) in `frontend/.env` if the API runs elsewhere.

**About the embedding backends**

| Backend | Behavior |
|---|---|
| `sentence_transformer` | Real semantic embeddings. Falls back to `hashing` **silently** if the model cannot be loaded. |
| `hashing` | Deterministic bag-of-words hashing. Works offline. **Not semantic**, so the 25% semantic score is only a rough lexical-overlap signal. |

Verify which backend is actually active in production.

---

## 8. Database

### PostgreSQL with pgvector

```sql
CREATE DATABASE resume_matching;
\c resume_matching
CREATE EXTENSION IF NOT EXISTS vector;
```

```bash
# backend/.env
DATABASE_URL=postgresql+psycopg2://user:password@localhost:5432/resume_matching

cd backend
alembic upgrade head
```

The migration was generated and tested against SQLite. Inspect the resulting tables (especially the `embedding` columns) the first time you run it on PostgreSQL.

### Schema

| Table | Purpose |
|---|---|
| `users` | Accounts: name, email, password hash, role |
| `resumes` | File metadata, raw text, extracted contact data, embedding |
| `candidate_profiles` | Structured skills, education, experience, projects, certifications |
| `jobs` | Title, description, parsed requirements, embedding |
| `match_results` | Sub-scores, matched and missing skills, explanation; unique per (resume, job) |

Embeddings use a portable `Vector` type: native pgvector on PostgreSQL, JSON on SQLite.

### Creating a new migration

```bash
alembic revision --autogenerate -m "describe change"
```

Autogenerate does not capture the custom `Vector` type correctly. After generating, make sure the migration imports `from app.db.vector_type import Vector` and uses `Vector(dim=384)`.

---

## 9. Running the Application

```bash
# Backend (development, auto-reload)
cd backend && uvicorn app.main:app --reload --port 8000

# Frontend (development)
cd frontend && npm run dev

# Frontend (production build)
cd frontend && npm run build && npm run preview
```

### Typical workflow

1. Register a **recruiter** account and a **candidate** account.
2. As the candidate, upload a resume at `/candidate/upload`.
3. As the recruiter, create a job at `/recruiter/jobs/new`. Use headings such as `Required Skills:` and `Preferred Skills:` for best extraction.
4. On the job page, click **Run matching on all candidates**.
5. Review the ranking and open **Details** for the score breakdown and explanation.

---

## 10. Testing

```bash
cd backend
python -m pytest -q
```

Tests run on SQLite with the `hashing` embedding backend, so no database server or model download is needed.

| Test file | Covers |
|---|---|
| `test_resume_parser.py` | Valid PDF and DOCX, unsupported type, empty document, missing sections |
| `test_skill_matching.py` | Exact match, alias normalization, missing skills, preferred-skill bonus |
| `test_matching_engine.py` | JD parsing, strong vs. weak candidate, score range 0-100 |
| `test_api.py` | Register, login, auth enforcement, upload validation, full matching flow, role and ownership checks |

---

## 11. Docker

```bash
cp .env.example .env
# Set JWT_SECRET_KEY (openssl rand -hex 32) and POSTGRES_PASSWORD
docker compose up --build
```

| Service | URL |
|---|---|
| Frontend (nginx) | http://localhost:3000 |
| Backend | http://localhost:8000/docs |
| PostgreSQL (pgvector image) | internal, port 5432 |

- The database container enables the `vector` extension on first start.
- The backend runs `alembic upgrade head` before starting.
- The first backend start downloads the embedding model, which needs internet access.
- Compose refuses to start if `JWT_SECRET_KEY` is unset.
- Uploads and database data persist in named volumes.

> These Docker files have not been executed yet. Expect to debug the first run.

---

## 12. API Reference

Interactive documentation is available at `/docs` (Swagger UI). Protected routes need the header `Authorization: Bearer <token>`.

### Endpoints

| Method | Path | Access |
|---|---|---|
| POST | `/api/auth/register` | Public |
| POST | `/api/auth/login` | Public |
| GET | `/api/auth/me` | Authenticated |
| POST | `/api/resumes/upload` | Authenticated |
| GET | `/api/resumes` | Candidates see own; recruiters and admins see all |
| GET | `/api/resumes/{id}` | Owner, recruiter, or admin |
| DELETE | `/api/resumes/{id}` | Owner, recruiter, or admin |
| POST | `/api/jobs` | Recruiter, admin |
| GET | `/api/jobs` | Authenticated (recruiters see their own) |
| GET | `/api/jobs/{id}` | Public |
| PUT / DELETE | `/api/jobs/{id}` | Job owner, admin |
| GET | `/api/candidates` | Recruiter, admin |
| POST | `/api/matching/{job_id}/{resume_id}` | Job owner, admin |
| POST | `/api/matching/job/{job_id}/run` | Job owner, admin |
| GET | `/api/matching/{job_id}/results` | Job owner, admin |
| GET | `/api/matching/{job_id}/{resume_id}` | Job owner, admin |
| GET | `/api/health` | Public |

### Example session

```bash
BASE=http://localhost:8000

# Register a recruiter
curl -s -X POST $BASE/api/auth/register -H "Content-Type: application/json" \
  -d '{"name":"Rita","email":"rita@example.com","password":"password123","role":"recruiter"}'

# Log in and capture the token
TOKEN=$(curl -s -X POST $BASE/api/auth/login -H "Content-Type: application/json" \
  -d '{"email":"rita@example.com","password":"password123"}' | python -c "import sys,json;print(json.load(sys.stdin)['access_token'])")

# Create a job
curl -s -X POST $BASE/api/jobs -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"title":"Backend Developer","description":"Backend Developer\n\nRequired Skills:\nJava, Spring Boot, PostgreSQL\n\nPreferred Skills:\nDocker\n\nMinimum 2 years of experience required."}'

# Run matching for a job (replace JOB_ID)
curl -s -X POST $BASE/api/matching/job/JOB_ID/run -H "Authorization: Bearer $TOKEN"

# Ranked results
curl -s $BASE/api/matching/JOB_ID/results -H "Authorization: Bearer $TOKEN"
```

### Error format

```json
{ "detail": "Unsupported file extension '.exe'. Allowed: .pdf, .docx" }
```

| Status | Meaning |
|---|---|
| 400 | Invalid input, such as bad file type, oversized or empty file, unreadable PDF |
| 401 | Missing or invalid token |
| 403 | Authenticated but not allowed |
| 404 | Record not found |
| 422 | Request body failed validation |
| 500 | Unexpected error (details are logged, never returned) |

---

## 13. AI / ML Methodology

### Extraction

Extraction is **rule-based and deterministic**, not a generative model. This keeps results inspectable and reproducible.

| Component | Approach |
|---|---|
| Text extraction | PyMuPDF for PDF, python-docx for DOCX |
| Section detection | Header keyword matching (education, experience, projects, certifications, skills) |
| Contact info | Regex for email and phone; name is a first-line heuristic |
| Skills | Curated taxonomy of aliases mapped to canonical names and categories |
| Job descriptions | Marker keywords split required from preferred skills; regex for experience range |

Skill normalization examples: `JS` becomes `JavaScript`, `ReactJS` becomes `React`, `Postgres` becomes `PostgreSQL`, `Node` becomes `Node.js`. Skills are grouped into programming languages, frameworks, databases, cloud, tools, and other. To add a skill, extend `backend/app/utils/skills_taxonomy.py`.

### Scoring

```text
overall = 0.40 * skill
        + 0.25 * semantic
        + 0.15 * experience
        + 0.10 * project
        + 0.05 * education
        + 0.05 * certification
```

Every sub-score is normalized to 0-100.

| Signal | How it is computed |
|---|---|
| Skill | Required-skill coverage (up to 90 points) plus preferred-skill coverage (up to 10 points) |
| Semantic | Cosine similarity between resume and job embeddings, scaled to 0-100 |
| Experience | Years estimated from date ranges in the resume, compared to the job's minimum |
| Project | Overlap between project technologies and the job's required and preferred skills |
| Education | Keyword match between the required degree level and the candidate's degrees |
| Certification | Simple count-based score (25 points per certification, capped at 100) |

**These weights are a reasonable starting heuristic. They are not scientifically optimal and have not been validated against real hiring outcomes.** They are configurable through environment variables.

### Explanations

Explanations are template-based. Each sentence is generated directly from computed values (matched skills, missing skills, estimated years), so nothing is invented. When information is absent from the resume, the output says *"Not identified in the submitted resume"*.

---

## 14. Sample Data and Evaluation

### Synthetic dataset

`ml/datasets/` contains 8 fictional resumes and 5 job descriptions covering strong, medium, and weak matches, missing skills, different experience levels, and different domains. No real personal data is used.

```bash
cd ml/datasets
python generate_sample_data.py     # writes PDFs to resumes/ and JSON to job_descriptions/
```

### Evaluation framework

```bash
python ml/evaluation/evaluate.py --labels ml/evaluation/labels.example.json --k 3
```

Reports Precision@k, Recall@k, F1@k, NDCG@k, and MRR per job, plus the macro average.

> **`labels.example.json` contains illustrative labels written by the developer, not ground truth.** It exists only to show the evaluation code runs. No accuracy figures should be quoted from it. To evaluate properly, have recruiters label a larger set of resume-job pairs and run the script on those labels.

---

## 15. Security and Responsible AI

**Security**
- Passwords hashed with bcrypt; sessions use signed JWTs
- Secrets come from environment variables; `.env` is git-ignored
- Uploads are checked for extension and size; stored filenames are random, so client filenames never reach the filesystem
- SQL access goes through the SQLAlchemy ORM
- CORS restricted to configured origins
- Role and ownership checks on resumes, jobs, and match results
- Generic 500 responses; no stack traces leak to clients

**Responsible AI**
- Scores support human review; they do not replace it
- No protected attributes are stored or used
- Contact details (name, email, phone) are extracted for display and never enter scoring
- Explanations avoid asserting that something is missing when it may simply not have been parsed
- Skill-based scoring can still encode bias through the resume wording it rewards. Audit outcomes before any real use.

---

## 16. Known Limitations

**Security issues to fix before any real deployment**
- **Self-registration allows the `admin` role.** The register endpoint accepts `role: "admin"` from any caller. Restrict registration to `candidate` and `recruiter` and create admins out of band.
- `GET /api/jobs/{id}` is public.
- Recruiters can read all uploaded resumes, not only those relevant to their jobs.
- No rate limiting, and JWTs cannot be revoked before expiry.

**Functional**
- Parsing is rule-based. Scanned PDFs, multi-column layouts, and unusual formats parse poorly. There is no OCR.
- Education matching is keyword based, and field of study is not extracted.
- The candidate name is a heuristic and can be wrong; the match detail page currently derives it from the resume header.
- Similarity is computed in Python; pgvector is used for storage but not for nearest-neighbour queries.
- Candidates cannot run matching themselves; only recruiters can.
- No pagination on list endpoints.
- Scoring weights are not validated to sum to 1.0.

**Verification gaps**
- Not yet run: Docker Compose, PostgreSQL + pgvector, the Sentence Transformers model, and the frontend in a browser.
- No metrics on real data exist.

---

## 17. Roadmap

1. Fix the security items in section 16
2. Run and debug the full Docker stack against PostgreSQL + pgvector
3. Use pgvector similarity queries instead of Python-side comparison
4. Browser-test the frontend and add frontend tests
5. Collect recruiter-labelled data and report real evaluation metrics
6. Add OCR for scanned resumes and spaCy-based entity extraction
7. Section-level embeddings (skills, projects, experience) for finer matching
8. Fairness and bias audit tooling
9. Pagination, rate limiting, and admin user management

---

## 18. License

Released under the MIT License. See [LICENSE](LICENSE).
