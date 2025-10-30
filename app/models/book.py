from datetime import date

from sqlalchemy import Boolean, Column, Date, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.core.db import Base


class Book(Base):
    """Book persistence model."""

    __tablename__ = "books"
    __table_args__ = (
        {"sqlite_autoincrement": True},
    )

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    genre = Column(String(100), nullable=True, index=True)
    published_date = Column(Date, nullable=True)
    is_archived = Column(Boolean, nullable=False, default=False, index=True)
    author_id = Column(Integer, ForeignKey("authors.id", ondelete="CASCADE"), nullable=False, index=True)

    author = relationship("Author", back_populates="books", lazy="joined")

    def __repr__(self) -> str:
        return f"<Book id={self.id} title={self.title!r} archived={self.is_archived}>"
