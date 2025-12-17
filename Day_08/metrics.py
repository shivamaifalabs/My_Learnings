import time

start_time = time.time()
total_requests = 0

def get_uptime():
    return round(time.time() - start_time)


# Middleware:--------------------------------
from starlette.middleware.base import BaseHTTPMiddleware

class MetricsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        global total_requests
        total_requests += 1
        return await call_next(request)

#----------------------------------

from fastapi import FastAPI
from metrics import get_uptime, total_requests
import psutil

app = FastAPI()

@app.get("/metrics")
def metrics():
    return {
        "uptime_seconds": get_uptime(),
        "total_requests": total_requests,
        "cpu_percent": psutil.cpu_percent(),
        "memory_percent": psutil.virtual_memory().percent
    }

app.add_middleware(MetricsMiddleware)
