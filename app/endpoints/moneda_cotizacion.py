from typing import List, Optional
from fastapi import APIRouter, Depends, Form
from pydantic import Json
from sqlalchemy.orm import Session  # type: ignore
from app import  repositories, schemas, services
from app.dependencies import Permiso, get_current_user, get_db_session
from app.dependencies.permisos import Permisos
from app.enums import PermisoAccionEnum as a
from app.enums import PermisoModeloEnum as m

api = APIRouter()


@api.get("/gestor_carga", response_model=List[schemas.MonedaCotizacion])
async def read_moneda_cotizacion_list_by_gestor_carga(
    db: Session = Depends(get_db_session),  # noqa: B008
    _: bool = Depends(Permiso(a.LISTAR, m.MONEDA_COTIZACION)),  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
):
    return repositories.get_moneda_cotizacion_list_by_gestor_carga_id(
        db, current_user.gestor_carga_id
    )


@api.get(
    "/cotizacion/moneda_origen/{moneda_origen}/moneda_destino/{moneda_destino}",
    response_model=Optional[schemas.MonedaCotizacion],
)
async def read_cotizacion_moneda(
    moneda_origen: int,
    moneda_destino: int,
    db: Session = Depends(get_db_session),
    current_user: schemas.AuthUser = Depends(get_current_user),
    _: bool = Depends(Permisos(a.LISTAR, [m.ESTADO_CUENTA, m.BANCO])),
):
    return services.read_cotizacion_moneda(
        db, moneda_origen, moneda_destino, current_user.gestor_carga_id
    )


@api.get(
    "/moneda/{moneda_id}/{gestor_carga_id}",
    response_model=Optional[schemas.MonedaCotizacion],
)
async def obtener_cotizacion_moneda(
    moneda_id: int,
    db: Session = Depends(get_db_session),
    current_user = Depends(get_current_user),
    _: bool = Depends(Permiso(a.LISTAR, m.MONEDA)),
):
    return services.get_cotizacion_moneda(db, moneda_id, current_user.gestor_carga_id)


@api.post(
    "/",
    response_model=schemas.MonedaCotizacion,
)
async def add_new_or_update_cotizacion(
    db: Session = Depends(get_db_session),  # noqa: B008
    data: Json[schemas.MonedaCotizacionForm] = Form(...),  # type: ignore  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.CREAR, m.MONEDA_COTIZACION)),  # noqa: B008
):
    return services.update_moneda_cotizacion_by_gestor_moneda_fecha(
        db, data, current_user.username
    )


@api.get("/{id}", response_model=schemas.MonedaCotizacion)
async def read_insumo_precio_venta_by_id(
    id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    _: bool = Depends(Permiso(a.VER, m.MONEDA_COTIZACION)),  # noqa: B008
):
    return services.get_moneda_cotizacion_by_id(db, id)
