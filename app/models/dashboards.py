import uuid
from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional

from app.models.users import User


class DashboardBase(SQLModel):
    user_id: uuid.UUID = Field(default_factory=uuid.uuid4, foreign_key="user.id")


class Dashboard(DashboardBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    users: List["User"] = Relationship(back_populates="dashboard")
