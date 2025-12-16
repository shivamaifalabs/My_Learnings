from fastapi import FastAPI, Request
import time
from app.logger_config import setup_logger, setup_access_logger

app = FastAPI()

logger = setup_logger()
access_logger = setup_access_logger()
