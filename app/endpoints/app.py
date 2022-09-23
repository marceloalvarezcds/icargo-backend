from fastapi import APIRouter

from .app_prov import api as app_prov_api

api = APIRouter()

api.include_router(app_prov_api)
