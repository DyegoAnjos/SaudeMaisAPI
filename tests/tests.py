from fastapi.testclient import TestClient
from fastapi_saudemaisapi.app import app


def test_app():
    client = TestClient(app)
    response = client.get('/')

    assert response.json() == {'hello': 'world'}
