from pydantic import BaseModel
from typing import Dict, Any
from datetime import datetime

class ChangeLogResponse(BaseModel):
    book_url: str
    change_type: str  # "new" or "updated"
    detected_at: datetime
    changes: Dict[str, Any] = {}
    details: Dict[str, Any] = {}