from typing import List
from pydantic import BaseModel
from .users import User

class kpi(BaseModel):
    id: int
    name: str
    description: str
    member: List[User]
