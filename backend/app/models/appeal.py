from pydantic import BaseModel
from typing import Optional


class Appeal(BaseModel):
    id: Optional[str] = None
    submission_id: str
    user_id: str
    reason: str
    status: str = "Pending"