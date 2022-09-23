from http import HTTPStatus
from typing import Optional

from fastapi import HTTPException, Request
from sqlalchemy.orm import Session  # type: ignore

from app.enums import CodigoRolEnum
from app.models import PuntoVenta, Rol, UserRol
from app.schemas import (
    ApiResponseData,
    Auth,
    UserCreate,
    UserPuntoVenta,
    UserPuntoVentaCreateForm,
)

from .auth import authenticate, create_token_by_user
from .generic_service import get_by_unique_columns
from .punto_venta import get_punto_venta_by_id
from .user import create_user


def create_user_for_punto_venta(
    punto_venta_id: int,
    db: Session,
    data: UserPuntoVentaCreateForm,
    is_admin: bool,
    gestor_carga_id: Optional[int],
    modified_by: str,
    request: Request,
) -> PuntoVenta:
    punto_venta = get_punto_venta_by_id(db, punto_venta_id)
    user_punto_venta_schema = UserCreate(
        email=punto_venta.email,
        surname=data.username,
        username=data.username,
        first_name=punto_venta.nombre,
        last_name=punto_venta.proveedor_nombre,
        password=data.password,
        confirm_password=data.confirm_password,
        punto_venta_id=punto_venta_id,
        is_admin=is_admin,
    )
    user = create_user(
        db, user_punto_venta_schema, gestor_carga_id, modified_by, request
    )
    rol_descripcion = (
        CodigoRolEnum.ADMIN_APP_PROVEEDOR.value
        if is_admin
        else CodigoRolEnum.USUARIO_APP_PROVEEDOR.value
    )
    rol: Rol = get_by_unique_columns(Rol, db, descripcion=rol_descripcion)
    user.user_roles.append(
        UserRol(
            user_id=user.id,
            rol_id=rol.id,
            created_by=modified_by,
            modified_by=modified_by,
        )
    )
    db.commit()
    return punto_venta


def login_user_punto_venta(
    db: Session, data: Auth, request: Request, is_for_admin=False
) -> ApiResponseData[UserPuntoVenta]:
    user = authenticate(db, username=data.username, password=data.password)
    if is_for_admin:
        if not user.is_admin:
            raise HTTPException(
                HTTPStatus.FORBIDDEN,
                "Este usuario no es Administrador del Punto de Venta",
            )
    else:
        if user.is_admin:
            raise HTTPException(
                HTTPStatus.FORBIDDEN, "No es Usuario del Punto de Venta"
            )
    token = create_token_by_user(db, user, request)
    return ApiResponseData(data=UserPuntoVenta.from_orm_with_token(user, token))
