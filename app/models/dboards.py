from sqlmodel import SQLModel, Field


class DBoards(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    dashboard_id: int = Field(foreign_key="dashboard.id")
    board_id: int = Field(foreign_key="board.id")
