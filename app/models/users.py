from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from app.models.boardusers import BoardUsers


class UserBase(SQLModel):
    name: str
    description: str
    email: str


class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    dashboard: "Dashboard" = Relationship(back_populates="user")
    boards: List["Board"] = Relationship(back_populates="users", link_model=BoardUsers)
