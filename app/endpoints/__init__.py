from fastapi import APIRouter

from app.endpoints import login, user

api = APIRouter()
api.include_router(login.api, prefix="/login", tags=["login"])
api.include_router(user.api, prefix="/user", tags=["user"])
