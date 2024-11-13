from typing import List
from ..models.boards import Board
from ..models.dashboards import DashboardBase


class DashboardRead(DashboardBase):
    boards: List[Board] = []
