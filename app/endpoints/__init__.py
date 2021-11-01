from fastapi import APIRouter

from app.endpoints import (
    cargo,
    centro_operativo,
    centro_operativo_clasificacion,
    ciudad,
    contacto,
    localidad,
    login,
    pais,
    user,
)

api = APIRouter()

api.include_router(cargo.api, prefix="/cargo", tags=["cargo"])
api.include_router(
    centro_operativo_clasificacion.api,
    prefix="/centro_operativo_clasificacion",
    tags=["centro_operativo_clasificacion"],
)
api.include_router(
    centro_operativo.api, prefix="/centro_operativo", tags=["centro_operativo"]
)
api.include_router(ciudad.api, prefix="/ciudad", tags=["ciudad"])
api.include_router(contacto.api, prefix="/contacto", tags=["contacto"])
api.include_router(localidad.api, prefix="/localidad", tags=["localidad"])
api.include_router(login.api, prefix="/login", tags=["login"])
api.include_router(pais.api, prefix="/pais", tags=["pais"])
api.include_router(user.api, prefix="/user", tags=["user"])


@api.get("/alive")
def alive() -> dict:
    return {"alive": True}
