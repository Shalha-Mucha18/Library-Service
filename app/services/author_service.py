from collections.abc import Sequence

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Author
from app.schemas import AuthorCreate


def create_author(db: Session, data: AuthorCreate) -> Author:
    """Create a new author ensuring name uniqueness."""
    existing_author = db.execute(select(Author).where(Author.name == data.name)).scalar_one_or_none()
    if existing_author:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Author with this name already exists.",
        )
    author = Author(name=data.name, date_of_birth=data.date_of_birth)
    db.add(author)
    db.flush()
    db.refresh(author)
    return author


def get_author(db: Session, author_id: int) -> Author:
    """Retrieve an author by identifier."""
    author = db.get(Author, author_id)
    if not author:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Author not found.")
    return author


def list_authors(db: Session) -> Sequence[Author]:
    """Return all authors ordered by name."""
    stmt = select(Author).order_by(Author.name.asc())
    return db.execute(stmt).scalars().all()
