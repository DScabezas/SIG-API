from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from app.models.dboards import DBoards
from app.models.boardusers import BoardUsers


class BoardBase(SQLModel):
    name: str


class Board(BoardBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    users: List["User"] = Relationship(back_populates="boards", link_model=BoardUsers)
    catalogos: List["Catalogo"] = Relationship(back_populates="board")
    dashboards: List["Dashboard"] = Relationship(
        back_populates="boards", link_model=DBoards
    )
