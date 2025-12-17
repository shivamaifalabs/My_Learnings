from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
import time
import uuid

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid.uuid4())
        method = request.method
        url = request.url.path
        start = time.time()

        print(f"➡ [{request_id}] Request: {method} {url}")

        response = await call_next(request)

        duration = round((time.time() - start) * 1000, 2)
        status = response.status_code

        # Log after response
        print(f"⬅ [{request_id}] Response: {status} (time: {duration}ms)")

       

        return response
