from pydantic import BaseModel


class PositionUpdate(BaseModel):
    position_index: int


class MoveKpiRequest(BaseModel):
    new_catalog_id: int
