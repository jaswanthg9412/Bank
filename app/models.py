
from pydantic import BaseModel, Field


class AccountCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)


class AmountRequest(BaseModel):
    amount: float = Field(gt=0)