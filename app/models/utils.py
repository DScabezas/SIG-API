from typing import Optional
from sqlmodel import Relationship, SQLModel, Field


class ColorBase(SQLModel):
    name: str
    description: str
    abbrev: str


class Color(ColorBase, table=True):
    id: int = Field(default=None, primary_key=True)
    kpi: Optional["Kpi"] = Relationship(back_populates="color")


class ChartBase(SQLModel):
    name: str
    description: str
    abbrev: str


class Chart(ChartBase, table=True):
    id: int = Field(default=None, primary_key=True)
    kpi: Optional["Kpi"] = Relationship(back_populates="chart")


class IconBase(SQLModel):
    name: str
    description: str
    abbrev: str


class Icon(IconBase, table=True):
    id: int = Field(default=None, primary_key=True)
    board: Optional["Board"] = Relationship(back_populates="icon")
