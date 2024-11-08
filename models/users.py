from sqlmodel import SQLModel, Field
from typing import Optional


class UserBase(SQLModel):
    name: str = Field(default=None)
    description: str = Field(default=None)
    email: str = Field(default=None)
    role_id: Optional[int] = Field(default=None)


class UserCreate(UserBase):
    pass


class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
