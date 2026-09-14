"""Celery application.

The worker exists so Twilio webhooks can return in <100ms while AI turns and
calendar calls run with retries. No beat schedule in the MVP.
"""

from celery import Celery

from app.core.config import get_settings

_settings = get_settings()

celery_app = Celery(
    "ai_revenue_recovery",
    broker=_settings.celery_broker_url,
    backend=None,
    include=["app.workers.tasks"],
)

celery_app.conf.update(
    task_acks_late=True,
    task_reject_on_worker_lost=True,
    worker_prefetch_multiplier=1,
    task_default_retry_delay=5,
    task_time_limit=120,
)
