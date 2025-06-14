from fastapi.testclient import TestClient
from services.ingest.app.main import Alert, app, classify_alert


client = TestClient(app)


def test_post_alerts():
    payload = {"id": "1", "description": "test alert", "severity": 5}
    response = client.post("/alerts", json=payload)
    assert response.status_code == 200
    assert response.json()["status"] == "received"
    assert "technique_id" in response.json()
    assert "asset_id" in response.json()


def test_receive_alert():
    payload = {"id": "1", "description": "test", "severity": 5}
    response = client.post("/alerts", json=payload)
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "received"
    assert "technique_id" in body
    assert "asset_id" in body


def test_classify_alert():
    alert = Alert(id="a", description="malware", severity=3)
    result = classify_alert(alert)
    assert result.technique_id == "T0001"
    assert result.asset_id == "asset-123"
