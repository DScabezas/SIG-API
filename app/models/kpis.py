from sqlmodel import SQLModel, Field, Relationship
from typing import Optional


class KpiBase(SQLModel):
    name: str


class Kpi(KpiBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    catalog_id: Optional[int] = Field(foreign_key="catalog.id")
    catalog: Optional["Catalog"] = Relationship(back_populates="kpis")
