from pydantic import BaseModel
from typing import Optional


class UserBase(BaseModel):
    name: str
    description: str
    email: str


class UserCreate(UserBase):
    pass


class UserUpdate(UserBase):
    name: Optional[str]
    description: Optional[str]
    email: Optional[str]
