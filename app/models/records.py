from pydantic import BaseModel
from .users import User
from .kpis import Kpi


class Record(BaseModel):
    id: int
    user: User
    kpis: list[Kpi]
