from fastapi import APIRouter

from app.api.routes import authors, books

api_router = APIRouter()
api_router.include_router(authors.router, prefix="/authors", tags=["authors"])
api_router.include_router(books.router, prefix="/books", tags=["books"])

__all__ = ["api_router"]
