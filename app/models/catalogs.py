from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional


class CatalogoBase(SQLModel):
    name: str


class Catalogo(CatalogoBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    board_id: Optional[int] = Field(foreign_key="board.id")
    board: Optional["Board"] = Relationship(back_populates="catalogos")
