import uuid
from sqlmodel import SQLModel
from app.models.boards import Board
from app.models.dashboards import DashboardBase


class DashboardRead(DashboardBase):
    id: int
    boards: list[Board] = []


class DashboardCreate(SQLModel):
    user_id: uuid.UUID
