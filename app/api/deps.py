from collections.abc import Generator

from sqlalchemy.orm import Session

from app.core.db import get_session


def get_db() -> Generator[Session, None, None]:
    """Dependency that returns a managed database session."""
    yield from get_session()
