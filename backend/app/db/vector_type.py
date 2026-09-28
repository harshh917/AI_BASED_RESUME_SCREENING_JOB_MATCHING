"""
A SQLAlchemy TypeDecorator that stores embeddings as a native `pgvector`
column on PostgreSQL, but transparently falls back to a JSON-encoded TEXT
column on SQLite. This keeps the ORM models identical in production and in
the (DB-less) test suite, per the "AI components / storage should be
swappable" engineering rule.
"""
import json
from typing import List, Optional

from sqlalchemy.types import JSON, TypeDecorator, UserDefinedType


class _PGVectorFallback(UserDefinedType):
    """Minimal stand-in used only when pgvector's real type isn't installed."""

    def get_col_spec(self, **kw):
        return "VECTOR"


try:
    from pgvector.sqlalchemy import Vector as _PGVector
except ImportError:  # pgvector python package not installed in this environment
    _PGVector = _PGVectorFallback


class Vector(TypeDecorator):
    """Portable vector type: pgvector on Postgres, JSON list on everything else."""

    impl = JSON
    cache_ok = True

    def __init__(self, dim: int, *args, **kwargs):
        self.dim = dim
        super().__init__(*args, **kwargs)

    def load_dialect_impl(self, dialect):
        if dialect.name == "postgresql":
            return dialect.type_descriptor(_PGVector(self.dim))
        return dialect.type_descriptor(JSON())

    def process_bind_param(self, value: Optional[List[float]], dialect):
        if value is None:
            return None
        if dialect.name == "postgresql":
            return value
        return json.dumps(list(value))

    def process_result_value(self, value, dialect):
        if value is None:
            return None
        if dialect.name == "postgresql":
            return list(value)
        return json.loads(value) if isinstance(value, str) else value
