from datetime import datetime, timezone
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from decimal import Decimal


class RecordBase(SQLModel):
    value: Decimal
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class Records(RecordBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    kpi_id: Optional[int] = Field(foreign_key="kpi.id")
    kpi: Optional["Kpi"] = Relationship(back_populates="records")
