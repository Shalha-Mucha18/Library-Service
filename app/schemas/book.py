from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.schemas.author import AuthorRead


class BookBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    author_id: int = Field(..., gt=0)
    genre: Optional[str] = Field(default=None, max_length=100)
    published_date: Optional[date] = None


class BookCreate(BookBase):
    pass


class BookRead(BookBase):
    id: int
    is_archived: bool
    author: AuthorRead

    model_config = ConfigDict(from_attributes=True)


class BookFilter(BaseModel):
    author_name: Optional[str] = Field(default=None, max_length=255)

    @field_validator("author_name", mode="before")
    @classmethod
    def normalize_author_name(cls, value: Optional[str]) -> Optional[str]:
        if value:
            value = value.strip()
            return value or None
        return value
