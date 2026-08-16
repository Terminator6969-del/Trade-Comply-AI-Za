"""
Celery application configuration for background tasks.
Used for async job processing (document extraction, classification, etc.)
"""

from celery import Celery

from app.core.config import settings

# Create Celery app
celery_app = Celery(
    "tradecomply",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
)

# Configure Celery
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 minutes hard limit
    task_soft_time_limit=25 * 60,  # 25 minutes soft limit
)


@celery_app.task(bind=True)
def debug_task(self):
    """Debug task for testing Celery."""
    print(f"Request: {self.request!r}")
