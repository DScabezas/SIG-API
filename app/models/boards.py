import uuid
from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from app.models.dboards import DBoards


class BoardBase(SQLModel):
    name: str
    icon: str
    user_id: uuid.UUID = Field(default_factory=uuid.uuid4, foreign_key="user.id")


class Board(BoardBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    dashboards: List["Dashboard"] = Relationship(
        back_populates="boards", link_model=DBoards
    )
    users: List["User"] = Relationship(back_populates="boards", link_model=DBoards)
    catalogos: List["Catalog"] = Relationship(back_populates="board")
