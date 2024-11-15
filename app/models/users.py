import uuid
from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from app.models.dboards import DBoards


class UserBase(SQLModel):
    name: Optional[str] = None
    email: Optional[str] = None
    given_name: Optional[str] = None
    surname: Optional[str] = None
    job_title: Optional[str] = None
    business_phone: Optional[str] = None
    mobile_phone: Optional[str] = None
    office_location: Optional[str] = None


class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    dashboard: "Dashboard" = Relationship(back_populates="users")
    boards: List["Board"] = Relationship(back_populates="users", link_model=DBoards)
