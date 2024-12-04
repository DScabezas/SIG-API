from typing import List, Optional
from pydantic import BaseModel

from app.models.kpis import KpiBase
from app.models.records import Records


class KpiRead(KpiBase):
    id: int
    catalog_id: int
    records: List["Records"]


class PositionUpdate(BaseModel):
    position_index: int


class MoveKpiRequest(BaseModel):
    new_catalog_id: int
