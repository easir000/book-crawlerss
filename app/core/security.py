# app/core/security.py
from fastapi import HTTPException, Security, status
from fastapi.security import APIKeyHeader
import os

# Load config AFTER .env is loaded
from app.core.config import MONGODB_URL  # This ensures load_dotenv() ran

API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise RuntimeError("API_KEY not set in environment. Check .env file.")

api_key_header = APIKeyHeader(name="X-API-Key")

def verify_api_key(api_key: str = Security(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API key"
        )