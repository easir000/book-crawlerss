# tests/test_book_model.py
import pytest
from datetime import datetime
from app.models.book import Book

def test_book_model_valid_data():
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
        "crawled_at": datetime(2024, 1, 1, 0, 0, 0)
    }
    book = Book(**data)
    assert book.rating == 3
    assert book.title == "Test Book"
    assert book.availability_count == 5

def test_book_model_rating_parsing():
    """Test rating parsing, including invalid cases (should return 0)."""
    test_cases = [
        ("star-rating One", 1),
        ("star-rating Two", 2),
        ("star-rating Three", 3),
        ("star-rating Four", 4),
        ("star-rating Five", 5),
        ("star-rating Invalid", 0),  # Invalid → 0
        ("", 0),                     # Empty → 0
        ("garbage", 0),              # Garbage → 0
        (3, 3),                      # Valid int
    ]
    for input_val, expected in test_cases:
        data = {
            "url": "http://test",
            "title": "Test",
            "category": "Fiction",
            "price_excl_tax": 10.0,
            "price_incl_tax": 10.0,
            "availability_raw": "In stock",
            "availability_count": 1,
            "num_reviews": 0,
            "image_url": "http://test.jpg",
            "rating": input_val,
            "raw_html": "<html></html>",
            "crawled_at": datetime.utcnow()
        }
        book = Book(**data)
        assert book.rating == expected

def test_book_model_missing_required_field():
    """Should raise ValidationError if required field is missing."""
    data = {
        "title": "Test Book",
        # missing "url"
        "category": "Fiction",
        "price_excl_tax": 10.99,
        "price_incl_tax": 10.99,
        "availability_raw": "In stock",
        "availability_count": 5,
        "num_reviews": 0,
        "image_url": "http://test.jpg",
        "rating": 3,
        "raw_html": "<html></html>",
        "crawled_at": datetime.utcnow()
    }
    with pytest.raises(ValueError):
        Book(**data)

def test_book_model_optional_description():
    """Should handle missing description."""
    data = {
        "url": "http://test",
        "title": "Test Book",
        "category": "Fiction",
        "price_excl_tax": 10.99,
        "price_incl_tax": 10.99,
        "availability_raw": "In stock",
        "availability_count": 5,
        "num_reviews": 0,
        "image_url": "http://test.jpg",
        "rating": 3,
        "raw_html": "<html></html>",
        "crawled_at": datetime.utcnow()
        # description is optional
    }
    book = Book(**data)
    assert book.description is None