import enum

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.endpoints import api
from . import models
from app.db import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "*",
]

# import endpoints
app.include_router(api)
# from app.endpoints import api

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

