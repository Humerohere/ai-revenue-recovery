"""FastAPI application entrypoint."""

from fastapi import FastAPI

from app.api.v1.router import api_router
from app.api.v1.routes import health
from app.core.config import get_settings

settings = get_settings()

app = FastAPI(
    title="AI Revenue Recovery",
    version="0.1.0",
    docs_url="/docs" if settings.app_env != "production" else None,
)

app.include_router(health.router)
app.include_router(api_router, prefix="/api/v1")

# Twilio webhook routers are mounted here as M1/M2 land:
#   app.include_router(twilio_voice.router)
#   app.include_router(twilio_sms.router)
