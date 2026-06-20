from pydantic import BaseModel
from typing import List


class SubmissionCreate(BaseModel):
    images: List[str]