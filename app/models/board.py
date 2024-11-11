from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from .boards import Boards


class Board(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(default=None)
    role: int = Field(default=None)
    descripcion: str = Field(default=None)
    users: List["User"] = Relationship(back_populates="boards", link_model=Boards)
