from typing import List, Optional
from pydantic import BaseModel

from app.models.kpis import KpiBase
from app.models.records import Records


class KpiRead(KpiBase):
    id: int
    records: List["Records"]
    color_schema: Optional[int]
    chart_type: Optional[int]
    catalog_id: Optional[int]


class KpiCreate(KpiBase):
    color_schema: Optional[int]
    chart_type: Optional[int]


class PositionUpdate(BaseModel):
    position_index: int


class MoveKpiRequest(BaseModel):
    new_catalog_id: int
