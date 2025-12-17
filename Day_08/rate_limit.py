from cachetools import TTLCache

from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, HTTPException
from cachetools import TTLCache

# max 5 requests per user per minute
LIMIT = 5

# store number of requests per user for 60 seconds
request_counts = TTLCache(maxsize=1000, ttl=60)

class RateLimiterMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # identify user 
        user_id = request.client.host

        # count number of calls in current minute
        count = request_counts.get(user_id, 0) + 1
        request_counts[user_id] = count

        if count > LIMIT:
            raise HTTPException(status_code=429, detail="Too many requests. Please slow down.")

        return await call_next(request)




from fastapi import FastAPI

app = FastAPI()
app.add_middleware(RateLimiterMiddleware)


@app.get("/data")
def get_data():
    return {"status": "ok"}
