import hashlib
import json

def compute_fingerprint(book_data: dict) -> str:
    core = {
        "title": book_data.get("title", ""),
        "price_incl_tax": book_data.get("price_incl_tax", 0.0),
        "availability_count": book_data.get("availability_count", 0),
        "rating": book_data.get("rating", 0)
    }
    blob = json.dumps(core, sort_keys=True, default=str)
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()