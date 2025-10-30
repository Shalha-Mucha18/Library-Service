from datetime import date

from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.orm import relationship

from app.core.db import Base


class Author(Base):
    """Author persistence model."""

    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True, index=True)
    date_of_birth = Column(Date, nullable=True)

    books = relationship("Book", back_populates="author", lazy="selectin")

    def __repr__(self) -> str:
        return f"<Author id={self.id} name={self.name!r} dob={self.date_of_birth}>"
