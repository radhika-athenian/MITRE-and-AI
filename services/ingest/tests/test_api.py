from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_post_alerts():
    payload = {"id": "1", "description": "test alert", "severity": 5}
    response = client.post("/alerts", json=payload)
    assert response.status_code == 200
    assert response.json() == {"status": "received"}
