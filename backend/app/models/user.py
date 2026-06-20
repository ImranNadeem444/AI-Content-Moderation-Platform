from pydantic import BaseModel, EmailStr
from typing import Optional


class User(BaseModel):
    id: Optional[str] = None
    name: str
    email: EmailStr
    password: str
    role: str = "user"