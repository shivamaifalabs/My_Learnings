import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s — %(levelname)s — %(message)s" #Handler
)

logging.debug("Debug info")
logging.info("App started")
logging.warning("Low disk space")
logging.error("Failed to save file")
logging.critical("System crash")

# Outputs:---
"""
2025-11-17 10:45:04 — DEBUG — Debug info
2025-11-17 10:45:04 — INFO — App started
2025-11-17 10:45:04 — WARNING — Low disk space
2025-11-17 10:45:04 — ERROR — Failed to save file
2025-11-17 10:45:04 — CRITICAL — System crash
"""


# Rotating File Handler:-

from logging.handlers import RotatingFileHandler

handler = RotatingFileHandler(
    "app.log",
    maxBytes=1_000_000,   # 1MB
    backupCount=5          # keep last 5 logs
)

# Logging with Extra Context:-

# logger.info("User logged in", extra={"user_id": 42})
#    --OR--
# logger.info(f"User logged in (id={user_id})")


# Logging with FastAPI ( Uvicorn ):--
from fastapi import FastAPI
import logging

logger = logging.getLogger("uvicorn.error")

app=FastAPI()
@app.get("/users")
async def get_user():
    logger.info("Fetching user...")

