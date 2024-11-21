from typing import List
import uuid
from app.models.boards import BoardBase
from app.models.users import User


class BoardUpdate(BoardBase):
    pass


class BoardRead(BoardBase):
    users: List[User]
    pass


class BoardCreate(BoardBase):
    user_id: uuid.UUID
    pass


class BoardCreateUsers(BoardBase):
    user_ids: List[uuid.UUID]
