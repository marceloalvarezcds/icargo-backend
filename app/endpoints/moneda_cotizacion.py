from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session  # type: ignore

from app import repositories, schemas, services
from app.dependencies import Permiso, get_current_user, get_db_session
from app.enums import PermisoAccionEnum as a
from app.enums import PermisoModeloEnum as m

api = APIRouter()


@api.get("/{moneda_origen_id}/cotizacion/{moneda_destino_id}", response_model=schemas.MonedaCotizacion)
async def get_cotizacion_by_moneda(
    moneda_origen_id: int,
    moneda_destino_id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    _: bool = Depends(Permiso(a.LISTAR, m.MONEDA)),  # noqa: B008
):
    return services.get_cotizacion_by_moneda(db, moneda_origen_id, moneda_destino_id)
