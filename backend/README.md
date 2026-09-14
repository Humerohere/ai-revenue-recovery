# Backend

FastAPI application, Celery worker, and database migrations.

```
app/
  api/            dashboard REST API (JWT, scoped to one shop)
  webhooks/       Twilio voice + SMS entrypoints
  services/       deterministic business rules
  ai/             LLM provider abstraction
  integrations/   Twilio and Google Calendar clients
  workers/        Celery app and tasks
  db/             SQLAlchemy models and session
alembic/          database migrations (run from this directory)
```

Tests live in the repository-root `tests/` directory, not here.
