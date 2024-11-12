from sqlmodel import SQLModel, Field
from typing import Optional


class UserBase(SQLModel):
    name: str
    description: str
    email: str


class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
