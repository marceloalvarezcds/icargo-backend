from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session  # type: ignore

from app import repositories, schemas, services

from app.dependencies import Permiso, get_current_user, get_db_session
from app.enums import PermisoAccionEnum as a
from app.enums import PermisoModeloEnum as m

api = APIRouter()

@api.get(
    "/cotizacion/moneda_origen/{moneda_origen}/moneda_destino/{moneda_destino}",
    response_model=List[schemas.MonedaCotizacion],
)
async def read_cotizacion_moneda(
    moneda_origen: int,
    moneda_destino: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.LISTAR, m.ESTADO_CUENTA)),  # noqa: B008
):
    return services.read_cotizacion_moneda(
        db, moneda_origen, moneda_destino, current_user.gestor_carga_id
    )

