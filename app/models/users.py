from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from .board import Board
from .boards import Boards


class UserBase(SQLModel):
    name: str = Field(default=None)
    description: str = Field(default=None)
    email: str = Field(default=None)


class UserCreate(UserBase):
    pass


class UserUpdate(UserBase):
    pass


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    boards: list[Board] = Relationship(back_populates="users", link_model=Boards)
