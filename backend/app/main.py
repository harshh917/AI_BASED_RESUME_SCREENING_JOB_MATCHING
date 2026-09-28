from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.exception_handlers import http_exception_handler
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api import applications, auth, candidates, jobs, matching, resumes, recommendations
from app.core.config import settings
from app.db import models  # noqa: F401  (ensures models are registered on Base)
from app.db.database import Base, engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    # For local/dev convenience only — production deployments should use
    # Alembic migrations (see backend/alembic) instead of create_all.
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title=settings.APP_NAME, version="0.1.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"detail": "Invalid request", "errors": exc.errors()},
    )


@app.exception_handler(HTTPException)
async def http_exc_handler(request: Request, exc: HTTPException):
    # Preserve FastAPI's normal HTTPException behaviour (401/403/404/etc.)
    return await http_exception_handler(request, exc)


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    # Never leak stack traces to the client.
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})


@app.get("/api/health", tags=["health"])
def health_check():
    return {"status": "ok", "app": settings.APP_NAME}


app.include_router(auth.router)
app.include_router(resumes.router)
app.include_router(jobs.router)
app.include_router(matching.router)
app.include_router(candidates.router)

app.include_router(applications.router)
app.include_router(recommendations.router)
