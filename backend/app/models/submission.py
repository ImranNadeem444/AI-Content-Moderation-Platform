from pydantic import BaseModel
from typing import List, Optional


class Submission(BaseModel):
    id: Optional[str] = None
    user_id: str
    images: List[str]
    outcome: str
    verdict_id: Optional[str] = None