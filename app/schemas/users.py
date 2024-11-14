from app.models.boards import Board
from ..models.users import UserBase


class UserUpdate(UserBase):
    pass


class UserRead(UserBase):
    pass
    boards: list["Board"]
