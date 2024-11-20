from typing import List
import uuid
from app.models.boards import BoardBase


class BoardUpdate(BoardBase):
    pass


class BoardRead(BoardBase):
    pass


class BoardCreate(BoardBase):
    user_id: uuid.UUID
    pass


class BoardCreateUsers(BoardBase):
    user_ids: List[uuid.UUID]
