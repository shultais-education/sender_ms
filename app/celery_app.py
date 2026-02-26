from celery import Celery
from app.core.config import settings


celery_app = Celery(
    "worker",
    broker=settings.celery_broker_url,
    backend=settings.celery_results_backend
)

celery_app.conf.update(
    timezone=settings.CELERY_TIMEZONE
)

celery_app.autodiscover_tasks(["app"])
