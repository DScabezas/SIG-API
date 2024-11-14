from typing import List, Optional

from app.models.boards import Board
from ..models.users import UserBase


class UserUpdate(UserBase):
    pass


class UserRead(UserBase):
    id: int
    boards: Optional[List[Board]] = []
