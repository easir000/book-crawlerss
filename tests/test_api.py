from fastapi.testclient import TestClient
from app.api.main import app
from app.models.book import BookResponse

API_KEY = "xT2fG9vLpQ8zRnK4mW7sY1aB3cE6hJ0l"

def test_invalid_api_key():
    client = TestClient(app)
    response = client.get("/books", headers={"X-API-Key": "wrong"})
    assert response.status_code == 403

def test_books_endpoint():
    client = TestClient(app)
    response = client.get("/books?size=1", headers={"X-API-Key": API_KEY})
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if data:
        BookResponse(**data[0])  # Validate schema

def test_books_pagination():
    client = TestClient(app)
    response = client.get("/books?page=1&size=2", headers={"X-API-Key": API_KEY})
    assert response.status_code == 200
    assert len(response.json()) <= 2

def test_get_book_by_id():
    client = TestClient(app)
    response = client.get("/books/68d8f15d3596606b883a8343", headers={"X-API-Key": API_KEY})
    if response.status_code == 200:  # Only if ID exists
        assert response.json()["id"] == "68d8f15d3596606b883a8343"

def test_changes_endpoint():
    client = TestClient(app)
    response = client.get("/changes", headers={"X-API-Key": API_KEY})
    assert response.status_code == 200
    assert isinstance(response.json(), list)