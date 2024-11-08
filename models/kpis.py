from sqlmodel import SQLModel, Field
from typing import Optional


class KpiBase(SQLModel):
    name: str = Field(default=None)
    description: str = Field(default=None)


class Kpi(KpiBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
