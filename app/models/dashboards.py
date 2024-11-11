from sqlmodel import SQLModel, Field, Relationship
from typing import Optional


class Dashboard(SQLModel, table=True):
    user_id: Optional[int] = Field(foreign_key="user.id", primary_key=True)
    board_id: Optional[int] = Field(foreign_key="board.id", primary_key=True)

    # Relaciones con User y Board
    user: "User" = Relationship(back_populates="dashboards")
    board: "Board" = Relationship(back_populates="dashboards")
