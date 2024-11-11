from sqlmodel import SQLModel, Field, Relationship
from typing import Optional


class KpiBase(SQLModel):
    name: str
    description: str


class Kpi(KpiBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    catalogo_id: int = Field(foreign_key="catalogo.id")

    catalogo: "Catalogo" = Relationship(
        back_populates="kpis"
    )  # Relación inversa con Catalogo
