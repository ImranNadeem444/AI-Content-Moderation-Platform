from pydantic import BaseModel


class AppealCreate(BaseModel):
    submission_id: str
    reason: str