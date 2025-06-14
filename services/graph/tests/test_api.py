from fastapi.testclient import TestClient
from app.main import app, graph

client = TestClient(app)

def test_update_graph():
    response = client.post('/graph/update', json={'source': 'a', 'target': 'b'})
    assert response.status_code == 200
    assert response.json()['status'] == 'updated'
    assert graph.number_of_edges() == 1

def test_read_graph():
    client.post('/graph/update', json={'source': 'x', 'target': 'y'})
    response = client.get('/graph')
    assert response.status_code == 200
    data = response.json()
    assert 'nodes' in data and 'links' in data
