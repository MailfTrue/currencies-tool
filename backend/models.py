from pydantic import BaseModel
from datetime import datetime


class Currency(BaseModel):
    id: str
    num_code: str
    char_code: str
    denomination: int
    name: str
    value: float
    previous: float


class Quotes(BaseModel):
    date: datetime
    previous_date: datetime
    currencies: list[Currency]
