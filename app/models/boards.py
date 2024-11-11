from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from app.models.catalogs import Catalogo  # Asegúrate de importar Catalogo correctamente


class BoardBase(SQLModel):
    name: str


class Board(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")  # Relación con User

    user: "User" = Relationship(back_populates="boards")  # Relación inversa con User
    catalogos: List["Catalogo"] = Relationship(
        back_populates="board"
    )  # Relación con Catalogo
    dashboards: List["Dashboard"] = Relationship(
        back_populates="board"
    )  # Relación con Dashboard
