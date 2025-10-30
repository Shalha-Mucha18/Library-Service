from collections.abc import Sequence

from fastapi import APIRouter, Depends, Query, status
from fastapi_cache import FastAPICache
from fastapi_cache.decorator import cache
from sqlalchemy.orm import Session

from app.api import deps
from app.core.config import settings
from app.schemas import BookCreate, BookFilter, BookRead
from app.services import book_service

router = APIRouter()


@router.post("/", response_model=BookRead, status_code=status.HTTP_201_CREATED)
async def create_book(
    payload: BookCreate,
    db: Session = Depends(deps.get_db),
) -> BookRead:
    """Create a new book."""
    book = book_service.create_book(db, payload)
    # Invalidate cached book listings to reflect the new record.
    try:
        FastAPICache.get_backend()
        await FastAPICache.clear(namespace="books")
    except RuntimeError:
        # Cache backend not initialised yet; nothing to invalidate.
        pass
    return BookRead.from_orm(book)


@router.get("/", response_model=list[BookRead])
@cache(expire=settings.CACHE_DEFAULT_EXPIRE_SECONDS, namespace="books")
async def list_books(
    author_name: str | None = Query(default=None, description="Filter books by author name."),
    db: Session = Depends(deps.get_db),
) -> Sequence[BookRead]:
    """List books with optional filtering by author name."""
    filters = BookFilter(author_name=author_name)
    books = book_service.list_books(db, filters=filters)
    return [BookRead.from_orm(book) for book in books]


@router.get("/{book_id}", response_model=BookRead)
async def get_book(
    book_id: int,
    db: Session = Depends(deps.get_db),
) -> BookRead:
    """Retrieve a single book."""
    book = book_service.get_book(db, book_id)
    return BookRead.from_orm(book)
