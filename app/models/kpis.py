from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from .table import Table


class KpiBase(SQLModel):
    name: str
    description: str


class Kpi(KpiBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    tabla_id: int = Field(foreign_key="tabla.id")
    tabla: "Table" = Relationship(back_populates="kpis")
