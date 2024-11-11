from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from .dashboard import Dashboard
from .users import User
from .table import Table


class BoardBase(SQLModel):
    name: str
    dashboard_id: int = Field(foreign_key="dashboard.id")  # Relación con Dashboard
    dashboard: "Dashboard" = Relationship(back_populates="boards")


class Board(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    tablas: List["Table"] = Relationship(back_populates="board")
    users: List["User"] = Relationship(
        back_populates="boards", link_model="Boards"
    )  # Relación con usuarios
    dashboard: "Dashboard" = Relationship(
        back_populates="boards"
    )  # Relación con Dashboard
