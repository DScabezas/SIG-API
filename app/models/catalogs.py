from sqlmodel import SQLModel, Field, Relationship
from typing import Optional


class Catalogo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)