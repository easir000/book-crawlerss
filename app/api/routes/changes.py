# app/api/routes/changes.py
from fastapi import APIRouter, Depends, Request
from motor.motor_asyncio import AsyncIOMotorClient
from app.core.security import verify_api_key
from app.core.config import MONGODB_URL, MONGODB_DB_NAME
from datetime import datetime, timedelta
from app.core.rate_limiter import limiter

router = APIRouter(dependencies=[Depends(verify_api_key)])

@router.get("")
@limiter.limit("100/hour")
async def get_changes(
    request: Request,  # ← REQUIRED
    _=Depends(verify_api_key)
):
    client = AsyncIOMotorClient(MONGODB_URL)
    db = client[MONGODB_DB_NAME]
    
    # Last 24 hours
    cutoff = datetime.utcnow() - timedelta(hours=24)
    changes = await db.change_log.find(
        {"detected_at": {"$gte": cutoff}}
    ).sort("detected_at", -1).to_list(length=100)
    
    # Convert ObjectId to str
    for c in changes:
        c["id"] = str(c.pop("_id"))
    return changes