import os
from dotenv import load_dotenv

load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
MONGODB_DB_NAME = os.getenv("MONGODB_DB_NAME", "books_db")
CRAWL_CONCURRENCY = int(os.getenv("CRAWL_CONCURRENCY", 10))
BASE_URL = "https://books.toscrape.com/"