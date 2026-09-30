
from fastapi import FastAPI
from app.routes.accounts import router as accounts_router

app = FastAPI(
    title="Bank Management System API",
    description="A banking API built with FastAPI and PostgreSQL",
    version="1.0.0"
)

app.include_router(accounts_router)


@app.get("/")
def home():
    return {
        "message": "Welcome to the Bank Management System API"
    }