

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_home():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Welcome to the Bank Management System API"
    }


def test_deposit_rejects_zero_amount():
    response = client.post(
        "/accounts/123/deposit",
        json={"amount": 0}
    )

    assert response.status_code == 422

def test_deposit_rejects_negative_amount():
    response = client.post(
        "/accounts/123/deposit",
        json={"amount": -500}
    )

    assert response.status_code == 422

def test_create_account(monkeypatch):
    def fake_create_account(name):
        return 1001

    monkeypatch.setattr(
        "app.routes.accounts.create_account",
        fake_create_account
    )

    response = client.post(
        "/accounts/",
        json={"name": "Test User"}
    )

    assert response.status_code == 200
    assert response.json() == {
        "message": "Account created successfully",
        "account_number": 1001,
        "account_holder": "Test User"
    }


def test_successful_deposit(monkeypatch):
    def fake_deposit_money(account_number, amount):
        return ("Test User", 1500.0)

    monkeypatch.setattr(
        "app.routes.accounts.deposit_money",
        fake_deposit_money
    )

    response = client.post(
        "/accounts/1001/deposit",
        json={"amount": 500}
    )

    assert response.status_code == 200
    assert response.json() == {
        "message": "Deposit successful",
        "account_number": 1001,
        "account_holder": "Test User",
        "deposited_amount": 500,
        "available_balance": 1500.0
    }


def test_successful_withdrawal(monkeypatch):
    def fake_withdraw_money(account_number, amount):
        return ("Test User", 1000.0)

    monkeypatch.setattr(
        "app.routes.accounts.withdraw_money",
        fake_withdraw_money
    )

    response = client.post(
        "/accounts/1001/withdraw",
        json={"amount": 500}
    )

    assert response.status_code == 200
    assert response.json() == {
        "message": "Withdrawal successful",
        "account_number": 1001,
        "account_holder": "Test User",
        "withdrawn_amount": 500,
        "available_balance": 1000.0
    }


def test_withdrawal_insufficient_balance(monkeypatch):
    def fake_withdraw_money(account_number, amount):
        return "insufficient_balance"

    monkeypatch.setattr(
        "app.routes.accounts.withdraw_money",
        fake_withdraw_money
    )

    response = client.post(
        "/accounts/1001/withdraw",
        json={"amount": 5000}
    )

    assert response.status_code == 400
    assert response.json() == {
        "detail": "Insufficient balance"
    }

def test_transaction_history(monkeypatch):
    monkeypatch.setattr(
        "app.routes.accounts.get_accounts",
        lambda: [(1001, "Test User", 1000.0)]
    )

    monkeypatch.setattr(
        "app.routes.accounts.get_transaction_history",
        lambda account_number: [
            ("deposit", 500.0, "2026-09-30T10:00:00")
        ]
    )

    response = client.get("/accounts/1001/transactions")

    assert response.status_code == 200
    assert response.json() == {
        "account_number": 1001,
        "account_holder": "Test User",
        "current_balance": 1000.0,
        "transactions": [
            {
                "transaction_type": "deposit",
                "amount": 500.0,
                "transaction_date": "2026-09-30T10:00:00"
            }
        ]
    }

def test_transaction_history_account_not_found(monkeypatch):
    monkeypatch.setattr(
        "app.routes.accounts.get_accounts",
        lambda: []
    )

    response = client.get("/accounts/9999/transactions")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Account not found"
    }

def test_get_single_account(monkeypatch):
    monkeypatch.setattr(
        "app.routes.accounts.get_accounts",
        lambda: [
            (1001, "Test User", 1500.0),
            (1002, "Another User", 2000.0)
        ]
    )

    response = client.get("/accounts/1001")

    assert response.status_code == 200
    assert response.json() == {
        "account_number": 1001,
        "account_holder": "Test User",
        "balance": 1500.0
    }

def test_get_single_account_not_found(monkeypatch):
    monkeypatch.setattr(
        "app.routes.accounts.get_accounts",
        lambda: []
    )

    response = client.get("/accounts/9999")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Account not found"
    }