"""Shared test fixtures.

Tests never touch Twilio, an LLM, or Google -- fakes are injected for all three.
"""

import os

import pytest

os.environ.setdefault("APP_ENV", "test")
os.environ.setdefault("DATABASE_URL", "postgresql+psycopg://arr:arr@localhost:5432/arr_test")
os.environ.setdefault("REDIS_URL", "redis://localhost:6379/15")
os.environ.setdefault("CELERY_BROKER_URL", "redis://localhost:6379/14")
os.environ.setdefault("SECRET_KEY", "test-secret-key")
os.environ.setdefault("ENCRYPTION_KEY", "dGVzdC1lbmNyeXB0aW9uLWtleS0zMi1ieXRlcy1wYWQ=")
os.environ.setdefault("AI_PROVIDER", "fake")
os.environ.setdefault("TWILIO_VALIDATE_SIGNATURE", "false")


@pytest.fixture
async def client():
    """HTTP client bound to the app (no running server)."""
    from httpx import ASGITransport, AsyncClient

    from app.main import app

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c
