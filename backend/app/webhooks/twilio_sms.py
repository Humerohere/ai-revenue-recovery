"""Twilio webhook handlers: twilio_sms.

M0 stub. Contract (PLAN.md s2/s4): verify signature -> persist webhook_event for
idempotency -> enqueue Celery task -> return immediately. No business logic inline.
"""

from fastapi import APIRouter

router = APIRouter(prefix="/webhooks/twilio", tags=["webhooks"])
