from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from app.models.dboards import DBoards


class UserBase(SQLModel):
    name: Optional[str] = None
    description: Optional[str] = None
    email: Optional[str] = None


class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    dashboard: "Dashboard" = Relationship(back_populates="users")
    boards: List["Board"] = Relationship(back_populates="users", link_model=DBoards)
