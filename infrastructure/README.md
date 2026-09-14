# Infrastructure

Everything about *running* the system, kept out of the application code.

```
docker/backend.Dockerfile   image for both the API and the Celery worker
```

The build context is the repository root (see `docker-compose.yml`), which is why
the Dockerfile's COPY paths start with `backend/`.

Local stack: `docker compose up --build` from the repository root.
CI lives in `.github/workflows/` because GitHub requires that path.

Deployment targets and secrets management are decided at M5, not before.
