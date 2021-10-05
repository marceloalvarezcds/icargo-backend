from fastapi import APIRouter

from app.endpoints import centro_operativo, login, user

api = APIRouter()

api.include_router(
    centro_operativo.api, prefix="/centro_operativo", tags=["centro_operativo"]
)
api.include_router(login.api, prefix="/login", tags=["login"])
api.include_router(user.api, prefix="/user", tags=["user"])


@api.get("/alive")
def alive() -> dict:
    return {"alive": True}
