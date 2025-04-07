from typing import List, Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session  # type: ignore
from app import  schemas, services
from app.dependencies import Permiso, get_current_user, get_db_session
from app.enums import PermisoAccionEnum as a
from app.enums import PermisoModeloEnum as m

api = APIRouter()

@api.get(
    "/cotizacion/moneda_origen/{moneda_origen}/moneda_destino/{moneda_destino}",
    response_model=schemas.MonedaCotizacion,
)
async def read_cotizacion_moneda(
    moneda_origen: int,
    moneda_destino: int,
    db: Session = Depends(get_db_session),
    current_user: schemas.AuthUser = Depends(get_current_user),
    _: bool = Depends(Permiso(a.LISTAR, m.ESTADO_CUENTA)),
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
