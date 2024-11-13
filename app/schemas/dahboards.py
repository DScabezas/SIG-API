from app.models.boards import Board
from app.models.dashboards import DashboardBase


class DashboardRead(DashboardBase):
    id: int
    boards: list[Board] = []
