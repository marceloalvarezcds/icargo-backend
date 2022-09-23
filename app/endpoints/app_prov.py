from fastapi import APIRouter

from . import app_prov_auth, app_prov_transactional_user

api = APIRouter()

api.include_router(
    app_prov_auth.api,
    prefix="/punto_venta",
    tags=["app_prov_punto_venta"],
)
api.include_router(
    app_prov_transactional_user.api,
    prefix="/transactional_user",
    tags=["transactional_user"],
)
