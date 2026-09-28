"""
Centralised application configuration.

Every configurable value (secrets, DB URL, scoring weights, upload limits)
is read from environment variables / .env so nothing is hardcoded and the
same code can run in dev, test, or docker without modification.
"""
from functools import lru_cache
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    APP_NAME: str = "AI Resume Matching System"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    DATABASE_URL: str = "postgresql+psycopg2://resume_user:resume_pass@localhost:5432/resume_matching"
    TEST_DATABASE_URL: str = "sqlite:///./test.db"

    JWT_SECRET_KEY: str = "insecure_dev_secret_change_me"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    UPLOAD_DIR: str = "../uploads/resumes"
    MAX_UPLOAD_SIZE_MB: int = 5
    ALLOWED_UPLOAD_EXTENSIONS: str = ".pdf,.docx"

    EMBEDDING_MODEL_NAME: str = "sentence-transformers/all-MiniLM-L6-v2"
    EMBEDDING_DIM: int = 384
    # "sentence_transformer" (real model, needs the model download) or
    # "hashing" (deterministic, offline fallback used automatically in tests/CI
    # and anywhere the model can't be downloaded).
    EMBEDDING_BACKEND: str = "sentence_transformer"

    CORS_ORIGINS: str = "http://localhost:5173,http://localhost:3000"

    WEIGHT_SKILL: float = 0.40
    WEIGHT_SEMANTIC: float = 0.25
    WEIGHT_EXPERIENCE: float = 0.15
    WEIGHT_PROJECT: float = 0.10
    WEIGHT_EDUCATION: float = 0.05
    WEIGHT_CERTIFICATION: float = 0.05

    @property
    def allowed_extensions_list(self) -> List[str]:
        return [e.strip().lower() for e in self.ALLOWED_UPLOAD_EXTENSIONS.split(",")]

    @property
    def cors_origins_list(self) -> List[str]:
        return [o.strip() for o in self.CORS_ORIGINS.split(",")]

    @property
    def scoring_weights(self) -> dict:
        return {
            "skill": self.WEIGHT_SKILL,
            "semantic": self.WEIGHT_SEMANTIC,
            "experience": self.WEIGHT_EXPERIENCE,
            "project": self.WEIGHT_PROJECT,
            "education": self.WEIGHT_EDUCATION,
            "certification": self.WEIGHT_CERTIFICATION,
        }


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
