"""Smoke test: the app boots and answers its liveness probe."""


async def test_health_ok(client):
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
