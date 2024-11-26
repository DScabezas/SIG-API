from typing import List
import uuid
from app.models.boards import BoardBase
from app.models.catalogs import Catalog
from app.models.users import User


class BoardUpdate(BoardBase):
    pass


class BoardRead(BoardBase):
    id: int
    users: List[User]
    catalogs: List[Catalog]
    pass


class BoardCreate(BoardBase):
    user_id: uuid.UUID
    pass


class BoardCreateUsers(BoardBase):
    user_ids: List[uuid.UUID]
    pass
