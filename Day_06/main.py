# app/main.py
from fastapi import FastAPI
from app.routers import auth, users
from app.database import create_all_tables
import asyncio

app = FastAPI(title="Auth Demo with Postgres")

app.include_router(auth.router)
app.include_router(users.router)


@app.on_event("startup")
async def startup():
    # For dev: create tables automatically:-
    await create_all_tables()

@app.get("/")
async def root():
    return {"msg": "Hello — API is running"}
