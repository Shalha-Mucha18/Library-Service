# Library Service API

A production-ready FastAPI application that powers an online library system. It provides CRUD endpoints for authors and books, supports filtering, integrates caching for read-heavy operations, and runs a scheduled background task (Celery) that archives books published more than 10 years ago.

## Features

- FastAPI REST endpoints with Pydantic validation and serialization.
- SQLAlchemy ORM models and session management.
- Query filtering via request parameters (`author_name`).
- Cache-aware list endpoints using Redis (with in-memory fallback).
- Periodic Celery beat task that archives outdated books.
- Configurable settings via environment variables.

## Tech Stack

- Python 3.10+
- FastAPI & Uvicorn
- SQLAlchemy
- Pydantic v2 & pydantic-settings
- fastapi-cache2
- Redis (cache and Celery broker/result backend)
- Celery + Celery beat

## Getting Started


1. **Create a virtual environment**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. **Install dependencies**
   ```bash
   pip install fastapi uvicorn[standard] SQLAlchemy fastapi-cache2 redis celery python-dotenv pydantic-settings
   ```

3. **(Optional) Configure environment**

   Copy `.env.example` to `.env` if you create one, then override settings like `DATABASE_URL`, `REDIS_URL`, etc.

4. **Run database migrations**

   This project uses SQLAlchemy models and auto-creates tables on startup. No manual migration step is required.

5. **Start services**

   - FastAPI app:
     ```bash
     uvicorn app:main:app --reload
     ```
   - Celery worker with beat (separate terminal):
     ```bash
     celery -A app.core.celery_app.celery_app worker -B --loglevel=info
     ```

   Ensure Redis is running and accessible at the configured URL.

## API Overview

- `POST /api/v1/authors/` — create an author.
- `GET /api/v1/authors/` — list authors.
- `GET /api/v1/authors/{id}` — retrieve author.
- `POST /api/v1/books/` — create a book.
- `GET /api/v1/books/` — list books (filterable by `author_name` query parameter).
- `GET /api/v1/books/{id}` — retrieve book.
- `GET /health` — health check endpoint.

## Background Task

Celery beat schedules `app.tasks.archive_outdated_books` every 30 minutes. The task marks books older than 10 years as archived. You can call it manually:

```bash
celery -A app.core.celery_app.celery_app call app.tasks.archive_outdated_books --args='[10]'
```

## Testing the API

With the server running, open the interactive docs:

- Swagger UI: <http://127.0.0.1:8000/docs>
- ReDoc: <http://127.0.0.1:8000/redoc>

Use `curl`, `HTTPie`, or any REST client for manual testing.

## Project Structure

```
app/
├── api/          # FastAPI routers & dependencies
├── core/         # config, database, celery
├── models/       # SQLAlchemy models
├── schemas/      # Pydantic DTOs
├── services/     # business logic
└── tasks/        # Celery tasks
main.py           # ASGI entrypoint (imports app factory)
```

## Next Steps

- Add Alembic migrations if schema evolution is expected.
- Extend CRUD to include update/delete operations.
- Add authentication/authorization if needed.
