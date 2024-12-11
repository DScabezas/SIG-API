from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional

from app.models.catalogs import Catalog
from app.models.records import Records
from app.models.utils import Chart, Color


class KpiBase(SQLModel):
    name: str
    description: Optional[str] = None
    formula: Optional[str] = None
    position_index: Optional[int] = Field(default=None)


class Kpi(KpiBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    catalog_id: Optional[int] = Field(foreign_key="catalog.id")
    color_schema: Optional[int] = Field(foreign_key="color.id")
    chart_type: Optional[int] = Field(foreign_key="chart.id")
    catalog: Optional["Catalog"] = Relationship(back_populates="kpis")
    color: Optional["Color"] = Relationship(back_populates="kpi")
    chart: Optional["Chart"] = Relationship(back_populates="kpi")
    records: List["Records"] = Relationship(back_populates="kpi")
