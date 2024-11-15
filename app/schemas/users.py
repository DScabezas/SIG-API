from typing import List, Optional
from uuid import UUID

from app.models.boards import Board
from ..models.users import UserBase


class UserUpdate(UserBase):
    pass


class UserRead(UserBase):
    id: UUID
    boards: Optional[List[Board]] = []


class UserInfoRead(UserBase):
    pass


class UserCreate(UserBase):
    id: UUID
    pass
