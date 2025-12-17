from fastapi import FastAPI
from cachetools import TTLCache

app = FastAPI()
cache = TTLCache(maxsize=100, ttl=60)  # 60 seconds TTL

fake_db_products = ["Laptop", "Mobile", "Keyboard", "Mouse"]  # As DB

@app.get("/products")
def get_products():
    if "products" in cache:
        #print(cache)
        return {"from_cache": True, "data": cache["products"]}
    
    # fetch from DB 
    data = fake_db_products
    cache["products"] = data   # store in cache
    return {"from_cache": False, "data": data}
