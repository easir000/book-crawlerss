# tests/test_change_detection.py
import pytest
from scheduler.change_detector import compute_fingerprint

def test_fingerprint_stability():
    """Fingerprint should be identical for identical data."""
    book = {
        "title": "Test Book",
        "price_incl_tax": 20.0,
        "availability_count": 5,
        "rating": 4
    }
    assert compute_fingerprint(book) == compute_fingerprint(book.copy())

def test_fingerprint_changes_on_price_update():
    """Fingerprint should change if price changes."""
    book1 = {"title": "Test", "price_incl_tax": 20.0, "availability_count": 5, "rating": 4}
    book2 = book1.copy()
    book2["price_incl_tax"] = 25.0
    assert compute_fingerprint(book1) != compute_fingerprint(book2)

def test_fingerprint_changes_on_availability_update():
    """Fingerprint should change if availability changes."""
    book1 = {"title": "Test", "price_incl_tax": 20.0, "availability_count": 5, "rating": 4}
    book2 = book1.copy()
    book2["availability_count"] = 0
    assert compute_fingerprint(book1) != compute_fingerprint(book2)

def test_fingerprint_ignores_non_core_fields():
    """Fingerprint should ignore fields like 'raw_html' or 'crawled_at'."""
    book1 = {"title": "Test", "price_incl_tax": 20.0, "availability_count": 5, "rating": 4}
    book2 = book1.copy()
    book2["raw_html"] = "<html>different</html>"
    book2["crawled_at"] = "2024-01-01T00:00:00Z"
    assert compute_fingerprint(book1) == compute_fingerprint(book2)

def test_fingerprint_handles_missing_fields():
    """Fingerprint should handle missing optional fields gracefully."""
    book = {"title": "Test", "price_incl_tax": 20.0}  # missing availability_count, rating
    # Should not raise an exception
    fp = compute_fingerprint(book)
    assert isinstance(fp, str)
    assert len(fp) == 64  # SHA-256