from fastapi.testclient import TestClient
from app.api.main import app

API_KEY = "xT2fG9vLpQ8zRnK4mW7sY1aB3cE6hJ0u"

def test_invalid_api_key():
    client = TestClient(app)
    response = client.get("/books", headers={"X-API-Key": "wrong"})
    assert response.status_code == 403

def test_books_endpoint():
    client = TestClient(app)
    response = client.get("/books", headers={"X-API-Key": API_KEY})
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if len(data) > 0:
        assert "title" in data[0]
        assert "id" in data[0]  # Must have id from _id