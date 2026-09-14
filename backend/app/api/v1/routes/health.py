"""Liveness and readiness probes."""

from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/health/ready")
async def ready() -> dict[str, str]:
    # M0 stub: M1 adds real Postgres + Redis checks.
    return {"status": "ok"}
