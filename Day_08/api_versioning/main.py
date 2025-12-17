from fastapi import FastAPI
from routers.v1 import user_route as user_v1
from routers.v2 import user_route as user_v2

app = FastAPI()

app.include_router(user_v1.router)
app.include_router(user_v2.router)
