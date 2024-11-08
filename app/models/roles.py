from pydantic import BaseModel


class RolesBase(BaseModel):
    description: str
    abbr: str


class Roles(RolesBase):
    id: int | None = None
