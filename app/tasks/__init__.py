"""Celery tasks package."""

from .books import archive_outdated_books

__all__ = ["archive_outdated_books"]
