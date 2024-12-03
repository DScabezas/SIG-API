import uuid
from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from app.models.catalogs import Catalog
from app.models.dboards import DBoards
from app.models.users import User


class BoardBase(SQLModel):
    name: str
    icon: str


class Board(BoardBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    dashboards: List["Dashboard"] = Relationship(
        back_populates="boards", link_model=DBoards
    )
    users: List["User"] = Relationship(back_populates="boards", link_model=DBoards)
    catalogs: List["Catalog"] = Relationship(back_populates="board")
