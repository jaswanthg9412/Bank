
# Bank Management System

A backend banking application built using Python, FastAPI, and PostgreSQL. This project provides REST APIs to create bank accounts, manage deposits and withdrawals, and view transaction history.

## Features

- Create bank accounts
- View all accounts
- Deposit money
- Withdraw money
- View transaction history
- Validate API requests
- Store account and transaction data in PostgreSQL

## Tech Stack

- Python
- FastAPI
- PostgreSQL
- Psycopg2
- Pydantic
- Uvicorn

## Project Structure

```text
BankManagementSystem/
├── app/
│   ├── routes/
│   │   ├── __init__.py
│   │   └── accounts.py
│   ├── __init__.py
│   ├── database.py
│   ├── main.py
│   └── models.py
├── .gitignore
├── requirements.txt
└── README.md
```

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/jaswanthg9412/Bank.git
cd Bank
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure PostgreSQL

Create a PostgreSQL database and configure the connection settings in `app/database.py`.

Do not commit database passwords or other secrets to GitHub.

### 5. Run the application

```bash
uvicorn app.main:app --reload
```

## API Documentation

Once the server is running, open:

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/accounts/` | Create an account |
| GET | `/accounts/` | View all accounts |
| POST | `/accounts/{account_number}/deposit` | Deposit money |
| POST | `/accounts/{account_number}/withdraw` | Withdraw money |
| GET | `/accounts/{account_number}/transactions` | View transaction history |

## Future Improvements

- User authentication and authorization
- Improved transaction handling
- Automated tests
- Frontend banking dashboard
- Deployment

## Author

Jaswanth G. Sainath Reddy

GitHub: https://github.com/jaswanthg9412