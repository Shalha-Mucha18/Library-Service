import logging

from app.core.celery_app import celery_app
from app.core.db import session_scope
from app.services.book_service import archive_books_older_than

logger = logging.getLogger(__name__)


@celery_app.task(name="app.tasks.archive_outdated_books")
def archive_outdated_books(years: int = 10) -> int:
    """Archive books published more than `years` ago."""
    with session_scope() as session:
        updated = archive_books_older_than(session, years=years)
        if updated:
            logger.info("Archived %s outdated books.", updated)
        else:
            logger.debug("No books required archiving at this run.")
        return updated
