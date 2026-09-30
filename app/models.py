from datetime import datetime
from pydantic import BaseModel, Field

# Request Models

class AccountCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)

class AmountRequest(BaseModel):
    amount: float = Field(gt=0)

# Response Models

class AccountCreatedResponse(BaseModel):
    message: str
    account_number: int
    account_holder: str

class AccountResponse(BaseModel):
    account_number: int
    account_holder: str
    balance: float

class DepositResponse(BaseModel):
    message: str
    account_number: int
    account_holder: str
    deposited_amount: float
    available_balance: float

class WithdrawalResponse(BaseModel):
    message: str
    account_number: int
    account_holder: str
    withdrawn_amount: float
    available_balance: float

class TransactionResponse(BaseModel):
    transaction_type: str
    amount: float
    transaction_date: datetime

class TransactionHistoryResponse(BaseModel):
    account_number: int
    account_holder: str
    current_balance: float
    transactions: list[TransactionResponse]
