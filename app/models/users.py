from pydantic import BaseModel
from .roles import Roles


class UserBase(BaseModel):
    name: str
    description: str
    email: str
    role: Roles


class UserCreate(UserBase):
    pass


class UserDelete(UserBase):
    pass


class UserGet(UserBase):
    pass


class User(UserBase):
    id: int | None = None
