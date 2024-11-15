from typing import Optional
from sqlmodel import SQLModel, Field


class DBoards(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    board_id: Optional[int] = Field(foreign_key="board.id")
    dashboard_id: Optional[int] = Field(foreign_key="dashboard.id")
    user_id: Optional[int] = Field(foreign_key="user.id")
