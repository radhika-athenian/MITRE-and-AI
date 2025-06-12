from fastapi.testclient import TestClient
from services.ingest.app.main import app

client = TestClient(app)

def test_receive_alert():
    payload = {"id": "1", "description": "test", "severity": 5}
    response = client.post("/alerts", json=payload)
    assert response.status_code == 200
    assert response.json() == {"status": "received"}

