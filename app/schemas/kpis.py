from typing import List, Optional
from pydantic import BaseModel

from app.models.kpis import KpiBase
from app.models.records import Records


class KpiRead(KpiBase):
    id: int
    catalog_id: int
    color_schema: int
    chart_type: int
    records: List["Records"]


class KpiCreate(KpiBase):
    color_schema: int
    chart_type: int


class PositionUpdate(BaseModel):
    position_index: int


class MoveKpiRequest(BaseModel):
    new_catalog_id: int
