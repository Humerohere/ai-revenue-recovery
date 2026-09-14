"""Application settings. Every secret comes from the environment; nothing is hardcoded."""

from functools import lru_cache
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_env: Literal["local", "test", "staging", "production"] = "local"
    log_level: str = "INFO"
    public_base_url: str = "http://localhost:8000"

    # Infrastructure
    database_url: str
    redis_url: str
    celery_broker_url: str

    # Security -- no defaults on purpose: the app must refuse to boot without them.
    secret_key: str
    encryption_key: str
    access_token_expire_minutes: int = 60

    # Twilio
    twilio_account_sid: str = ""
    twilio_auth_token: str = ""
    twilio_validate_signature: bool = True

    # AI
    ai_provider: Literal["anthropic", "openai", "fake"] = "anthropic"
    ai_model: str = "claude-sonnet-5"
    anthropic_api_key: str = ""
    openai_api_key: str = ""
    max_ai_turns: int = 12

    # Google Calendar
    google_client_id: str = ""
    google_client_secret: str = ""
    google_redirect_uri: str = ""

    # Deterministic business rules
    missed_call_min_seconds: int = 10
    quiet_hours_start: int = 21
    quiet_hours_end: int = 8


@lru_cache
def get_settings() -> Settings:
    return Settings()  # type: ignore[call-arg]
