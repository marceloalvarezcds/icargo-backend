from fastapi import FastAPI

from app.logger import logger  # noqa

app = FastAPI(title="FastAPI Test")
