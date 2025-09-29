# app/api/main.py
from fastapi import FastAPI
from dotenv import load_dotenv
import os
from fastapi.middleware.cors import CORSMiddleware
from app.core.rate_limiter import limiter
from app.api.routes import books, changes

from dotenv import load_dotenv

load_dotenv()

# Validate critical config
if not os.getenv("API_KEY"):
    raise RuntimeError("API_KEY not set in environment")

app = FastAPI(
    title="Book Crawler API",
    description="RESTful API for books.toscrape.com data with authentication and change tracking.",
    version="1.0.0"
)

# Rate limiting
app.state.limiter = limiter

# CORS (optional)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(books.router, prefix="/books", tags=["Books"])
app.include_router(changes.router, prefix="/changes", tags=["Changes"])

# Health check
@app.get("/health")
async def health():
    return {"status": "ok"}