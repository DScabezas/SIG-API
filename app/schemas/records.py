from pydantic import BaseModel
from decimal import Decimal


class RecordCreate(BaseModel):
    value: Decimal
