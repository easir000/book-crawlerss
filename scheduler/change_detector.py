# scheduler/change_detector.py
import hashlib
import json
import logging
from datetime import datetime
from crawler.storage import db

# Alert logger setup
alert_logger = logging.getLogger("alerts")
if not alert_logger.handlers:
    handler = logging.FileHandler("alerts.log")
    alert_logger.addHandler(handler)
    alert_logger.setLevel(logging.WARNING)

def compute_fingerprint(book_dict: dict) -> str:  # ← Line 23: FIXED PARAM NAME & PARENTHESIS
    """Generate SHA-256 fingerprint of key book fields."""
    core = {
        "title": book_dict.get("title", ""),
        "price_incl_tax": book_dict.get("price_incl_tax", 0.0),
        "availability_count": book_dict.get("availability_count", 0),
        "rating": book_dict.get("rating", 0),
    }
    blob = json.dumps(core, sort_keys=True, default=str)
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()

async def detect_and_log_changes(current_book: dict):
    """Detect changes and log to database."""
    # ← USE current_book (function parameter), NOT book_data
    current_book["fingerprint"] = compute_fingerprint(current_book)  # Line 26
    current_book["crawled_at"] = current_book.get("crawled_at") or datetime.utcnow()

    existing = await db.books.find_one({"url": current_book["url"]})  # Line 29

    if not existing:
        await db.books.insert_one(current_book)
        await db.change_log.insert_one({
            "book_url": current_book["url"],
            "change_type": "new",
            "detected_at": current_book["crawled_at"],
            "details": {"title": current_book["title"]}
        })
    elif existing.get("fingerprint") != current_book["fingerprint"]:
        # Updated book
        await db.books.replace_one({"url": current_book["url"]}, current_book)
        # Log specific field changes (simplified)
        changes = {}
        for field in ["price_incl_tax", "availability_count", "rating"]:
            if existing.get(field) != current_book[field]:
                changes[field] = {
                    "old": existing.get(field),
                    "new": current_book[field]
                }
        await db.change_log.insert_one({
            "book_url": current_book["url"],
            "change_type": "updated",
            "detected_at": current_book["crawled_at"],
            "changes": changes
        })