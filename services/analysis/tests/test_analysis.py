from fastapi.testclient import TestClient
from services.analysis.app.main import app, update_graph, top_paths


def test_update_and_paths():
    update_graph({"technique_id": "T1111", "asset_id": "asset-x"})
    assert top_paths


def test_get_top_paths_endpoint():
    client = TestClient(app)
    update_graph({"technique_id": "T1112", "asset_id": "asset-y"})
    response = client.get("/top-paths")
    assert response.status_code == 200
    assert isinstance(response.json(), list)