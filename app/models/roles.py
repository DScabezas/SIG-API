from sqlmodel import SQLModel, Field
from typing import Optional


class RolesBase(SQLModel):
    name: str = Field(default=None)
    description: str = Field(default=None)
    abbr: str = Field(default=None)


class Roles(RolesBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)