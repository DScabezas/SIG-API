from sqlmodel import Relationship, SQLModel, Field
from typing import List, Optional

from app.models.boardusers import BoardUsers


class UserBase(SQLModel):
    name: Optional[str] = None
    description: Optional[str] = None
    email: Optional[str] = None


class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    dashboard: "Dashboard" = Relationship(back_populates="users")
    boards: List["Board"] = Relationship(back_populates="users", link_model=BoardUsers)
