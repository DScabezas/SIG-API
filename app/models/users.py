from pydantic import BaseModel

class User(BaseModel):
    name: str
    description: str
    email: str
