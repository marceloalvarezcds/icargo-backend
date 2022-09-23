from fastapi import APIRouter, Body, Depends, Request
from sqlalchemy.orm import Session  # type: ignore

from app import schemas, services
from app.dependencies import get_current_punto_venta_no_admin_user as get_current_user
from app.dependencies import get_db_session

api = APIRouter()


@api.post("/login", response_model=schemas.ApiResponseData[schemas.UserPuntoVenta])
def login(
    request: Request,
    db: Session = Depends(get_db_session),  # noqa: B008
    data: schemas.Auth = Body(...),  # noqa: B008
):
    return services.login_user_punto_venta(db, data, request)


@api.post(
    "/admin/login", response_model=schemas.ApiResponseData[schemas.UserPuntoVenta]
)
def admin_login(
    request: Request,
    db: Session = Depends(get_db_session),  # noqa: B008
    data: schemas.Auth = Body(...),  # noqa: B008
    _: schemas.AuthPuntoVentaUser = Depends(get_current_user),  # noqa: B008
):
    return services.login_user_punto_venta(db, data, request, True)
