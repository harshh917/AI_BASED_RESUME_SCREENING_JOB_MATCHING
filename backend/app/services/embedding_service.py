"""
Embedding generation, behind a small abstraction so the underlying model can
be swapped without touching callers (matching_engine, API routes, etc.).

Two backends:
  - SentenceTransformerBackend: the real
    `sentence-transformers/all-MiniLM-L6-v2` model (384-dim). Used in
    production/docker.
  - HashingEmbeddingBackend: a deterministic, dependency-free fallback
    (feature-hashed bag-of-words, L2 normalized) used automatically when the
    real model can't be loaded (e.g. no network access to download weights,
    such as in this sandboxed dev/test environment) so the rest of the
    pipeline (cosine similarity, pgvector storage, tests) keeps working
    end-to-end. It is NOT a semantic model — swap EMBEDDING_BACKEND to
    "sentence_transformer" for real semantic similarity.
"""
import hashlib
import math
import re
from abc import ABC, abstractmethod
from functools import lru_cache
from typing import List

from app.core.config import settings

_TOKEN_RE = re.compile(r"[A-Za-z][A-Za-z0-9+.#]*")


class EmbeddingBackend(ABC):
    @abstractmethod
    def encode(self, text: str) -> List[float]:
        ...

    @property
    @abstractmethod
    def dimension(self) -> int:
        ...


class SentenceTransformerBackend(EmbeddingBackend):
    def __init__(self, model_name: str):
        from sentence_transformers import SentenceTransformer  # imported lazily

        self._model = SentenceTransformer(model_name)
        self._dim = self._model.get_sentence_embedding_dimension()

    def encode(self, text: str) -> List[float]:
        vector = self._model.encode(text or "", normalize_embeddings=True)
        return vector.tolist()

    @property
    def dimension(self) -> int:
        return self._dim


class HashingEmbeddingBackend(EmbeddingBackend):
    """Deterministic offline fallback: hashes tokens into a fixed-size
    vector (a lightweight relative of the classic hashing-trick vectorizer),
    then L2-normalizes so cosine similarity behaves sensibly."""

    def __init__(self, dim: int):
        self._dim = dim

    def encode(self, text: str) -> List[float]:
        vector = [0.0] * self._dim
        tokens = _TOKEN_RE.findall((text or "").lower())
        for token in tokens:
            idx = int(hashlib.md5(token.encode("utf-8")).hexdigest(), 16) % self._dim
            vector[idx] += 1.0
        norm = math.sqrt(sum(v * v for v in vector)) or 1.0
        return [v / norm for v in vector]

    @property
    def dimension(self) -> int:
        return self._dim


@lru_cache
def get_embedding_backend() -> EmbeddingBackend:
    if settings.EMBEDDING_BACKEND == "sentence_transformer":
        try:
            return SentenceTransformerBackend(settings.EMBEDDING_MODEL_NAME)
        except Exception:
            # Model weights unavailable (e.g. offline environment) — fall
            # back rather than crashing the whole service.
            return HashingEmbeddingBackend(settings.EMBEDDING_DIM)
    return HashingEmbeddingBackend(settings.EMBEDDING_DIM)


def generate_embedding(text: str) -> List[float]:
    return get_embedding_backend().encode(text)


def cosine_similarity(vec_a: List[float], vec_b: List[float]) -> float:
    if not vec_a or not vec_b or len(vec_a) != len(vec_b):
        return 0.0
    dot = sum(a * b for a, b in zip(vec_a, vec_b))
    norm_a = math.sqrt(sum(a * a for a in vec_a))
    norm_b = math.sqrt(sum(b * b for b in vec_b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    similarity = dot / (norm_a * norm_b)
    return max(0.0, min(1.0, similarity))  # clamp for safety
