"""
Upload safety helpers: extension allow-list, size limit, and safe filename
generation (never trust the client-supplied filename).
"""
import os
import uuid

from app.core.config import settings


class InvalidFileError(Exception):
    pass


def validate_extension(filename: str) -> str:
    ext = os.path.splitext(filename)[1].lower()
    if ext not in settings.allowed_extensions_list:
        raise InvalidFileError(
            f"Unsupported file extension '{ext}'. Allowed: {', '.join(settings.allowed_extensions_list)}"
        )
    return ext


def validate_size(content: bytes) -> None:
    max_bytes = settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024
    if len(content) > max_bytes:
        raise InvalidFileError(f"File exceeds the {settings.MAX_UPLOAD_SIZE_MB}MB upload limit")
    if len(content) == 0:
        raise InvalidFileError("Uploaded file is empty")


def safe_filename(original_filename: str, ext: str) -> str:
    """Generate a random, collision-free filename. The original filename is
    never used to build a filesystem path (protects against path traversal /
    injection via crafted filenames)."""
    return f"{uuid.uuid4().hex}{ext}"
