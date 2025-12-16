from fastapi import FastAPI
from pydantic import BaseModel

app=FastAPI(title="Testing Pydantic Model---")

class RegisterUser(BaseModel):
    username: str
    email: str
    password: str
    age: int

@app.post("/register")
def register_user(user: RegisterUser):
    return user

