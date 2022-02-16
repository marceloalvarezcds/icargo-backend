from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session  # type: ignore

from app import models, schemas, services
from app.dependencies import Permiso, get_current_user, get_db_session
from app.enums import PermisoAccionEnum as a
from app.enums import PermisoModeloEnum as m

api = APIRouter()


@api.get(
    "/insumo/{insumo_id}/moneda/{moneda_id}/punto_venta/{punto_venta_id}",
    response_model=schemas.InsumoPuntoVentaPrecioList,
)
async def read_last_insumo_punto_venta_precio(
    insumo_id: int,
    moneda_id: int,
    punto_venta_id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    current_user: models.User = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.VER, m.INSUMO_PUNTO_VENTA_PRECIO)),  # noqa: B008
):
    return services.get_insumo_punto_venta_precio_by_insumo_id_and_moneda_id_and_punto_venta_id(
        db, insumo_id, moneda_id, punto_venta_id, current_user.gestor_carga_id
    )
