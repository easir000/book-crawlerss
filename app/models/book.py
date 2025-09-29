# app/models/book.py
from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime

# === Model used during crawling (stored in DB) ===
class Book(BaseModel):
    url: str
    title: str
    description: Optional[str] = None
    category: str
    price_excl_tax: float
    price_incl_tax: float
    availability_raw: str
    availability_count: int
    num_reviews: int
    image_url: str
    rating: int = Field(ge=1, le=5)
    raw_html: str
    crawled_at: datetime
    status: str = "success"

    @field_validator('rating', mode='before')
    def parse_rating(cls, v):
        if isinstance(v, int):
            return v
        if isinstance(v, str):
            word = v.split()[-1] if v else "Zero"
            mapping = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
            return mapping.get(word, 0)
        return 0


# === Model used in API responses ===
class BookResponse(BaseModel):
    id: str
    url: str
    title: str
    description: Optional[str] = None
    category: str
    price_excl_tax: float
    price_incl_tax: float
    availability_count: int
    num_reviews: int
    image_url: str
    rating: int
    crawled_at: datetime