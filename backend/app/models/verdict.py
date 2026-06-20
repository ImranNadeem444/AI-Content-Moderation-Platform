from pydantic import BaseModel
from typing import List, Optional


class VerdictCategory(BaseModel):
    category: str
    result: bool
    confidence: float
    reason: str


class Verdict(BaseModel):
    id: Optional[str] = None
    submission_id: str
    overall_outcome: str
    categories: List[VerdictCategory]