from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from app.models.dashboards import Dashboard
from app.models.catalogs import Catalogo


from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional


class UserBase(SQLModel):
    name: str
    description: str
    email: str


class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    dashboards: List["Dashboard"] = Relationship(back_populates="user")
    catalogos: List["Catalogo"] = Relationship(
        back_populates="user"
    )  # Relación con Catalogo
    boards: List["Board"] = Relationship(back_populates="user")  # Relación con Board
