from collections.abc import Sequence
from datetime import date, timedelta

from fastapi import HTTPException, status
from sqlalchemy import and_, func, select, update
from sqlalchemy.orm import Session, selectinload

from app.models import Author, Book
from app.schemas import BookCreate, BookFilter


def create_book(db: Session, data: BookCreate) -> Book:
    """Create a new book ensuring the author exists."""
    author = db.get(Author, data.author_id)
    if not author:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Author not found.")

    book = Book(
        title=data.title,
        author_id=data.author_id,
        published_date=data.published_date,
        genre=data.genre,
    )
    db.add(book)
    db.flush()
    db.refresh(book)
    db.refresh(book, attribute_names=["author"])
    return book


def get_book(db: Session, book_id: int) -> Book:
    """Retrieve a book by identifier."""
    stmt = select(Book).options(selectinload(Book.author)).where(Book.id == book_id)
    book = db.execute(stmt).scalar_one_or_none()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found.")
    return book


def list_books(db: Session, filters: BookFilter | None = None) -> Sequence[Book]:
    """Return filtered books sorted by publication date descending."""
    filters = filters or BookFilter()
    stmt = select(Book).options(selectinload(Book.author)).order_by(
        Book.published_date.desc(), Book.title.asc()
    )

    if filters.author_name:
        stmt = stmt.join(Book.author).where(
            func.lower(Author.name).contains(filters.author_name.lower())
        )

    return db.execute(stmt).scalars().all()


def archive_books_older_than(db: Session, years: int = 10) -> int:
    """Archive books that were published more than `years` ago."""
    cutoff_date = date.today() - timedelta(days=years * 365)
    stmt = (
        update(Book)
        .where(
            and_(
                Book.published_date.is_not(None),
                Book.published_date <= cutoff_date,
                Book.is_archived.is_(False),
            )
        )
        .values(is_archived=True)
        .execution_options(synchronize_session=False)
    )
    result = db.execute(stmt)
    return result.rowcount or 0
