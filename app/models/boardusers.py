from sqlmodel import SQLModel, Field


class BoardUsers(SQLModel, table=True):
    board_id: int = Field(default=None, foreign_key="board.id", primary_key=True)
    user_id: int = Field(default=None, foreign_key="user.id", primary_key=True)
