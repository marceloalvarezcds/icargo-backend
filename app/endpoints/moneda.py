from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session  # type: ignore

from app import repositories, schemas, services
from app.dependencies import Permiso, get_current_user, get_db_session
from app.enums import PermisoAccionEnum as a
from app.enums import PermisoModeloEnum as m

api = APIRouter()


@api.get("/", response_model=List[schemas.Moneda])
async def read_moneda_list(
    db: Session = Depends(get_db_session),  # noqa: B008
    _: bool = Depends(Permiso(a.LISTAR, m.MONEDA)),  # noqa: B008
):
    return repositories.get_moneda_list(db)


@api.get(
    "/insumo/{insumo_id}/punto_venta/{punto_venta_id}",
    response_model=List[schemas.Moneda],
)
async def read_moneda_list_by_insumo_id_and_punto_venta_id(
    insumo_id: int,
    punto_venta_id: int,
    db: Session = Depends(get_db_session),  # noqa: B008
    current_user: schemas.AuthUser = Depends(get_current_user),  # noqa: B008
    _: bool = Depends(Permiso(a.LISTAR, m.MONEDA)),  # noqa: B008
):
    return services.get_moneda_list_by_insumo_id_and_punto_venta_id(
        db, insumo_id, punto_venta_id, current_user.gestor_carga_id
    )
