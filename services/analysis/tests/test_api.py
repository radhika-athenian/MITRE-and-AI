from fastapi.testclient import TestClient
from app.main import app, graph

client = TestClient(app)

def test_add_edge():
    response = client.post('/analysis/edge', json={'source': 'a', 'target': 'b'})
    assert response.status_code == 200
    assert graph.number_of_edges() == 1


def test_get_paths():
    client.post('/analysis/edge', json={'source': 'b', 'target': 'c'})
    response = client.get('/analysis/path', params={'source': 'a', 'target': 'c', 'k': 2})
    assert response.status_code == 200
    data = response.json()
    assert len(data['paths']) >= 1
