from datetime import date

from pydantic import BaseModel, ConfigDict, Field


class AuthorBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    date_of_birth: date | None = None


class AuthorCreate(AuthorBase):
    pass


class AuthorRead(AuthorBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
