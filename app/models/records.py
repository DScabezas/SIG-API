from sqlmodel import SQLModel, Field
from typing import Optional
from .kpis import Kpi


class RecordBase(SQLModel):
    user_id: int = Field(default=None)


class Record(RecordBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
