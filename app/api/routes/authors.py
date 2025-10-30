from collections.abc import Sequence

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api import deps
from app.schemas import AuthorCreate, AuthorRead
from app.services import author_service

router = APIRouter()


@router.post("/", response_model=AuthorRead, status_code=status.HTTP_201_CREATED)
def create_author(
    payload: AuthorCreate,
    db: Session = Depends(deps.get_db),
) -> AuthorRead:
    """Create a new author record."""
    author = author_service.create_author(db, payload)
    return AuthorRead.from_orm(author)


@router.get("/", response_model=list[AuthorRead])
def list_authors(
    db: Session = Depends(deps.get_db),
) -> Sequence[AuthorRead]:
    """Return all authors ordered by name."""
    authors = author_service.list_authors(db)
    return [AuthorRead.from_orm(author) for author in authors]


@router.get("/{author_id}", response_model=AuthorRead)
def get_author(
    author_id: int,
    db: Session = Depends(deps.get_db),
) -> AuthorRead:
    """Return a single author."""
    author = author_service.get_author(db, author_id)
    return AuthorRead.from_orm(author)
