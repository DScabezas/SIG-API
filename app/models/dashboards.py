from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from app.models.dboards import DBoards


class DashboardBase(SQLModel):
    user_id: int = Field(foreign_key="user.id")


class Dashboard(DashboardBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    boards: List["Board"] = Relationship(
        back_populates="dashboards", link_model=DBoards
    )
