from typing import Optional
from uuid import UUID
from sqlmodel import SQLModel, Field


class DBoards(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    board_id: Optional[int] = Field(foreign_key="board.id")
    user_id: Optional[UUID] = Field(foreign_key="user.id")
