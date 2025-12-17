from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       # who can talk to us
    allow_methods=["*"],       # which HTTP methods are allowed
    allow_headers=["*"],       # which request headers are allowed
    allow_credentials=True,    # allow cookies/Authorization headers
)
