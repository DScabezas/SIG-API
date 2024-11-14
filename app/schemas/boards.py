from typing import List
from app.models.boards import BoardBase


class BoardUpdate(BoardBase):
    pass


class BoardRead(BoardBase):
    pass


class BoardCreate(BoardBase):
    pass


class BoardCreateUsers(BoardBase):
    user_ids: List[int]
