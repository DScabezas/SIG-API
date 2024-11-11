from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional


class CatalogoBase(SQLModel):
    name: str


class Catalogo(CatalogoBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")  # Relación con el usuario
    board_id: int = Field(foreign_key="board.id")  # Relación con el board

    user: "User" = Relationship(back_populates="catalogos")  # Relación inversa con User
    board: "Board" = Relationship(
        back_populates="catalogos"
    )  # Relación inversa con Board
    kpis: List["Kpi"] = Relationship(back_populates="catalogo")  # Relación con KPIs
