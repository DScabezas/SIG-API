from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List


class CatalogBase(SQLModel):
    name: str


class Catalog(CatalogBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    board_id: Optional[int] = Field(foreign_key="board.id")
    board: Optional["Board"] = Relationship(back_populates="catalogos")
    kpis: List["Kpi"] = Relationship(back_populates="catalog")
