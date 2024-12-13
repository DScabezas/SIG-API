from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from app.models.catalogs import Catalog
from app.models.dboards import DBoards
from app.models.users import User
from app.models.utils import Icon


class BoardBase(SQLModel):
    name: str
    icon_id: Optional[int] = Field(foreign_key="icon.id")


class Board(BoardBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    users: List["User"] = Relationship(back_populates="boards", link_model=DBoards)
    catalogs: List["Catalog"] = Relationship(back_populates="board")
    icon: Optional["Icon"] = Relationship(back_populates="board")
