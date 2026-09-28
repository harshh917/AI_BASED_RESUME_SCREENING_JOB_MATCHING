# AI-Based Resume Screening and Intelligent Job Matching System

A decision-support system that helps recruiters compare resumes against job descriptions using resume parsing, skill extraction and normalization, semantic embeddings, and explainable weighted scoring. It does **not** make hiring decisions, and it never uses protected attributes (gender, religion, caste, race, age, photo, marital status, nationality) for scoring or ranking. No such fields exist in the data model.

## Features
- JWT auth with candidate / recruiter / admin roles
- PDF and DOCX resume upload with validation (extension allow-list, size limit, random stored filenames)
- Rule-based extraction of education, experience, projects, certifications and categorized skills
- Job description parsing into required vs. preferred skills, experience range, education requirement
- Multi-signal matching: skills, semantic similarity, experience, projects, education, certifications
- Plain-language explanations; missing information is reported as "Not identified in the submitted resume"
- Recruiter ranking table with score filter and per-candidate detail page
- Candidate applications with resume selection, cover note, status pipeline, and recruiter review
- Resume browser preview for candidates and recruiters
- Job lifecycle management: edit, active/closed/draft status, delete, and application statistics
- Candidate job recommendations using the same deterministic matching engine
- Explainable matched/missing skills and component scores
- Evaluation workspace and Precision/Recall/F1@k, NDCG@k, MRR evaluation scripts

## Architecture
```
React (Vite, Tailwind) --Axios--> FastAPI --SQLAlchemy--> PostgreSQL + pgvector
                                     |
                                     +-- services/: resume_parser, jd_parser, skill_extractor,
                                                    embedding_service, matching_engine, explanation_service
```
Business logic lives in `backend/app/services/`; API routes only validate, authorize and call services.

## Tech stack
React, Vite, Tailwind CSS v4, Axios, React Router / Python 3.11+, FastAPI, Pydantic, SQLAlchemy, Alembic / PostgreSQL + pgvector / Sentence Transformers (`all-MiniLM-L6-v2`), PyMuPDF, python-docx / pytest.

## Folder structure
```
backend/   FastAPI app, alembic/, tests/
frontend/  Vite React app
ml/        datasets/ (synthetic), evaluation/ (metrics + runner), notebooks/, experiments/
uploads/   local upload storage (git-ignored)
docker-compose.yml
```

## Setup (local, without Docker)
### Backend
```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env        # then edit JWT_SECRET_KEY and DATABASE_URL
```
Database options:
- **PostgreSQL + pgvector (recommended):** create a database, run `CREATE EXTENSION IF NOT EXISTS vector;`, set `DATABASE_URL=postgresql+psycopg2://user:pass@localhost:5432/resume_matching`, then `alembic upgrade head`.
- **SQLite (quick start):** set `DATABASE_URL=sqlite:///./dev.db`. Embeddings are stored as JSON and similarity is computed in Python.

```bash
uvicorn app.main:app --reload --port 8000     # API docs at http://localhost:8000/docs
```

### Frontend
```bash
cd frontend
npm install
npm run dev                                   # http://localhost:5173
```
Set `VITE_API_BASE_URL` if the API is not at `http://localhost:8000`.

### Tests
```bash
cd backend && python -m pytest -q
```

### Docker
```bash
cp .env.example .env     # set JWT_SECRET_KEY (openssl rand -hex 32) and POSTGRES_PASSWORD
docker compose up --build
# frontend http://localhost:3000, API http://localhost:8000/docs
```

### Sample data
```bash
cd ml/datasets && python generate_sample_data.py   # writes 8 fictional resume PDFs + 5 JD JSON files
```

## Environment variables
See `backend/.env.example`. Key ones: `DATABASE_URL`, `JWT_SECRET_KEY`, `MAX_UPLOAD_SIZE_MB`, `EMBEDDING_BACKEND` (`sentence_transformer` or `hashing`), `CORS_ORIGINS`, and the six `WEIGHT_*` values.

## API summary
| Method | Path | Access |
|---|---|---|
| POST | /api/auth/register, /api/auth/login | public |
| GET | /api/auth/me | authenticated |
| POST/GET/DELETE | /api/resumes/upload, /api/resumes, /api/resumes/{id} | owner (candidates), recruiter/admin read |
| POST/GET/PUT/DELETE | /api/jobs, /api/jobs/{id} | recruiter/admin (writes) |\n| GET | /api/jobs/{id}/stats | job owner / admin |\n| GET | /api/recommendations/jobs | candidate/admin |
| GET | /api/candidates | recruiter/admin |
| POST | /api/matching/{job_id}/{resume_id}, /api/matching/job/{job_id}/run | job owner / admin |
| GET | /api/matching/{job_id}/results, /api/matching/{job_id}/{resume_id} | job owner / admin |

## Matching methodology
```
overall = 0.40*skill + 0.25*semantic + 0.15*experience + 0.10*project + 0.05*education + 0.05*certification
```
All sub-scores are 0-100. Weights are configurable and are a starting heuristic, **not** scientifically optimal or validated. Skills: required-skill coverage (up to 90 points) plus preferred-skill bonus (up to 10), using a curated alias taxonomy. Semantic: cosine similarity of embeddings. Experience: years estimated from date ranges vs. the JD minimum. All scoring is deterministic and inspectable.

## Evaluation
`ml/evaluation/evaluate.py` computes Precision/Recall/F1@k, NDCG@k and MRR from a labels file. The bundled labels are illustrative developer guesses, so no accuracy is claimed. Evaluate with real recruiter-labelled data before reporting metrics.

## Known limitations
- Resume/JD parsing is rule-based; unusual layouts, multi-column PDFs and scanned (image) PDFs will parse poorly. No OCR.
- Education matching is keyword based; the `field` of study is not extracted.
- Candidate names come from a heuristic (first line of the resume).
- Similarity is computed in Python, not yet via pgvector queries; vectors are stored in pgvector on Postgres.
- Candidate-side self-matching is not implemented (recruiters run matching).
- The `hashing` embedding backend is a non-semantic offline fallback. If the Sentence Transformers model cannot be loaded, the app silently falls back to it, so check your logs/config in production.
- spaCy is listed in requirements but the current extractors do not use it yet.
- Docker files were written but not executed in the authoring environment; see the note in the project report.

## Future improvements
pgvector ANN queries, OCR for scanned PDFs, spaCy NER for names/organisations, section-level embeddings, admin user management, bias/fairness audits, rate limiting, pagination.
