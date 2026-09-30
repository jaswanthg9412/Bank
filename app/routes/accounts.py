
from fastapi import APIRouter, HTTPException
from app.database import (
    create_account,
    get_accounts,
    deposit_money,
    withdraw_money,
    get_transaction_history
)
from app.models import (
    AccountCreate,
    AmountRequest,
    AccountCreatedResponse,
    AccountResponse,
    DepositResponse,
    WithdrawalResponse,
    TransactionHistoryResponse
)

router = APIRouter(
    prefix="/accounts",
    tags=["Accounts"]
)


# Create Account
@router.post("/", response_model=AccountCreatedResponse)
def create_bank_account(account: AccountCreate):
    try:
        account_number = create_account(account.name)
        return {
            "message": "Account created successfully",
            "account_number": account_number,
            "account_holder": account.name
        }
    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail="Could not create account"
        ) from error


# View All Accounts
@router.get("/", response_model=list[AccountResponse])
def view_accounts():
    try:
        accounts = get_accounts()
        return [
            {
                "account_number": acc[0],
                "account_holder": acc[1],
                "balance": float(acc[2])
            }
            for acc in accounts
        ]
    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail="Could not retrieve accounts"
        ) from error

@router.get("/{account_number}", response_model=AccountResponse)
def view_single_account(account_number: int):
    try:
        accounts = get_accounts()

        account = next(
            (acc for acc in accounts if acc[0] == account_number),
            None
        )

        if account is None:
            raise HTTPException(
                status_code=404,
                detail="Account not found"
            )

        return {
            "account_number": account[0],
            "account_holder": account[1],
            "balance": float(account[2])
        }

    except HTTPException:
        raise
    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail="Could not retrieve account"
        ) from error


# Deposit Money
@router.post("/{account_number}/deposit", response_model=DepositResponse)
def deposit(account_number: int, request: AmountRequest):
    try:
        result = deposit_money(account_number, request.amount)

        if result is None:
            raise HTTPException(
                status_code=404,
                detail="Account not found"
            )

        name, balance = result
        return {
            "message": "Deposit successful",
            "account_number": account_number,
            "account_holder": name,
            "deposited_amount": request.amount,
            "available_balance": float(balance)
        }
    except HTTPException:
        raise
    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail="Deposit failed"
        ) from error


# Withdraw Money
@router.post("/{account_number}/withdraw", response_model=WithdrawalResponse)
def withdraw(account_number: int, request: AmountRequest):
    try:
        result = withdraw_money(account_number, request.amount)

        if result == "not_found":
            raise HTTPException(
                status_code=404,
                detail="Account not found"
            )

        if result == "insufficient_balance":
            raise HTTPException(
                status_code=400,
                detail="Insufficient balance"
            )

        name, balance = result
        return {
            "message": "Withdrawal successful",
            "account_number": account_number,
            "account_holder": name,
            "withdrawn_amount": request.amount,
            "available_balance": float(balance)
        }
    except HTTPException:
        raise
    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail="Withdrawal failed"
        ) from error


# Transaction History
@router.get("/{account_number}/transactions", response_model=TransactionHistoryResponse)
def transaction_history(account_number: int):
    try:
        accounts = get_accounts()
        account = next(
            (acc for acc in accounts if acc[0] == account_number),
            None
        )

        if account is None:
            raise HTTPException(
                status_code=404,
                detail="Account not found"
            )

        transactions = get_transaction_history(account_number)

        return {
            "account_number": account_number,
            "account_holder": account[1],
            "current_balance": float(account[2]),
            "transactions": [
                {
                    "transaction_type": transaction[0],
                    "amount": float(transaction[1]),
                    "transaction_date": transaction[2]
                }
                for transaction in transactions
            ]
        }
    except HTTPException:
        raise
    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail="Could not retrieve transaction history"
        ) from error