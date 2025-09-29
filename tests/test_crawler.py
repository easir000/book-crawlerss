import pytest
from app.models.book import Book

def test_book_model():
    data = {
        "url": "http://test",
        "title": "Test Book",
        "category": "Fiction",
        "price_excl_tax": 10.99,
        "price_incl_tax": 10.99,
        "availability_raw": "In stock (5 available)",
        "availability_count": 5,
        "num_reviews": 0,
        "image_url": "http://test.jpg",
        "rating": "star-rating Three",
        "raw_html": "<html></html>",
        "crawled_at": "2024-01-01T00:00:00Z"
    }
    book = Book(**data)
    assert book.rating == 3
    assert book.title == "Test Book"