# app/core/config.py
import os
from dotenv import load_dotenv

load_dotenv()  # ← Critical: loads .env at import time

MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
MONGODB_DB_NAME = os.getenv("MONGODB_DB_NAME", "books_db")