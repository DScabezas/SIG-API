from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from app.models.dboards import DBoards


class Board(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(nullable=False)

    dashboards: List["Dashboard"] = Relationship(
        back_populates="boards", link_model=DBoards
    )
