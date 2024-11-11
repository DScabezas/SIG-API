from sqlmodel import SQLModel, Field


class Boards(SQLModel, table=True):
    id: int = Field(primary_key=True)
    board_id: int = Field(foreign_key="board.id")
    user_id: int = Field(foreign_key="user.id")
