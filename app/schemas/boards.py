from typing import List
from app.models.boards import BoardBase


class BoardCreate(BoardBase):
    user_ids: List[int]
