from fastapi.testclient import TestClient
from services.graph.app.main import app, graph, update_graph, init_db, load_graph


def test_update_graph():
    init_db()
    load_graph()
    graph.clear()
    alert = {"technique_id": "T1000", "asset_id": "asset-1"}
    update_graph(alert)
    assert "tech:T1000" in graph.nodes
    assert "asset:asset-1" in graph.nodes
    assert graph.has_edge("asset:asset-1", "tech:T1000")


def test_get_nodes_endpoint():
    init_db()
    load_graph()
    graph.clear()
    alert = {"technique_id": "T1001", "asset_id": "asset-2"}
    update_graph(alert)
    client = TestClient(app)
    response = client.get("/nodes")
    assert response.status_code == 200
    body = response.json()
    assert "tech:T1001" in body
    assert "asset:asset-2" in body