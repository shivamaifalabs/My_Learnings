from fastapi import FastAPI
import aiohttp
import asyncio

app = FastAPI()

async def fetch(session, url):
    async with session.get(url) as resp:
        return await resp.json()

@app.get("/multi-api")
async def multi_api():
    urls = [
        "https://httpbin.org/delay/2",
        "https://httpbin.org/delay/3",
        "https://httpbin.org/get"
    ]

    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, url) for url in urls]
        results = await asyncio.gather(*tasks)

    return {"results": results}
