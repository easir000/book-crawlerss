from fastapi import APIRouter, Depends, Query, Request, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from app.models.book import BookResponse
from app.core.security import verify_api_key
from app.core.rate_limiter import limiter
from app.core.config import MONGODB_URL, MONGODB_DB_NAME
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)

router = APIRouter(dependencies=[Depends(verify_api_key)])


# === LIST endpoint: GET /books ===
@router.get("", response_model=List[BookResponse])
@limiter.limit("100/hour")
async def get_books(
    request: Request,
    category: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    rating: Optional[int] = Query(None, ge=1, le=5),
    sort_by: str = "rating",
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    _=Depends(verify_api_key)
):
    valid_sort_fields = {"rating", "price", "reviews"}
    if sort_by not in valid_sort_fields:
        raise HTTPException(status_code=400, detail="Invalid sort_by parameter")

    query = {}
    if category:
        query["category"] = category
    if min_price is not None or max_price is not None:
        price_filter = {}
        if min_price is not None:
            price_filter["$gte"] = min_price
        if max_price is not None:
            price_filter["$lte"] = max_price
        query["price_incl_tax"] = price_filter
    if rating is not None:
        query["rating"] = rating

    sort_field_map = {
        "rating": "rating",
        "price": "price_incl_tax",
        "reviews": "num_reviews"
    }
    db_sort_field = sort_field_map[sort_by]

    client = AsyncIOMotorClient(MONGODB_URL)
    try:
        db = client[MONGODB_DB_NAME]
        cursor = db.books.find(query).sort(db_sort_field, -1)
        skip = (page - 1) * size
        books = await cursor.skip(skip).limit(size).to_list(length=size)

        for book in books:
            if "_id" in book:
                book["id"] = str(book["_id"])
                del book["_id"]
        return books
    except Exception as e:
        logger.error(f"Database error in get_books: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
    finally:
        client.close()


# === DETAIL endpoint: GET /books/{id} ===
@router.get("/{book_id}", response_model=BookResponse)
@limiter.limit("100/hour")
async def get_book_by_id(
    request: Request,
    book_id: str,
    _=Depends(verify_api_key)
):
    if not ObjectId.is_valid(book_id):
        raise HTTPException(status_code=400, detail="Invalid book ID")

    client = AsyncIOMotorClient(MONGODB_URL)
    try:
        db = client[MONGODB_DB_NAME]
        book = await db.books.find_one({"_id": ObjectId(book_id)})
        if not book:
            raise HTTPException(status_code=404, detail="Book not found")

        book["id"] = str(book["_id"])
        del book["_id"]
        return book
    except Exception as e:
        logger.error(f"Database error in get_book_by_id: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
    finally:
        client.close()