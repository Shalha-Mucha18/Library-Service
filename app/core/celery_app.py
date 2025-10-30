from celery import Celery

from app.core.config import settings


celery_app = Celery(
    "library_service",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=["app.tasks"],
)

celery_app.conf.update(
    timezone="UTC",
    task_default_queue="library_service",
    beat_schedule={
        "archive-old-books": {
            "task": "app.tasks.archive_outdated_books",
            "schedule": 60 * 30,  # every 30 minutes
            "options": {"expires": 60 * 20},
        }
    },
)
