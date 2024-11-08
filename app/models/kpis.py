from typing import List
from pydantic import BaseModel
from .users import User


class KpiBase(BaseModel):
    name: str
    description: str
    member: List[User]


class KpiCreate(BaseModel):
    pass


class Kpi(KpiBase):
    id: int | None = None
