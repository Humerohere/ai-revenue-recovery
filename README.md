# Revive

Missed call → SMS → AI conversation → qualified lead → booked appointment →
shop notified. Built for independent US auto repair shops.

Product context and engineering rules live in [CLAUDE.md](CLAUDE.md).
The MVP implementation plan lives in [docs/PLAN.md](docs/PLAN.md).

## Status

**M0 — skeleton.** Structure, config, infra and CI are in place; business logic
is stubbed with a pointer to the milestone that fills it in.

## Layout

```
revive/
├── backend/            FastAPI app, Celery worker, Alembic migrations
├── frontend/           Next.js dashboard (starts at M4)
├── infrastructure/     Dockerfiles and deployment config
├── docs/               PLAN.md and design notes
├── tests/              unit + integration tests for the backend
├── CLAUDE.md
├── README.md
├── .env.example
└── docker-compose.yml
```

Two files sit at the root that the tree above leaves implicit: `pyproject.toml`
(ruff, mypy and pytest config, with `pythonpath = ["backend"]` so tests import
`app.*` directly) and `.github/workflows/ci.yml` (GitHub requires that path).

## Local setup

```bash
cp .env.example .env          # then fill in secrets
python -m venv .venv
.venv/Scripts/activate        # Windows; use source .venv/bin/activate elsewhere
pip install -r backend/requirements-dev.txt

docker compose up -d db redis
cd backend && alembic upgrade head && cd ..
uvicorn app.main:app --reload --app-dir backend
```

Or run everything in containers: `docker compose up --build`.

Exposing webhooks to Twilio during development needs a tunnel
(`ngrok http 8000`); put the public URL in `PUBLIC_BASE_URL`.

## Checks

```bash
ruff check .
ruff format --check .
mypy backend/app
pytest
```

## Rules enforced by code, not by prompt

- The LLM has no pricing tool, so it cannot quote a price.
- `book_appointment` rejects any slot id that did not come from `get_available_slots`.
- Lead qualification is a pure function, never the model's judgement.
- STOP/HELP and the opt-out list are handled before the model sees a message.
