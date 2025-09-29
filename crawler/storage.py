# crawler/storage.py
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from crawler.config import MONGODB_URL, MONGODB_DB_NAME

class Database:
    def __init__(self):
        self._client: AsyncIOMotorClient | None = None
        self._db: AsyncIOMotorDatabase | None = None

    async def connect(self):
        self._client = AsyncIOMotorClient(MONGODB_URL)
        self._db = self._client[MONGODB_DB_NAME]
        # Create indexes
        await self.books.create_index("url", unique=True)
        await self.books.create_index([
            ("category", 1),
            ("price_incl_tax", 1),
            ("rating", 1)
        ])
        await self.change_log.create_index("detected_at")

    async def close(self):
        if self._client:
            self._client.close()

    @property
    def books(self):
        if self._db is None:
            raise RuntimeError("Database not connected. Call connect() first.")
        return self._db.books

    @property
    def change_log(self):
        if self._db is None:
            raise RuntimeError("Database not connected. Call connect() first.")
        return self._db.change_log

# Singleton instance
db = Database()