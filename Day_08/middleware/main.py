from fastapi import FastAPI
from middleware import LoggingMiddleware

app = FastAPI()
app.add_middleware(LoggingMiddleware)

# ROUTES:-------

@app.get("/")
def home():
    return {"message": "Hello from FastAPI"}

@app.get("/users")
def get_users():
    return {"users": ["Shivam", "Rohit", "Virat"]}

@app.post("/login")
def login(username: str):
    return {"message": f"Welcome {username}"}
