from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional

from app.models.catalogs import Catalog
from app.models.records import Records


class KpiBase(SQLModel):
    name: str
    description: Optional[str] = None
    formula: Optional[str] = None
    color_schema: Optional[str] = None
    chart_type: Optional[str] = None
    position_index: Optional[int] = Field(default=None)


class Kpi(KpiBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    catalog_id: Optional[int] = Field(foreign_key="catalog.id")
    catalog: Optional["Catalog"] = Relationship(back_populates="kpis")
    records: List["Records"] = Relationship(back_populates="kpi")
